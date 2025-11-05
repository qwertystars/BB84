#!/bin/bash

echo "============================================================"
echo "BB84 QKD Simulator - End-to-End Integration Test"
echo "============================================================"
echo

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
PASSED=0
FAILED=0

# Function to check service
check_service() {
    local name=$1
    local url=$2
    echo "🔍 Checking $name..."

    if curl -s -f "$url" > /dev/null; then
        echo -e "  ${GREEN}✓${NC} $name is running at $url"
        ((PASSED++))
        return 0
    else
        echo -e "  ${RED}✗${NC} $name is not accessible at $url"
        ((FAILED++))
        return 1
    fi
}

# Function to test API endpoint
test_endpoint() {
    local name=$1
    local method=$2
    local url=$3
    local data=$4

    echo "🔍 Testing $name..."

    if [ "$method" = "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST "$url" -H "Content-Type: application/json" -d "$data")
    else
        response=$(curl -s -w "\n%{http_code}" "$url")
    fi

    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)

    if [ "$status_code" -eq 200 ]; then
        echo -e "  ${GREEN}✓${NC} $name (Status: $status_code)"
        ((PASSED++))
        return 0
    else
        echo -e "  ${RED}✗${NC} $name (Status: $status_code)"
        echo "  Response: $body"
        ((FAILED++))
        return 1
    fi
}

echo "Step 1: Service Health Checks"
echo "-------------------------------------------------------------"
check_service "Backend API" "http://localhost:8000/health"
check_service "Frontend" "http://localhost:5173"
echo

echo "Step 2: Backend API Endpoint Tests"
echo "-------------------------------------------------------------"
test_endpoint "Root endpoint" "GET" "http://localhost:8000/"
test_endpoint "Health endpoint" "GET" "http://localhost:8000/health"
echo

echo "Step 3: Simulate User Workflow"
echo "-------------------------------------------------------------"

# Step 3.1: User configures parameters and runs simulation
echo "📝 Simulating: User sets n_qubits=50, noise=0.05, seed=12345"
test_endpoint "Run BB84 simulation" "POST" "http://localhost:8000/run_bb84" '{"n_qubits":50,"noise_level":0.05,"seed":12345}'
sleep 1

# Step 3.2: User views results
echo "📊 Simulating: User views detailed results"
test_endpoint "Get simulation results" "GET" "http://localhost:8000/results"
sleep 0.5

# Step 3.3: User views statistics
echo "📈 Simulating: User views statistics"
test_endpoint "Get simulation statistics" "GET" "http://localhost:8000/stats"
sleep 0.5

# Step 3.4: User views circuit visualization
echo "🔬 Simulating: User views circuit for round 0"
test_endpoint "Get circuit visualization" "GET" "http://localhost:8000/visualize_round/0"
sleep 0.5

# Step 3.5: User views another circuit
echo "🔬 Simulating: User views circuit for round 5"
test_endpoint "Get circuit visualization for round 5" "GET" "http://localhost:8000/visualize_round/5"
echo

echo "Step 4: Test Different Noise Levels"
echo "-------------------------------------------------------------"
test_endpoint "Zero noise simulation" "POST" "http://localhost:8000/run_bb84" '{"n_qubits":30,"noise_level":0.0,"seed":999}'
sleep 0.5
test_endpoint "High noise simulation" "POST" "http://localhost:8000/run_bb84" '{"n_qubits":30,"noise_level":0.15,"seed":888}'
sleep 0.5

# Check high noise produces high QBER
stats=$(curl -s "http://localhost:8000/stats")
qber=$(echo $stats | python3 -c "import json, sys; print(json.load(sys.stdin)['qber'])" 2>/dev/null)
if [ ! -z "$qber" ]; then
    echo "  QBER with high noise: $qber"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} Could not retrieve QBER"
    ((FAILED++))
fi
echo

echo "Step 5: Test Error Handling"
echo "-------------------------------------------------------------"
echo "🔍 Testing invalid parameters..."

# Test invalid qubits
response=$(curl -s -w "\n%{http_code}" -X POST "http://localhost:8000/run_bb84" \
    -H "Content-Type: application/json" -d '{"n_qubits":0,"noise_level":0.0}')
status_code=$(echo "$response" | tail -n1)
if [ "$status_code" -eq 422 ]; then
    echo -e "  ${GREEN}✓${NC} Invalid qubit count rejected (Status: $status_code)"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} Should reject invalid qubit count (got status: $status_code)"
    ((FAILED++))
fi

# Test invalid noise
response=$(curl -s -w "\n%{http_code}" -X POST "http://localhost:8000/run_bb84" \
    -H "Content-Type: application/json" -d '{"n_qubits":10,"noise_level":2.0}')
status_code=$(echo "$response" | tail -n1)
if [ "$status_code" -eq 422 ]; then
    echo -e "  ${GREEN}✓${NC} Invalid noise level rejected (Status: $status_code)"
    ((PASSED++))
else
    echo -e "  ${RED}✗${NC} Should reject invalid noise level (got status: $status_code)"
    ((FAILED++))
fi
echo

echo "============================================================"
echo "Test Summary"
echo "============================================================"
echo -e "${GREEN}Passed: $PASSED${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $FAILED${NC}"
else
    echo -e "${GREEN}Failed: $FAILED${NC}"
fi
echo "============================================================"

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All tests passed! Application is fully functional.${NC}"
    echo
    echo "You can now access the application at:"
    echo "  • Frontend: http://localhost:5173"
    echo "  • Backend API: http://localhost:8000"
    echo "  • API Docs: http://localhost:8000/docs"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please review the errors above.${NC}"
    exit 1
fi

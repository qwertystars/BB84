# BB84 Quantum Key Distribution Simulator

A full-stack web application that simulates the BB84 quantum key distribution protocol with multiple scenarios, built with FastAPI backend and React frontend.

## Features

- **4 Simulation Scenarios**: Ideal conditions, channel noise, eavesdropping, and decoherence-free space
- **Interactive UI**: Real-time parameter adjustment and result visualization
- **Data Visualization**: QBER and key length graphs using Recharts
- **Batch Simulations**: Run multiple simulations for statistical analysis
- **Modern Design**: Responsive UI with TailwindCSS and glassmorphism effects

## Architecture

### Backend (FastAPI + Python)
- **FastAPI**: REST API framework
- **Qiskit**: Quantum simulation library (simulated for BB84)
- **NumPy**: Numerical computations
- **Pydantic**: Data validation

### Frontend (React + Vite)
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **TailwindCSS**: Styling framework
- **Recharts**: Data visualization
- **Axios**: HTTP client
- **React Router**: Navigation

## Project Structure

```
bb84-simulation/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── models.py               # Pydantic models
│   ├── utils.py                # Utility functions
│   ├── requirements.txt        # Python dependencies
│   └── simulations/
│       ├── ideal.py            # Ideal conditions simulation
│       ├── error_only.py       # Channel noise simulation
│       ├── error_with_eve.py   # Eavesdropping simulation
│       └── decoherence_free.py # Decoherence-free simulation
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── LoadingSpinner.jsx
│   │   │   ├── SimulationForm.jsx
│   │   │   └── ResultsDisplay.jsx
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   └── Simulation.jsx
│   │   ├── api/
│   │   │   └── index.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 16+
- npm or yarn

### Option 1: Single Service Deployment (Production - Recommended)

This setup combines the frontend and backend into a single web service, perfect for deploying on platforms like Render.

1. **Build the frontend:**
```bash
./build.sh
```

2. **Install backend dependencies:**
```bash
pip install -r backend/requirements.txt
```

3. **Start the combined server:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

The application will be available at `http://localhost:8000` with both the frontend and API served from the same port.

### Option 2: Separate Development Servers (Development)

For local development with hot-reload:

#### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

#### Frontend Setup

1. Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. **Home Page**: Learn about BB84 protocol and available scenarios
2. **Simulation Page**: 
   - Select a scenario from the dropdown
   - Adjust parameters (qubit count, error rate, Eve fraction)
   - Run single or batch simulations
   - View results including sifted key, QBER, and statistical analysis
   - Analyze trends using interactive graphs

## Simulation Scenarios

### 1. Ideal Conditions
- No channel noise or eavesdropping
- QBER should be ~0%
- Maximum security and efficiency

### 2. Channel with Random Error
- Simulates realistic quantum channel noise
- Configurable error rate (0-50%)
- No eavesdropping present

### 3. Channel with Error and Eavesdropping
- Combines channel noise with Eve's intercept-resend attack
- Configurable error rate and Eve fraction
- Demonstrates eavesdropper detection through QBER analysis

### 4. Decoherence-Free Space
- Theoretical scenario where quantum coherence is preserved
- Even with eavesdropping, QBER remains ~0%
- Demonstrates ideal quantum communication conditions

## API Endpoints

- `GET /` - API information
- `GET /scenarios` - List available scenarios
- `POST /simulate/{scenario}` - Run simulation with POST body
- `GET /simulate/{scenario}` - Run simulation with query parameters

## Data Visualization

The application provides:
- **QBER Trends**: Line chart showing Quantum Bit Error Rate across multiple runs
- **Key Length Analysis**: Visualization of sifted key length variations
- **Statistical Summary**: Average QBER and key length for batch simulations
- **Real-time Results**: Immediate display of simulation outcomes

## Security Features

- Input validation for all parameters
- Error handling and user feedback
- CORS configuration for secure API access
- Parameter bounds to prevent invalid simulations

## Deployment on Render

This project is configured for easy deployment on Render as a single web service.

### Quick Deploy

1. **Connect your GitHub repository to Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository

2. **Render will automatically detect the `render.yaml` configuration**
   - Service Name: bb84-simulator
   - Environment: Python
   - Build Command: `./build.sh && pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn main:app --host 0.0.0.0 --port 10000`

3. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application

### Manual Configuration (if render.yaml is not detected)

If you need to configure manually:
- **Environment**: Python 3.11
- **Build Command**: `./build.sh && pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port 10000`
- **Port**: 10000 (automatically set by Render)

### Environment Variables

No environment variables are required for basic deployment. The application automatically detects the production environment and uses relative URLs for API calls.

### Custom Domain

You can add a custom domain in the Render dashboard under "Settings" → "Custom Domain".

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the project repository.

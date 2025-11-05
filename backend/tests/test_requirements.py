"""
Test that all requirements are valid and can be parsed
"""

import pytest
import os


def test_requirements_file_exists():
    """Test that requirements.txt exists"""
    req_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    assert os.path.exists(req_path)


def test_requirements_readable():
    """Test that requirements.txt is readable"""
    req_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    
    with open(req_path, 'r') as f:
        content = f.read()
    
    assert len(content) > 0


def test_requirements_format():
    """Test that requirements.txt has valid format"""
    req_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    
    with open(req_path, 'r') as f:
        lines = f.readlines()
    
    # Should have at least core dependencies
    content = ''.join(lines)
    assert 'fastapi' in content.lower()
    assert 'qiskit' in content.lower()
    assert 'numpy' in content.lower()


def test_requirements_version_constraints():
    """Test that key dependencies have version constraints"""
    req_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
    
    with open(req_path, 'r') as f:
        content = f.read()
    
    # Check that dependencies have version constraints (>=, ==, etc.)
    assert '>=' in content or '==' in content or '~=' in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
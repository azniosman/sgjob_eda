#!/bin/bash

# Singapore Salary Dashboard Launcher
# This script launches the Streamlit dashboard

echo "=========================================="
echo "Singapore Salary Benchmarking Dashboard"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if dependencies are installed
echo "Checking dependencies..."
python -c "import streamlit; import pandas; import plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required packages..."
    pip install -r requirements.txt
fi

# Navigate to dashboard directory and run
echo ""
echo "Starting dashboard..."
echo "Dashboard will open in your browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the dashboard"
echo ""

cd dashboard
streamlit run app.py

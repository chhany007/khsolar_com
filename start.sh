#!/bin/bash
# Render.com start script for KHSolar Streamlit app

echo "Starting KHSolar on Render.com..."
echo "Python version: $(python --version)"
echo "Streamlit version: $(streamlit --version)"

# Start Streamlit with Render-specific configuration
streamlit run app.py \
  --server.port=${PORT:-10000} \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --server.enableCORS=false \
  --server.enableXsrfProtection=false \
  --browser.gatherUsageStats=false

#!/usr/bin/env python3
"""
Cryptocurrency Price Prediction - Launch Script
Trains the ML models and starts the Flask web application
"""

import os
import sys
from pathlib import Path
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Get script directory
SCRIPT_DIR = Path(__file__).resolve().parent
os.chdir(SCRIPT_DIR)

print("\n" + "="*70)
print("🚀 CRYPTOCURRENCY PRICE PREDICTION SYSTEM")
print("="*70)

# Check if models exist
models_dir = SCRIPT_DIR / 'models'
required_files = [
    'xgboost_model.pkl',
    'lightgbm_model.pkl',
    'random_forest_model.pkl',
    'svr_model.pkl'
]

models_exist = all((models_dir / f).exists() for f in required_files)

if not models_exist:
    print("\n⚠️  Models not found. Please train them first:")
    print("   1. Run: jupyter notebook CRYPTO_PRICE_PREDICTION.ipynb")
    print("   2. Execute all cells to train and save models")
    print("   3. Models will be saved to: ./models/")
    sys.exit(1)

print("\n✅ Models found successfully!")
print("📂 Model files verified:")
for f in required_files:
    print(f"   ✓ {f}")

# Install required dependencies
print("\n📦 Checking dependencies...")
try:
    import subprocess
    dependencies = [
        'Flask',
        'Flask-CORS',
        'yfinance',
        'pandas',
        'numpy',
        'scikit-learn',
        'xgboost',
        'lightgbm',
        'joblib'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep.lower().replace('-', '_'))
            print(f"   ✓ {dep}")
        except ImportError:
            print(f"   ⏳ Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", dep])
            print(f"   ✓ {dep} installed")
except Exception as e:
    print(f"   ⚠️  Warning installing dependencies: {e}")

print("\n🌐 Starting Flask application...")
print("📡 Web interface: http://localhost:5000")
print("📊 API Docs: http://localhost:5000/api/")
print("ℹ️  About: http://localhost:5000/about")
print("\nPress Ctrl+C to stop the server\n")

# Import and run Flask app
try:
    from app_crypto_predict import app
    app.run(debug=False, host='0.0.0.0', port=5000)
except KeyboardInterrupt:
    print("\n\n👋 Server stopped by user")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 🚀 Setup Instructions - Cryptocurrency Price Prediction

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Git (optional)
- 2GB+ free disk space
- Internet connection (for data download)

---

## Installation Steps

### Step 1: Navigate to Project Directory
```bash
cd "d:\New folder\SONAR-Rock-vs-Mine-Prediction\Crypto"
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Train Machine Learning Models

**Important**: Models must be trained before running the web app!

```bash
# Start Jupyter Notebook
jupyter notebook CRYPTO_PRICE_PREDICTION.ipynb
```

Inside Jupyter:
1. Run all cells in order (Kernel → Run All)
2. Wait for training to complete (~10-15 minutes)
3. Models will be saved to `models/` folder automatically
4. Close Jupyter when done

**What gets generated**:
- `models/xgboost_model.pkl`
- `models/lightgbm_model.pkl`
- `models/random_forest_model.pkl`
- `models/ridge_model.pkl`
- `models/scaler_X.pkl`
- `models/scaler_y.pkl`
- `models/feature_cols.pkl`
- `models/model_metadata.pkl`

### Step 5: Start the Web Application

Choose one option:

#### Option A: Python Script (Recommended)
```bash
python run_app.py
```

#### Option B: Batch File (Windows)
```bash
RUN_APP.bat
```

#### Option C: PowerShell (Windows)
```bash
.\RUN_APP.ps1
```

#### Option D: Direct Flask
```bash
python app_crypto_predict.py
```

#### Option E: Production (Gunicorn)
```bash
gunicorn app_crypto_predict:app --bind 0.0.0.0:5000 --workers 4
```

### Step 6: Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

---

## Verification Checklist

- [ ] Python 3.12+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip list | grep -E "flask|xgboost|lightgbm"`
- [ ] Models trained: `ls models/` shows 8 .pkl files
- [ ] Flask app starts without errors
- [ ] Web interface loads: http://localhost:5000
- [ ] Can make a prediction with sample data

---

## Troubleshooting

### Issue 1: "command not found: python"
**Solution**: 
- Ensure Python is installed: `python --version`
- Windows: Use `python` or `py`
- macOS/Linux: Use `python3`

### Issue 2: "No module named 'flask'"
**Solution**:
```bash
pip install flask
pip install -r requirements.txt
```

### Issue 3: "Models not found"
**Solution**:
1. Train models: `jupyter notebook CRYPTO_PRICE_PREDICTION.ipynb`
2. Run all cells
3. Check `models/` folder exists with all .pkl files
4. Restart Flask app

### Issue 4: "Port 5000 already in use"
**Solution**:
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>

# Or use different port
python -c "from app_crypto_predict import app; app.run(port=5001)"
```

### Issue 5: "yfinance download fails"
**Solution**:
- Check internet connection
- Verify ticker format: "BTC-USD", not "BTC"
- Try later (Yahoo Finance may have rate limits)
- Use alternative data source

### Issue 6: Out of Memory
**Solution**:
- Reduce historical days to 365 instead of 1825
- Close other applications
- Increase available RAM
- Use smaller data size

---

## File Structure After Setup

```
Crypto/
├── models/
│   ├── xgboost_model.pkl
│   ├── lightgbm_model.pkl
│   ├── random_forest_model.pkl
│   ├── ridge_model.pkl
│   ├── scaler_X.pkl
│   ├── scaler_y.pkl
│   ├── feature_cols.pkl
│   └── model_metadata.pkl
│
├── templates/
│   ├── crypto_form.html
│   ├── crypto_result.html
│   ├── crypto_about.html
│   ├── 404.html
│   └── 500.html
│
├── static/
│   ├── css/
│   └── js/
│
├── CRYPTO_PRICE_PREDICTION.ipynb
├── app_crypto_predict.py
├── run_app.py
├── RUN_APP.bat
├── RUN_APP.ps1
├── requirements.txt
├── runtime.txt
├── Procfile
├── .env.example
├── PROJECT_GUIDE.md
├── SETUP_INSTRUCTIONS.md
├── API_DOCUMENTATION.md
└── MODEL_ANALYSIS.md
```

---

## Next Steps

1. **Explore Web Interface**: Navigate through the app, try predictions
2. **Test API**: Use `/api/` endpoints
3. **View Results**: Check predictions vs actual prices
4. **Deploy**: Use Heroku/Render.com for production
5. **Customize**: Modify models, add more cryptos, adjust parameters

---

## Development Mode

For development with auto-reload:
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app_crypto_predict.py
```

---

## Production Deployment

### Local Production
```bash
gunicorn app_crypto_predict:app --bind 0.0.0.0:5000 --workers 4 --timeout 120
```

### Environment Variables
Create `.env` file:
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your_random_secret_key
```

Load with:
```bash
pip install python-dotenv
from dotenv import load_dotenv
load_dotenv()
```

---

## Performance Optimization

### For Faster Predictions
1. Cache predictions: Add caching to reduce repeated calculations
2. Use smaller historical window: 365 days instead of 1825
3. Reduce model complexity: Use fewer estimators
4. Parallel processing: Enable model parallelism

### For Better Accuracy
1. Use more historical data: 5 years instead of 1 year
2. Add more indicators: Custom technical analysis
3. Optimize hyperparameters: GridSearch/RandomSearch
4. Ensemble with more models: Add LSTM, Prophet, etc.

**Note on Real-Time Data**: The application fetches fresh data on every request (3-9 seconds). For faster predictions, consider caching recent data, but this reduces accuracy as market conditions change rapidly.

---

## Monitoring & Logging

### Enable Flask Logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Monitor Performance
```bash
# Check predictions per second
watch -n 1 'ps aux | grep app_crypto'

# Memory usage
python -m memory_profiler app_crypto_predict.py
```

---

## Updating & Maintenance

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Retrain Models
```bash
jupyter notebook CRYPTO_PRICE_PREDICTION.ipynb
# Run all cells again
```

### Backup Models
```bash
cp -r models/ models_backup/
```

---

## Support & Resources

- **Flask Documentation**: https://flask.palletsprojects.com/
- **XGBoost Guide**: https://xgboost.readthedocs.io/
- **Jupyter Notebook**: https://jupyter.org/
- **Python Package Index**: https://pypi.org/

---

**Setup Complete!** ✅

You're now ready to make cryptocurrency price predictions.

Start with: `python run_app.py`

Visit: `http://localhost:5000`

# 💰 Cryptocurrency Price Prediction - Complete Project Guide

## 📋 Project Overview

**CryptoPredict** is a production-ready machine learning system for cryptocurrency price prediction using ensemble modeling and 20+ technical indicators.

### Key Features
- ✅ **Multi-Model Ensemble**: XGBoost, LightGBM, Random Forest, Ridge Regression
- ✅ **20+ Technical Indicators**: RSI, MACD, Bollinger Bands, ATR, Stochastic, and more
- ✅ **Real-time Data Fetching**: Live prices from Yahoo Finance (3-9 seconds refresh, no caching)
- ✅ **24-Hour Predictions**: Next day's closing price with ±10% realistic range
- ✅ **Professional Web Interface**: Responsive HTML5/CSS3 UI with Chart.js
- ✅ **REST API**: Programmatic access to predictions
- ✅ **Production Ready**: Gunicorn WSGI deployment with sanity checks
- ✅ **Multiple Cryptocurrencies**: BTC, ETH, XRP, LTC, ADA, SOL, DOT, DOGE

---

## 🎯 Project Goals

### Goal 1: Price Direction Prediction
Predict whether cryptocurrency price will move UP or DOWN with high confidence

### Goal 2: Price Value Prediction
Forecast the actual closing price using ensemble predictions

### Goal 3: Technical Signal Generation
Generate buy/sell signals based on predictions and technical indicators

---

## 🏗️ Project Structure

```
Crypto/
├── 📘 MACHINE LEARNING
│   ├── CRYPTO_PRICE_PREDICTION.ipynb    # ML training notebook (complete)
│   └── models/                          # Trained models folder
│       ├── xgboost_model.pkl            # XGBoost model
│       ├── lightgbm_model.pkl           # LightGBM model
│       ├── random_forest_model.pkl      # Random Forest model
│       ├── ridge_model.pkl              # Ridge Regression model
│       ├── scaler_X.pkl                 # Feature scaler
│       ├── scaler_y.pkl                 # Target scaler
│       ├── feature_cols.pkl             # Feature column names
│       └── model_metadata.pkl           # Model metadata
│
├── 🌐 WEB APPLICATION
│   ├── app_crypto_predict.py            # Flask backend (580+ lines)
│   ├── run_app.py                       # Python launcher
│   ├── templates/
│   │   ├── crypto_form.html             # Input form page
│   │   ├── crypto_result.html           # Results display page
│   │   └── crypto_about.html            # About & documentation page
│   └── static/
│       ├── css/                         # CSS files
│       └── js/                          # JavaScript files
│
├── ⚙️ CONFIGURATION
│   ├── requirements.txt                 # Python dependencies
│   ├── runtime.txt                      # Python version
│   ├── Procfile                         # Heroku deployment
│   ├── .env.example                     # Environment variables
│   ├── RUN_APP.bat                      # Windows batch launcher
│   └── RUN_APP.ps1                      # PowerShell launcher
│
└── 📖 DOCUMENTATION
    ├── PROJECT_GUIDE.md                 # This file
    ├── MODEL_ANALYSIS.md                # Model selection details
    ├── SETUP_INSTRUCTIONS.md            # Setup guide
    └── API_DOCUMENTATION.md             # REST API reference
```

---

## 📊 Dataset & Features

### Data Source
- **Source**: Yahoo Finance (OHLCV data via yfinance library)
- **Cryptocurrencies**: BTC, ETH, XRP, LTC, ADA, SOL, DOT, DOGE
- **Update Frequency**: **Real-time** (fetched fresh on every request, no caching)
- **Refresh Time**: 3-9 seconds (download + feature engineering + prediction)
- **Training Data**: 5 years (1,825 days)
- **Prediction Data**: 1 year (365 days, configurable)
- **Prediction Timeframe**: Next 24 hours (next day's closing price)
- **Prediction Range**: ±10% of current price (realistic daily volatility)

### Technical Indicators (20+ Features)

#### Moving Averages
- SMA (10, 20, 50)
- EMA (12, 26)

#### Momentum
- RSI (14)
- MACD
- MACD Signal
- MACD Histogram

#### Volatility
- ATR (14)
- Bollinger Bands (Upper, Middle, Lower)

#### Stochastic
- Stoch %K
- Stoch %D

#### Volume
- Volume MA
- Volume Ratio

#### Price Changes
- Daily Return
- Log Return
- Price Change
- High-Low Range

---

## 🤖 Machine Learning Models

### 1. XGBoost Regressor
**Type**: Gradient Boosting  
**Parameters**: 300 estimators, learning_rate=0.05, max_depth=7  
**Use Case**: Captures complex feature interactions  
**Expected RMSE**: ~$150-300 (varies with market conditions)

### 2. LightGBM Regressor
**Type**: Light Gradient Boosting  
**Parameters**: 300 estimators, learning_rate=0.05, max_depth=7  
**Use Case**: Fast training with similar accuracy to XGBoost  
**Expected RMSE**: ~$150-300

### 3. Random Forest Regressor
**Type**: Ensemble of Decision Trees  
**Parameters**: 300 estimators, max_depth=15  
**Use Case**: Robust to outliers, good feature importance  
**Expected RMSE**: ~$200-400

### 4. Ridge Regression
**Type**: Linear Regression with L2 Regularization  
**Parameters**: alpha=1.0  
**Use Case**: Stable predictions, prevents overfitting  
**Expected RMSE**: ~$150-300  
**Weight in Ensemble**: 50% (highest weight due to stability)

### Ensemble Approach
Final prediction = Weighted Average:
- Ridge Regression: 50%
- Random Forest: 20%
- XGBoost: 15%
- LightGBM: 15%

**Benefits**:
- Reduces bias from individual models
- Improves generalization with weighted voting
- More stable predictions (Ridge gets highest weight)
- Better handling of different market conditions
- Sanity checks prevent unrealistic predictions (±10% range)

---

## 🚀 Quick Start Guide

### Step 1: Install Dependencies
```bash
cd Crypto
pip install -r requirements.txt
```

### Step 2: Train Models
```bash
jupyter notebook CRYPTO_PRICE_PREDICTION.ipynb
```
Run all cells to:
- Download cryptocurrency data
- Calculate technical indicators
- Train all 4 models
- Evaluate performance
- Save models to `models/` folder

### Step 3: Start Web Application
```bash
# Option 1: Python
python run_app.py

# Option 2: Batch file (Windows)
RUN_APP.bat

# Option 3: PowerShell (Windows)
.\RUN_APP.ps1

# Option 4: Direct Flask
python app_crypto_predict.py
```

### Step 4: Access Web Interface
Open browser: `http://localhost:5000`

---

## 📈 Model Evaluation Metrics

### RMSE (Root Mean Squared Error)
- Measures average prediction error in dollars
- Lower is better
- Typical range: $100-400

### MAE (Mean Absolute Error)
- Average absolute prediction error
- More interpretable than RMSE
- Typical range: $80-300

### MAPE (Mean Absolute Percentage Error)
- Percentage error relative to price
- Typical range: 1-5%
- Good for comparing across different price ranges

### R² Score
- Coefficient of determination (0-1)
- Higher is better
- Typical range: 0.85-0.95

---

## 🌐 REST API Documentation

### Endpoint 1: Make Prediction
```
POST /api/predict
Content-Type: application/json

{
    "crypto": "BTC-USD",
    "days": 365
}

Response:
{
    "success": true,
    "current_price": 42500.50,
    "predicted_price": 44200.75,
    "all_predictions": {
        "xgboost": 44150.00,
        "lightgbm": 44300.00,
        "random_forest": 44050.00,
        "svr": 44300.00,
        "ensemble": 44200.75
    },
    "price_change": 1700.25,
    "price_change_pct": 4.0,
    "direction": "UP",
    "confidence": 4.0,
    "last_update": "2025-11-27 14:30:00",
    "data_points": 365
}
```

### Endpoint 2: Get Indicators
```
GET /api/indicators

Response:
{
    "success": true,
    "indicators": {
        "Moving Averages": ["SMA_10", "SMA_20", ...],
        "Momentum": ["RSI_14", "MACD", ...],
        ...
    },
    "total_indicators": 20
}
```

### Endpoint 3: Get Models Info
```
GET /api/models

Response:
{
    "success": true,
    "models": ["xgboost", "lightgbm", "random_forest", "svr"],
    "best_model": "xgboost",
    "results": {
        "xgboost": {"RMSE": 250.50, "MAE": 180.25, ...},
        ...
    }
}
```

### Endpoint 4: Health Check
```
GET /health

Response:
{
    "status": "healthy",
    "models_loaded": true,
    "timestamp": "2025-11-27T14:30:00"
}
```

---

## 🔄 Prediction Workflow

### 1. Input Stage
- User selects cryptocurrency (BTC, ETH, etc.)
- Specifies historical data range (30-1825 days, default: 365)
- Submits form or API request

### 2. Real-Time Data Collection (~2-5 seconds)
- Download latest OHLCV data from Yahoo Finance
- Fetch data from selected days back to present
- Verify data completeness and quality

### 3. Feature Engineering (~1-3 seconds)
- Calculate 20+ technical indicators
- Handle missing values (forward/backward fill)
- Sanitize data (remove infinities, clip outliers)
- Create feature vectors

### 4. Preprocessing
- Scale features using RobustScaler
- Prepare for model input
- Normalize target variable with MinMaxScaler

### 5. Model Predictions (~0.5-1 second)
- XGBoost prediction
- LightGBM prediction
- Random Forest prediction
- Ridge Regression prediction
- Calculate weighted ensemble (Ridge: 50%, RF: 20%, XGB: 15%, LGB: 15%)

### 6. Sanity Checks & Post-Processing
- **Clamp predictions to ±10% of current price** (realistic 24-hour range)
- Inverse-scale predictions to USD
- Calculate price change (USD and %)
- Determine direction (UP/DOWN)
- Compute confidence metric
- Log warnings for out-of-range predictions

### 7. Display Results
- Current market price (live)
- 24-hour predicted price (ensemble)
- Individual model predictions breakdown
- Price change and direction with color coding
- Confidence score (0-100%)
- Interactive Chart.js visualization (30-day history + prediction)
- Last update timestamp

**Total Time**: ~3-9 seconds per prediction (always fresh data!)

---

## ⚙️ Deployment Options

### Local Development
```bash
python run_app.py
# Access: http://localhost:5000
```

### Heroku Cloud Deployment
```bash
heroku login
heroku create crypto-price-prediction
git push heroku main
heroku open
```

### Render.com Deployment
1. Connect GitHub repository
2. Set Python runtime: 3.12.3
3. Set build command: `pip install -r Crypto/requirements.txt`
4. Set start command: `cd Crypto && gunicorn app_crypto_predict:app`
5. Auto-deploy on push

### Docker Containerization
```dockerfile
FROM python:3.12.3
WORKDIR /app
COPY Crypto/ .
RUN pip install -r requirements.txt
CMD ["gunicorn", "app_crypto_predict:app"]
```

### AWS/Google Cloud
- Use standard Python 3.12 runtime
- Environment: `FLASK_ENV=production`
- Use Gunicorn with 4+ workers
- Enable auto-scaling for multiple instances

---

## 📝 Configuration

### Environment Variables
```bash
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your_secret_key_here

# Model Configuration
MODEL_TYPE=xgboost
PREDICTION_DAYS=365
CRYPTO_SYMBOL=BTC

# API Configuration
PORT=5000
HOST=0.0.0.0
```

### requirements.txt
Core ML: numpy, pandas, scikit-learn, xgboost, lightgbm  
Web: Flask, Flask-CORS, Werkzeug, gunicorn  
Data: yfinance, pandas-ta, pandas-datareader  
Optional: matplotlib, seaborn, plotly, shap

---

## ⚠️ Important Disclaimers

### Research Use Only
This system is designed for educational and research purposes. It should NOT be used as the sole basis for investment decisions.

### Risk Factors
- Cryptocurrency markets are highly volatile
- Past performance doesn't guarantee future results
- Unexpected market events can cause rapid changes
- Models can be wrong

### Recommendations
- Always conduct your own research
- Consult with qualified financial advisors
- Use proper risk management strategies
- Never invest more than you can afford to lose
- Consider stop-loss and take-profit levels
- Monitor news and market conditions

---

## 🔧 Troubleshooting

### Models Not Loading
**Problem**: "Models not loaded" error
**Solution**:
1. Train models: `jupyter notebook CRYPTO_PRICE_PREDICTION.ipynb`
2. Verify files exist in `models/` folder
3. Check file paths and permissions

### Port Already in Use
**Problem**: "Address already in use"
**Solution**:
```bash
# Find process using port 5000
lsof -i :5000
# Kill process
kill -9 <PID>
```

### Data Download Fails
**Problem**: "Cannot download data from Yahoo Finance"
**Solution**:
1. Check internet connection
2. Verify ticker symbol (e.g., BTC-USD, not BTC)
3. Try different date range
4. Use yfinance directly to test

### Memory Issues
**Problem**: "Out of memory" during training
**Solution**:
1. Reduce historical days (try 365 instead of 1825)
2. Reduce number of samples in training
3. Increase available RAM
4. Use smaller models

---

## 📚 Resources

### Libraries & Documentation
- **XGBoost**: https://xgboost.readthedocs.io/
- **LightGBM**: https://lightgbm.readthedocs.io/
- **Flask**: https://flask.palletsprojects.com/
- **Scikit-learn**: https://scikit-learn.org/
- **Pandas**: https://pandas.pydata.org/
- **Pandas-TA**: https://github.com/twopirllc/pandas-ta

### Cryptocurrency Resources
- **Yahoo Finance**: https://finance.yahoo.com/
- **CoinMarketCap**: https://coinmarketcap.com/
- **TradingView**: https://www.tradingview.com/

### Learning Resources
- Machine Learning Mastery
- Towards Data Science (Medium)
- Fast.ai Deep Learning Course

---

## 📞 Support

### Common Issues
See **Troubleshooting** section above

### Contact
- GitHub: [Your Repository]
- Email: [Your Email]

### Contributing
Contributions welcome! Please follow:
1. Fork repository
2. Create feature branch
3. Submit pull request
4. Include tests and documentation

---

## 📄 License

MIT License - Free for educational and research use

---

**Project Status**: ✅ **COMPLETE & PRODUCTION READY**

**Last Updated**: November 28, 2025  
**Version**: 1.1.0 (with realistic prediction ranges)

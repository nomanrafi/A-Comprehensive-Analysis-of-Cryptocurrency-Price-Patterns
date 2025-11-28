from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import joblib
import os
from pathlib import Path
import warnings
import yfinance as yf
from datetime import datetime, timedelta
import sys
import io

# Optional import for pandas_ta
try:
    import pandas_ta as ta
except:
    ta = None

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

warnings.filterwarnings('ignore')

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'crypto_price_prediction_2025'

SCRIPT_DIR = Path(__file__).resolve().parent
print(f"📍 Application directory: {SCRIPT_DIR}")

# ==========================================
# 1. LOAD MODELS AND SCALERS
# ==========================================

def load_models():
    """Load trained models and preprocessing objects"""
    try:
        models_dir = SCRIPT_DIR / 'models'
        
        print(f"🔍 Checking for model files in: {models_dir}")
        
        # Check if files exist
        required_files = [
            'xgboost_model.pkl',
            'lightgbm_model.pkl',
            'random_forest_model.pkl',
            'ridge_model.pkl',
            'scaler_X.pkl',
            'scaler_y.pkl',
            'feature_cols.pkl',
            'model_metadata.pkl'
        ]
        
        missing_files = []
        for f in required_files:
            fpath = models_dir / f
            print(f"   - {f}: {fpath.exists()}")
            if not fpath.exists():
                missing_files.append(str(fpath))
        
        if missing_files:
            print(f"❌ Missing model files:")
            for f in missing_files:
                print(f"   - {f}")
            return None
        
        print("📦 Loading model files...")
        
        # Load all models
        xgb_model = joblib.load(str(models_dir / 'xgboost_model.pkl'))
        lgb_model = joblib.load(str(models_dir / 'lightgbm_model.pkl'))
        rf_model = joblib.load(str(models_dir / 'random_forest_model.pkl'))
        ridge_model = joblib.load(str(models_dir / 'ridge_model.pkl'))
        
        # Load scalers and metadata
        scaler_X = joblib.load(str(models_dir / 'scaler_X.pkl'))
        scaler_y = joblib.load(str(models_dir / 'scaler_y.pkl'))
        feature_cols = joblib.load(str(models_dir / 'feature_cols.pkl'))
        metadata = joblib.load(str(models_dir / 'model_metadata.pkl'))
        
        print(f"   ✓ XGBoost model loaded")
        print(f"   ✓ LightGBM model loaded")
        print(f"   ✓ Random Forest model loaded")
        print(f"   ✓ Ridge Regression model loaded")
        print(f"   ✓ Scalers loaded")
        print(f"   ✓ Metadata loaded")
        
        return {
            'xgboost': xgb_model,
            'lightgbm': lgb_model,
            'random_forest': rf_model,
            'ridge': ridge_model,
            'scaler_X': scaler_X,
            'scaler_y': scaler_y,
            'feature_cols': feature_cols,
            'metadata': metadata
        }
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        import traceback
        traceback.print_exc()
        return None


MODELS = load_models()

# ==========================================
# 2. FEATURE ENGINEERING FUNCTION
# ==========================================

def calculate_rsi(prices, period=14):
    """Calculate RSI indicator"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_atr(high, low, close, period=14):
    """Calculate ATR indicator"""
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr

def calculate_stochastic(high, low, close, k_period=14, d_period=3):
    """Calculate Stochastic Oscillator"""
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
    d_percent = k_percent.rolling(window=d_period).mean()
    return k_percent, d_percent

def create_features(df):
    """Calculate technical indicators for price prediction"""
    try:
        print(f"[DEBUG] create_features called with df shape: {df.shape if df is not None else 'None'}")
        print(f"[DEBUG] df columns: {df.columns.tolist() if df is not None else 'None'}")
        
        if df is None or len(df) == 0:
            print("[DEBUG] df is None or empty!")
            return None
            
        df_tech = df.copy()
        
        # Ensure required columns exist
        required_cols = ['Close', 'Open', 'High', 'Low', 'Volume']
        for col in required_cols:
            if col not in df_tech.columns:
                print(f"[DEBUG] Missing column: {col}")
                print(f"[DEBUG] Available columns: {df_tech.columns.tolist()}")
                return None
        
        print("[DEBUG] All required columns present, calculating indicators...")
        
        # Moving Averages
        df_tech['SMA_10'] = df_tech['Close'].rolling(window=10).mean()
        df_tech['SMA_20'] = df_tech['Close'].rolling(window=20).mean()
        df_tech['SMA_50'] = df_tech['Close'].rolling(window=50).mean()
        df_tech['EMA_12'] = df_tech['Close'].ewm(span=12, adjust=False).mean()
        df_tech['EMA_26'] = df_tech['Close'].ewm(span=26, adjust=False).mean()
        
        # RSI
        df_tech['RSI_14'] = calculate_rsi(df_tech['Close'], 14)
        
        # MACD
        ema_12 = df_tech['Close'].ewm(span=12, adjust=False).mean()
        ema_26 = df_tech['Close'].ewm(span=26, adjust=False).mean()
        df_tech['MACD'] = ema_12 - ema_26
        df_tech['MACD_Signal'] = df_tech['MACD'].ewm(span=9, adjust=False).mean()
        df_tech['MACD_Diff'] = df_tech['MACD'] - df_tech['MACD_Signal']
        
        # Bollinger Bands
        sma_20 = df_tech['Close'].rolling(window=20).mean()
        std_20 = df_tech['Close'].rolling(window=20).std()
        df_tech['BB_Upper'] = sma_20 + (2 * std_20)
        df_tech['BB_Lower'] = sma_20 - (2 * std_20)
        df_tech['BB_Middle'] = sma_20
        
        # ATR
        df_tech['ATR_14'] = calculate_atr(df_tech['High'], df_tech['Low'], df_tech['Close'], 14)
        
        # Stochastic
        df_tech['Stoch_K'], df_tech['Stoch_D'] = calculate_stochastic(df_tech['High'], df_tech['Low'], df_tech['Close'])
        
        # Volume
        df_tech['Volume_MA'] = df_tech['Volume'].rolling(window=20).mean()
        df_tech['Volume_Ratio'] = df_tech['Volume'] / df_tech['Volume_MA'].replace(0, 1)
        
        # Returns
        df_tech['Daily_Return'] = df_tech['Close'].pct_change()
        df_tech['Log_Return'] = np.log(df_tech['Close'] / df_tech['Close'].shift(1))
        
        # Price changes
        df_tech['Price_Change'] = df_tech['Close'] - df_tech['Open']
        df_tech['High_Low'] = df_tech['High'] - df_tech['Low']

        # --- SANITIZATION START ---
        # Replace infinite values with NaN
        df_tech.replace([np.inf, -np.inf], np.nan, inplace=True)
        
        # Fill NaN values (forward fill then backward fill)
        df_tech.fillna(method='ffill', inplace=True)
        df_tech.fillna(method='bfill', inplace=True)
        
        # Clip potentially explosive values to reasonable ranges
        # Volume ratio shouldn't be massive unless it's a pump/dump, but > 10 is extreme
        if 'Volume_Ratio' in df_tech.columns:
            df_tech['Volume_Ratio'] = df_tech['Volume_Ratio'].clip(lower=0, upper=10)
            
        # Daily returns shouldn't be > 100% or < -90% in a single day for major cryptos usually
        if 'Daily_Return' in df_tech.columns:
            df_tech['Daily_Return'] = df_tech['Daily_Return'].clip(lower=-0.9, upper=1.0)
            
        if 'Log_Return' in df_tech.columns:
            df_tech['Log_Return'] = df_tech['Log_Return'].clip(lower=-2.5, upper=2.5)
        # --- SANITIZATION END ---
        
        print(f"[DEBUG] Features created successfully! Shape: {df_tech.shape}")
        return df_tech
    except Exception as e:
        print(f"[ERROR] Error creating features: {e}")
        import traceback
        traceback.print_exc()
        return None


def get_prediction(crypto_symbol='BTC-USD', days_back=365):
    """Get price prediction for cryptocurrency"""
    if MODELS is None:
        return None, "Models not loaded"
    
    try:
        # Download data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        df = yf.download(crypto_symbol, start=start_date, end=end_date, progress=False)
        
        # Handle MultiIndex from yfinance
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        df.reset_index(inplace=True)
        
        # Ensure column names are correct
        df.columns = df.columns.str.strip()
        
        # Create features
        df_tech = create_features(df)
        
        if df_tech is None:
            return {
                'success': False,
                'error': 'Failed to calculate technical indicators'
            }
        
        df_clean = df_tech.dropna()
        
        # Get latest data point
        feature_cols = MODELS['feature_cols']
        X_latest = df_clean[feature_cols].values[-1:].reshape(1, -1)
        
        # Scale
        X_scaled = MODELS['scaler_X'].transform(X_latest)
        
        # Make predictions
        xgb_pred = MODELS['xgboost'].predict(X_scaled)[0]
        lgb_pred = MODELS['lightgbm'].predict(X_scaled)[0]
        rf_pred = MODELS['random_forest'].predict(X_scaled)[0]
        ridge_pred = MODELS['ridge'].predict(X_scaled)[0]
        
        # Ensemble prediction (weighted average - Ridge gets more weight as it's best model)
        ensemble_pred = np.mean([xgb_pred * 0.15, lgb_pred * 0.15, rf_pred * 0.2, ridge_pred * 0.5])
        
        # Inverse transform
        predictions = {
            'xgboost': float(MODELS['scaler_y'].inverse_transform([[xgb_pred]])[0][0]),
            'lightgbm': float(MODELS['scaler_y'].inverse_transform([[lgb_pred]])[0][0]),
            'random_forest': float(MODELS['scaler_y'].inverse_transform([[rf_pred]])[0][0]),
            'ridge': float(MODELS['scaler_y'].inverse_transform([[ridge_pred]])[0][0]),
            'ensemble': float(MODELS['scaler_y'].inverse_transform([[ensemble_pred]])[0][0])
        }
        
        # --- SANITY CHECK START ---
        # Current price
        current_price = float(df_clean['Close'].iloc[-1])
        
        # For 24-hour predictions, realistic range is ±10% (0.90x to 1.10x)
        # Even in volatile crypto markets, 10% daily moves are significant
        # Bitcoin rarely moves more than 15-20% in a single day except during extreme events
        min_reasonable = current_price * 0.90  # -10%
        max_reasonable = current_price * 1.10  # +10%
        
        for model_name in predictions:
            pred = predictions[model_name]
            if pred < min_reasonable or pred > max_reasonable:
                print(f"⚠️ [WARNING] {model_name} prediction ${pred:,.2f} is outside reasonable 24h range (${min_reasonable:,.2f}-${max_reasonable:,.2f}). Clamping.")
                predictions[model_name] = max(min_reasonable, min(pred, max_reasonable))
        # --- SANITY CHECK END ---
        
        # Current price
        current_price = float(df_clean['Close'].iloc[-1])
        
        # Price change prediction
        price_change = predictions['ensemble'] - current_price
        price_change_pct = (price_change / current_price) * 100
        
        return {
            'success': True,
            'current_price': current_price,
            'predicted_price': predictions['ensemble'],
            'all_predictions': predictions,
            'price_change': price_change,
            'price_change_pct': price_change_pct,
            'direction': 'UP' if price_change > 0 else 'DOWN',
            'direction_color': '🟢' if price_change > 0 else '🔴',
            'confidence': abs(price_change_pct),
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_points': len(df_clean),
            'historical_data': {
                'dates': df_clean['Date'].dt.strftime('%Y-%m-%d').tolist()[-30:],
                'prices': df_clean['Close'].tolist()[-30:]
            }
        }
    
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


# ==========================================
# 3. FLASK ROUTES
# ==========================================

@app.route('/', methods=['GET', 'POST'])
def index():
    """Home page with prediction form"""
    try:
        if request.method == 'POST':
            crypto_symbol = request.form.get('crypto', 'BTC-USD')
            days = int(request.form.get('days', 365))
            
            prediction = get_prediction(crypto_symbol, days)
            
            if prediction.get('success'):
                return render_template('crypto_result.html', prediction=prediction)
            else:
                return render_template('crypto_form.html', error=prediction.get('error'))
        
        return render_template('crypto_form.html')
    except Exception as e:
        return render_template('crypto_form.html', error=str(e))


@app.route('/about')
def about():
    """About page"""
    return render_template('crypto_about.html', metadata=MODELS['metadata'] if MODELS else None)


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """REST API for predictions"""
    try:
        data = request.get_json()
        crypto_symbol = data.get('crypto', 'BTC-USD')
        days = int(data.get('days', 365))
        
        prediction = get_prediction(crypto_symbol, days)
        
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/indicators', methods=['GET'])
def api_indicators():
    """Get available technical indicators"""
    try:
        if MODELS is None:
            return jsonify({'error': 'Models not loaded'}), 500
        
        indicators = {
            'Moving Averages': ['SMA_10', 'SMA_20', 'SMA_50', 'EMA_12', 'EMA_26'],
            'Momentum': ['RSI_14', 'MACD', 'MACD_Signal', 'MACD_Diff'],
            'Volatility': ['ATR_14', 'BB_Upper', 'BB_Lower', 'BB_Middle'],
            'Stochastic': ['Stoch_K', 'Stoch_D'],
            'Volume': ['Volume_MA', 'Volume_Ratio'],
            'Returns': ['Daily_Return', 'Log_Return', 'Price_Change', 'High_Low']
        }
        
        return jsonify({
            'success': True,
            'indicators': indicators,
            'total_indicators': sum(len(v) for v in indicators.values())
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/models', methods=['GET'])
def api_models():
    """Get model information"""
    try:
        if MODELS is None:
            return jsonify({'error': 'Models not loaded'}), 500
        
        return jsonify({
            'success': True,
            'models': MODELS['metadata']['models_trained'],
            'best_model': MODELS['metadata']['best_model'],
            'results': MODELS['metadata']['results']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': MODELS is not None,
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    print(f"\n{'='*70}")
    print(f"🚀 CRYPTOCURRENCY PRICE PREDICTION - Flask Application")
    print(f"{'='*70}")
    
    if MODELS is None:
        print(f"⚠️  WARNING: Models not loaded. Please train models first!")
        print(f"   Run: jupyter notebook CRYPTO_PRICE_PREDICTION.ipynb")
    else:
        print(f"✅ Models loaded successfully!")
        print(f"   Best model: {MODELS['metadata']['best_model'].upper()}")
        print(f"   Features: {MODELS['metadata']['num_features']}")
    
    print(f"\n🌐 Starting Flask development server...")
    print(f"📡 Local URL: http://127.0.0.1:5000")
    print(f"🌍 API Base: http://127.0.0.1:5000/api/\n")
    
    app.run(debug=False, host='0.0.0.0', port=5000)

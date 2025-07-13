import pandas as pd
import numpy as np
import joblib
import holidays
from sklearn.metrics import mean_absolute_error
from sklearn.inspection import partial_dependence
import lightgbm as lgb
from sklearn.model_selection import TimeSeriesSplit


def prepare_data(df):
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    
    df['DayOfYear'] = df['Date'].dt.dayofyear
    df['WeekOfYear'] = df['Date'].dt.isocalendar().week
    df['Quarter'] = df['Date'].dt.quarter
    
    df['InventoryRatio'] = df['Inventory Level'] / df['Units Sold'].replace(0, 1)
    df['StockoutRisk'] = (df['Inventory Level'] < df['Units Sold'].rolling(7).mean()).astype(int)
    
    df['PriceRatio'] = df['Price'] / (df['Competitor Pricing'] + 1e-6)
    df['EffectivePrice'] = df['Price'] * (1 - df['Discount']/100)
    
    df = df.sort_values(['Store ID', 'Product ID', 'Date'])
    for lag in [1, 7, 14]:
        df[f'Lag_{lag}'] = df.groupby(['Store ID', 'Product ID'])['Units Sold'].shift(lag)
    
    for window in [7, 14]:
        df[f'RollingMean_{window}'] = df.groupby(['Store ID', 'Product ID'])['Lag_1'].transform(
            lambda x: x.rolling(window, min_periods=1).mean()
        )

    cal = holidays.US(years=[2022, 2023])
    df['IsHoliday'] = df['Date'].dt.date.isin(cal).astype(int)
    
    df = df.drop(columns=['Date', 'Units Ordered', 'Demand'])

    cat_cols = ['Store ID', 'Product ID', 'Category', 'Region', 
                'Weather Condition', 'Seasonality']
    for col in cat_cols:
        df[col] = df[col].astype('category')
        
    return df.dropna()

def safe_mape(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    non_zero_idx = y_true != 0
    return np.mean(np.abs((y_true[non_zero_idx] - y_pred[non_zero_idx]) / y_true[non_zero_idx]))

def train_model(df):
    df = prepare_data(df)
    
    tscv = TimeSeriesSplit(n_splits=3)
    X = df.drop(columns=['Units Sold'])
    y = df['Units Sold']
    
    best_score = float('inf')
    
    for fold, (train_idx, val_idx) in enumerate(tscv.split(X)):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        
        model = lgb.LGBMRegressor(
            n_estimators=200,
            learning_rate=0.05,
            max_depth=5,
            random_state=42
        )
        
        model.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            eval_metric='mape',
            categorical_feature=['Store ID', 'Region']
        )
        
        if model.best_score_['valid_0']['mape'] < best_score:
            joblib.dump(model, "model/demand_predictor.pkl")
            best_score = model.best_score_['valid_0']['mape']
    
    return model

def historical_validation():
    print("Running Historical Validation...")
    df = pd.read_csv("Database/sales_data.csv")
    train_df = df[pd.to_datetime(df['Date']) < '2023-07-01']
    test_df = df[pd.to_datetime(df['Date']) >= '2023-07-01']
    
    model = train_model(train_df)
    test_df = prepare_data(test_df)
    
    X_test = test_df.drop(columns=['Units Sold'])
    y_test = test_df['Units Sold']
    preds = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, preds)
    mape = safe_mape(y_test, preds)
    
    print(f"Historical Performance (Last 6 Months):")
    print(f"  - MAE: {mae:.2f}")
    print(f"  - MAPE: {mape:.2%}")
    print(f"  - Understock Rate: {(y_test > preds).mean():.2%}")
    
    return {'mae': mae, 'mape': mape, 'predictions': preds}

def business_impact_analysis():
    print("\nRunning Business Impact Analysis...")
    val_results = historical_validation()
    df = pd.read_csv("Database/sales_data.csv")
    test_df = df[pd.to_datetime(df['Date']) >= '2023-07-01']
    test_df = prepare_data(test_df)
    
    # Simulate business metrics
    test_df['Predicted'] = val_results['predictions']
    test_df['Overstock'] = (test_df['Inventory Level'] - test_df['Units Sold']).clip(lower=0)
    test_df['Stockout'] = (test_df['Units Sold'] > test_df['Inventory Level']).astype(int)
    
    waste_cost = test_df['Overstock'].sum() * test_df['Price'].mean() * 0.15
    lost_sales = test_df[test_df['Stockout'] == 1]['Units Sold'].sum() * test_df['Price'].mean() * 0.3
    
    print("Estimated Business Impact:")
    print(f"  - Potential Waste Reduction: ${waste_cost:,.2f}")
    print(f"  - Potential Lost Sales Prevention: ${lost_sales:,.2f}")
    print(f"  - Total Opportunity: ${waste_cost + lost_sales:,.2f}")
    
    return {'waste_cost': waste_cost, 'lost_sales': lost_sales}

def model_diagnostics():
    print("\nRunning Model Diagnostics...")
    model = joblib.load("model/demand_predictor.pkl")
    df = pd.read_csv("Database/sales_data.csv")
    df = prepare_data(df)
    
    importance = pd.DataFrame({
        'Feature': model.booster_.feature_name(),
        'Importance': model.booster_.feature_importance()
    }).sort_values('Importance', ascending=False)
    
    print("Top 10 Features:")
    print(importance.head(10))
    
    # Partial Dependence
    print("\nPartial Dependence Samples:")
    for feature in ['Price', 'Discount', 'Lag_7']:
        if feature in importance['Feature'].values:
            pdp = partial_dependence(model, df.drop(columns=['Units Sold']), 
                                   features=[feature])
            print(f"  - {feature}: Min Effect {min(pdp['average'][0]):.2f}, Max Effect {max(pdp['average'][0]):.2f}")
    
    return importance

def sensitivity_analysis():
    print("\nRunning Sensitivity Analysis...")
    model = joblib.load("model/demand_predictor.pkl")
    df = pd.read_csv("Database/sales_data.csv")
    base_df = prepare_data(df)
    
    scenarios = []
    for epidemic in [0, 1]:
        for discount in [0, 30]:
            test_df = base_df.copy()
            test_df['Epidemic'] = epidemic
            test_df['Discount'] = discount
            preds = model.predict(test_df.drop(columns=['Units Sold']))
            
            scenarios.append({
                'Epidemic': epidemic,
                'Discount': discount,
                'AvgPrediction': np.mean(preds),
                'PctChange': (np.mean(preds) - np.mean(base_df['Units Sold'])) / np.mean(base_df['Units Sold'])
            })
    
    results = pd.DataFrame(scenarios)
    print("Scenario Analysis:")
    print(results)
    
    return results

# ----------------------------
# 4. Main Execution
# ----------------------------
if __name__ == "__main__":
    print("="*50)
    print("Sales Prediction Model Test Suite")
    print("="*50)
    
    # Run all tests
    hist_val = historical_validation()
    business_impact = business_impact_analysis()
    diagnostics = model_diagnostics()
    sensitivity = sensitivity_analysis()
    
    print("\nAll tests completed!")
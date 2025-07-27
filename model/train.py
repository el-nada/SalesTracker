import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

store_sales = pd.read_csv("Database/sales_data.csv")
store_sales['Date'] = pd.to_datetime(
    store_sales['Date'], errors='coerce'
)
# Drop rows with invalid dates
invalid_dates = store_sales['Date'].isna().sum()
if invalid_dates > 0:
    store_sales = store_sales.dropna(subset=['Date'])

def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate daily sales data into weekly features and generate
    additional engineered features for forecasting.
    """
    # Week start marker
    df['Week_Marker'] = df['Date'] - pd.to_timedelta(
        df['Date'].dt.dayofweek, unit='D'
    )

    # Aggregation rules
    agg_dict = {
        'Units Sold': 'sum',
        'Inventory Level': 'mean',
        'Price': 'mean',
        'Discount': 'mean',
        'Promotion': 'mean',
        'Competitor Pricing': 'mean',
        'Demand': 'mean',
        'Units Ordered': 'sum',
        'Epidemic': 'max',
        'Store ID': lambda x: x.mode()[0],
        'Product ID': lambda x: x.mode()[0],
        'Category': lambda x: x.mode()[0],
        'Region': lambda x: x.mode()[0],
        'Date': ['min', 'max', 'count']
    }
    weekly = df.groupby('Week_Marker').agg(agg_dict).reset_index()

    # Flatten columns
    weekly.columns = [
        'Week_Marker', 'Units_Sold', 'Inventory_Level', 'Price',
        'Discount', 'Promotion', 'Competitor_Pricing', 'Demand',
        'Units_Ordered', 'Epidemic', 'Store_ID', 'Product_ID',
        'Category', 'Region', 'Week_Start', 'Week_End', 'Days_in_Week'
    ]

    # Drop first and last incomplete weeks
    weekly = weekly.iloc[1:-1].copy()

    # Temporal features
    weekly['Week_Num'] = weekly['Week_Start'].dt.isocalendar().week
    weekly['Month'] = weekly['Week_Start'].dt.month
    weekly['Quarter'] = weekly['Week_Start'].dt.quarter
    weekly['Year'] = weekly['Week_Start'].dt.year

    # Advanced features
    weekly['Price_Change'] = weekly['Price'].pct_change()
    weekly['Discount_Intensity'] = weekly['Discount'] * weekly['Promotion']
    weekly['Competitive_Advantage'] = weekly['Competitor_Pricing'] - weekly['Price']

    # Lag features for past 8 weeks
    lag_weeks = 8
    for i in range(1, lag_weeks + 1):
        weekly[f'Sales_Lag_{i}'] = weekly['Units_Sold'].shift(i)
        weekly[f'Demand_Lag_{i}'] = weekly['Demand'].shift(i)

    # Drop any rows with missing values introduced by lags
    return weekly.dropna()

def build_model() -> RandomForestRegressor:
    """
    Create and return a scikit-learn pipeline that:
    - Standardizes numerical features
    - One-hot encodes categorical features
    - Fits a RandomForestRegressor
    """
    # Categorical and numerical feature lists
    categorical_features = ['Store_ID', 'Product_ID', 'Category', 'Region']
    numerical_features = [
        'Inventory_Level', 'Price', 'Discount', 'Promotion',
        'Competitor_Pricing', 'Demand', 'Week_Num', 'Month',
        'Quarter', 'Year', 'Price_Change', 'Discount_Intensity',
        'Competitive_Advantage'
    ]
    # Add lag features
    for i in range(1, 9):
        numerical_features.extend([f'Sales_Lag_{i}', f'Demand_Lag_{i}'])

    preprocessor = ColumnTransformer([
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features)
    ])

    pipeline = make_pipeline(
        preprocessor,
        RandomForestRegressor(
            n_estimators=300,
            max_depth=10,
            min_samples_split=5,
            random_state=42,
            n_jobs=-1
        )
    )
    return pipeline

def save_model(model, path: str = 'model/sales_rf_model.pkl') -> None:
    """Save the trained model pipeline to disk using joblib."""
    joblib.dump(model, path)
    print(f"Model saved to {path}")


def load_model(path: str = 'model/sales_rf_model.pkl'):
    """Load and return a model pipeline from disk."""
    return joblib.load(path)


def predict_sales(model, input_df: pd.DataFrame) -> np.ndarray:
    """Given a feature-engineered DataFrame, predict units sold."""
    return model.predict(input_df)

if __name__ == '__main__':
    # Feature Creation
    weekly_sales = create_features(store_sales)
    print(f"Weekly data: {len(weekly_sales)} rows from {weekly_sales['Week_Start'].min()} to {weekly_sales['Week_Start'].max()}")

    # Prepare train/test split
    target = 'Units_Sold'
    X = weekly_sales.drop(columns=[target, 'Week_Marker', 'Week_Start', 'Week_End', 'Days_in_Week'])
    y = weekly_sales[target]
    test_size = 8
    X_train, X_test = X.iloc[:-test_size], X.iloc[-test_size:]
    y_train, y_test = y.iloc[:-test_size], y.iloc[-test_size:]

    # Train and save model
    model = build_model()
    model.fit(X_train, y_train)
    save_model(model)

    # Evaluate
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Evaluation metrics -> RMSE: {rmse:.2f}, MAE: {mae:.2f}, R²: {r2:.4f}")

    # Visualization
    plt.figure(figsize=(12, 6))
    plt.plot(weekly_sales['Week_Start'].iloc[:-test_size], y_train, label='Train')
    plt.plot(weekly_sales['Week_Start'].iloc[-test_size:], y_test, 'g-', label='Actual')
    plt.plot(weekly_sales['Week_Start'].iloc[-test_size:], y_pred, 'r--', label='Predicted')
    plt.xlabel('Week Start')
    plt.ylabel('Units Sold')
    plt.title('Sales Forecast vs Actual')
    plt.legend(); plt.grid(True); plt.show()

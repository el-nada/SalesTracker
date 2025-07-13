import os
import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import seaborn as sns
from train import prepare_data  

def safe_mape(y_true, y_pred):
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    non_zero = y_true != 0
    return np.mean(np.abs((y_true[non_zero] - y_pred[non_zero]) / y_true[non_zero]))

print("Starting evaluation...")

df = pd.read_csv("Database/sales_data.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values("Date")

# 80/20 Time-based Split
split_index = int(len(df) * 0.8)
train_df = df.iloc[:split_index]
test_df = df.iloc[split_index:]

# Prepare data
train_prepared = prepare_data(train_df)
test_prepared = prepare_data(test_df)

X_test = test_prepared.drop(columns=["Units Sold"])
y_test = test_prepared["Units Sold"]

model = joblib.load("model/demand_predictor.pkl")
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mape = safe_mape(y_test, y_pred)

print(f"\nEvaluation on Last 20%:")
print(f"  - MAE: {mae:.2f}")
print(f"  - MAPE: {mape:.2%}")

comparison = test_df.iloc[-len(y_test):].copy()
comparison["Predicted Units Sold"] = y_pred.round(2)

cols_to_keep = ["Date", "Store ID", "Product ID", "Units Sold", "Predicted Units Sold"]
os.makedirs("results", exist_ok=True)
comparison[cols_to_keep].to_csv("results/predictions_vs_actuals.csv", index=False)

print("Predictions saved to 'results/predictions_vs_actuals.csv'")


def plot_actual_vs_predicted(test_df, product_ids, start_date=None, end_date=None):
    df_filtered = test_df[test_df['Product ID'].isin(product_ids)].copy()

    if start_date:
        df_filtered = df_filtered[df_filtered['Date'] >= pd.to_datetime(start_date)]
    if end_date:
        df_filtered = df_filtered[df_filtered['Date'] <= pd.to_datetime(end_date)]

    plt.figure(figsize=(15, 7))
    sns.lineplot(data=df_filtered, x='Date', y='Units Sold', hue='Product ID', style=None, markers=True, dashes=False)
    sns.lineplot(data=df_filtered, x='Date', y='Predicted Units Sold', hue='Product ID', style=None, markers=False, dashes=True)
    
    plt.title('Actual vs Predicted Units Sold')
    plt.xlabel('Date')
    plt.ylabel('Units Sold')
    plt.legend(title='Product ID')
    plt.show()

print (comparison)
plot_actual_vs_predicted(comparison, product_ids=['P0001', 'P0015'], start_date='2024-01-20', end_date='2024-02-05')
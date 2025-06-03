import pandas as pd

def load_data():
    df = pd.read_csv("data/retail_data.csv")
    
    df['Date'] = pd.to_datetime(df['Date'])

    # Drop row with missing values 
    df = df.dropna(subset=['Units Sold', 'Inventory', 'Store ID', 'Category'])

    return df


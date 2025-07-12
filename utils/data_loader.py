import pandas as pd

def load_data():
    df = pd.read_csv("Database/sales_data.csv")
    
    df['Date'] = pd.to_datetime(df['Date'])

    # Drop row with missing values 
    df = df.dropna(subset=['Units Sold', 'Inventory Level', 'Store ID', 'Category'])

    return df

def compute_kpis(df):
    df['Date'] = pd.to_datetime(df['Date'])

    latest_date = df['Date'].max()
    previous_date = latest_date - pd.Timedelta(days=1)

    today_data = df[df['Date'] == latest_date].copy()
    yesterday_data = df[df['Date'] == previous_date].copy()

    today_data['Sales'] = today_data['Units Sold'] * today_data['Price']
    yesterday_data['Sales'] = yesterday_data['Units Sold'] * yesterday_data['Price']
    
    today_sales = today_data['Sales'].sum()
    yesterday_sales = yesterday_data['Sales'].sum()

    delta_sales = today_sales - yesterday_sales
    delta_sales_pct = (delta_sales / yesterday_sales * 100) if yesterday_sales != 0 else 0

    total_units = today_data['Units Sold'].sum()
    yesterday_units = yesterday_data['Units Sold'].sum()
    delta_units = total_units - yesterday_units
    delta_units_pct = (delta_units / yesterday_units * 100) if yesterday_units != 0 else 0

    return {
        "total_sales": f"${today_sales:,.0f}",
        "delta_sales": f"{delta_sales_pct:+.1f}%",
        "units_sold": int(total_units),
        "delta_units": f"{delta_units_pct:+.1f}%",
    }

def compute_filter_args(df): 
    date_range = df['Date'].min(), df['Date'].max()

    store_options = df['Store ID'].unique()
    category_options = df['Category'].unique()
    highest_price = df['Price'].max().round()
    lowest_price = df['Price'].min().round()
    return (date_range, store_options, category_options, (highest_price, lowest_price))
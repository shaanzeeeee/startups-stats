import pandas as pd

df = pd.read_csv("yc_companies.csv")
print(f"Total rows: {len(df)}")
print(f"Columns: {list(df.columns)}")

print(f"\nNull counts:")
print(df.isnull().sum())

print(f"\nUnique countries: {df['Company Country'].nunique()}")
print(f"Unique batches: {df['Batch'].nunique()}")
print(f"Unique industries: {df['Industry'].nunique()}")
print(f"Unique sub-industries: {df['Sub Industry'].nunique()}")

print(f"\nFirst 5 rows:")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
print(df.head().to_string())

print(f"\nSample well-known companies:")
known = ["DoorDash", "Airbnb", "Stripe", "Coinbase", "Dropbox"]
matches = df[df["Company Name"].isin(known)]
print(matches.to_string())

print(f"\nTop 10 countries:")
print(df["Company Country"].value_counts().head(10))

print(f"\nTop 10 batches:")
print(df["Batch"].value_counts().head(10))

print(f"\nEmpty-string columns:")
for col in df.columns:
    empty = (df[col].astype(str).str.strip() == "").sum()
    if empty > 0:
        print(f"  {col}: {empty}")

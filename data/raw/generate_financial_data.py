import pandas as pd
import numpy as np

np.random.seed(42)

companies = [
    "Apple", "Microsoft", "Google", "Amazon", "Meta",
    "Tesla", "Netflix", "Nvidia", "IBM", "Oracle"
]

years = list(range(2000, 2025))  # 25 years
records_per_year = 20  # 25 × 20 × 10 ≈ 5000 rows

data = []

for company in companies:
    base_revenue = np.random.uniform(20_000, 300_000)

    for year in years:
        for _ in range(records_per_year):
            growth = np.random.uniform(0.95, 1.15)
            revenue = base_revenue * growth

            net_income = revenue * np.random.uniform(0.05, 0.30)
            assets = revenue * np.random.uniform(1.5, 3.5)
            liabilities = assets * np.random.uniform(0.3, 0.8)
            cash_flow = net_income * np.random.uniform(0.8, 1.3)

            data.append([
                company,
                year,
                round(revenue, 2),
                round(net_income, 2),
                round(assets, 2),
                round(liabilities, 2),
                round(cash_flow, 2)
            ])

        base_revenue = revenue  # growth carries forward

df = pd.DataFrame(
    data,
    columns=[
        "Company",
        "Year",
        "Revenue",
        "NetIncome",
        "Assets",
        "Liabilities",
        "CashFlow"
    ]
)

print("Total rows:", len(df))

df.to_csv("sec_financials.csv", index=False)
print("Saved as sec_financials.csv")

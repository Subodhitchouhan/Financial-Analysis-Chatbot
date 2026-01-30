import pandas as pd
import os

# ================= SAFE PROJECT ROOT =================
# chatbot/financial_chatbot.py → go UP one level to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "cleaned_financials.csv"
)

# ================= LOAD DATA =================
df = pd.read_csv(DATA_PATH)
df = df.sort_values(["Company", "Year"])

# ================= DERIVED METRICS =================
df["Profit_Margin"] = (df["NetIncome"] / df["Revenue"]) * 100
df["Debt_Ratio"] = (df["Liabilities"] / df["Assets"]) * 100
df["Revenue_Growth"] = df.groupby("Company")["Revenue"].pct_change() * 100
df["Profit_Growth"] = df.groupby("Company")["NetIncome"].pct_change() * 100


def chatbot(query: str):
    query = query.lower()
    companies = df["Company"].unique()

    def find_company():
        for c in companies:
            if c.lower() in query:
                return c
        return None

    company = find_company()

    if "revenue" in query and company:
        val = df[df["Company"] == company].iloc[-1]["Revenue"]
        return f"{company}'s latest revenue is ${val:,.0f} million."

    if "net income" in query and company:
        val = df[df["Company"] == company].iloc[-1]["NetIncome"]
        return f"{company}'s latest net income is ${val:,.0f} million."

    if "profit margin" in query and company:
        val = df[df["Company"] == company].iloc[-1]["Profit_Margin"]
        return f"{company}'s profit margin is {val:.2f}%."

    if "debt" in query and company:
        val = df[df["Company"] == company].iloc[-1]["Debt_Ratio"]
        return f"{company}'s debt ratio is {val:.2f}%."

    if "revenue growth" in query and company:
        val = df[df["Company"] == company].iloc[-1]["Revenue_Growth"]
        return f"{company}'s revenue growth is {val:.2f}%."

    if "profit growth" in query and company:
        val = df[df["Company"] == company].iloc[-1]["Profit_Growth"]
        return f"{company}'s profit growth is {val:.2f}%."

    # if "compare" in query:
    #     return (
    #         df.groupby("Company")["Revenue"]
    #         .mean()
    #         .sort_values(ascending=False)
    #         .to_string()
    #     )

# ================= COMPARISON QUERIES =================

    # 1. Compare Revenue
    if "compare" in query and "revenue" in query or query.strip() == "compare":
        data = df.groupby("Company")["Revenue"].mean().sort_values(ascending=False)
        response = "Average Revenue Comparison:\n\n"
        for i, (c, v) in enumerate(data.items(), 1):
            response += f"{i}. {c}: ${v:,.0f} M\n"
        return response


    # 2. Compare Net Income
    if "compare" in query and ("profit" in query or "net income" in query):
        data = df.groupby("Company")["NetIncome"].mean().sort_values(ascending=False)
        response = " Average Net Income Comparison:\n\n"
        for i, (c, v) in enumerate(data.items(), 1):
            response += f"{i}. {c}: ${v:,.0f} M\n"
        return response


    # 3. Compare Profit Margin
    if "compare" in query and "margin" in query:
        data = df.groupby("Company")["Profit_Margin"].mean().sort_values(ascending=False)
        response = " Profit Margin Comparison:\n\n"
        for i, (c, v) in enumerate(data.items(), 1):
            response += f"{i}. {c}: {v:.2f}%\n"
        return response


    # 4. Compare Debt
    if "compare" in query and "debt" in query:
        data = df.groupby("Company")["Debt_Ratio"].mean().sort_values()
        response = "Debt Ratio Comparison (Lower is Better):\n\n"
        for i, (c, v) in enumerate(data.items(), 1):
            response += f"{i}. {c}: {v:.2f}%\n"
        return response


    # 5. Compare Revenue Growth
    if "compare" in query and "growth" in query:
        growth = df.groupby("Company")["Revenue_Growth"].mean().sort_values(ascending=False)
        response = " Revenue Growth Comparison:\n\n"
        for i, (c, v) in enumerate(growth.items(), 1):
            response += f"{i}. {c}: {v:.2f}%\n"
        return response


    # 6. Compare Risk
    if "compare" in query and "risk" in query:
        risk_df = df.groupby("Company").mean(numeric_only=True)
        risk_df["Risk_Score"] = risk_df["Debt_Ratio"] - risk_df["Profit_Margin"]
        risk_df = risk_df.sort_values("Risk_Score", ascending=False)

        response = " Risk Comparison (Higher = More Risk):\n\n"
        for i, row in enumerate(risk_df.iterrows(), 1):
            response += f"{i}. {row[0]}\n"
        return response


    # 7. Compare Financial Health
    if "financial health" in query and "compare" in query:
        health = df.groupby("Company").mean(numeric_only=True)
        health["Health_Score"] = (
            health["Profit_Margin"] + health["Revenue_Growth"] - health["Debt_Ratio"]
        )
        health = health.sort_values("Health_Score", ascending=False)

        response = " Financial Health Comparison:\n\n"
        for i, row in enumerate(health.iterrows(), 1):
            response += f"{i}. {row[0]}\n"
        return response


    # 8. Compare Two Companies
    if "vs" in query:
        parts = query.split("vs")
        if len(parts) == 2:
            c1 = parts[0].split()[-1].capitalize()
            c2 = parts[1].strip().capitalize()

            d1 = df[df["Company"] == c1].iloc[-1]
            d2 = df[df["Company"] == c2].iloc[-1]

            return (
                f" {c1} vs {c2}\n\n"
                f"Revenue: ${d1['Revenue']:,.0f} M vs ${d2['Revenue']:,.0f} M\n"
                f"Profit Margin: {d1['Profit_Margin']:.2f}% vs {d2['Profit_Margin']:.2f}%\n"
                f"Debt Ratio: {d1['Debt_Ratio']:.2f}% vs {d2['Debt_Ratio']:.2f}%"
            )


    # 9. Top 3 Companies
    if "top" in query:
        top = df.groupby("Company")["Revenue"].mean().sort_values(ascending=False).head(3)
        response = " Top 3 Companies by Revenue:\n\n"
        for i, (c, v) in enumerate(top.items(), 1):
            response += f"{i}. {c}: ${v:,.0f} M\n"
        return response


    # 10. Best Investment
    if "best" in query and "invest" in query:
        score = df.groupby("Company").mean(numeric_only=True)
        score["Score"] = (
            score["Profit_Margin"] + score["Revenue_Growth"] - score["Debt_Ratio"]
        )
        best = score.sort_values("Score", ascending=False).index[0]
        return f" {best} appears to be the best investment option (Not financial advice)."



    if "most profitable" in query:
        best = df.groupby("Company")["NetIncome"].max().idxmax()
        return f"{best} is the most profitable company."

    if "lowest debt" in query:
        best = df.groupby("Company")["Debt_Ratio"].mean().idxmin()
        return f"{best} has the lowest debt ratio."

    if "invest" in query and company:
        row = df[df["Company"] == company].iloc[-1]
        if row["Profit_Margin"] > 15 and row["Debt_Ratio"] < 50:
            return f"{company} looks like a good investment (Not financial advice)."
        return f"{company} may be risky to invest in (Not financial advice)."

    return "Ask about revenue, profit, growth, debt, comparison, or investment."

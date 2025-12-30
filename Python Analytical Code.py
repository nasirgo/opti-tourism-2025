import pandas as pd
import numpy as np

# --- CONFIGURATION ---
FILE_NAME = r"C:\Users\nasse\OneDrive - unime.it\Desktop\final Day 1 validation\Gemini work\Phase 3, 4\Master_Simulation.xlsx"
# Based on your upload, the sheet name is "Daily_Engine"
SHEET_NAME = "Daily_Engine"
OUTPUT_FILE = "OptiFlow_Daily_Intelligence.xlsx"

print(f"🚀 Initializing Data Enrichment for {FILE_NAME}...")

# 1. LOAD THE DAILY LOG
try:
    df = pd.read_excel(FILE_NAME, sheet_name=SHEET_NAME)
    # Filter out any empty rows at the end or side
    df = df.dropna(subset=['Date', 'Daily Revenue'])
    print("✅ Daily Revenue Log Loaded.")
except Exception as e:
    print(f"❌ Error: Could not find '{SHEET_NAME}'. Check the tab name!")
    exit()

# 2. INJECT COST LOGIC (From P&L_Monthly)
print("🧠 Injecting Operational Cost Logic...")

# Variable costs per room sold (excluding commission)
# 7 (Laundry) + 12 (House) + 5 (Amen) + 12 (F&B) + 13.68 (Energy) + 1.6 (Water)
VAR_COST_PER_ROOM = 51.28
COMMISSION_PCT = 0.20
DAILY_FIXED_COST = 665.17 # (€20,221.16 / 30.4 days)

# Calculate Daily Columns
df['Var_Costs_Ops'] = df['Rooms_Sold'] * VAR_COST_PER_ROOM
df['Commissions'] = df['Daily Revenue'] * COMMISSION_PCT
df['Total_Var_Costs'] = df['Var_Costs_Ops'] + df['Commissions']
df['Fixed_Costs'] = DAILY_FIXED_COST
df['Total_Costs'] = df['Total_Var_Costs'] + df['Fixed_Costs']
df['Daily_Profit'] = df['Daily Revenue'] - df['Total_Costs']

# 3. THE 7 ANALYTICAL INSIGHTS

# Q1: Monthly Performance
df['Date'] = pd.to_datetime(df['Date'])
monthly = df.groupby(df['Date'].dt.strftime('%m'))[['Daily Revenue', 'Daily_Profit', 'Rooms_Sold']].sum()

# Q2: Weekend vs Weekday (The Strategy Check)
# 0=Mon, 4=Fri, 5=Sat, 6=Sun. We check Fri-Sun as 'Weekend'
df['Day_Type'] = np.where(df['Date'].dt.dayofweek >= 4, 'Weekend (Fri-Sun)', 'Weekday (Mon-Thu)')
weekend_strat = df.groupby('Day_Type')[['Daily Revenue', 'Daily_Profit']].mean()

# Q4: Top 10 "Golden Days" (Max Profit)
golden_days = df.sort_values('Daily_Profit', ascending=False).head(10)[['Date', 'Daily Revenue', 'Daily_Profit']]

# Q5: Top 10 "Bleed Days" (Max Loss)
bleed_days = df.sort_values('Daily_Profit', ascending=True).head(10)[['Date', 'Daily Revenue', 'Daily_Profit']]

# 4. EXPORT THE "INTELLIGENCE" FILE
with pd.ExcelWriter(OUTPUT_FILE) as writer:
    df.to_excel(writer, sheet_name='Master_Enriched_Data', index=False)
    monthly.to_excel(writer, sheet_name='Monthly_Summary')
    weekend_strat.to_excel(writer, sheet_name='Weekend_Analysis')
    golden_days.to_excel(writer, sheet_name='Top_Performers')
    bleed_days.to_excel(writer, sheet_name='Winter_Bleed_Days')

print(f"🎉 SUCCESS! Master Intelligence File Created: {OUTPUT_FILE}")
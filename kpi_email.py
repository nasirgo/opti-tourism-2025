import datetime

# 1. THE DATA (Simulating your Google Sheet)
today = datetime.date.today()
stats = {"occupancy": 0.42, "revpar": 90.50, "competitor_revpar": 85.00}

# 2. THE LOGIC (Calculating Variance)
variance = round(((stats["revpar"] - stats["competitor_revpar"]) / stats["competitor_revpar"]) * 100, 1)
status = "✅ WINNING" if variance > 0 else "❌ LOSING"

# 3. THE EMAIL (Simulating the Send)
print(f"""
Subject: 📊 CEO Morning Brief - {today}
To: gm@palazzoviceconte.com
------------------------------------------------
Good Morning.

Yesterday's Performance:
- Occupancy: {int(stats['occupancy']*100)}%
- RevPAR:    €{stats['revpar']} (Market: €{stats['competitor_revpar']})

Market Position: {status} ({variance}% vs Competitors)

[Sent via Python Automation Layer]
------------------------------------------------
""")
import json
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests
import matplotlib.pyplot as plt

# Load JSON Data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

bot_activities = load_json('/Users/siddharthganjoo/Desktop/empriical/bot_activities.json')
human_activities = load_json('/Users/siddharthganjoo/Desktop/empriical/human_activities.json')

# Convert to DataFrame
bot_df = pd.DataFrame(bot_activities)
human_df = pd.DataFrame(human_activities)

# Convert 'date' to datetime format for both DataFrames
bot_df['date'] = pd.to_datetime(bot_df['date'])
human_df['date'] = pd.to_datetime(human_df['date'])

# Aggregate data into time series (e.g., daily count)
bot_daily = bot_df['date'].dt.date.value_counts().sort_index()
human_daily = human_df['date'].dt.date.value_counts().sort_index()

# Find the overall start and end dates
start_date = min(bot_daily.index.min(), human_daily.index.min())
end_date = max(bot_daily.index.max(), human_daily.index.max())

# Create an index that covers the entire date range
idx = pd.date_range(start=start_date, end=end_date)

# Reindex and fill missing dates with zeros
bot_daily = bot_daily.reindex(idx, fill_value=0)
human_daily = human_daily.reindex(idx, fill_value=0)

# Combine into a single DataFrame for Granger Causality Test
time_series_df = pd.concat([bot_daily, human_daily], axis=1)
time_series_df.columns = ['bot_activities', 'human_activities']

# Apply Granger Causality Test
granger_test_results = grangercausalitytests(time_series_df, maxlag=5, verbose=True)

# Visualization
time_series_df.plot(figsize=(12, 6))
plt.title('Daily Bot and Human Activities')
plt.xlabel('Date')
plt.ylabel('Number of Activities')
plt.show()

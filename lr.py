import json
import pandas as pd
import numpy as np

# Load JSON Data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Load bot and human activities
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
bot_daily_aligned = bot_daily.reindex(idx, fill_value=0)
human_daily_aligned = human_daily.reindex(idx, fill_value=0)

# Prepare DataFrame for regression
df = pd.DataFrame({'bot_activities': bot_daily_aligned, 'human_activities': human_daily_aligned})

# Define predictor (X) and response (y)
X = df[['bot_activities']].values
y = df['human_activities'].values

# Add a column of ones to X for the intercept
X = np.column_stack((np.ones(X.shape[0]), X))

# Perform linear regression using numpy
beta = np.linalg.lstsq(X, y, rcond=None)[0]

# Output the coefficients
print('Intercept:', beta[0])
print('Slope:', beta[1])

import json
import pandas as pd
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

# Sort dataframes by date
bot_df = bot_df.sort_values(by='date')
human_df = human_df.sort_values(by='date')

# Find the closest human activity time after each bot activity
response_times = []
for bot_time in bot_df['date']:
    # Filter human activities that are after the current bot activity
    filtered_human_df = human_df[human_df['date'] > bot_time]
    
    # Check if there are any human activities after the bot activity
    if not filtered_human_df.empty:
        # Get the time of the first human activity after the bot activity
        first_human_time = filtered_human_df.iloc[0]['date']
        
        # Calculate the response time in seconds
        response_time = (first_human_time - bot_time).total_seconds()
        response_times.append(response_time)

# Visualization
plt.hist(response_times, bins=30)
plt.title('Response Times of Human Activities Following Bot Activities')
plt.xlabel('Response Time (seconds)')
plt.ylabel('Frequency')
plt.show()

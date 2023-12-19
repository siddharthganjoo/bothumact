import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Seaborn settings for aesthetics
sns.set(style="whitegrid")

BOT_ACTIVITIES_FILE = '/Users/siddharthganjoo/Desktop/empriical/bot_activities.json'
HUMAN_ACTIVITIES_FILE = '/Users/siddharthganjoo/Desktop/empriical/human_activities.json'

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def basic_info(data):
    contributors = set([activity['contributor'] for activity in data])
    dates = [datetime.strptime(activity['date'][:19], "%Y-%m-%dT%H:%M:%S") for activity in data]
    print("Total Activities: {}".format(len(data)))
    print("Unique Contributors: {}".format(len(contributors)))
    print("Date Range: {} to {}".format(min(dates), max(dates)))

def activity_distribution(bot_data, human_data):
    bot_activities = pd.DataFrame(bot_data)
    human_activities = pd.DataFrame(human_data)

    bot_activity_counts = bot_activities['activity'].value_counts()
    human_activity_counts = human_activities['activity'].value_counts()

    combined_df = pd.DataFrame({'Bots': bot_activity_counts, 'Humans': human_activity_counts})
    combined_df.plot(kind='bar', figsize=(15, 7))
    plt.title('Bot vs Human Activity Distribution')
    plt.ylabel('Number of Activities')
    plt.xlabel('Activity Type')
    plt.xticks(rotation=45)
    plt.show()

def temporal_analysis(bot_data, human_data):
    bot_activities = pd.DataFrame(bot_data)
    human_activities = pd.DataFrame(human_data)

    bot_activities['date'] = pd.to_datetime(bot_activities['date'].str[:19])
    human_activities['date'] = pd.to_datetime(human_activities['date'].str[:19])

    bot_activities.set_index('date', inplace=True)
    human_activities.set_index('date', inplace=True)

    bot_resampled = bot_activities.resample('M').size()
    human_resampled = human_activities.resample('M').size()

    plt.figure(figsize=(15, 7))
    plt.plot(bot_resampled.index, bot_resampled.values, label='Bots')
    plt.plot(human_resampled.index, human_resampled.values, label='Humans')
    plt.title('Temporal Activity Comparison')
    plt.xlabel('Date')
    plt.ylabel('Number of Activities')
    plt.legend()
    plt.show()

def main():
    bot_activities = load_json(BOT_ACTIVITIES_FILE)
    human_activities = load_json(HUMAN_ACTIVITIES_FILE)

    print("Basic Info for Bot Activities:")
    basic_info(bot_activities)
    print("\nBasic Info for Human Activities:")
    basic_info(human_activities)

    print("\nComparing Activity Distribution:")
    activity_distribution(bot_activities, human_activities)

    print("\nComparing Temporal Activity:")
    temporal_analysis(bot_activities, human_activities)

if __name__ == "__main__":
    main()

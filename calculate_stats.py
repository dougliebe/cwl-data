import pandas as pd
import os

current_directory = os.getcwd()
print(f"Current working directory: {current_directory}")

def calculate_stats(df):
    # Calculate Traded Kills
    df['traded_kills'] = df['kills'] - df['non_traded_kills']

    # Calculate Traded Deaths and Non-Traded Deaths
    df['opponents_traded_kill_pct'] = df.apply(lambda row: df[df['team'] != row['team']]['traded_kills'].sum() / df[df['team'] != row['team']]['kills'].sum(), axis=1)
    df['traded_deaths'] = df['opponents_traded_kill_pct'] * df['deaths']
    df['non_traded_deaths'] = df['deaths'] - df['traded_deaths']

    # Calculate Assists on NTKs and TKs
    df['teammate_ntk_pct'] = df.apply(lambda row: (df[(df['team'] == row['team']) & (df['player'] != row['player'])]['non_traded_kills'].sum()) / (df[(df['team'] == row['team']) & (df['player'] != row['player'])]['kills'].sum()), axis=1)
    df['assists_on_ntks'] = df['assists'] * df['teammate_ntk_pct']
    df['assists_on_tks'] = df['assists'] - df['assists_on_ntks']

    # Calculate Kills with and without Assists
    df['kills_assisted_pct'] = df.apply(lambda row: df[(df['team'] == row['team']) & (df['player'] != row['player'])]['assists'].sum() / 3 / row['kills'], axis=1)
    # df['kills_with_assists'] = df['kills'] * df['kills_assisted_pct']
    # df['kills_without_assists'] = df['kills'] - df['kills_with_assists']
    df['tk_with_assists'] = df['traded_kills'] * df['kills_assisted_pct']
    df['tk_without_assists'] = df['traded_kills'] - df['tk_with_assists']
    df['ntk_with_assists'] = df['non_traded_kills'] * df['kills_assisted_pct']
    df['ntk_without_assists'] = df['non_traded_kills'] - df['ntk_with_assists']

    # Calculate Effective Kills
    df['effective_kills'] = df['ntk_with_assists'] * 1 * 0.50 + \
        df['ntk_without_assists'] * 1 + \
        df['tk_with_assists'] * 0.23 * 0.50 + \
        df['tk_without_assists'] * 0.23 + \
        df['assists_on_ntks'] * 1 * 0.50 + \
        df['assists_on_tks'] * 0.23 * 0.50
        
    # Calculate Effective Deaths
    df['effective_deaths'] = 0.23 * df['traded_deaths'] + 1 * df['non_traded_deaths']

    return df

# Example usage
if __name__ == "__main__":
    # Load the data
    data = {
        'team': ['LV', 'LV', 'LV', 'LV', 'LAT', 'LAT', 'LAT', 'LAT'],
        'player': ['attach', 'gio', 'purj', 'nero', 'ghosty', 'joed', 'kremp', 'nastie'],
        'kills': [22, 30, 22, 41, 26, 29, 28, 24],
        'deaths': [25, 26, 28, 28, 27, 29, 28, 31],
        'non_traded_kills': [17, 21, 12, 27, 19, 20, 18, 17],
        'assists': [11, 11, 13, 8, 11, 11, 12, 18]
    }
    df = pd.DataFrame(data)

    # Calculate the new stats
    df = calculate_stats(df)
    
    # ## save to csv
    # df.to_csv('D:/ANALYTICS/COD/cwl-data/test.csv', index=False)

    # Display the results
    print(df)
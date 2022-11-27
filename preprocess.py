import pandas
import numpy as np

def calculate_values(wins, losses, method="linear"):
    if method == "linear":
        # Wins linearly increase value of matchup
        h2h = wins - losses
    elif method == "scaled":
        # Normalizes value of matchup between [-1, 1]
        h2h = (wins - losses) / (wins + losses)

        # Soften matchups with < 3 sets
        # Effectively converts 1-0 to 2-1, and 2-0 to 5-1
        scale = (wins + losses) / 3.0
        scale[scale > 1.0] = 1.0
        scale.fillna(1.0)
        h2h = h2h * scale
    return h2h

def add_attendance_bonus(df, h2h, wins, bonus_scale=0.1, max_sets=100, verbose=0):
    """ Attendance bonus
    For any matchup without data, set the value to (s_A - s_B) / (s_A + s_B)
    where s_A and s_B are the number of sets attended by player A and B respectively.
    E.g. For s_A = 10 and s_B = 0, the bonus is 1, for s_A = s_B = 10, the bonus is 0.
    Return: modified dataframe with attendance bonuses
    """
    attendance = {}
    player_names = parse_player_names()
    # Replace NaN with 0 because we'll be summing them
    df_safe = df.fillna(0.0)
    for i, name in enumerate(player_names):
        # Get results for player i
        player_col = df_safe.loc[:, name].values
        # Cap each set-count to max_sets?
        capped_sets = np.minimum(player_col, max_sets)
        # Sum the number of wins and losses (sets played) for player name
        attendance[i] = np.sum(capped_sets)

    # Fill in the attendance bonus for each missing set
    for i, name in enumerate(player_names):
        bonus_sum = 0
        for j, _ in enumerate(player_names):
            if np.isnan(h2h.iloc[i,j]):
                bonus = (attendance[i] - attendance[j]) / (attendance[i] + attendance[j] + 1)
                bonus *= bonus_scale
                h2h.iloc[i,j] = bonus
                bonus_sum += bonus
        if verbose > 0:
            print(f"{name} attendance bonus: {bonus_sum}")

    # If 2 players have 0 sets played, the resulting value is NaN.
    h2h = h2h.fillna(0.0)
    return h2h


def parse_csv(attendance_scalar=0.1, verbose=0):
    df = pandas.read_csv("2022.csv")

    # Copy column names to loss columns (see csv for info)
    names = {col: df.columns[i-1] for i, col in enumerate(df.columns) if i >= 3 and i <= 124 and i % 2 == 0}
    #names = {col: df.columns[i-1] for i, col in enumerate(df.columns) if i >= 2 and i <= 124 and i % 2 == 1}
    df.rename(columns=names, inplace=True)

    # Extract wins and losses
    # 2022
    wins = df.iloc[:-1, 3:-12:2]
    losses = df.iloc[:-1, 4:-12:2]
    # 2019
    #wins = df.iloc[:, 3:-16:2]
    #losses = df.iloc[:, 4:-15:2]
    # 2020
    #wins = df.iloc[:, 2:-16:2]
    #losses = df.iloc[:, 3:-15:2]

    h2h = calculate_values(wins, losses, method="scaled")

    # Set self matchups to 0
    for i in range(len(h2h)):
        h2h.iloc[i,i] = 0.0

    # Add in attendance bonus for 0-0 (NaN) matchups
    h2h = add_attendance_bonus(df, h2h, wins, bonus_scale=attendance_scalar, verbose=verbose)
    h2h.to_csv("2022-score.csv")
    return h2h.values


def parse_player_names():
    df = pandas.read_csv("2022.csv")

    # Fix column names
    names = {col: df.columns[i-1] for i, col in enumerate(df.columns) if i >= 3 and i <= 124 and i % 2 == 0}
    #names = {col: df.columns[i-1] for i, col in enumerate(df.columns) if i >= 2 and i <= 124 and i % 2 == 1}
    df.rename(columns=names, inplace=True)
    # 2022
    wins = df.iloc[:-1, 3:-12:2]
    # 2019
    #wins = df.iloc[:, 3:-16:2]
    # 2020
    #wins = df.iloc[:, 2:-16:2]
    return list(wins.columns)

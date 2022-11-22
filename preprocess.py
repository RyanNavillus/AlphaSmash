import pandas

def parse_csv():
    df = pandas.read_csv("data.csv")

    # Fix column names
    names = {col: df.columns[i-1] for i, col in enumerate(df.columns) if i >= 3 and i <= 124 and i % 2 == 0}
    df.rename(columns=names, inplace=True)

    # Extract wins and losses
    wins = df.iloc[:-11, 3:-32:2]
    wins = wins.fillna(0.0)
    losses = df.iloc[:-11, 4:-32:2]
    losses = losses.fillna(0.0)

    # Scale values with < 3 sets
    h2h = (wins - losses) / (wins + losses)
    h2h = h2h.fillna(0.0)
    scale = (wins + losses) / 3.0
    scale[scale > 1.0] = 1.0
    h2h = h2h * scale
    return h2h.values

def parse_player_names():
    df = pandas.read_csv("data.csv")

    # Fix column names
    names = {col: df.columns[i-1] for i, col in enumerate(df.columns) if i >= 3 and i <= 124 and i % 2 == 0}
    df.rename(columns=names, inplace=True)
    wins = df.iloc[:-11, 3:-32:2]
    return list(wins.columns)

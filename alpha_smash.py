import numpy as np
from open_spiel.python.egt import alpharank
from open_spiel.python.egt import utils
from open_spiel.python.egt import heuristic_payoff_table
from preprocess import parse_csv, parse_player_names


# Matrix game of 2022 smash results
# Columns/Row Headers are Mang0, Zain, IBDW, Amsa, Hungrybox, Jmook, Leffen, Axe, Plup, Wizzrobe
# i.e Row 4 Column 2 is Amsa vs. Zain
# Each value represents the winrate that row player has against column player, normalized to [-1, 1]
# Formula (s_r - s_c) / (s_r + s_c) where s_r and s_c are the set wins for the row and column players respectively
# i.e. 0.00 represents a 50% winrate, 1.00 represents a 100% winrate, -1.00 represents a -100% winrate
# Note: This does not account for absolute number of wins. i.e. 1-2, 2-4, and 4-8 all have the value -0.33
matrix_list = [
    [0.00, -0.20, 0.67, -0.50, 0.00, -0.33, 1.00, 1.00, 1.00, 0.00],
    [0.20, 0.00, 0.00, -0.33, 0.60, 0.00, 0.00, 0.20, 0.00, -1.00],
    [-0.67, 0.00, 0.00, 0.33, 0.50, 0.60, -1.00, 1.00, 1.00, -1.00],
    [0.50, 0.33, -0.33, 0.00, 0.20, 0.50, 0.33, 1.00, -1.00, 0.00],
    [0.00, -0.60, -0.50, -0.20, 0.00, 0.80, -0.33, 1.00, -0.14, -1.00],
    [0.33, 0.00, -0.60, -0.50, -0.80, 0.00, 0.33, -0.33, 0.00, 1.00],
    [-1.00, 0.00, 1.00, -0.33, 0.33, -0.33, 0.00, 1.00, 1.00, 1.00],
    [-0.50, -0.20, -1.00, -1.00, -1.00, 0.33, -1.00, 0.00, 0.00, -0.33],
    [-1.00, 0.00, -1.00, 1.00, 0.14, 0.00, -1.00, 0.00, 0.00, 1.00],
    [0.00, -1.00, -1.00, 0.00, -1.00, -1.00, -1.00, 0.00, -1.00, 0.00],
]

matrix_list = np.asarray(matrix_list)
matrix_list = parse_csv()


payoff_tables = [heuristic_payoff_table.from_matrix_game(matrix_list)]

res = alpharank.sweep_pi_vs_alpha(payoff_tables, visualize=False, return_alpha=True, strat_labels=parse_player_names(), legend_sort_clusters=True)

payoffs_are_hpt_format = utils.check_payoffs_are_hpt(payoff_tables)

# Check if the game is symmetric (i.e., players have identical strategy sets
# and payoff tables) and return only a single-player’s payoff table if so.
# This ensures Alpha-Rank automatically computes rankings based on the
# single-population dynamics.
_, payoff_tables = utils.is_symmetric_matrix_game(payoff_tables)

# Compute Alpha-Rank
(rhos, rho_m, pi, num_profiles, num_strats_per_population) = alpharank.compute(
    payoff_tables, alpha=90)

# Report results
# alpharank.print_results(payoff_tables, payoffs_are_hpt_format, pi=pi)

rankings = reversed(sorted(zip(pi, parse_player_names())))
for i, (score, player) in enumerate(rankings):
    adjust = "\t" if len(player) < 11 else ""
    print(f"{i+1}. {player} \t{adjust}({score:.4f})")

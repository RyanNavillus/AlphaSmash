import argparse
import numpy as np
from open_spiel.python.egt import alpharank
from open_spiel.python.egt import utils
from open_spiel.python.egt import heuristic_payoff_table
from open_spiel.python.egt import alpharank_visualizer
from preprocess import parse_csv, parse_player_names


parser = argparse.ArgumentParser()
parser.add_argument("--alphasweep", action="store_true", help="Perform and visualize sweep over alpha parameter")
parser.add_argument("--attendance_sweep", action="store_true", help="Perform and visualize sweep over alpha parameter")
parser.add_argument("--n_network", type=int, default=0, help="Visualize network of top players")
parser.add_argument("--verbose", action="store_true", help="Print out extra information")


if __name__ == "__main__":
    args = parser.parse_args()

    # Matrix game of 2022 smash results
    matrix_list = parse_csv(verbose=args.verbose)

    # Convert to Heuristic Payoff Table
    payoff_tables = [heuristic_payoff_table.from_matrix_game(matrix_list)]

    # Perform sweep of alpha hyperparameter and visualize results
    player_names = parse_player_names()
    if args.alphasweep:
        res = alpharank.sweep_pi_vs_alpha(payoff_tables, visualize=True, return_alpha=True, strat_labels=player_names, legend_sort_clusters=True)

    # Check if the game is symmetric (i.e., players have identical strategy sets
    # and payoff tables) and return only a single-player’s payoff table if so.
    # This ensures Alpha-Rank automatically computes rankings based on the
    # single-population dynamics.
    payoffs_are_hpt_format = utils.check_payoffs_are_hpt(payoff_tables)
    _, payoff_tables = utils.is_symmetric_matrix_game(payoff_tables)

    # Compute Alpha-Rank
    (rhos, rho_m, pi, num_profiles, num_strats_per_population) = alpharank.compute(payoff_tables, alpha=10)

    # Print Alpha-Rank results
    utils.print_rankings_table(
        payoff_tables,
        pi,
        player_names,
        num_top_strats_to_print=100)

    if args.n_network > 0:
        # Visualize transition network
        m_network_plotter = alpharank_visualizer.NetworkPlot(payoff_tables, rhos,
                                                             rho_m, pi, player_names,
                                                             num_top_profiles=args.n_network)
        m_network_plotter.compute_and_draw_network()

    if args.attendance_sweep:
        pi_list = np.empty((num_profiles, 0))
        bonus_list = []
        for i in reversed(np.linspace(0, 1, 11)):
            matrix_list = parse_csv(attendance_scalar=i, verbose=args.verbose)
            payoff_tables = [heuristic_payoff_table.from_matrix_game(matrix_list)]
            payoffs_are_hpt_format = utils.check_payoffs_are_hpt(payoff_tables)
            _, payoff_tables = utils.is_symmetric_matrix_game(payoff_tables)
            _, _, pi, num_profiles, num_strats_per_population = alpharank.compute(payoff_tables, alpha=10)
            pi_list = np.append(pi_list, np.reshape(pi, (-1, 1)), axis=1)
            bonus_list.append(i)

        alpharank_visualizer.plot_pi_vs_alpha(pi_list.T,
                                              bonus_list,
                                              1,
                                              num_strats_per_population,
                                              player_names,
                                              10,
                                              plot_semilogx=True,
                                              xlabel=r"Attendance bonus")

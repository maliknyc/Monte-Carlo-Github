import random
import matplotlib.pyplot as plt
import math

def run_single_simulation(starting_wealth, return_win_percent, p_up, return_loss_percent, p_down, upper_bet_limit, lower_threshold):
    """
    Runs a single simulation of the Gambler's Ruin problem with dynamic wagering based on the Kelly Criterion.

    Parameters:
    - starting_wealth (float): Initial amount of wealth.
    - return_win_percent (float): Percentage profit on a win (e.g., 260 for 260%).
    - p_up (float): Probability of winning each bet.
    - return_loss_percent (float): Percentage loss on a loss (e.g., -100 for losing the wager).
    - p_down (float): Probability of losing each bet.
    - upper_bet_limit (int): Maximum number of bets to simulate.
    - lower_threshold (float): Wealth level to stop betting (0 for bankruptcy).

    Returns:
    - wealth_history (list): List of wealth after each bet.
    - peak_wealth (float): Highest wealth achieved during the simulation.
    - min_wealth (float): Lowest wealth achieved during the simulation.
    - went_bankrupt (bool): Whether the simulation ended in ruin.
    - bet_count (int): Total number of bets placed in the simulation.
    """
    current_wealth = starting_wealth
    bet_count = 0
    wealth_history = [current_wealth]
    peak_wealth = starting_wealth
    min_wealth = starting_wealth
    went_bankrupt = False

    while bet_count < upper_bet_limit and current_wealth > lower_threshold:
        bet_count += 1

        # calculate kelly fraction
        b = return_win_percent / 100  # net odds
        f_star = (b * p_up - p_down) / b  # KELLY CRITERION

        # ensure f_star is within [0,1]
        f_star = max(0, min(f_star, 1))

        # determine wager amount
        wager_amount = f_star * current_wealth

        # calculate up_amount and down_amount based on wager_amount
        up_amount = wager_amount * b  # Profit on win
        down_amount = abs(wager_amount * (return_loss_percent / 100))  # Loss on loss (typically wager_amount)

        # simulate bet outcome
        outcome = random.random()

        if outcome < p_up:
            current_wealth += up_amount
            result = "Win"
        elif outcome < p_up + p_down:
            current_wealth -= down_amount
            result = "Lose"
        else:
            result = "No Change"

        wealth_history.append(current_wealth)

        if current_wealth > peak_wealth:
            peak_wealth = current_wealth
        if current_wealth < min_wealth:
            min_wealth = current_wealth

        # uncomment below to see detailed bet outcomes...
        # print(f"Bet {bet_count}: {result} | Wager: {wager_amount:.2f} | Current Wealth: {current_wealth:.2f}")

        # check if wealth has hit the lower threshold
        if current_wealth <= lower_threshold:
            print(f"\n--- Stopping Simulation ---")
            print(f"Wealth has reached the lower threshold of {lower_threshold}.")
            went_bankrupt = True
            break
    else:
        pass
        # uncomment below if you want to see when upper bet limit is reached...
        # print("\n--- Stopping Simulation ---")
        # print(f"Reached the upper limit of {upper_bet_limit} bets.")

    # Final Results
    print(f"Total Bets Placed: {bet_count}")
    return wealth_history, peak_wealth, min_wealth, went_bankrupt, bet_count

def run_multiple_simulations(num_simulations, starting_wealth, return_win_percent, p_up, return_loss_percent, p_down, upper_bet_limit, lower_threshold):
    """
    Runs multiple simulations of the Gambler's Ruin problem with dynamic wagering based on the Kelly Criterion.

    Parameters:
    - num_simulations (int): Number of simulations to run.
    - All other parameters as defined in run_single_simulation.

    Returns:
    - final_wealths (list): Final wealth from each simulation.
    - peak_wealths (list): Peak wealth from each simulation.
    - min_wealths (list): Minimum wealth from each simulation.
    - all_wealth_histories (list): Wealth histories from all simulations.
    - ruin_count (int): Number of simulations that ended in ruin.
    - smallest_min_wealth (float): Smallest minimum wealth achieved across all simulations.
    - highest_peak_wealth (float): Highest peak wealth achieved across all simulations.
    """
    ruin_count = 0
    final_wealths = []
    peak_wealths = []
    min_wealths = []
    all_wealth_histories = []
    smallest_min_wealth = float('inf')
    highest_peak_wealth = float('-inf')
    max_bets_before_ruin = 0
    simulations_with_max_bets_before_ruin = []

    for sim in range(1, num_simulations + 1):
        # uncomment below to see individual simulation headers...
        # print(f"\n=== Simulation {sim} ===")
        wealth_history, peak_wealth, min_wealth, went_bankrupt, bet_count = run_single_simulation(
            starting_wealth, return_win_percent, p_up, return_loss_percent, p_down, upper_bet_limit, lower_threshold
        )
        all_wealth_histories.append(wealth_history)
        final_wealths.append(wealth_history[-1])
        peak_wealths.append(peak_wealth)
        min_wealths.append(min_wealth)

        if min_wealth < smallest_min_wealth:
            smallest_min_wealth = min_wealth
        if peak_wealth > highest_peak_wealth:
            highest_peak_wealth = peak_wealth

        if went_bankrupt:
            ruin_count += 1

            # track the simulation(s) with the most bets before ruin
            if bet_count > max_bets_before_ruin:
                max_bets_before_ruin = bet_count
                simulations_with_max_bets_before_ruin = [sim]
            elif bet_count == max_bets_before_ruin:
                simulations_with_max_bets_before_ruin.append(sim)

    # calculate ruin probability and other statistics
    ruin_probability = (ruin_count / num_simulations) * 100
    average_final_wealth = sum(final_wealths) / num_simulations
    average_peak_wealth = sum(peak_wealths) / num_simulations
    average_min_wealth = sum(min_wealths) / num_simulations

    # FINAL SUMMARY
    print("\n=== All Simulations Summary ===")
    print(f"Total Simulations Run: {num_simulations}")
    print(f"Ruin Occurred in {ruin_count} Simulations ({ruin_probability:.2f}%)")
    print(f"Average Final Wealth: {average_final_wealth:.2f}")
    print(f"Average Peak Wealth Achieved: {average_peak_wealth:.2f}")
    print(f"Average Minimum Wealth Achieved: {average_min_wealth:.2f}")
    print(f"Smallest Minimum Wealth Achieved: {smallest_min_wealth}")
    print(f"Highest Peak Wealth Achieved: {highest_peak_wealth}")

    # add the new summary for simulations that hit ruin and survived the most bets
    if ruin_count > 0:
        print(f"Simulation(s) that hit ruin and survived the most bets ({max_bets_before_ruin} bets): {simulations_with_max_bets_before_ruin}")
    else:
        print("No simulations ended in ruin.")

    print()

    return final_wealths, peak_wealths, min_wealths, all_wealth_histories, ruin_count, smallest_min_wealth, highest_peak_wealth

def plot_sample_histories(all_wealth_histories, num_samples=10):
    """
    Plots the wealth progression for a sample of simulations.

    Parameters:
    - all_wealth_histories (list): List of wealth histories from all simulations.
    - num_samples (int): Number of simulations to plot.
    """
    plt.figure(figsize=(12, 6))
    for i, history in enumerate(all_wealth_histories[:num_samples]):
        plt.plot(history, label=f"Simulation {i+1}")
    plt.xlabel("# of Bets")
    plt.ylabel("Wealth")
    plt.title(f"Wealth Progression w/ Kelly (First {num_samples} Simulations)")
    #plt.legend()
    plt.grid(True)
    plt.show()

def plot_final_wealth_histogram(final_wealths):
    """
    Plots a histogram of the final wealths from all simulations.

    Parameters:
    - final_wealths (list): Final wealth from each simulation.
    """
    plt.figure(figsize=(12, 6))
    plt.hist(final_wealths, bins=50, edgecolor='black', alpha=0.7)
    plt.xlabel("Final Wealth")
    plt.ylabel("Frequency")
    plt.title("Final Wealth After Simulations (Kelly)")
    plt.grid(True)
    plt.show()

def simulate_gamblers_ruin_advanced():
    """
    Runs the advanced Gambler's Ruin simulation with predefined parameters.
    """
    print("=== Advanced Gambler's Ruin Simulation ===\n")
    
    # PARAMETERS! (NOTE: MUST BE A POSITIVE EV BET)
    starting_wealth = 1000      # Starting wealth
    return_win_percent = 110     # Percentage profit on a win (e.g., 260% for 2.6x profit)
    return_loss_percent = -100   # Percentage loss on a loss (-100% to lose the wager)
    p_up = 0.5                    # Probability of winning each bet
    p_down = 1 - p_up                  # Probability of losing each bet (1 - p_up)
    upper_bet_limit = 1000     # Maximum number of bets
    lower_threshold = 5           # Bankruptcy threshold
    num_simulations = 440        # Number of simulations to run
    
    
    
    # calculate Expected Value (EV) and other statistics
    b = return_win_percent / 100  # Net odds
    bet_EV = round((p_up * b - p_down) * 100, 3)  # EV per $100 wagered
    bet_ER = round(bet_EV / 100, 3)  # EV per $1 wagered
    # variance calculation for binary outcomes
    bet_Var = round((p_up * (b**2)) + (p_down * (1**2)) - (bet_ER**2), 5)
    bet_Std = round(math.sqrt(bet_Var), 5)
    
    print(f"Starting Advanced Simulation with the following parameters:")
    print(f"Starting Wealth: {starting_wealth}")
    print(f"Return on Win: {return_win_percent}% (Profit Multiplier: {b})")
    print(f"Return on Loss: {return_loss_percent}% (Loss Multiplier: 1)")
    print(f"Probability of Winning: {p_up}")
    print(f"Probability of Losing: {p_down}")
    print(f"Upper Limit of Bets: {upper_bet_limit}")
    print(f"Lower Threshold: {lower_threshold}")
    print(f"Number of Simulations: {num_simulations}\n")
    
    final_wealths, peak_wealths, min_wealths, all_wealth_histories, ruin_count, smallest_min_wealth, highest_peak_wealth = run_multiple_simulations(
        num_simulations, starting_wealth, return_win_percent, p_up, return_loss_percent, p_down, upper_bet_limit, lower_threshold
    )
    
    # plot a sample of wealth histories
    plot_sample_histories(all_wealth_histories, num_samples=num_simulations)
    
    # plot histogram of final wealths
    plot_final_wealth_histogram(final_wealths)
    
    print("=== Additional Insights ===")
    print(f"Expected Value of Bet (EV): {bet_EV}")
    print(f"Expected Return of Bet (ER): {bet_ER}")
    print(f"Expected Variance of Bet (Var): {bet_Var}")
    print(f"Expected Standard Deviation of Bet (Std): {bet_Std}")

if __name__ == "__main__":
    simulate_gamblers_ruin_advanced()

'''
NEXT OBJECTIVE:
    Employ strategies derived from different CRRA functions from gamma = 1 (Kelly Criterion) to gamma = 0
'''


import random
import matplotlib.pyplot as plt
import math

def run_single_simulation(starting_wealth, up_amount, p_up, down_amount, p_down, upper_bet_limit, lower_threshold):
    """
    Runs simulation of repeated fixed bets.

    Parameters:
    - starting_wealth (float): Initial amount of wealth
    - up_amount (float): Amount won per successful bet
    - p_up (float): Probability of winning each bet
    - down_amount (float): Amount lost per unsuccessful bet
    - p_down (float): Probability of losing each bet
    - upper_bet_limit (int): Maximum # of bets to simulate
    - lower_threshold (float): Wealth level to stop betting (typically 0 or 1)

    Returns:
    - wealth_history (list): List of wealth after each bet
    - peak_wealth (float): Highest wealth achieved during simulation
    - min_wealth (float): Lowest wealth achieved during simulation
    - went_bankrupt (bool): Whether simulation ended in ruin
    - bet_count (int): Total number of bets placed in simulation
    """
    current_wealth = starting_wealth
    bet_count = 0
    wealth_history = [current_wealth]
    peak_wealth = starting_wealth
    min_wealth = starting_wealth
    went_bankrupt = False

    while bet_count < upper_bet_limit and current_wealth > lower_threshold:
        bet_count += 1
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

        # Print the outcome of the current bet
        #print(f"Bet {bet_count}: {result} | Current Wealth: {current_wealth}")

        # Check if wealth has hit the lower threshold
        if current_wealth <= lower_threshold:
     #       print("\n--- Stopping Simulation ---")
     #       print(f"Wealth has reached the lower threshold of {lower_threshold}.")
            went_bankrupt = True
            break
    else:
        pass
        #print("\n--- Stopping Simulation ---")
        #print(f"Reached the upper limit of {upper_bet_limit} bets.")

    # Final Results
    #print("\n=== Simulation Summary ===")
  #  print(f"Total Bets Placed: {bet_count}")
    #print(f"Final Wealth: {current_wealth}")
    #print(f"Peak Wealth Achieved: {peak_wealth}")
    #print(f"Minimum Wealth Achieved: {min_wealth}\n")

    return wealth_history, peak_wealth, min_wealth, went_bankrupt, bet_count

def run_multiple_simulations(num_simulations, starting_wealth, up_amount, p_up, down_amount, p_down, upper_bet_limit, lower_threshold):
    """
    Runs multiple simulations of repeated fixed bets

    Parameters:
    - num_simulations (int): Number of simulations to run
    - All other parameters as defined in run_single_simulation

    Returns:
    - final_wealths (list): Final wealth from each simulation
    - peak_wealths (list): Peak wealth from each simulation
    - min_wealths (list): Minimum wealth from each simulation
    - all_wealth_histories (list): Wealth histories from all simulations
    - ruin_count (int): Number of simulations that ended in ruin
    - smallest_min_wealth (float): Smallest minimum wealth achieved across all simulations
    - highest_peak_wealth (float): Highest peak wealth achieved across all simulations
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
        #print(f"\n=== Simulation {sim} ===")
        wealth_history, peak_wealth, min_wealth, went_bankrupt, bet_count = run_single_simulation(
            starting_wealth, up_amount, p_up, down_amount, p_down, upper_bet_limit, lower_threshold
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
    plt.title(f"Wealth Progression (First {num_samples} Simulations)")
    #plt.legend()
    plt.grid(True)
    plt.show()

def plot_final_wealth_histogram(final_wealths):
    """
    Plots histogram of the final wealths from all simulations

    Parameters:
    - final_wealths (list): Final wealth from each simulation
    """
    plt.figure(figsize=(12, 6))
    plt.hist(final_wealths, bins=50, edgecolor='black', alpha=0.7)
    plt.xlabel("Final Wealth")
    plt.ylabel("Frequency")
    plt.title("Final Wealth After Simulations")
    plt.grid(True)
    plt.show()

def simulate_gamblers_ruin_advanced():
    """
    Runs the advanced Gambler's Ruin simulation with predefined parameters
    """
    print("=== Advanced Gambler's Ruin Simulation ===\n")
    


    # PARAMETERS!
    starting_wealth = 1000      # starting wealth
    wager_amount = 20            # amount wagered each bet
    return_win_percent = 110     # (decimal odds - 1) * 100
  # return_loss_percent = -100   # not used
    p_up = 0.5                    # probability of winning each bet
    p_down = 1 - p_up             # probability of losing each bet
    upper_bet_limit = 1000    # max number of bets
    lower_threshold = 500           # bankruptcy threshold
    num_simulations = 1000        # number of simulations to run
    

    # calculate up_amount and down_amount based on wager and percentage returns
    up_amount = wager_amount * (return_win_percent / 100)    # e.g., 25 * 2.6 = 65
    down_amount = wager_amount # always just the wager amount
    
    # calculate Expected Value (EV) and other statistics
    bet_EV = round((p_up * up_amount) - (p_down * down_amount), 3)
    bet_ER = bet_EV / down_amount
    bet_Var = round(((p_up * ((return_win_percent/100)**2) + (p_down))) - (bet_ER**2), 5)
    bet_Std = round(math.sqrt(bet_Var), 5)
    
    print(f"Starting Advanced Simulation with the following parameters:")
    print(f"Starting Wealth: {starting_wealth}")
    print(f"Wager Amount per Bet: {wager_amount}")
    print(f"Return on Win: {return_win_percent}% (Profit Amount: {up_amount})")
    print(f"Probability of Winning: {p_up}")
    print(f"Probability of Losing: {p_down}")
    print(f"Upper Limit of Bets: {upper_bet_limit}")
    print(f"Lower Threshold: {lower_threshold}")
    print(f"Number of Simulations: {num_simulations}\n")
    
    final_wealths, peak_wealths, min_wealths, all_wealth_histories, ruin_count, smallest_min_wealth, highest_peak_wealth = run_multiple_simulations(
        num_simulations, starting_wealth, up_amount, p_up, down_amount, p_down, upper_bet_limit, lower_threshold
    )
    
    plot_sample_histories(all_wealth_histories, num_samples=100)
    
    # plot histogram of final wealths
    plot_final_wealth_histogram(final_wealths)
    
    print("=== Additional Insights ===")
    #print(f"Maximum Wealth Achieved Across All Simulations: {highest_peak_wealth}")
    #print(f"Minimum Wealth Achieved Across All Simulations: {smallest_min_wealth}\n")
    print(f"Expected Value of Bet: {bet_EV}")
    print(f"Expected Return of Bet: {bet_ER}")
    print(f"Expected Variance of Bet: {bet_Var}")
    print(f"Expected Standard Deviation of Bet: {bet_Std}")

if __name__ == "__main__":
    simulate_gamblers_ruin_advanced()
    
'''
NEXT OBJECTIVE:
    Employ strategies derived from different CRRA functions from gamma = 1 (Kelly Criterion) to gamma = 0
'''

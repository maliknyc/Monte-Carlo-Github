import random
import matplotlib.pyplot as plt

def run_single_simulation(starting_wealth, up_amount, p_up, down_amount, p_down, upper_bet_limit, lower_threshold):
    """
    Runs a single simulation of the Gambler's Ruin problem.

    Parameters:
    - starting_wealth (float): Initial amount of wealth.
    - up_amount (float): Amount won per successful bet.
    - p_up (float): Probability of winning each bet.
    - down_amount (float): Amount lost per unsuccessful bet.
    - p_down (float): Probability of losing each bet.
    - upper_bet_limit (int): Maximum number of bets to simulate.
    - lower_threshold (float): Wealth level to stop betting (0 for bankruptcy or 1).

    Returns:
    - wealth_history (list): List of wealth after each bet.
    - peak_wealth (float): Highest wealth achieved during the simulation.
    - min_wealth (float): Lowest wealth achieved during the simulation.
    - went_bankrupt (bool): Whether the simulation ended in ruin.
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

        # Update peak and minimum wealth
        if current_wealth > peak_wealth:
            peak_wealth = current_wealth
        if current_wealth < min_wealth:
            min_wealth = current_wealth

        # Print the outcome of the current bet
        #print(f"Bet {bet_count}: {result} | Current Wealth: {current_wealth}")

        # Check if wealth has hit the lower threshold
        if current_wealth <= lower_threshold:
            print("\n--- Stopping Simulation ---")
            print(f"Wealth has reached the lower threshold of {lower_threshold}.")
            went_bankrupt = True
            break
    else:
        pass
        #print("\n--- Stopping Simulation ---")
        #print(f"Reached the upper limit of {upper_bet_limit} bets.")

    # Final Results
    #print("\n=== Simulation Summary ===")
    #print(f"Total Bets Placed: {bet_count}")
    #print(f"Final Wealth: {current_wealth}")
    #print(f"Peak Wealth Achieved: {peak_wealth}")
    #print(f"Minimum Wealth Achieved: {min_wealth}\n")

    return wealth_history, peak_wealth, min_wealth, went_bankrupt

def run_multiple_simulations(num_simulations, starting_wealth, up_amount, p_up, down_amount, p_down, upper_bet_limit, lower_threshold):
    """
    Runs multiple simulations of the Gambler's Ruin problem.

    Parameters:
    - num_simulations (int): Number of simulations to run.
    - All other parameters as defined in run_single_simulation.

    Returns:
    - final_wealths (list): Final wealth from each simulation.
    - peak_wealths (list): Peak wealth from each simulation.
    - min_wealths (list): Minimum wealth from each simulation.
    - all_wealth_histories (list): Wealth histories from all simulations.
    - ruin_count (int): Number of simulations that ended in ruin.
    """
    ruin_count = 0
    final_wealths = []
    peak_wealths = []
    min_wealths = []
    all_wealth_histories = []
    smallest_min_wealth = float('inf')
    highest_peak_wealth = float('-inf')

    for sim in range(1, num_simulations + 1):
        #print(f"\n=== Simulation {sim} ===")
        wealth_history, peak_wealth, min_wealth, went_bankrupt = run_single_simulation(
            starting_wealth, up_amount, p_up, down_amount, p_down, upper_bet_limit, lower_threshold
        )
        all_wealth_histories.append(wealth_history)
        final_wealths.append(wealth_history[-1])
        peak_wealths.append(peak_wealth)
        min_wealths.append(min_wealth)

        # Update smallest minimum wealth and highest peak wealth
        if min_wealth < smallest_min_wealth:
            smallest_min_wealth = min_wealth
        if peak_wealth > highest_peak_wealth:
            highest_peak_wealth = peak_wealth

        if went_bankrupt:
            ruin_count += 1

    # Calculate ruin probability and other statistics
    ruin_probability = (ruin_count / num_simulations) * 100
    average_final_wealth = sum(final_wealths) / num_simulations
    average_peak_wealth = sum(peak_wealths) / num_simulations
    average_min_wealth = sum(min_wealths) / num_simulations

    # Final Summary
    print("\n=== All Simulations Summary ===")
    print(f"Total Simulations Run: {num_simulations}")
    print(f"Ruin Occurred in {ruin_count} Simulations ({ruin_probability:.2f}%)")
    print(f"Average Final Wealth: {average_final_wealth:.2f}")
    print(f"Average Peak Wealth Achieved: {average_peak_wealth:.2f}")
    print(f"Average Minimum Wealth Achieved: {average_min_wealth:.2f}")
    print(f"Smallest Minimum Wealth Achieved: {smallest_min_wealth}")
    print(f"Highest Peak Wealth Achieved: {highest_peak_wealth}\n")

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
    plt.xlabel("Number of Bets")
    plt.ylabel("Wealth")
    plt.title(f"Sample Wealth Progression Over Bets (First {num_samples} Simulations)")
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
    plt.hist(final_wealths, bins=30, edgecolor='black', alpha=0.7)
    plt.xlabel("Final Wealth")
    plt.ylabel("Frequency")
    plt.title("Histogram of Final Wealth After Simulations")
    plt.grid(True)
    plt.show()

def simulate_gamblers_ruin_advanced():
    """
    Runs the advanced Gambler's Ruin simulation with predefined parameters.
    """
    print("=== Advanced Gambler's Ruin Simulation ===\n")
    
    # Define Parameters Here
    starting_wealth = 100          # Starting wealth (e.g., 10 units)
    up_amount = 11                 # Potential upside per bet (e.g., +1 unit)
    p_up = 0.5                    # Probability of winning each bet (e.g., 0.6 for 60%)
    down_amount = 10               # Potential downside per bet (e.g., -1 unit)
    p_down = 0.5                  # Probability of losing each bet (e.g., 0.4 for 40%)
    upper_bet_limit = 1000          # Upper limit of bets to prevent infinite loops
    lower_threshold = 0           # Lower threshold to stop betting (0 for bankruptcy)
    num_simulations = 100        # Number of simulations to run
    
    bet_EV = (p_up * up_amount) - (p_down * down_amount)
    
    print(f"Starting Advanced Simulation with the following parameters:")
    print(f"Starting Wealth: {starting_wealth}")
    print(f"Potential Upside per Bet: {up_amount}")
    print(f"Probability of Winning: {p_up}")
    print(f"Potential Downside per Bet: {down_amount}")
    print(f"Probability of Losing: {p_down}")
    print(f"Upper Limit of Bets: {upper_bet_limit}")
    print(f"Lower Threshold: {lower_threshold}")
    print(f"Number of Simulations: {num_simulations}\n")

    
    # Run Multiple Simulations
    final_wealths, peak_wealths, min_wealths, all_wealth_histories, ruin_count, smallest_min_wealth, highest_peak_wealth = run_multiple_simulations(
        num_simulations, starting_wealth, up_amount, p_up, down_amount, p_down, upper_bet_limit, lower_threshold
    )
    
    # Plot sample wealth histories
    plot_sample_histories(all_wealth_histories, num_samples=num_simulations)
    
    # Plot histogram of final wealths
    plot_final_wealth_histogram(final_wealths)
    
    # Additional Insights
    print("=== Additional Insights ===")
    print(f"Maximum Wealth Achieved Across All Simulations: {highest_peak_wealth}")
    print(f"Minimum Wealth Achieved Across All Simulations: {smallest_min_wealth}\n")
    print(f"Expected Value of Bet: {bet_EV}")

if __name__ == "__main__":
    simulate_gamblers_ruin_advanced()

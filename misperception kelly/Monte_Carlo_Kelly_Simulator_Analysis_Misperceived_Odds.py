import random
import matplotlib.pyplot as plt
import math
import pandas as pd
import numpy as np

def run_single_simulation(starting_wealth, p_up_actual, p_down_actual, upper_bet_limit, lower_threshold, f_scaled, b):

    current_wealth = starting_wealth
    bet_count = 0
    wealth_history = [current_wealth]
    peak_wealth = starting_wealth
    min_wealth = starting_wealth
    went_bankrupt = False

    while bet_count < upper_bet_limit and current_wealth > lower_threshold:
        bet_count += 1

        # calculate wager_amount as a fraction of current wealth
        wager_amount = current_wealth * f_scaled
       # print(wager_amount)

        # calculate up_amount and down_amount based on wager_amount and odds
        up_amount = wager_amount * b    # amount gained if the bet is won
        down_amount = wager_amount      # amount lost if the bet is lost

        outcome = random.random()

        if outcome < p_up_actual:
            current_wealth += up_amount
            result = "Win"
        elif outcome < p_up_actual + p_down_actual:
            current_wealth -= down_amount
            result = "Lose"
        else:
            result = "No Change"

        wealth_history.append(current_wealth)

        if current_wealth > peak_wealth:
            peak_wealth = current_wealth
        if current_wealth < min_wealth:
            min_wealth = current_wealth

        # uncomment the following line to print each bet's outcome
        # print(f"Bet {bet_count}: {result} | Current Wealth: {current_wealth:.2f}")

        # check if wealth has hit the lower threshold
        if current_wealth <= lower_threshold:
            # uncomment the following lines to print ruin information
            # print("\n--- Stopping Simulation ---")
            # print(f"Wealth has reached the lower threshold of {lower_threshold}.")
            went_bankrupt = True
            break

    # Final results (uncomment to print individual simulation summaries)
    # print("\n=== Simulation Summary ===")
    # print(f"Total Bets Placed: {bet_count}")
    # print(f"Final Wealth: {current_wealth:.2f}")
    # print(f"Peak Wealth Achieved: {peak_wealth:.2f}")
    # print(f"Minimum Wealth Achieved: {min_wealth:.2f}\n")

    return wealth_history, peak_wealth, min_wealth, went_bankrupt, bet_count

def run_multiple_simulations(num_simulations, starting_wealth, p_up_actual, p_down_actual, upper_bet_limit, lower_threshold, f_scaled, b):

    ruin_count = 0
    final_wealths = []
    peak_wealths = []
    min_wealths = []
    all_wealth_histories = []
    smallest_min_wealth = float('inf')
    highest_peak_wealth = float('-inf')
    max_bets_before_ruin = 0
    simulations_with_max_bets_before_ruin = []

    # lists for individual sim stats
    mean_log_wealth_list = []    # mean of log-wealth
    std_log_wealth_list = []     # std of log-wealth
    slope_log_wealth_list = []   # slope of log-wealth
    time_to_ruin_list = []       # time to ruin (if applicable)

    for sim in range(1, num_simulations + 1):
        # uncomment the following line to track simulation progress
        # print(f"\n=== Simulation {sim} ===")
        wealth_history, peak_wealth, min_wealth, went_bankrupt, bet_count = run_single_simulation(
            starting_wealth, p_up_actual, p_down_actual, upper_bet_limit, lower_threshold, f_scaled, b
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

        # log-transformed wealth history
        log_wealth = np.log(wealth_history)
        
        mean_log = np.mean(log_wealth)
        std_log = np.std(log_wealth)

        # find slope of line of best fit for log-wealth
        # polyfit to fit: log_wealth = slope * bet_number + intercept
        slope, intercept = np.polyfit(range(len(log_wealth)), log_wealth, 1)

        mean_log_wealth_list.append(mean_log)
        std_log_wealth_list.append(std_log)
        slope_log_wealth_list.append(slope)

        # record time to ruin if applicable, else NaN
        if went_bankrupt:
            time_to_ruin_list.append(bet_count)
        else:
            time_to_ruin_list.append(np.nan)

    # calculate ruin probability and other statistics
    ruin_probability = (ruin_count / num_simulations) * 100
    average_final_wealth = sum(final_wealths) / num_simulations
    average_peak_wealth = sum(peak_wealths) / num_simulations
    average_min_wealth = sum(min_wealths) / num_simulations
    highest_final_wealth = max(final_wealths)

    # dataframe w/ all individual sim stats
    data = {
        'Simulation': range(1, num_simulations + 1),
        'Mean_Log_Wealth': mean_log_wealth_list,
        'Std_Log_Wealth': std_log_wealth_list,
        'Slope_Log_Wealth': slope_log_wealth_list,
        'Time_to_Ruin': time_to_ruin_list,
        'Peak_Wealth': peak_wealths,
        'Min_Wealth': min_wealths,
        'Final_Wealth': final_wealths
    }

    simulation_df = pd.DataFrame(data)

    # final summary
    print("\n=== All Simulations Summary ===")
    print(f"Total Simulations Run: {num_simulations}")
    print(f"Ruin Occurred in {ruin_count} Simulations ({ruin_probability:.2f}%)")
    print(f"Average Final Wealth: {average_final_wealth:.2f}")
    print(f"Average Peak Wealth Achieved: {average_peak_wealth:.2f}")
    print(f"Highest Peak Wealth Achieved: {highest_peak_wealth}")
    print(f"Average Minimum Wealth Achieved: {average_min_wealth:.2f}")
    print(f"Smallest Minimum Wealth Achieved: {smallest_min_wealth}")
    print(f"Highest Final Wealth Achieved: {highest_final_wealth}")  # added line

    if ruin_count > 0:
        print(f"Simulation(s) that hit ruin and survived the most bets ({max_bets_before_ruin} bets): {simulations_with_max_bets_before_ruin}")
    else:
        print("No simulations ended in ruin.")

    # --- Added Code Starts Here ---
    if ruin_count > 0:
        valid_times = [t for t in time_to_ruin_list if not np.isnan(t)]
        average_time_to_ruin = sum(valid_times) / ruin_count
        print(f"Average Time to Ruin: {average_time_to_ruin:.2f} bets")
    else:
        print("No simulations ended in ruin. Average Time to Ruin is undefined.")
    
    # Compute average of mean log-wealth across all simulations
    average_mean_log_wealth = sum(mean_log_wealth_list) / num_simulations
    # Compute average of standard deviations of log-wealth across all simulations
    average_std_log_wealth = sum(std_log_wealth_list) / num_simulations
    # Compute average slope of log-wealth across all simulations
    average_beta = sum(slope_log_wealth_list) / num_simulations
    
    # Print the newly computed statistics
    print(f"Mean of Log-Wealth: {average_mean_log_wealth:.4f}")
    print(f"Standard Deviation of Log-Wealth: {average_std_log_wealth:.4f}")
    print(f"Average Slope of Log-Wealth: {average_beta:.10f}")
    # --- Added Code Ends Here ---

    print()

    return final_wealths, peak_wealths, min_wealths, all_wealth_histories, ruin_count, smallest_min_wealth, highest_peak_wealth, simulation_df  # modified return

def plot_sample_histories(all_wealth_histories, num_samples=10, g=1, scale=1, alph=1):

    plt.figure(figsize=(12, 6), dpi = 300)
    for i, history in enumerate(all_wealth_histories[:num_samples]):
        plt.plot(history, label=f"Simulation {i+1}")
    plt.xlabel("# of Bets")
    plt.ylabel("Wealth")
    plt.title(f"Wealth Progression after {num_samples} Simulations (γ = {g}; α = {alph}; K% = {scale})")
   # plt.legend()
    plt.grid(True)
    plt.show()

def plot_sample_histories_log(all_wealth_histories, num_samples=10, num_sims = 10, g=1, scale=1, alph=1):

    plt.figure(figsize=(12, 6), dpi = 300)
    for i, history in enumerate(all_wealth_histories[:num_samples]):
        plt.plot(history, label=f"Simulation {i+1}")
    plt.xlabel("# of Bets")
    plt.ylabel("Wealth")
    plt.title(f"Log-Wealth Progression after {num_sims} Simulations (γ = {g}; α = {alph}; K% = {scale})")
    plt.yscale('log')
    plt.grid(True, which="both", ls="--")
    plt.show()

def plot_final_wealth_histogram(final_wealths, num_simulations, g=1, scale=1, alph=1):

    plt.figure(figsize=(12, 6), dpi = 300)
    plt.hist(final_wealths, bins=75, edgecolor='black', alpha=0.7)
    plt.xlabel("Final Wealth")
    plt.ylabel("Frequency")
    plt.title(f"Final Wealth Distribution after {num_simulations} Simulations (γ = {g}; α = {alph}; K% = {scale})")
    plt.grid(True)
    plt.show()

def compute_optimal_fraction(p_perceived, b, g):

    if g == 0:
        # risk-neutral case: maximize expected value
        f_star = (p_perceived * b - (1 - p_perceived)) / b
    else:
        try:
            ratio = (p_perceived * b) / (1 - p_perceived)
            numerator = ratio**(1/g) - 1
            denominator = b + ratio**(1/g)
            f_star = numerator / denominator
        except ZeroDivisionError:
            print("Error: Division by zero encountered in computing f*.")
            f_star = 0
    return f_star

def simulate_gamblers_ruin_advanced():

    print("=== Monte Carlo Betting Simulation with Perceived vs. Actual Probabilities ===\n")

    # SIMULATION PARAMETERS!
    starting_wealth = 1000          # starting wealth

    # Actual Probability of Winning (used for determining outcomes)
    p_up_actual = 1/34       # actual probability of winning each bet
    p_down_actual = 1 - p_up_actual


    '''
    # Perceived Probability of Winning (used for sizing the bet)
    p_up_perceived = 0.51            # perceived probability of winning each bet
    p_down_perceived = 1 - p_up_perceived
    '''
    
    # Perceived Probability of Winning (Using Probability Weighting)
    alpha = 1 # 0.9884032 is the point at which one bets on negative ev roulette
  #  p_up_perceived = math.exp(- (math.log(2))**(1 - alpha) * (-math.log(p_up_actual))**alpha) # modified 50% one
    p_up_perceived = np.exp(-((-np.log(p_up_actual)) ** alpha))
    p_down_perceived = 1 - p_up_perceived



    upper_bet_limit = 10000           # max number of bets
    lower_threshold = 10           # bankruptcy threshold
    num_simulations = 1000           # number of simulations to run

    # BET PARAMETERS
    return_win_percent = 3500         # (decimal odds - 1) * 100, e.g., 2000 for b = 20
    b = return_win_percent / 100      # net odds (b to 1)

    # STRATEGY PARAMETERS
    g = 0.93                          # relative risk aversion coefficient (1 for Kelly)
    scale = 1                       # scaling factor (1 for full Kelly, 0.5 for half-Kelly)

    # calculate optimal fraction based on perceived probability
    f_star = compute_optimal_fraction(p_up_perceived, b, g)
    f_scaled = f_star * scale

    # ensure the fraction is between 0 and 1
    if f_scaled < 0:
        print("Warning: computed scaled fraction is negative. setting f_scaled to 0.")
        f_scaled = 0
    elif f_scaled > 1:
        print("Warning: computed scaled fraction exceeds 1. setting f_scaled to 1.")
        f_scaled = 1
        
    '''
    actual_ev = (p_up_actual * (100 * (b+1)))
    actual_edge = actual_ev/100
    
    perceived_ev = (p_up_perceived * (100 * (b+1)))
    perceived_edge = perceived_ev/100
    '''

    actual_ev = (p_up_actual * b) - (p_down_actual * 1)
    actual_edge = actual_ev * 100 
    
    perceived_ev = (p_up_perceived * b) - (p_down_perceived * 1)
    perceived_edge = perceived_ev * 100
    
    print(f"Actual EV (per $100 stake): {actual_ev:.3f}")
    print(f"Actual Edge: {actual_edge:.3f}%")
    print(f"Perceived EV (per $100 stake): {perceived_ev:.3f}")
    print(f"Perceived Edge: {perceived_edge:.3f}%\n")
    
    print(f"Parameters for Simulation:")
    print(f"Starting Wealth: ${starting_wealth}")
    print(f"Perceived Probability of Winning (p_up_perceived): {p_up_perceived:.4f}")
    print(f"Actual Probability of Winning (p_up_actual): {p_up_actual}")
    print(f"Net Odds (b): {b} to 1")
    print(f"Relative Risk Aversion (g): {g}")
    print(f"Scaling Factor (scale): {scale}")
    print(f"Optimal Fraction (f*): {f_star:.4f}")
    print(f"Scaled Fraction (f_scaled): {f_scaled:.4f}\n")
    
    print(f"Upper bet limit: {upper_bet_limit}")
    print(f"Ruin threshold: {lower_threshold}")

    # calculate EV and other statistics based on scaled fraction
    # since wager_amount is a fraction, EV per bet = f_scaled * (p_up_actual * b - p_down_actual)
    bet_EV = f_scaled * (p_up_actual * b - p_down_actual)
    bet_Var = f_scaled**2 * (p_up_actual * (b**2) + p_down_actual)
    bet_Std = math.sqrt(bet_Var)


#    print(f"Betting Statistics with Scaled Fraction:")
 #   print(f"Expected Value of Bet (EV): {bet_EV:.4f}")
  #  print(f"Expected Variance of Bet (Var): {bet_Var:.4f}")
   # print(f"Expected Standard Deviation of Bet (Std): {bet_Std:.4f}\n")

    # run multiple simulations and capture the new DataFrame
    final_wealths, peak_wealths, min_wealths, all_wealth_histories, ruin_count, smallest_min_wealth, highest_peak_wealth, simulation_df = run_multiple_simulations(
        num_simulations, starting_wealth, p_up_actual, p_down_actual, upper_bet_limit, lower_threshold, f_scaled, b
    )

    # plot sample wealth histories (original linear scale)
    plot_sample_histories(all_wealth_histories, num_samples=num_simulations, g=g, scale=(scale*100), alph=alpha)

    # plot sample wealth histories with log scale
    plot_sample_histories_log(all_wealth_histories, num_samples=100, num_sims=num_simulations, g=g, scale=(scale*100), alph=alpha)

    # plot histogram of final wealths
    plot_final_wealth_histogram(final_wealths, num_simulations=num_simulations, g=g, scale=(scale*100), alph=alpha)

    # optionally, you can save the DataFrame to a CSV file for further analysis
    simulation_df.to_csv('simulation_results.csv', index=False)

  #  print("=== Simulation DataFrame Head ===")
  # print(simulation_df.head())  # display the first few rows of the DataFrame

    # uncomment the following lines if you want additional insights printed
    # print("\n=== Additional Insights ===")
    # print(f"Expected Value of Bet: {bet_EV:.4f}")
    # print(f"Expected Variance of Bet: {bet_Var:.4f}")
    # print(f"Expected Standard Deviation of Bet: {bet_Std:.4f}")
    # print(final_wealths)

if __name__ == "__main__":
    simulate_gamblers_ruin_advanced()

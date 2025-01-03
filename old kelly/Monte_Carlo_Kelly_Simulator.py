import random
import matplotlib.pyplot as plt
import math

def run_single_simulation(starting_wealth, p_up, p_down, upper_bet_limit, lower_threshold, f_scaled, b):

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

        # calculate up_amount and down_amount based on wager_amount and odds
        up_amount = wager_amount * b    # amount gained if bet is won
        down_amount = wager_amount      # amount lost if bet is lost

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

        # uncomment following line to print each bet's outcome...
        # print(f"Bet {bet_count}: {result} | Current Wealth: {current_wealth:.2f}")

        # check if wealth has hit ruin
        if current_wealth <= lower_threshold:
            # uncomment the following lines to print ruin information...
            # print("\n--- Stopping Simulation ---")
            # print(f"Wealth has reached the lower threshold of {lower_threshold}.")
            went_bankrupt = True
            break

    # Final Results (Uncomment to print individual simulation summaries)
    # print("\n=== Simulation Summary ===")
   #print(f"Total Bets Placed: {bet_count}")
    # print(f"Final Wealth: {current_wealth:.2f}")
    # print(f"Peak Wealth Achieved: {peak_wealth:.2f}")
    # print(f"Minimum Wealth Achieved: {min_wealth:.2f}\n")

    return wealth_history, peak_wealth, min_wealth, went_bankrupt, bet_count

def run_multiple_simulations(num_simulations, starting_wealth, p_up, p_down, upper_bet_limit, lower_threshold, f_scaled, b):

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
        # uncomment the following line to track simulation progress...
        # print(f"\n=== Simulation {sim} ===")
        wealth_history, peak_wealth, min_wealth, went_bankrupt, bet_count = run_single_simulation(
            starting_wealth, p_up, p_down, upper_bet_limit, lower_threshold, f_scaled, b
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


    if ruin_count > 0:
        print(f"Simulation(s) that hit ruin and survived the most bets ({max_bets_before_ruin} bets): {simulations_with_max_bets_before_ruin}")
    else:
        print("No simulations ended in ruin.")

    print()

    return final_wealths, peak_wealths, min_wealths, all_wealth_histories, ruin_count, smallest_min_wealth, highest_peak_wealth

def plot_sample_histories(all_wealth_histories, num_samples=10, g=1, scale=1):

    plt.figure(figsize=(12, 6))
    for i, history in enumerate(all_wealth_histories[:num_samples]):
        plt.plot(history, label=f"Simulation {i+1}")
    plt.xlabel("# of Bets")
    plt.ylabel("Wealth")
    plt.title(f"Wealth Progression after {num_samples} Simulations (γ = {g}; K% = {scale})")
    #plt.legend()
    plt.grid(True)
    plt.show()

def plot_final_wealth_histogram(final_wealths, num_simulations, g=1, scale=1):

    plt.figure(figsize=(12, 6))
    plt.hist(final_wealths, bins=75, edgecolor='black', alpha=0.7)
    plt.xlabel("Final Wealth")
    plt.ylabel("Frequency")
    plt.title(f"Final Wealth Distribution after {num_simulations} Simulations (γ = {g}; K% = {scale})")
    plt.grid(True)
    plt.show()

def compute_optimal_fraction(p, b, g):

    if g == 0:
        # risk-neutral case: maximize expected value
        f_star = (p * b - (1 - p)) / b
    else:
        try:
            numerator = ( (p * b) / (1 - p) )**(1/g) - 1
            denominator = b + ( (p * b) / (1 - p) )**(1/g)
            f_star = numerator / denominator
        except ZeroDivisionError:
            print("Error: Division by zero encountered in computing f*.")
            f_star = 0
    return f_star

def simulate_gamblers_ruin_advanced():

    print("=== Monte Carlo Betting Simulation ===\n")

    # SIMULATION PARAMETERS!
    starting_wealth = 1000          # starting wealth
    p_up = 0.5                       # probability of winning each bet
    p_down = 1 - p_up                # probability of losing each bet
    upper_bet_limit = 100000           # max number of bets
    lower_threshold = 5              # bankruptcy threshold
    num_simulations = 500            # number of simulations to run

    # BET PARAMETERS
    return_win_percent = 110         # (decimal odds - 1) * 100
    b = return_win_percent / 100     # net odds (b to 1)

    # STRATEGY PARAMETERS
    g = 0.5                          # gamma > 0 (1 for Kelly)
    scale = 1                      # scaling factor (1 for full Kelly, 0.5 for half-Kelly)

    # calculate optimal fraction based on CRRA utility
    f_star = compute_optimal_fraction(p_up, b, g)
    f_scaled = f_star * scale

    # ensure the fraction is between 0 and 1
    if f_scaled < 0:
        print("Warning: Computed scaled fraction is negative. Setting f_scaled to 0.")
        f_scaled = 0
    elif f_scaled > 1:
        print("Warning: Computed scaled fraction exceeds 1. Setting f_scaled to 1.")
        f_scaled = 1

    print(f"Parameters for Simulation:")
    print(f"Starting Wealth: {starting_wealth}")
    print(f"Probability of Winning (p_up): {p_up}")
    print(f"Probability of Losing (p_down): {p_down}")
    print(f"Net Odds (b): {b} to 1")
    print(f"Relative Risk Aversion (g): {g}")
    print(f"Scaling Factor (scale): {scale}")
    print(f"Optimal Fraction (f*): {f_star:.4f}")
    print(f"Scaled Fraction (f_scaled): {f_scaled:.4f}\n")

    # calculate EV and other statistics based on scaled fraction
    # since wager_amount is a fraction, EV per bet = f_scaled * (p_up * b - p_down)
    bet_EV = f_scaled * (p_up * b - p_down)
    bet_Var = f_scaled**2 * (p_up * (b**2) + p_down)
    bet_Std = math.sqrt(bet_Var)

    print(f"Betting Statistics with Scaled Fraction:")
    print(f"Expected Value of Bet (EV): {bet_EV:.4f}")
    print(f"Expected Variance of Bet (Var): {bet_Var:.4f}")
    print(f"Expected Standard Deviation of Bet (Std): {bet_Std:.4f}\n")

    final_wealths, peak_wealths, min_wealths, all_wealth_histories, ruin_count, smallest_min_wealth, highest_peak_wealth = run_multiple_simulations(
        num_simulations, starting_wealth, p_up, p_down, upper_bet_limit, lower_threshold, f_scaled, b
    )

    # plot sample wealth histories
    plot_sample_histories(all_wealth_histories, num_samples=100, g=g, scale=(scale*100))

    # plot histogram of final wealths
    plot_final_wealth_histogram(final_wealths, num_simulations=100, g=g, scale=(scale*100))

#    print("=== Additional Insights ===")
 #   print(f"Expected Value of Bet: {bet_EV:.4f}")
  #  print(f"Expected Variance of Bet: {bet_Var:.4f}")
   # print(f"Expected Standard Deviation of Bet: {bet_Std:.4f}")
    #print(final_wealths)

if __name__ == "__main__":
    simulate_gamblers_ruin_advanced()

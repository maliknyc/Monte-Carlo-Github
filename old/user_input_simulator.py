import random

def simulate_gamblers_ruin():
    print("=== Gambler's Ruin Simulation ===\n")
    
    # Input Parameters
    while True:
        try:
            starting_wealth = float(input("Enter your starting wealth (e.g., 10): "))
            if starting_wealth <= 0:
                print("Starting wealth must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for starting wealth.")
    
    while True:
        try:
            up_amount = float(input("Enter the potential upside per bet (e.g., 1): "))
            if up_amount <= 0:
                print("Upside amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for potential upside.")
    
    while True:
        try:
            p_up = float(input("Enter the probability of winning (e.g., 0.55): "))
            if not (0 < p_up < 1):
                print("Probability of winning must be between 0 and 1.")
                continue
            break
        except ValueError:
            print("Please enter a valid probability between 0 and 1 for winning.")
    
    while True:
        try:
            down_amount = float(input("Enter the potential downside per bet (e.g., 1): "))
            if down_amount <= 0:
                print("Downside amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for potential downside.")
    
    while True:
        try:
            p_down = float(input("Enter the probability of losing (e.g., 0.45): "))
            if not (0 <= p_down < 1):
                print("Probability of losing must be between 0 and 1.")
                continue
            if p_up + p_down > 1:
                print("The sum of probabilities of winning and losing cannot exceed 1.")
                continue
            break
        except ValueError:
            print("Please enter a valid probability between 0 and 1 for losing.")
    
    while True:
        try:
            upper_bet_limit = int(input("Enter the upper limit of bets (e.g., 100): "))
            if upper_bet_limit <= 0:
                print("Upper limit of bets must be a positive integer.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for the upper limit of bets.")
    
    while True:
        try:
            lower_threshold = float(input("Enter the lower threshold to stop betting (0 or 1): "))
            if lower_threshold not in [0, 1]:
                print("Lower threshold must be either 0 or 1.")
                continue
            break
        except ValueError:
            print("Please enter a valid number for the lower threshold (0 or 1).")
    
    print("\n--- Starting Simulation ---\n")
    
    # Initialize variables
    current_wealth = starting_wealth
    bet_count = 0
    history = []  # To store the history of bets
    peak_wealth = starting_wealth
    min_wealth = starting_wealth
    
    while bet_count < upper_bet_limit and current_wealth > lower_threshold:
        bet_count += 1
        outcome = random.random()
        
        if outcome < p_up:
            current_wealth += up_amount
            history.append((bet_count, "Win", current_wealth))
            result = "Win"
        elif outcome < p_up + p_down:
            current_wealth -= down_amount
            history.append((bet_count, "Lose", current_wealth))
            result = "Lose"
        else:
            # No change in wealth
            history.append((bet_count, "No Change", current_wealth))
            result = "No Change"
        
        # Update peak and minimum wealth
        if current_wealth > peak_wealth:
            peak_wealth = current_wealth
        if current_wealth < min_wealth:
            min_wealth = current_wealth
        
        # Print the outcome of the current bet
        print(f"Bet {bet_count}: {result} | Current Wealth: {current_wealth}")
        
        # Check if wealth has hit the lower threshold
        if current_wealth <= lower_threshold:
            print("\n--- Stopping Simulation ---")
            print(f"Wealth has reached the lower threshold of {lower_threshold}.")
            break
    
    else:
        print("\n--- Stopping Simulation ---")
        print(f"Reached the upper limit of {upper_bet_limit} bets.")
    
    # Final Results
    print("\n=== Simulation Summary ===")
    print(f"Total Bets Placed: {bet_count}")
    print(f"Final Wealth: {current_wealth}")
    print(f"Peak Wealth Achieved: {peak_wealth}")
    print(f"Minimum Wealth Achieved: {min_wealth}")

if __name__ == "__main__":
    simulate_gamblers_ruin()

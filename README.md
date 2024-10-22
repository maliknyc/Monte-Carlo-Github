# Monte Carlo Betting Simulation with CRRA Utility

This simulation models betting strategies using the **Kelly Criterion** and extends it via **Constant Relative Risk Aversion (CRRA)** utility functions. You can explore alternative betting strategies by adjusting the risk aversion coefficient (`g`) and a scaling factor.

## Features
- Isoelastic (CRRA) utility function: adjustable betting strategy based on γ
- Scaling for half-Kelly or other custom betting strategies
- Monte Carlo simulations to test strategies over time
- Wealth progression and distribution plots

### Requirements
- **Python 3.8+**
- **matplotlib** (`pip install matplotlib`)

## Usage

Modify parameters in the `simulate_gamblers_ruin_advanced()` function:

```python
# Example configuration: Half-Kelly strategy for betting with a 5% edge

# SIMULATION PARAMETERS!
starting_wealth = 100 # starting wealth
p_up = 0.5
upper_bet_limit = 1000 # max number of bets. Increase to observe maximization of geometric growth under Kelly (or to observe long-term growth).
lower_threshold = 1 # bankruptcy threshold. (Kelly technically never hits ruin because it assumes money is infinitely divisible, so you might raise this to > 0.)
num_simulations = 100 # number of simulations

# BET PARAMETERS
return_win_percent = 110 # (decimal odds - 1)
b = return_win_percent / 100 # net odds (b to 1)

# STRATEGY PARAMETERS
g = 1.0      # Risk aversion (1 = Kelly)
scale = 0.5  # Scaling (0.5 = Half-Kelly)
```

## CRRA Utility Function

The Constant Relative Risk Aversion (CRRA) utility function used in this simulation is defined as:

$$
U(w) =
\begin{cases} 
\frac{w^{1 - γ} - 1}{1 - γ} & \text{for } γ \neq 1 \\
\ln(w) & \text{for } γ = 1
\end{cases}
$$

Where:
- \( w \) is wealth.
- \( γ \) is the relative risk aversion coefficient.

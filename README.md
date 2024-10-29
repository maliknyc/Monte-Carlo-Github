# Monte Carlo Betting Simulation with CRRA Utility

This simulation models betting strategies using the **Kelly Criterion** and extends it via **Constant Relative Risk Aversion (CRRA)** utility functions. Where the Kelly Criterion is derived from and prescribes logarithmic utility, my proposed generalized Kelly Criterion is derived from the general CRRA utility function (which logarithmic utility is in the family of) and allows for the exploration of alternative betting strategies by adjusting the risk aversion coefficient (`γ`) and a scaling factor.

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

## Kelly Criterion
$$
f^* = \frac{pb - (1 - p)}{b}
$$

Where:
- \( f* \) is the optimal fraction of capital to bet.
- \( p \) is the probability of winning the bet.
- \( b \) is the odds received on the bet (net payout for each unit wagered, decimal odds - 1).

## Generalized Kelly Criterion
$$
f^* = \frac{\left( \frac{pb}{1 - p} \right)^{1/γ} - 1}{b + \left( \frac{pb}{1 - p} \right)^{1/γ}}
$$

Where:
- \( γ \) is the risk aversion constant.
- Note: When γ = 1, the Generalized Kelly Criterion simplifies to the standard Kelly Criterion (the same way the isoelastic utility function is the logarithmic function when γ = 1).

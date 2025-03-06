import yfinance as yf
import numpy as np
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

# Step 1: Download historical stock data
end_date = date.today().strftime("%Y-%m-%d")
start_date = '2000-01-01'
ticker = "GOOG"
#Alphabet Int
data = yf.download(ticker, start= start_date, end= end_date)
prices = data['Close']
print (prices)

# Step 2: Calculate daily returns and statistics
returns = np.log(1 + prices.pct_change())
mu = returns.mean()
sigma = returns.std()

print (mu, sigma)

#Step 3: Monte Carlo Simulation - Parameter Settings
days = 252  # Number of trading days in a year
simulations = 5000  # Number of simulations
T = 30  # Time horizon
S0 = prices.iloc[-1] # Starting price = Latest price

# Generate random paths
dt = 1
drift = (mu - 0.5 * sigma**2) * dt
drift = drift.to_numpy()[0]

volatility = sigma * np.sqrt(dt)
volatility = volatility.to_numpy()[0]



price_paths = np.zeros((T,simulations))
price_paths[0] = np.full (simulations, S0)

#Step 4: Monte Carlo Simulation
for i in range(1, T):

    for simulation in range(simulations):
        noise = np.random.normal(0, 1)


        price_paths[i, simulation] = price_paths[i-1, simulation] * np.exp(drift + volatility * noise) #GBM formula
print(price_paths[1][:10])
plt.figure(figsize=(10, 6))
plt.plot(price_paths)
plt.title(f"Monte Carlo Simulation for {ticker} Stock Price")
plt.xlabel("Days")
plt.ylabel("Price")
plt.show()

final_prices = price_paths[-1]
mean_price = np.mean(final_prices)
confidence_interval = np.percentile(final_prices, [5, 95])  # 90% confidence interval

print(f"Mean Predicted Price: {mean_price:.2f}")
print(f"90% Confidence Interval: {confidence_interval}")

#Calculate rate of return based on simulation output
simulated_returns = (price_paths[-1] - price_paths[0]) / price_paths[0]
print (simulated_returns)
# Calculate VaR under 95% confidence level
confidence_level = 0.995
VaR_monte_carlo = -np.percentile(simulated_returns, 100 * (confidence_level))

print(f"Monte Carlo VaR (95% confidence): {VaR_monte_carlo:.4f}")

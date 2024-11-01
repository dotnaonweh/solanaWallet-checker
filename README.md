
# Wallet Winrate Checker

This tool retrieves information about Solana wallet addresses, including the following details:
- **SOL Balance**
- **PnL** (Profit/Loss) for the specified period (7-day or 30-day)
- **Winrate**
- **Realized Profit**
- **Last Active Timestamp**

It allows users to input a list of wallet addresses, select a winrate period, and outputs filtered results if the winrate exceeds 60%.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [Example Output](#example-output)

## Features
- **Select winrate period**: Option to choose between a 7-day or 30-day period.
- **Data Processing**: Retrieves and displays relevant wallet information.
- **Filtering**: Saves results only if the winrate is above 60%.

## Requirements
- Python 3.7+
- Required Python Packages:
  - `undetected_chromedriver`
  - `selenium`
  - `tabulate`
  - `termcolor`

## Setup
1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Chrome version**:
   Ensure your Chrome version matches the version specified in the script. Update the `TARGET_VERSION` in `bypass.py` if needed.

3. **Add wallet addresses**:
   Create a file `list.txt` in the same directory, with each wallet address on a new line.

## Usage
To run the script, use:
```bash
python bypass.py
```

Follow the on-screen prompts to choose the winrate period (`7d` or `30d`). Results will be displayed in the terminal and saved in `results.txt` if they meet the filtering criteria.

## Example Output
```
+------------------+-------------+----------+---------+------------------+------------------------+
| Wallet Address   | SOL Balance | PnL 7d   | Winrate | Realized Profit  | Last Active Timestamp  |
+------------------+-------------+----------+---------+------------------+------------------------+
| <address>        | 3.14 SOL    | 12.5%    | 65.0%   | 0.50 USD         | 2024-11-01 14:35:22    |
+------------------+-------------+----------+---------+------------------+------------------------+
```

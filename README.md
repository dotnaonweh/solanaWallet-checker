# Wallet Winrate Checker

This project retrieves and displays information about Solana wallet addresses, including SOL balance, PnL for the last 30 days, winrate, realized profit, and last active timestamp. The user can choose between a 7-day or 30-day period for the winrate.

## Requirements

- Python 3.7+
- `requests` library
- `tabulate` library

## Installation

1. Clone the repository:
```sh
git clone https://github.com/your-username/wallet-winrate-checker.git
cd wallet-winrate-checker
```
2. Install the required libraries:
```sh
pip install requests tabulate
```

## Usage

1. Create a `list.txt` file in the project directory and add the wallet addresses you want to check, one per line.
2. Run the script:
```sh
python script.py
```
3. When prompted, enter the desired period for the winrate (7d or 30d).
4. The script will fetch and display the information for each wallet address in a tabular format and save the results to results.txt in JSON format.

## Example
### Input
Create a list.txt file with the following content:
```python
666B6G6Ge5agUH76uTwpcqaw8FuLuTrQWAc4qKzBg2zC
```

### Running the Script
```sh
$ python script.py
Welcome to Solana Wallet Checker!
How many days do you want the winrate? 7d/30d
Example: 7d
> 
```

### Output
#### Console
```sql
+----------------------------------------------+---------------+-----------+-----------+-------------------+-------------------------+
| Wallet Address                               |   SOL Balance | PnL 30d   | Winrate   | Realized Profit   | Last Active Timestamp   |
+==============================================+===============+===========+===========+===================+=========================+
| 666B6G6Ge5agUH76uTwpcqaw8FuLuTrQWAc4qKzBg2zC |         666   | 66%       | 66%       | 666$              | 2024-08-06 19:53:18     |
+----------------------------------------------+---------------+-----------+-----------+-------------------+-------------------------+
```
`results.txt`
```json
[
    {
        "Wallet Address": "666B6G6Ge5agUH76uTwpcqaw8FuLuTrQWAc4qKzBg2zC",
        "SOL Balance": "666",
        "PnL 30d": "6%",
        "Winrate": "66%",
        "Realized Profit": "666",
        "Last Active Timestamp": "2024-08-06 19:53:18"
    }
]
```

## CREDIT
- GMGN for providing the API used in this project.
"# solana-wallet-checker" 
"# solana-wallet-checker" 
"# solana-wallet-checker" 
"# solanaWallet-checker" 
"# solanaWallet-checker" 

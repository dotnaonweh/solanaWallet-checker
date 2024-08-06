import requests
import json
from datetime import datetime
from tabulate import tabulate

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

# Ask the user for the desired period
print('Welcome to Solana Wallet Checker!')
print('How many days do you want the winrate? 7d/30d\nExample: 7d')
period = input("> ").strip()

# Validate input
if period not in ['7d', '30d']:
    print("Invalid input. Please enter '7d' or '30d'.")
    exit()

params = {
    'period': period,
}

try:
    with open('list.txt', 'r') as file:
        last = file.read()

    results = []
    for line in last.split('\n'):
        if line.strip():
            response = requests.get(
                f'https://gmgn.ai/defi/quotation/v1/smartmoney/sol/walletNew/{line}',
                params=params,
                headers=headers,
            )
            data = response.json()
            sol_balance = data['data']['sol_balance']
            pnl_30d = data['data']['pnl_30d']
            winrate = data['data']['winrate'] if data['data']['winrate'] is not None else 0
            realized_profit = data['data']['realized_profit'] if data['data']['realized_profit'] is not None else 0
            last_active_timestamp = data['data'].get('last_active_timestamp', 0)
            last_pnl_30d = pnl_30d * 100
            last_winrate = winrate * 100

            result = {
                'Wallet Address': line,
                'SOL Balance': f'{float(sol_balance):.2f}',
                'PnL 30d': f'{round(last_pnl_30d, 2)}%',
                'Winrate': f'{round(last_winrate, 2)}%',
                'Realized Profit': f'{(realized_profit):.2f}$',
                'Last Active Timestamp': datetime.fromtimestamp(last_active_timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            }
            results.append(result)

            print(tabulate([result], headers="keys", tablefmt="grid"))

            with open('results.txt', 'a') as file:
                file.write(json.dumps(result, indent=4) + '\n')

except Exception as e:
    print(f'An error occurred: {e}')

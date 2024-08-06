import requests
import json
from datetime import datetime
from tabulate import tabulate

API_URL = 'https://gmgn.ai/defi/quotation/v1/smartmoney/sol/walletNew/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

def get_period():
    print('Welcome to Solana Wallet Checker!')
    period = input('How many days do you want the winrate? 7d/30d\nExample: 7d\n> ').strip()
    if period not in ['7d', '30d']:
        print("Invalid input. Please enter '7d' or '30d'.")
        exit()
    return period

def fetch_wallet_data(wallet_address, period):
    try:
        response = requests.get(f'{API_URL}{wallet_address}', params={'period': period}, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f'Error fetching data for wallet {wallet_address}: {e}')
        return None

def process_data(data, wallet_address):
    if data:
        try:
            sol_balance = data['data']['sol_balance']
            pnl_30d = data['data']['pnl_30d']
            winrate = data['data']['winrate'] if data['data']['winrate'] is not None else 0
            realized_profit = data['data']['realized_profit'] if data['data']['realized_profit'] is not None else 0
            last_active_timestamp = data['data'].get('last_active_timestamp', 0)
            last_pnl_30d = pnl_30d * 100
            last_winrate = winrate * 100

            result = {
                'Wallet Address': wallet_address,
                'SOL Balance': f'{float(sol_balance):.2f}',
                'PnL 30d': f'{round(last_pnl_30d, 2)}%',
                'Winrate': f'{round(last_winrate, 2)}%',
                'Realized Profit': f'{realized_profit:.2f}$',
                'Last Active Timestamp': datetime.fromtimestamp(last_active_timestamp).strftime('%Y-%m-%d %H:%M:%S'),
            }
            return result
        except KeyError as e:
            print(f'ERROR : Make sure your list is correct.')
    return None

def main():
    period = get_period()

    try:
        with open('list.txt', 'r') as file:
            wallet_addresses = file.read().strip().split('\n')
        
        results = []
        for wallet_address in wallet_addresses:
            if wallet_address.strip():
                data = fetch_wallet_data(wallet_address, period)
                result = process_data(data, wallet_address)
                
                if result:
                    results.append(result)
                    print(tabulate([result], headers="keys", tablefmt="grid"))
                    
                    with open('results.txt', 'a') as file:
                        file.write(json.dumps(result, indent=4) + '\n')

    except FileNotFoundError:
        print("The file 'list.txt' was not found.")
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

if __name__ == "__main__":
    main()

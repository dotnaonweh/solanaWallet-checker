import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime
from tabulate import tabulate
from termcolor import colored
import time

# Configuration
API_URL = 'https://gmgn.ai/defi/quotation/v1/smartmoney/sol/walletNew/'

def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    
    # Explicitly set the Chrome version (update this to match your Chrome version)
    uc.TARGET_VERSION = 129

    driver = uc.Chrome(options=options, version_main=129)
    return driver

def get_period():
    print('Welcome to Solana Wallet Checker!')
    period = input('How many days do you want the winrate? 7d/30d\nExample: 7d\n> ').strip()
    if period not in ['7d', '30d']:
        print("Invalid input. Please enter '7d' or '30d'.")
        exit()
    return period

def fetch_wallet_data(driver, wallet_address, period):
    url = f'{API_URL}{wallet_address}?period={period}'
    try:
        driver.get(url)
        time.sleep(2)  # Wait for 5 seconds to allow the page to load
        
        # Wait for the pre tag to be present
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "pre"))
        )
        
        # Get the page source and find the pre tag
        page_source = driver.page_source
        start_index = page_source.find("<pre>") + 5
        end_index = page_source.find("</pre>")
        json_data = page_source[start_index:end_index]
        
        return json.loads(json_data)
    except Exception as e:
        print(f'Error fetching data for wallet {wallet_address}: {e}')
        return None

def process_data(data, wallet_address, period):
    if data:
        try:
            sol_balance = data['data']['sol_balance'] if data['data']['sol_balance'] is not None else 0
            pnl_key = 'pnl_30d' if period == '30d' else 'pnl_7d'
            pnl = data['data'][pnl_key] if data['data'][pnl_key] is not None else 0
            winrate = data['data']['winrate'] if data['data']['winrate'] is not None else 0
            realized_profit_key = 'realized_profit_30d' if period == '30d' else 'realized_profit_7d'
            realized_profit = data['data'][realized_profit_key] if data['data'][realized_profit_key] is not None else 0
            last_active_timestamp = data['data'].get('last_active_timestamp', 0)
            last_pnl = pnl * 100
            last_winrate = winrate * 100

            winrate_str = f'{round(last_winrate, 2)}%'
            if last_winrate > 60:
                winrate_str = colored(winrate_str, 'green')

            result = {
                'Wallet Address': wallet_address,
                'SOL Balance': f'{float(sol_balance):.2f}',
                f'PnL {period}': f'{round(last_pnl, 2)}%',
                'Winrate': winrate_str,
                f'Realized Profit {period}': f'{realized_profit:.2f}$',
                'Last Active Timestamp': datetime.fromtimestamp(last_active_timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                'Winrate Value': last_winrate,
            }
            return result
        except KeyError as e:
            print(f'ERROR: Make sure your list is correct.')
    return None

def main():
    period = get_period()
    driver = setup_driver()

    try:
        with open('list.txt', 'r') as file:
            wallet_addresses = file.read().strip().split('\n')
        
        results = []
        for wallet_address in wallet_addresses:
            if wallet_address.strip():
                data = fetch_wallet_data(driver, wallet_address, period)
                result = process_data(data, wallet_address, period)
                
                if result and result['Winrate Value'] > 60:  # Save only if winrate is above 60%
                    results.append(result)
                    print(tabulate([result], headers="keys", tablefmt="grid"))
                    
                    with open('results.txt', 'a') as file:
                        result_to_save = {k: v for k, v in result.items() if k != 'Winrate Value'}
                        file.write(json.dumps(result_to_save, indent=4) + '\n')

    except FileNotFoundError:
        print("The file 'list.txt' was not found.")
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

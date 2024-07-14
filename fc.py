import requests
import time
import json
from datetime import datetime, timedelta

def read_api_keys(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]

def send_post_request(api_key):
    url = 'https://svc.fincakebot.online/mine'
    headers = {
        'X-Api-Key': api_key
    }
    payload = {
        'count': 500
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.status_code

def countdown_timer(seconds):
    end_time = datetime.now() + timedelta(seconds=seconds)
    while datetime.now() < end_time:
        time_left = end_time - datetime.now()
        print(f'Time left: {time_left}', end='\r')
        time.sleep(1)

def main():
    api_keys = read_api_keys('data.txt')
    total_accounts = len(api_keys)
    print(f'Total accounts: {total_accounts}')

    for i, api_key in enumerate(api_keys, start=1):
        print(f'Processing account {i}/{total_accounts}')
        status_code = send_post_request(api_key)
        if status_code == 200:
            print(f'Account {i} processed successfully')
        else:
            print(f'Account {i} failed with status code: {status_code}')
        if i < total_accounts:
            print('Waiting for 5 seconds before switching to next account...')
            time.sleep(5)

    print('All accounts processed. Starting 1-hour countdown...')
    countdown_timer(3600)
    print('1 hour is up. Restarting process...')

if __name__ == '__main__':
    while True:
        main()

import os
import csv
import json
import time
import ssl
import requests
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from pydiglib.pydig import pydig
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

# TLS 1.2
#class TLSAdapter(HTTPAdapter):
 #   def __init__(self, ssl_version=None, **kwargs):
  #      self.ssl_version = ssl_version
   #     super().__init__(**kwargs)

    #def init_poolmanager(self, *args, **kwargs):
     #   kwargs['ssl_version'] = self.ssl_version
      #  super().init_poolmanager(*args, **kwargs)

# Function to check a single website via HTTPS
def check_https(url):
    session = requests.Session()
    #adapter = TLSAdapter(ssl_version=ssl.PROTOCOL_TLSv1_2)
    #session.mount('https://', adapter)
    try:
        response = session.get(url, timeout=15, verify=True)
        if 200 <= response.status_code <= 208:
            return f"Accessible (Status Code: {response.status_code})"
        elif 300 <= response.status_code <= 308:
            return f"Redirected (Status Code: {response.status_code})"
        elif 400 <= response.status_code <= 451:
            return f"Blocked - Client Error (Status Code: {response.status_code})"
        else:
            return f"Blocked (Status Code: {response.status_code})"
    except requests.RequestException as e:
        return f"Error: {e}"

# Function to query DNS information
def query_dns(domain):
    try:
        response = pydig(["queryBot.py", domain])
        return {
            'return_code': response.rcode,
            'ip': response.rdatalist,
            'size': response.msglen,
            'ttl': response.ttl,
            'response_time': response.response_time,
            'exception': False
        }
    except Exception as e:
        return {
            'return_code': None,
            'ip': None,
            'size': None,
            'ttl': None,
            'response_time': None,
            'exception': True,
            'error_message': str(e)
        }

# Batches
def process_batch(batch, output_file):
    results = []
    with ThreadPoolExecutor(max_workers=200) as executor:
        future_to_url = {executor.submit(check_https, "https://" + url): url for url in batch}
        for future in tqdm(future_to_url, desc="Processing batch"):
            url = future_to_url[future]
            try:
                https_status = future.result()
                dns_response = query_dns(url)
                results.append({
                    'website': url,
                    'https_status': https_status,
                    **dns_response  
                })
            except Exception as exc:
                results.append({'website': url, 'https_status': f"Error: {exc}", 'dns_response': None})

    # Append batch results to a single CSV file
    results_df = pd.DataFrame(results)
    if not os.path.exists(output_file):
        results_df.to_csv(output_file, index=False) 
    else:
        results_df.to_csv(output_file, mode='a', header=False, index=False)  


def split_file(txt_file, batch_size, start_from=None):
    with open(txt_file, 'r') as file:
        #websites = [line.strip() for line in file if line.strip()]
        websites = [line.strip().split(',')[1].strip('{').strip('"') for line in file if ',' in line] #line to change based on the .txt file in input
    if start_from:
        if start_from in websites:
            start_index = websites.index(start_from)
            websites = websites[start_index:]
        else:
            print(f"Website '{start_from}' not found in the file. Starting from the beginning.")

    return [websites[i:i + batch_size] for i in range(0, len(websites), batch_size)]


def check_websites_and_dns(txt_file, output_file, batch_size=1000, start_from=None):
    batches = split_file(txt_file, batch_size, start_from)
    print(f"Total batches: {len(batches)}")

    for batch_number, batch in enumerate(batches, start=1):
        print(f"Processing batch {batch_number}/{len(batches)}...")
        process_batch(batch, output_file)
        time.sleep(1)  # Sleep for 0.5 seconds after each batch


txt_file_path = input('enter input file: ')
output_file_path = input('enter output file: ')
start = None
check_websites_and_dns(txt_file_path, output_file_path, start_from=start)


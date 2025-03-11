import csv
from collections import Counter, defaultdict
import ast

def process_status_data(status, rows):
    """
    Process a group of rows with the same https_status and calculate various metrics.

    """
    # Initialize metrics
    filtered_sites = []
    ttl_values = []
    ip_addresses = []
    dns_status = []
    
    for row in rows:
        #if status in row['https_status']:
            filtered_sites.append(row)
            ttl = float(row['ttl']) if row['ttl'].strip() else None
            if ttl is not None:
                ttl_values.append(ttl)
            dns = row['return_code'] if row['return_code'].strip() else None
            if dns is not None:
                dns_status.append(dns)
            ip = row['ip'] if row['ip'].strip() else None
            if ip is not None:
                try:
                    ip_list = ast.literal_eval(ip)  # Convert string representation of list to list
                    ip_addresses.extend(ip_list)
                except (ValueError, SyntaxError):
                    continue  # Skip rows with malformed IP addresses

    # Calculate metrics
    https_status_counter = len(filtered_sites)
    dns_status_counter = Counter(dns_status)
    dns_common = dns_status_counter.most_common()  # Get most common DNS status
    ip_counter = Counter(ip_addresses)
    ip_common = ip_counter.most_common(3)  # Get top 3 IPs
    average_ttl = sum(ttl_values) / len(ttl_values) if ttl_values else 0

    # Write group analysis results to CSV
    return [status, https_status_counter, dns_common, ip_common, round(average_ttl)]

def get_last_three_words(text):
    """
    Extract the last three words from a text string.
    """
    words = text.split()
    return " ".join(words[-3:]) if len(words) >= 3 else text

def extract_numbers(column_value):
    """
    Extracts numbers from a column value like '["182"]}}' and returns them as a list of integers.
    """
    try:
        numbers = ast.literal_eval(column_value.strip().split("}}")[0])  # Extract the list portion
        return [int(num) for num in numbers]
    except (ValueError, SyntaxError):
        return []

def analyze_csv(input_csv, output_csv):
    """
    Analyze a CSV file to group data by 'https_status', including rows with specific text,
    and calculate metrics for each group.
    """
    # Dictionaries to store grouped data
    grouped_data = defaultdict(list)
    seen_websites = set()
    total_filtered_domains = 0 

    ssl_data = []
    connection_data = []
    timeout_data = []
    dismatch = []
    expired = []
    failure = []

    with open(input_csv, 'r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile, delimiter=',')
        print(reader.fieldnames)
        for row in reader:
            website = row['Column1.3']

            # Ensure uniqueness: Skip if website already processed
            if website in seen_websites:
                continue
            seen_websites.add(website)

            category_numbers = extract_numbers(row['Column5'])  

            if any(num in filter_list for num in category_numbers):
             total_filtered_domains += 1  
             https_status = row['https_status']
             if "self signed certificate in certificate chain" in https_status:
                ssl_data.append(row)
             elif "ConnectTimeoutError" in https_status:
                timeout_data.append(row)
             elif "NewConnectionError" in https_status:
                connection_data.append(row)
             elif "doesn't match" in https_status:
                dismatch.append(row)
             elif "certificate has expired" in https_status:
                expired.append(row)
             elif "handshake failure" in https_status:
                failure.append(row)
             else:
                key = get_last_three_words(https_status)
                grouped_data[key].append(row)

    grouped_data["SSL Errors"] = ssl_data
    grouped_data["Timeout Errors"] = timeout_data
    grouped_data["Connection Errors"] = connection_data
    grouped_data["Dismatch"] = dismatch
    grouped_data["Certificate expired"] = expired
    grouped_data["handshake failure"] = failure 

    processed_rows = []
    for status, rows in grouped_data.items():
        processed_rows.append(process_status_data(status, rows))

    # Sort the processed rows by the 'Count' column (second element in each row)
    processed_rows.sort(key=lambda x: x[1], reverse=True)
    
    with open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["https_status", "Count", "DNS Status", "Top 3 IPs", "Average TTL"])
        writer.writerows(processed_rows)
        # Process the group
       
        for status, rows in grouped_data.items():
            #if len(grouped_data.items())>1:
            process_status_data(status, rows)
       


    print(f"Analysis complete. Results saved to {output_csv}")
    print(len(seen_websites))
    print(total_filtered_domains)

#only for dns for family datset
filter_list= [6, 40, 42, 44, 45, 46, 161, 10, 30, 149, 166, 170, 204, 174, 12, 1, 7, 38, 197, 176, 171, 121, 122, 120, 43, 143]
   

input_csv = input('enter input file: ')    
output_csv = input('enter output file: ')
analyze_csv(input_csv,output_csv)  

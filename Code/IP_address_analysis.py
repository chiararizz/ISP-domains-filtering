#script to check the weighted percentage of IP addresses that compare in both measurements W and W/O parental control
import pandas as pd

def calculate_weighted_ip_percentage(file1, file2):

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    
    df1_filtered = df1[df1['Count'] > 3]
    df2_filtered = df2[df2['Count'] > 3]
    
    # Calculate total weight (sum of counts in file1)
    total_weight = df1_filtered['Count'].sum()
    
    # Find matching IPs and their respective weights
    matching_ips = df1_filtered[df1_filtered['IP Address'].isin(df2_filtered['IP Address'])]
    
    # Calculate matching weight
    matching_weight = matching_ips['Count'].sum()
    
    # Avoid division by zero
    if total_weight == 0:
        return 0.0
    
    # Calculate weighted percentage
    weighted_percentage = (matching_weight / total_weight) * 100
    return weighted_percentage

imput_file1= input('enter first file: ')
input_file2= input('enter second file: ')
percentage = calculate_weighted_ip_percentage(input_file1, input_file2)
print(f"Weighted percentage of matching IPs: {percentage:.2f}%")

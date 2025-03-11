import csv
from collections import defaultdict

def process_csv(input_file, output_file):
   
    group_counts = defaultdict(int)

    
    with open(input_file, 'r', newline='', encoding='utf-8') as infile:
        csv_reader = csv.reader(infile, delimiter=';')
        header = next(csv_reader)  # Skip the header
        
       
        acc_count=0
        group_count=0
        for row in csv_reader:
           
            if "Accessible" in row[6]:
                category_1 = row[3] 
                category_2 = row[4]  
                acc_count+=1
                group_key = (category_1,category_2)
                group_counts[group_key] += 1
                group_count+=group_counts[group_key]
   
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        csv_writer = csv.writer(outfile)

    
        csv_writer.writerow(["Category 1", "Category 2", "Count"])

      
        for (category_1,category_2), count in group_counts.items():
            csv_writer.writerow([category_1, category_2, count])

    print(f"New CSV file created: {output_file}")
    print(acc_count,group_count)


# File paths
input_file = input('enter input file: ')
output_file = input ('enter output file: ')

process_csv(input_file, output_file)

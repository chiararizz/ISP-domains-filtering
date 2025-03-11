#dns for family only
#script to map the category numbers of the output files into category names

import pandas as pd

file2_path = input('enter category_names file: ')
file1_path = input('enter input file: ')
output_file = input('enter output file: ')


df_mapping = pd.read_csv(file2_path)

mapping_dict = {int(row['Number']): row['Category_name'] for _, row in df_mapping.iterrows()}

# ------------------------------

df1 = pd.read_csv(file1_path)

# ------------------------------

# ------------------------------
def get_category_names(row):
    names = []

    for col in ['Category']:
        val = row[col]

        if pd.notnull(val) and str(val).strip() not in ['', '[]']:
            try:
            
                num = int(str(val).strip())
               
                if num in mapping_dict:
                    names.append(mapping_dict[num])
            except ValueError:
              
                pass
  
    return '; '.join(names)


df1['Category Names'] = df1.apply(get_category_names, axis=1)

# ------------------------------

df1.to_csv(output_file, index=False, encoding='utf-8')
print(f"Output written to {output_file}")

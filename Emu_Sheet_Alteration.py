import pandas as pd
import os

# Read the input CSV file
sheet = pd.read_csv('EmuDump/ColColl2 - ColColl2.csv')

# Group by ecatalogue_key
grouped = sheet.groupby('ecatalogue_key')

#List of all the data
consolidated_data = []


for key, group in grouped:
    row_data = {'ecatalogue_key': key}
    
    #prefix For Collectors finding how many and adding them up
    for i, entry in enumerate(group.itertuples(), 1):
        for col in sheet.columns:
            if col != 'ecatalogue_key':  # Skip the key column
                # Add prefixed column with the value
                #Row data is column by columb getting each row corresponding to numbers and appending. 
                row_data[f'col_{i}_{col}'] = getattr(entry, col)
    
    #Add to large data list (Per row)
    consolidated_data.append(row_data)


#New File Logic
result = pd.DataFrame(consolidated_data)
output_name = input("Output_Name: ")
if not output_name.endswith('.csv'):
    output_name += '.csv'

desktop_path = os.path.expanduser("~/Desktop")
output_folder = os.path.join(desktop_path, "Outputs")
os.makedirs(output_folder, exist_ok=True)

result.to_csv(os.path.join(output_folder, output_name), index=False)
print(f"Data saved to {os.path.join(output_folder, output_name)}")
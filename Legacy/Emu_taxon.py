import pandas as pd
import os

# Read and rename columns the input CSV file
sheet = pd.read_csv('EmuDump/IdeTaxonCuba.csv')
sheet.columns = ['IdeTaxonRef_key', 'ecatalogue_key', 'taxon_irn', 'taxon_parent_irn']

# Group by ecatalogue_key
grouped = sheet.groupby('ecatalogue_key')

final_data = []

for key, group in grouped:
    row_data = {'ecatalogue_key': key}
    
    # Process each entry per group
    for i, entry in enumerate(group.itertuples(), 1):
        for col in sheet.columns:
            if col != 'ecatalogue_key':
                row_data[f'taxon_{i}_{col}'] = getattr(entry, col)
    
    # Add data by row
    final_data.append(row_data)

# New File Logic
result = pd.DataFrame(final_data)
output_name = input("Output_Name: ")
if not output_name.endswith('.csv'):
    output_name += '.csv'

desktop_path = os.path.expanduser("~/Desktop")
output_folder = os.path.join(desktop_path, "Outputs")
os.makedirs(output_folder, exist_ok=True)

result.to_csv(os.path.join(output_folder, output_name), index=False, float_format='%.0f')
print(f"Data saved to {os.path.join(output_folder, output_name)}")
import pandas as pd
import os

# Get input folder path from user
input_folder = input("Enter the input folder path: ")

# Define file paths
colcolle_file = os.path.join(input_folder, 'ColColle.csv')
ecatalog_file = os.path.join(input_folder, 'ecatalog.csv')
idetaxon_file = os.path.join(input_folder, 'IdeTaxon.csv')

# Process ColColle file
print("Processing ColColle file...")
colcolle_df = pd.read_csv(colcolle_file, low_memory=False)
# Rename IRN columns in ColColle file
rename_dict = {}
for col in colcolle_df.columns:
    if col.lower() == 'irn':
        rename_dict[col] = 'Collector_irn'
if rename_dict:
    colcolle_df.rename(columns=rename_dict, inplace=True)

# Group ColColle by ecatalogue_key
grouped_colcolle = colcolle_df.groupby('ecatalogue_key')
colcolle_consolidated = []

for key, group in grouped_colcolle:
    row_data = {'ecatalogue_key': key}
    
    for i, (idx, row) in enumerate(group.iterrows(), 1):
        for col in colcolle_df.columns:
            if col != 'ecatalogue_key':  # Skip the key column
                row_data[f'col_{i}_{col}'] = row[col]
    
    colcolle_consolidated.append(row_data)

colcolle_result = pd.DataFrame(colcolle_consolidated)

# Process ecatalog file
print("Processing ecatalog file...")
ecatalog_df = pd.read_csv(ecatalog_file, low_memory=False)

# Rename specific irn columns in ecatalog file by position
# Column C (index 2) - rename to catalog_irn
# Column P (index 15) - rename to site_irn
# Column AC (index 28) - rename to site_parent_irn
if len(ecatalog_df.columns) > 28:  # Make sure we have enough columns
    # Get column names at specific positions
    col_c = ecatalog_df.columns[2]  # Column C (index 2)
    col_p = ecatalog_df.columns[15]  # Column P (index 15)
    col_ac = ecatalog_df.columns[28]  # Column AC (index 28)
    
    # Rename columns that contain 'irn' at specific positions
    rename_dict = {}
    if 'irn' in col_c.lower():
        rename_dict[col_c] = 'catalog_irn'
    if 'irn' in col_p.lower():
        rename_dict[col_p] = 'site_irn'
    if 'irn' in col_ac.lower():
        rename_dict[col_ac] = 'site_parent_irn'
    
    # Apply renaming if needed
    if rename_dict:
        ecatalog_df.rename(columns=rename_dict, inplace=True)

# Process IdeTaxon file
print("Processing IdeTaxon file...")
idetaxon_df = pd.read_csv(idetaxon_file, low_memory=False)

# Rename columns in IdeTaxon file
# Column C (index 2) - rename to taxon_irn
# Column D (index 3) - rename to taxon_parent_irn
if len(idetaxon_df.columns) > 3:  # Make sure we have enough columns
    col_c = idetaxon_df.columns[2]  # Column C (index 2)
    col_d = idetaxon_df.columns[3]  # Column D (index 3)
    
    rename_dict = {}
    if 'irn' in col_c.lower():
        rename_dict[col_c] = 'taxon_irn'
    if 'irn' in col_d.lower():
        rename_dict[col_d] = 'taxon_parent_irn'
    
    if rename_dict:
        idetaxon_df.rename(columns=rename_dict, inplace=True)

# Group IdeTaxon by ecatalogue_key if it exists, otherwise skip this step
idetaxon_result = None
if 'ecatalogue_key' in idetaxon_df.columns:
    grouped_idetaxon = idetaxon_df.groupby('ecatalogue_key')
    idetaxon_consolidated = []

    for key, group in grouped_idetaxon:
        row_data = {'ecatalogue_key': key}
        
        # Use DataFrame.iloc instead of itertuples to avoid issues with column names containing periods
        for i, (idx, row) in enumerate(group.iterrows(), 1):
            for col in idetaxon_df.columns:
                if col != 'ecatalogue_key':  # Skip the key column
                    row_data[f'taxon_{i}_{col}'] = row[col]
        
        idetaxon_consolidated.append(row_data)

    idetaxon_result = pd.DataFrame(idetaxon_consolidated)

# Merge the data in the order: ecatalog, ideTaxon, ColColle
merged_data = ecatalog_df  # Start with ecatalog data

# Add IdeTaxon data if available
if idetaxon_result is not None:
    merged_data = pd.merge(merged_data, idetaxon_result, on='ecatalogue_key', how='outer')

# Add ColColle data last
merged_data = pd.merge(merged_data, colcolle_result, on='ecatalogue_key', how='outer')

# Save the combined result
output_name = input("Output_Name: ")
if not output_name.endswith('.csv'):
    output_name += '.csv'

desktop_path = os.path.expanduser("~/Desktop")
output_folder = os.path.join(desktop_path, "EMU_Combined_Sheets")
os.makedirs(output_folder, exist_ok=True)

output_file = os.path.join(output_folder, output_name)
merged_data.to_csv(output_file, index=False)
print(f"Combined data saved to {output_file}")
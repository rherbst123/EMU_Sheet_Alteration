# EMU Sheet Alteration

A Python utility for processing and merging EMU database CSV exports. Created By: Riley Herbst & Alex Wcislo

## Inputs

This tool processes three CSV files exported from EMU database:
- `ecatalog.csv` - Main catalog data
- `IdeTaxon.csv` - Taxonomic information
- `ColColle.csv` - Collector information

The script consolidates related records, renames IRN columns for clarity, and merges the data into a single CSV file.

## Usage

1. Run the script: `python Emu_Sheet_Alteration.py`
2. Enter the path to the folder containing your CSV files when prompted
3. Enter a name for the output file when prompted
4. The merged CSV will be saved to `~/Desktop/Outputs/`

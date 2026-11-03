import pandas as pd

df = pd.read_csv('example_raster.csv')

# Define the columns of interest
columns_of_interest = ['E_CT', 'E_CA', 'E_SA', 'E_FA']

# Create a mask to identify rows where any of the specified columns have values different from 'X'
mask = df[columns_of_interest].apply(lambda row: (row != 'X').any(), axis=1)

# Filter the DataFrame using the mask
rows_with_different_values = df[mask]

# Display the rows with values different from 'X'
rows_with_different_values.to_csv('filtered_results.reproduced.csv', index=True)



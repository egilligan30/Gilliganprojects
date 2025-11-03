import pandas as pd
import us  # if don't have, pip install us in terminal

import os


os.chdir(r"C:\Users\name_redacted\OneDrive\Desktop\Sports betting paper data\ginicoefficientcounty\long")

df = pd.read_stata("ginicoefficientcountydta.dta")


#split county name into county and state
df[['county', 'state_full']] = df['CountyName'].str.split(',', expand=True)

# Clean up whitespace and casing
df['county'] = df['county'].str.strip().str.upper()
df['state_full'] = df['state_full'].str.strip().str.upper()

# Use the us library to get state name to abbreviation mapping
state_name_to_abbr = {state.name.upper(): state.abbr.upper() for state in us.states.STATES}

# Map full state name to abbreviation
df['state_abbr'] = df['state_full'].map(state_name_to_abbr)


#fips reference file load from Census
fips_url = "https://www2.census.gov/geo/docs/reference/codes/files/national_county.txt"
fips = pd.read_csv(
    fips_url,
    header=None,
    names=["state_abbr", "state_fips", "county_fips", "county_name", "class_code"]
)

# Standardize casing for merge
fips['state_abbr'] = fips['state_abbr'].str.strip().str.upper()
fips['county_name'] = fips['county_name'].str.strip().str.upper()


#merge data sets on county and state abbreviation
df_merged = df.merge(
    fips,
    left_on=['county', 'state_abbr'],
    right_on=['county_name', 'state_abbr'],
    how='left'  # keep all rows from original dataset
)

#create 5 digit fips codes
df_merged['fips'] = (
    df_merged['state_fips'].astype(str).str.zfill(2) +
    df_merged['county_fips'].astype(str).str.zfill(3)
)

#save as new .dta file to cd
df_merged.to_stata("fipsnew.dta", write_index=False)

print("FIPS codes added successfully.")


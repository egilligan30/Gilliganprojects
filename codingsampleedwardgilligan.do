clear
cd "C:\Users\redcated_name\OneDrive\Desktop\Sports betting paper data\povertyestimates"
import excel "povertyestimates2013.xlsx"

drop in 1
drop in 1
drop in 1
drop F G 
drop I J 
drop L M O P R S U V X-AE

ds
foreach var of varlist `r(varlist)' {
    
    quietly {
        local newname = `var' in 1
        // Take the first row value of the variable as a temporary "name" for cleaning
    }

    local newname = subinstr("`newname'", "/", "_", .)
    // Replace slashes with underscores to make a valid Stata variable name

    local newname = subinstr("`newname'", " ", "_", .)
    // Replace spaces with underscores for compatibility

    local newname = ustrregexra("`newname'", "[^A-Za-z0-9_]", "")
    // Remove any remaining characters that are not letters, numbers, or underscores

    local newname = ustrregexra("`newname'", "_+", "_")
    // Collapse multiple underscores into a single underscore

    local newname = ustrregexra("`newname'", "^_+|_+$", "")
    // Remove leading or trailing underscores

    if ustrregexm("`newname'", "^[0-9]") {
        local newname = "v" + "`newname'"
        // If the name starts with a number, prepend "v" because Stata variable names cannot start with a digit
    }

    local newname = substr("`newname'", 1, 32)
    // Truncate the variable name to max character length

    rename `var' `newname'
    // Give the cleaned name to the variable
}

drop in 1

gen str5 state_fips_str = substr("00" + State_FIPS_Code, -2, 2)
gen str5 county_fips_str = substr("000" + County_FIPS_Code, -3, 3)
// Convert numeric FIPS codes to fixed-length strings with leading zeros
// "00" + State_FIPS_Code ensures at least 2 characters, "000" + County_FIPS_Code ensures at least 3 characters

gen county_fips = state_fips_str + county_fips_str
// Concatenate state and county strings to create a full 5-digit county FIPS code

drop state_fips_str county_fips_str
drop State_FIPS_Code County_FIPS_Code
// Remove intermediate variables now that the full county FIPS is created

local states "Alabama Alaska Arizona Arkansas California Colorado Connecticut Delaware Florida Georgia Hawaii Idaho Illinois Indiana Iowa Kansas Kentucky Louisiana Maine Maryland Massachusetts Michigan Minnesota Mississippi Missouri Montana Nebraska Nevada New Hampshire New Jersey New Mexico New York North Carolina North Dakota Ohio Oklahoma Oregon Pennsylvania Rhode Island South Carolina South Dakota Tennessee Texas Utah Vermont Virginia Washington West Virginia Wisconsin Wyoming"
foreach s of local states {
    drop if Name == "`s'"
    // Remove rows that contain state totals rather than county-level data
}

drop in 1
drop Postal_Code

ds Name, not
local vars_to_destring `r(varlist)'
destring `vars_to_destring', replace
// Convert string variables that represent numeric values into numeric variables

gen Year = 2013
// Add a variable indicating the year of the data

save "povertyestimates2013dta.dta", replace

def remove_missing_values(values:[]):
"""
Removal of missing values
    Input: List of values, including missing values like None, ‘’ and nan
    Output: list of values removing the missing ones
"""
    missing_values = [None, '', 'nan', 'NAN']
    return [val for val in values if val not in missing_values]


def fill_missing_values(values, fill_value=0):
"""
    o Inputs
        ▪ List of values, including missing values
        ▪ The value to fill the missing values (default to 0)
    o Output: list of values where the missing values are replaced with the given filling value
"""
    missing_values = [None, '', 'nan', 'NAN']
    return [fill_value if val in missing else val for val in values ]    

def remove_duplicated_values():
    o Input: List of values
    o Output: List of unique values

def norm_min_max(): 
normalization of numerical values using the min-max method
    o Inputs:
        ▪ List of numerical values
        ▪ New minimum (default to 0.0)
        ▪ New maximum (default to 1.0)
    o Output: list of normalized values

def standardization():
Standardization of numerical values using the z-score method
    o Input: List of numerical values
    o Output: List of standardized values

def clipping():
• Clipping numerical values to a certain range
    o Inputs:
        ▪ List of numerical values
        ▪ Minimum value to clip
        ▪ Maximum value to clip
    o Output: List of clipped values

def converst_val_to_int():
• Conversion of values to integers
    o Input: List of strings (it can include both numerical and non-numerical values)
    o Output: List of values converted to integers (non-numerical values are excluded from the output)

def log_scale_transform():
• Logarithmic scale transformation
    o Input: List of values
    o Output: List of values converted to logarithmic scale (just the original positive numbers)

def tokenization():
• Tokenization of text into words, selecting only alphanumeric characters and lowercasing words
    o Input: Text to be processed
    o Output: Processed text

def select_aphanumeric_spaces():
• Selection of alphanumerical characters and spaces
    o Input: Text to be processed
    o Output: Processed text

def removal_stopwords():
• Removal of stop-words from text (it should be lower-cased)
    o Inputs
        ▪ Text to be processed
        ▪ Stop words to be removed
    o Output: Processed text

def flatten_list():
• Flatten a list of lists
    o Input: A list of lists
    o Output: A flattened list

def random_shuffling_list():
• Random shuffling of a list of values
    o Inputs
        ▪ List of values
        ▪ Seed to ensure reproducibility
    o Output: list of shuffled values
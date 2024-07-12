def check_and_clean_columns(columns):
    has_dot = False
    cleaned_columns = []
    
    for col in columns:
        if '.' in col:
            has_dot = True
            cleaned_columns.append(col.split('.')[-1])
        else:
            cleaned_columns.append(col)
    
    return cleaned_columns, has_dot

# Example usage
column_list = ["em.rule", "user_id", "order.date", "product_name"]

cleaned_columns, contains_dot = check_and_clean_columns(column_list)

print("Original columns:", column_list)
print("Cleaned columns:", cleaned_columns)
print("Contains columns with dot:", contains_dot)


def validate_columns(extracted_tables, extracted_columns, exception_data, rule_metadata, issue_data):
    table_column_mapping = {
        "exception_data": exception_data,
        "rule_metadata": rule_metadata,
        "issue_data": issue_data
    }
    
    valid_columns = set()
    for table in extracted_tables:
        if table in table_column_mapping:
            valid_columns.update(table_column_mapping[table])
    
    invalid_columns = set(extracted_columns) - valid_columns
    
    if invalid_columns:
        return False, list(invalid_columns)
    else:
        return True, []

# Example usage
exception_data = ["id", "exception_type", "description"]
rule_metadata = ["rule_id", "rule_name", "rule_type"]
issue_data = ["issue_id", "issue_description", "status"]

# Replace these with your actual extracted data
extracted_tables = ["exception_data", "rule_metadata"]
extracted_columns = ["id", "rule_id", "description", "status"]

is_valid, invalid_cols = validate_columns(extracted_tables, extracted_columns, 
                                          exception_data, rule_metadata, issue_data)

if is_valid:
    print("All extracted columns belong to at least one of the extracted tables.")
    # Proceed with your data processing here
else:
    print("No data matched.")
    print("The following columns do not belong to any of the extracted tables:", invalid_cols)

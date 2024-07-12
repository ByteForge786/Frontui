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

import re

import re

def extract_sql_components(query):
    # Remove comments and normalize whitespace
    query = re.sub(r'--.*$|\s+', ' ', query, flags=re.MULTILINE).strip()
    query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)  # Remove multi-line comments

    # Extract table names
    table_pattern = r'\b(?:FROM|JOIN|INTO|UPDATE|INSERT\s+INTO)\s+(\w+(?:\s*\.\s*\w+)?(?:\s+(?:AS\s+)?\w+)?(?:\s*,\s*\w+(?:\s*\.\s*\w+)?(?:\s+(?:AS\s+)?\w+)?)*)'
    tables = set()
    for match in re.finditer(table_pattern, query, re.IGNORECASE):
        tables.update(re.findall(r'\b(\w+)(?:\.\w+)?(?:\s+(?:AS\s+)?\w+)?', match.group(1)))

    # Extract column names
    column_pattern = r'\bSELECT\s+(.*?)(?:\s+FROM|\s*$)'
    columns_match = re.search(column_pattern, query, re.IGNORECASE | re.DOTALL)
    
    columns = set()
    if columns_match:
        columns_str = columns_match.group(1)
        if '*' in columns_str:
            columns.add('*')
        else:
            # Split columns and clean them
            column_list = re.findall(r'((?:\w+\.)?(?:\w+)(?:\s*\(.*?\))?)\s*(?:,|$|\s+AS\s+)', columns_str, re.DOTALL)
            for col in column_list:
                col = col.strip()
                if '(' in col:  # Handle function calls
                    columns.add(col.split('(')[0])
                    columns.update(re.findall(r'(\w+\.\w+|\w+)', col))
                else:
                    columns.add(col)
    else:
        # Handle INSERT, UPDATE, DELETE statements
        column_matches = re.findall(r'\b(?:INSERT\s+INTO|UPDATE).*?\(([^)]+)\)', query, re.IGNORECASE)
        if column_matches:
            columns.update(col.strip() for col in column_matches[0].split(','))

    # Extract additional columns from WHERE, GROUP BY, ORDER BY clauses
    additional_columns = re.findall(r'\b(?:WHERE|GROUP\s+BY|ORDER\s+BY)\s+(.*?)(?:\s*$|\s+(?:LIMIT|OFFSET))', query, re.IGNORECASE | re.DOTALL)
    for clause in additional_columns:
        columns.update(re.findall(r'(\w+\.\w+|\w+)', clause))

    # Remove table names from columns
    columns = set(col.split('.')[-1] if '.' in col else col for col in columns)

    return list(tables), list(columns)

# Example usage
queries = [
    "SELECT r.rule_id, k.robinhood FROM lauda WHERE xyz condition",
    "SELECT t1.col1, t2.col2 AS alias FROM table1 t1 JOIN table2 t2 ON t1.id = t2.id",
    "SELECT * FROM users",
    "INSERT INTO users (name, email) VALUES ('John', 'john@example.com')",
    "UPDATE employees SET salary = 5000 WHERE id = 1",
    "SELECT COUNT(*) AS total FROM (SELECT DISTINCT user_id FROM orders) AS subquery",
    "WITH cte AS (SELECT id FROM customers) SELECT cte.id, orders.order_id FROM cte JOIN orders ON cte.id = orders.customer_id"
]

for i, query in enumerate(queries, 1):
    tables, columns = extract_sql_components(query)
    print(f"\nQuery {i}:")
    print("Table names:", tables)
    print("Column names:", columns)

# Example usage
queries = [
    "SELECT r.rule_id, k.robinhood FROM lauda WHERE xyz condition",
    "SELECT t1.col1, t2.col2 AS alias FROM table1 t1 JOIN table2 t2 ON t1.id = t2.id",
    "SELECT * FROM users",
    "INSERT INTO users (name, email) VALUES ('John', 'john@example.com')",
    "UPDATE employees SET salary = 5000 WHERE id = 1",
    "SELECT COUNT(*) AS total FROM (SELECT DISTINCT user_id FROM orders) AS subquery",
    "WITH cte AS (SELECT id FROM customers) SELECT cte.id, orders.order_id FROM cte JOIN orders ON cte.id = orders.customer_id"
]

for i, query in enumerate(queries, 1):
    tables, columns = extract_sql_components(query)
    print(f"\nQuery {i}:")
    print("Query:", query)
    print("Table names:", tables)
    print("Column names:", columns)

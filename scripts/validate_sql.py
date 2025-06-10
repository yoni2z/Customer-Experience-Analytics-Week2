import sqlparse
import re
import sys

with open('scripts/database.py', 'r') as f:
    content = f.read()

# Extract SQL statements from cursor.execute("""...""")
sqls = re.findall(r'cursor\.execute\(\s*"""(.*?)"""\s*\)', content, re.DOTALL)
valid = all(sqlparse.parse(sql.strip()) for sql in sqls if sql.strip())

print('SQL syntax check passed' if valid else 'SQL syntax error')
sys.exit(0 if valid else 1)
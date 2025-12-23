from flask import Flask, render_template, jsonify
import csv

app = Flask(__name__)

def load_portfolio_data():
    """Load portfolio data from CSV file dynamically."""
    data = []
    columns = []
    with open('portfolio_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        for i, row in enumerate(reader):
            record = {'id': i}
            for col in columns:
                try:
                    record[col] = float(row[col])
                except ValueError:
                    record[col] = row[col]
            data.append(record)
    return data, columns

def get_column_groups(columns):
    """Group columns by prefix (dec, obj, aux, etc.)."""
    groups = {}
    for col in columns:
        # Extract prefix (letters before any numbers or at start)
        prefix = ''.join(c for c in col if c.isalpha()).lower()
        # Common prefixes
        for p in ['dec', 'obj', 'aux']:
            if col.lower().startswith(p):
                prefix = p
                break
        if prefix not in groups:
            groups[prefix] = []
        groups[prefix].append(col)
    return groups

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    data, columns = load_portfolio_data()
    return jsonify(data)

@app.route('/api/columns')
def get_columns():
    """Return column metadata for dynamic UI generation."""
    _, columns = load_portfolio_data()
    groups = get_column_groups(columns)
    return jsonify({
        'all': columns,
        'groups': groups
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

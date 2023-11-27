from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)

# Configure your SQL Server connection
server = '172.31.151.88'
database = 'Dessy'
username = 'dessyuser'
password = 'PwdDessyU5er@2022'
driver = '{ODBC Driver 17 for SQL Server}'

# Function to execute a stored procedure
def execute_stored_procedure():
    connection = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    cursor = connection.cursor()

    # Replace 'your_stored_procedure' with the actual name of your stored procedure
    cursor.execute("EXEC [sp_SERVPERF_ResponseTime_View] 1,'2023-09-27','2023-10-27','A1'")

    # Fetch the results
    result = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return result

# Define a route for the API endpoint
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # Execute the stored procedure
        result = execute_stored_procedure()

        # Convert the result to a list of dictionaries for JSON response
        #keys = [column[0] for column in result.description]
        keys = ['Order', 'Equipment', 'Notif', 'MPG', 'WCTR','NotiDateTime','ArrivedDateTime','MBU','Location','ResponseTime','RTFailed']
        data = [dict(zip(keys, row)) for row in result]

        return jsonify({'data': data})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
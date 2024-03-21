# pymysql-toolkit

<p>This is a Python package for interacting with a MySQL database.</p>

<h2>Usage</h2>

<p>Before using the package, make sure you have the following prerequisites:</p>

<ul>
  <li>Python installed on your system</li>
  <li>MySQL server running</li>
  <li>Required Python packages (pymysql)</li>
  <li>Connection details stored in a JSON file</li>
</ul>

<h3>Setting Up Connection Details</h3>

<p>Store your MySQL database connection details in a JSON file named <code>connection_details.json</code> in the following format:</p>

<pre><code>{
  "mysql_conn": {
    "host": "your_host",
    "user": "your_username",
    "password": "your_password",
    "database": "your_database_name"
  }
}
</code></pre>

<h3>Running the Package</h3>

<p>To use the package, import the necessary functions from <code>pymysql_functions</code> and call them as needed. Here's an example:</p>

<pre><code>import pymysql_functions

# Get connection details
conn_detail = pymysql_functions.conn_details('connection_details.json', 'mysql_conn')

# Establish connection to MySQL database
conn, curr = pymysql_functions.get_connection(conn_detail)

# Call other functions as needed
pymysql_functions.show_tables(conn, curr)
# Example: pymysql_functions.create_table(curr, conn)

# Close connection
curr.close()
conn.close()
</code></pre>

<h2>Functions</h2>

<ul>
  <li><code>conn_details(filename, dbname)</code>: Retrieves connection details from a JSON file.</li>
  <li><code>get_connection(conn_detail)</code>: Establishes a connection to the MySQL database.</li>
  <li><code>show_tables(conn, curr)</code>: Displays a list of tables in the database and their details.</li>
  <li><code>create_table(curr, conn)</code>: Allows the user to create a new table in the database.</li>
  <li><code>insert_data(conn, curr)</code>: Allows the user to insert data into a table.</li>
  <li><code>create_table_file(conn, curr, file_name, delimiter)</code>: Creates a table in the database based on a file containing column names and data types.</li>
  <li><code>load_file_data(conn, curr, file_name, delimiter)</code>: Loads data from a file into a table in the database.</li>
  <li><code>delete_data(conn, curr, table_name, cond)</code>: Deletes data from a table based on specified conditions.</li>
  <li><code>update_data(conn, curr, table_name)</code>: Updates data in a table based on specified conditions.</li>
  <li><code>manual_query(conn, curr)</code>: Allows the user to execute manual SQL queries.</li>
</ul>

<h2>Contributing</h2>

<p>Contributions to the project are welcome! Feel free to fork the repository, make changes, and submit pull requests.</p>

<h2>Let's Connect:</h2>
<p>LinkedIn: https://www.linkedin.com/in/ankushkamboj</p>
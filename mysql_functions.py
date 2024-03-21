import pymysql as pm
import json

def conn_details(filename,dbname):
	"""Retrieves connection details from a JSON file.

    Parameters:
    filename (str): The path to the JSON file containing connection details.
    dbname (str): The name of the connection details in the JSON file.
    
	Returns:
    dict: A dictionary containing the connection details.
    """
	f=open(filename)
	js=json.load(f)
	return js[dbname]

def get_connection(conn_detail):
	"""Establishes a connection to the MySQL database.

    Parameters:
    conn_detail (dict): A dictionary containing the connection details.

    Returns:
    tuple: A tuple containing the connection object and cursor object.
    """
	try:
		host=conn_detail['host']
		user=conn_detail['user']
		password=conn_detail['password']
		db=conn_detail['database']
		conn=pm.connect(host=host,user=user,password=password,database=db)
		curr=conn.cursor()
		
	except Exception as msg:
		print("Error in get connection...",msg)
	else:
		print("Connection Successfully Created!!")
		return(conn,curr)
	


def show_tables(conn,curr):
	"""Displays a list of tables in the database and their details.

    Parameters:
    conn: The connection object to the MySQL database.
    curr: The cursor object for executing queries.
    """
	table_list={}
	curr.execute("show tables")
	data=curr.fetchall()
	for l,i in enumerate(data):
		for i,j in enumerate(i):
			table_list[f"{l+1}"]=j
	for key,v in table_list.items():
		print(f"Press {key}  for {v} details..")
	option =input("Enter your choice: ")
	while option not in table_list:
		option= input('Please enter valid choice! :')
	query=f"SELECT * FROM {table_list[option]};"
	curr.execute(query)
	data=curr.fetchall()
	print()
	for i in data:
		for j in i:
			print(j,end=' ')
		print()
	curr.close()
	conn.close()
	


def create_table(curr,conn):
	"""Allows the user to create a new table in the database.

    Parameters:
    curr: The cursor object for executing queries.
    conn: The connection object to the MySQL database.
	"""
	data_types = {1: 'int',2: 'Varchar(20)',3:'float'}
	table_name = input('Enter table name: ')
	str = ""
	str1 = ""
	while True:
		col = input("Enter the name of column: ")
		for i , j in data_types.items():
			print(f'{i} for {j}')
		choice = int(input("Enter choice: "))
		while choice not in data_types:
			choice = int(input("Please enter valid choice!: "))
		data_type = data_types[choice]
		str1+= f"{col} {data_type} "
		str += str1
		str1 = ", "
		option = input("Press [n] to end or Press any key to continue: ").lower()
		if option  == 'n':
			break
	query = f"CREATE TABLE {table_name} ({str})"
	curr.execute(query)
	print(f"Table {table_name} created sucessfully!")


def insert_data(conn,curr):
	"""Allows the user to insert data into a table.

    Parameters:
    conn: The connection object to the MySQL database.
    curr: The cursor object for executing queries.
    """
	query_show_tables = 'show tables'
	curr.execute(query_show_tables)
	tables = curr.fetchall()
	table_list = {}
	for index, value in enumerate(tables):
		for key, column in enumerate(value):
			table_list[f'{index+1}'] = column
	for key, values in table_list.items():
		print(f'Press [{key}] for {values}')
	choice = input('Enter your choice: ')
	while choice not in table_list:
		choice = input('Please enter valid choice!: ')
	table_name = table_list[choice]
	print(table_name)
	query = 'desc students'
	curr.execute(query)
	data = curr.fetchall()
	data_types = {}
	for i , j in enumerate(data):
		data_types[data[i][0]]= data[i][1]
	values_ = []
	for key, values in data_types.items():
		values_.append(input(f'Enter {key} of {values} data type: ')) 
	raw_query =[f"'{value}'" for value in values_]
	insert_query = f'INSERT INTO {table_name} VALUES ({','.join(raw_query)})'
	curr.execute(insert_query)
	conn.commit()
	print("Record insertred sucessfully")
	curr.close()
	conn.close()
	
	
	
def create_table_file(conn, curr, file_name, delimeter):
	"""Creates a table in the database based on a file containing column names and data types.

    Parameters:
    conn: The connection object to the MySQL database.
    curr: The cursor object for executing queries.
    file_name (str): The path to the file containing column names and data types.
    delimiter (str): The delimiter used in the file to separate column names and data types.
	"""
	with open (file_name) as f:
		table_name = input("Enter table name: ")
		h =  f.readline().split(delimeter)
		col = ""
		for i in h:
			data_type = input(f"Enter data type for {i} column :")
			col = col + i + " " + data_type + ","
		tQuery = f"create table {table_name} (f{col[:len(col)-1]})"
		curr.execute(tQuery)
		conn.commit()
		print(f"{table_name} table created sucessfully!")
	return table_name

def load_file_data(conn , curr, file_name, delimeter):
	"""Loads data from a file into a table in the database.

    Parameters:
    conn: The connection object to the MySQL database.
    curr: The cursor object for executing queries.
    file_name (str): The path to the file containing data.
    delimiter (str): The delimiter used in the file to separate data values.
    """
	option = input("Do you want to create table [y/n]").lower()
	if option == 'y':
		table_name = create_table_file(conn, curr, file_name, delimeter)
	else:
		table_name = input("Enter table name: ")
		with open (file_name) as f:
			h = f.readline()
			data = f.readlines()
			for i in data:
				data_ = i.split("\n")[0].split(delimeter)
				qdata = [f"'{i}'" for i in data_]
				qdata = ','.join(qdata)
				fQuery = f"insert into {table_name} values({qdata})"
				print(fQuery)
				curr.execute(fQuery)
				conn.commit()
		print('Data inserted sucessfully!')


def delete_data(conn,curr, table_name, cond):
	"""Deletes data from a table based on specified conditions.

    Parameters:
    conn: The connection object to the MySQL database.
    curr: The cursor object for executing queries.
    table_name (str): The name of the table from which data will be deleted.
    cond (str): The condition to specify which rows to delete.
    """
	query = f'DELETE FROM {table_name} WHERE {cond}'
	curr.execute(query)
	conn.commit()
	print('Record deleted sucessfully')
	curr.close()
	conn.close()

def update_data(conn,curr,table_name):
	"""Updates data in a table based on specified conditions.

    Parameters:
    conn: The connection object to the MySQL database.
    curr: The cursor object for executing queries.
    table_name (str): The name of the table to update.
    """
	column_name = input('Enter column name: ')
	value = input('Enter value to change: ')
	cond = input('Enter condition: ')
	query = f'UPDATE {table_name} SET {column_name} = {value} WHERE {cond}'
	curr.execute(query)
	conn.commit()
	print('Record udated sucessfully')
	curr.close()
	conn.close()


def manual_query(conn,curr):
	"""Allows the user to execute manual SQL queries.

    Parameters:
    conn: The connection object to the MySQL database.
    curr: The cursor object for executing queries.
    """
	while True:
		query = input('Enter sql query here: ')
		curr.execute(query)
		conn.commit()
		print('Query successfully executed: ')
		data = curr.fetchall()
		print(data)
		choice = input('Press [n] to exit or press any key to continue: ').lower()
		if choice == 'n':
			curr.close()
			conn.close()
			break
		    
def main():
	try:
		conn,curr=get_connection(conn_details('connection_details.json',"mysql_conn"))
		# call any function here
	except Exception as msg:
		print("Error in Calling function flow...",msg)
	finally:
		print("I am closing connection")
	
if __name__ == "__main__":
    main()
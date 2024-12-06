# MySQL DB Visualizer

A simple graphical user interface (GUI) application built with Python using `Tkinter` and `mysql-connector-python` to connect to a MySQL database, visualize table data, and perform basic CRUD (Create, Read, Update, Delete) operations.

## Features

- **Connect to MySQL Database**: Enter your host, username, password, and database name to establish a connection.
- **Table Selection**: Choose a table from the database to view and manage data.
- **View Data**: Display rows from the selected table in a table format.
- **Add Row**: Add new rows to the table via a simple input form.
- **Edit Row**: Double-click any row to open a form to edit its data.
- **Delete Row**: Delete selected rows from the table with confirmation.

## Requirements

- Python 3.x
- `tkinter` (usually included with Python by default)
- `mysql-connector-python`

You can install the required MySQL connector by running the following command:

```bash
pip install mysql-connector-python
```
Clone the Repository
```bash
git clone https://github.com/abbyseb/mysql-db-visualizer.git
cd mysql-db-visualizer
```
Install the requirements
```bash
pip install mysql-connector-python==8.0.33
pip install tk
```
## MySQL Server Download
```bash
https://dev.mysql.com/downloads/mysql/8.0.html
```
## Working Screenshots

GUI:
<img width="1205" alt="Screenshot 2024-12-05 at 8 53 44 AM" src="https://github.com/user-attachments/assets/f43a634f-bd76-41c5-a589-d84734e2c268">

Edit Row Functionality:
<img width="1207" alt="Screenshot 2024-12-05 at 8 53 15 AM" src="https://github.com/user-attachments/assets/d6cd7c67-56b3-42f2-9d59-90cf6b59a9a7">

Delete Row Functionality:
<img width="1204" alt="Screenshot 2024-12-05 at 8 54 09 AM" src="https://github.com/user-attachments/assets/3ebfad4f-2638-46fa-bd03-349537ba3c00">

Add Row Functionality:
<img width="1207" alt="Screenshot 2024-12-05 at 8 54 48 AM" src="https://github.com/user-attachments/assets/aba9c889-b1bb-438f-8bb2-676eeba951d3">


References:

[1] https://www.geeksforgeeks.org/python-gui-tkinter/
[2]https://www.geeksforgeeks.org/python-creating-a-button-in-tkinter/?ref=lbp
[3]https://www.w3schools.com/python/python_mysql_getstarted.asp
[4]https://www.w3schools.com/python/python_mysql_select.asp
[5]https://www.w3schools.com/python/python_mysql_update.asp
[6]https://www.w3schools.com/python/python_mysql_insert.asp

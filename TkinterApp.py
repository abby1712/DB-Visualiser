import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class DBVisualizerApp:

    def __init__(self, root):
        # Initialize the main window (root)
        self.root = root
        self.root.title("MySQL DB Visualizer")  # Set the title of the window
        self.root.geometry("800x600")  # Set the window size

        # Initialize database connection and cursor to None
        self.conn = None
        self.cursor = None

        # Call the method to create the UI widgets
        self.create_widgets()

    def create_widgets(self):
        # Create the Database Connection Frame
        connection_frame = tk.Frame(self.root, padx=10, pady=10)
        connection_frame.pack(fill=tk.X)  # Pack the frame with horizontal expansion

        # Create and place the "Host" label and input field
        tk.Label(connection_frame, text="Host:").grid(
            row=0, column=0, padx=5, pady=5)  # Label for h ost input
        self.host_entry = tk.Entry(connection_frame)  # Entry widget for host
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)

        # Create and place the "User" label and input field
        tk.Label(connection_frame, text="User:").grid(
            row=0, column=2, padx=5, pady=5)  # Label for user input
        self.user_entry = tk.Entry(connection_frame)  # Entry widget for user
        self.user_entry.grid(row=0, column=3, padx=5, pady=5)

        # Create and place the "Password" label and input field
        tk.Label(connection_frame, text="Password:").grid(
            row=0, column=4, padx=5, pady=5)  # Label for password input
        self.password_entry = tk.Entry(connection_frame, show="*")  # Entry widget for password, show * for masking
        self.password_entry.grid(row=0, column=5, padx=5, pady=5)

        # Create and place the "Database" label and input field
        tk.Label(connection_frame, text="Database:").grid(
            row=0, column=6, padx=5, pady=5)  # Label for database input
        self.database_entry = tk.Entry(connection_frame)  # Entry widget for database name
        self.database_entry.grid(row=0, column=7, padx=5, pady=5)

        # Create and place the "Connect" button to initiate DB connection
        self.connect_button = tk.Button(
            connection_frame, text="Connect", command=self.connect_db)  # Button to trigger the DB connection
        self.connect_button.grid(row=0, column=8, padx=5, pady=5)

        # Create the Table Selection Frame (for selecting tables)
        table_frame = tk.Frame(self.root, padx=10, pady=10)
        table_frame.pack(fill=tk.X)  # Pack this frame horizontally

        # Create and place the "Table" label and dropdown menu
        tk.Label(table_frame, text="Table:").grid(
            row=0, column=0, padx=5, pady=5)  # Label for table selection
        self.table_dropdown = ttk.Combobox(table_frame, state="readonly")  # Dropdown for table selection
        self.table_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.table_dropdown.bind("<<ComboboxSelected>>", self.load_table)  # Bind event to load table data when selected

        # Create the Data Table Frame (to display data in a table format)
        self.tree = ttk.Treeview(self.root, show="headings")  # Treeview widget to display table data
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Pack it with expand to take up available space

        # Bind double-click event to enable row editing
        self.tree.bind("<Double-1>", self.edit_row)

        # Create the Button Frame (for Add/Delete row functionality)
        button_frame = tk.Frame(self.root, padx=10, pady=10)
        button_frame.pack(fill=tk.X)  # Pack it horizontally

        # Create and place the "Add Row" button
        self.add_button = tk.Button(
            button_frame, text="Add Row", command=self.add_row)  # Button to add a new row
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)  # Pack the button on the left

        # Create and place the "Delete Row" button
        self.delete_button = tk.Button(
            button_frame, text="Delete Row", command=self.delete_row)  # Button to delete a selected row
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)  # Pack the button on the left

    def connect_db(self):
        try:
            # Try to establish a connection to the MySQL database using the connection details
            self.conn = mysql.connector.connect(
                host=self.host_entry.get(),  # Get the host from the entry widget
                user=self.user_entry.get(),  # Get the user from the entry widget
                password=self.password_entry.get(),  # Get the password from the entry widget
                database=self.database_entry.get()  # Get the database name from the entry widget
            )
            
            # Create a cursor object to interact with the database
            self.cursor = self.conn.cursor()

            # Load the list of tables after successful connection
            self.load_tables()

            # Display a success message box
            messagebox.showinfo("Success", "Connected to the database.")
        
        except mysql.connector.Error as err:
            # Catch and handle any errors that occur during the connection attempt
            # Display an error message box with the error details
            messagebox.showerror("Error", f"Failed to connect: {err}")


    def load_tables(self):
        try:
            # Execute the SQL query to show all tables in the database
            self.cursor.execute("SHOW TABLES")
            
            # Fetch all the table names and store them in a list
            tables = [row[0] for row in self.cursor.fetchall()]  # Fetch all rows and get the first column (table name)
            
            # Check if there are no tables found in the database
            if not tables:
                # Display a warning message if no tables are found
                messagebox.showwarning(
                    "No Tables", "No tables found in the database.")
            
            # Update the dropdown menu with the list of tables
            self.table_dropdown["values"] = tables
        
        except mysql.connector.Error as err:
            # Catch any MySQL errors that occur while loading the tables
            # Display an error message with the details of the exception
            messagebox.showerror("Error", f"Failed to load tables: {err}")


    def load_table(self, event=None):
        # Get the name of the selected table from the dropdown
        table = self.table_dropdown.get()
        
        try:
            # Execute the SQL query to get the table structure (column names)
            self.cursor.execute(f"DESCRIBE {table}")
            
            # Fetch the column names from the query result and store them in a list
            columns = [col[0] for col in self.cursor.fetchall()]  # Extract column names (first element of each row)
            
            # Set the column names of the treeview based on the fetched columns
            self.tree["columns"] = columns

            # Set the column headers and properties for each column
            for col in columns:
                self.tree.heading(col, text=col)  # Set the header text for each column
                self.tree.column(col, anchor=tk.W, width=100)  # Set column properties like text alignment and width

            # Execute the SQL query to fetch all rows from the selected table
            self.cursor.execute(f"SELECT * FROM {table}")
            rows = self.cursor.fetchall()  # Fetch all rows of data from the table

            # If no rows are returned, display a message to inform the user
            if not rows:
                messagebox.showinfo(
                    "No Data", "No rows found in the selected table.")

            # Clear any existing rows in the treeview before inserting the new data
            self.tree.delete(*self.tree.get_children())
            
            # Insert the rows into the treeview for display
            for row in rows:
                self.tree.insert("", tk.END, values=row)  # Insert each row into the treeview

        except mysql.connector.Error as err:
            # If any error occurs (e.g., invalid table name or query error), show an error message
            messagebox.showerror("Error", f"Failed to load table: {err}")


    def edit_row(self, event):
        # Get the ID of the selected item in the treeview (the currently selected row)
        selected_item = self.tree.focus()
        
        # If no item is selected, exit the function
        if not selected_item:
            return

        # Retrieve the current values (data) of the selected row
        values = self.tree.item(selected_item, "values")
        
        # Get the list of column IDs (i.e., the column names)
        column_ids = self.tree["columns"]

        # Create a new top-level window for editing the selected row
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Row")  # Set the title of the edit window

        # Dictionary to store the Entry widgets for each column
        entries = {}

        # Create an entry field for each column in the table to allow editing
        for i, col in enumerate(column_ids):
            # Create a label for each column
            tk.Label(edit_window, text=col).grid(row=i, column=0, padx=5, pady=5)
            
            # Create an Entry widget for editing the corresponding value
            entry = tk.Entry(edit_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            
            # Insert the current value of the selected row into the entry widget
            entry.insert(0, values[i])

            # Store the entry widget in the `entries` dictionary, using the column name as the key
            entries[col] = entry


        def save_changes():
            # Collect the updated values from the Entry widgets and store them in a dictionary
            updated_values = {col: entries[col].get() for col in column_ids}
            
            # Create a list of placeholders for the SQL query, one for each column
            placeholders = ", ".join(f"{col}=%s" for col in column_ids)
            
            # Build the UPDATE SQL query string to update the selected row in the table
            query = f"UPDATE {self.table_dropdown.get()} SET {placeholders} WHERE {column_ids[0]}=%s"
            
            try:
                # Execute the query with the updated values and the original primary key (ID)
                self.cursor.execute(query, list(updated_values.values()) + [values[0]])

                # Commit the transaction to save the changes to the database
                self.conn.commit()

                # Reload the table to reflect the updated data
                self.load_table()

                # Close the edit window
                edit_window.destroy()

                # Display a success message
                messagebox.showinfo("Success", "Row updated successfully.")
            
            except mysql.connector.Error as err:
                # Catch any MySQL errors and display an error message
                messagebox.showerror("Error", f"Failed to update row: {err}")

        # Create and place a "Save" button in the edit window that calls save_changes when clicked
        save_button = tk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=len(column_ids), column=1, pady=10)


    def add_row(self):
        # Get the name of the selected table from the dropdown
        table = self.table_dropdown.get()
        
        # If no table is selected, show an error message and exit the function
        if not table:
            messagebox.showerror("Error", "No table selected.")
            return

        # Get the column names from the Treeview widget (representing the table structure)
        columns = self.tree["columns"]

        # Create a new top-level window for adding a new row
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Row")  # Set the title of the new window

        # Dictionary to store the Entry widgets for each column
        entries = {}

        # Create an entry field for each column in the table to allow the user to input values
        for i, col in enumerate(columns):
            # Create a label for each column
            tk.Label(add_window, text=col).grid(row=i, column=0, padx=5, pady=5)
            
            # Create an Entry widget for entering data for the current column
            entry = tk.Entry(add_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            
            # Store the Entry widget in the `entries` dictionary, using the column name as the key
            entries[col] = entry

        # Function to save the new row data to the database
        def save_new_row():
            # Collect the values entered by the user from the Entry widgets
            values = [entries[col].get() for col in columns]
            
            # Create placeholders for the SQL query (e.g., "%s, %s, %s")
            placeholders = ", ".join(["%s"] * len(columns))
            
            # Build the SQL INSERT query to add the new row into the selected table
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
            
            try:
                # Execute the INSERT query with the collected values
                self.cursor.execute(query, values)
                
                # Commit the transaction to save the new row to the database
                self.conn.commit()

                # Reload the table to show the newly added row
                self.load_table()

                # Close the add new row window
                add_window.destroy()

                # Show a success message
                messagebox.showinfo("Success", "Row added successfully.")
            
            except mysql.connector.Error as err:
                # If any MySQL error occurs, display an error message
                messagebox.showerror("Error", f"Failed to add row: {err}")

        # Create and place a "Save" button in the add window that calls `save_new_row` when clicked
        save_button = tk.Button(add_window, text="Save", command=save_new_row)
        save_button.grid(row=len(columns), column=1, pady=10)



    def delete_row(self):
        # Get the currently selected row in the Treeview widget
        selected_item = self.tree.focus()
        
        # If no row is selected, show a warning message and exit the function
        if not selected_item:
            messagebox.showwarning(
                "Select Row", "Please select a row to delete.")
            return

        # Retrieve the values of the selected row
        values = self.tree.item(selected_item, "values")
        
        # Get the column names from the Treeview widget
        column_ids = self.tree["columns"]
        
        # Assuming the first column is the primary key, get its name and value from the selected row
        primary_key = column_ids[0]
        primary_key_value = values[0]

        # Ask the user for confirmation before proceeding with the deletion
        confirm = messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete the row with {primary_key} = {primary_key_value}?")

        # If the user confirms the deletion, proceed with the deletion process
        if confirm:
            # Get the name of the selected table from the dropdown
            table = self.table_dropdown.get()
            
            try:
                # Prepare the SQL DELETE query using the primary key to identify the row
                query = f"DELETE FROM {table} WHERE {primary_key} = %s"
                
                # Execute the DELETE query with the primary key value as a parameter
                self.cursor.execute(query, (primary_key_value,))
                
                # Commit the transaction to delete the row from the database
                self.conn.commit()

                # Reload the table to reflect the changes (the deleted row will no longer appear)
                self.load_table()

                # Show a success message after the row is deleted
                messagebox.showinfo("Success", "Row deleted successfully.")
            
            except mysql.connector.Error as err:
                # If there is an error in the deletion process, show an error message
                messagebox.showerror("Error", f"Failed to delete row: {err}")


if __name__ == "__main__":
    # Create the main Tkinter window (root window)
    root = tk.Tk()
    
    # Initialize the DBVisualizerApp class with the root window
    app = DBVisualizerApp(root)
    
    # Start the Tkinter event loop to run the application
    root.mainloop()

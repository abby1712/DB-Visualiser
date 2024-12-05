import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


class DBVisualizerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("MySQL DB Visualizer")
        self.root.geometry("800x600")

        self.conn = None
        self.cursor = None

        self.create_widgets()

    def create_widgets(self):
        # Database Connection Frame
        connection_frame = tk.Frame(self.root, padx=10, pady=10)
        connection_frame.pack(fill=tk.X)

        tk.Label(connection_frame, text="Host:").grid(
            row=0, column=0, padx=5, pady=5)
        self.host_entry = tk.Entry(connection_frame)
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="User:").grid(
            row=0, column=2, padx=5, pady=5)
        self.user_entry = tk.Entry(connection_frame)
        self.user_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(
            row=0, column=4, padx=5, pady=5)
        self.password_entry = tk.Entry(connection_frame, show="*")
        self.password_entry.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(connection_frame, text="Database:").grid(
            row=0, column=6, padx=5, pady=5)
        self.database_entry = tk.Entry(connection_frame)
        self.database_entry.grid(row=0, column=7, padx=5, pady=5)

        self.connect_button = tk.Button(
            connection_frame, text="Connect", command=self.connect_db)
        self.connect_button.grid(row=0, column=8, padx=5, pady=5)

        # Table Selection Frame
        table_frame = tk.Frame(self.root, padx=10, pady=10)
        table_frame.pack(fill=tk.X)

        tk.Label(table_frame, text="Table:").grid(
            row=0, column=0, padx=5, pady=5)
        self.table_dropdown = ttk.Combobox(table_frame, state="readonly")
        self.table_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.table_dropdown.bind("<<ComboboxSelected>>", self.load_table)

        # Data Table Frame
        self.tree = ttk.Treeview(self.root, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.tree.bind("<Double-1>", self.edit_row)

        # Button Frame
        button_frame = tk.Frame(self.root, padx=10, pady=10)
        button_frame.pack(fill=tk.X)

        self.add_button = tk.Button(
            button_frame, text="Add Row", command=self.add_row)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(
            button_frame, text="Delete Row", command=self.delete_row)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)


    def connect_db(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host_entry.get(),
                user=self.user_entry.get(),
                password=self.password_entry.get(),
                database=self.database_entry.get()
            )
            self.cursor = self.conn.cursor()
            self.load_tables()
            messagebox.showinfo("Success", "Connected to the database.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to connect: {err}")

    def load_tables(self):
        try:
            self.cursor.execute("SHOW TABLES")
            tables = [row[0] for row in self.cursor.fetchall()]
            if not tables:
                messagebox.showwarning(
                    "No Tables", "No tables found in the database.")
            self.table_dropdown["values"] = tables
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load tables: {err}")

    def load_table(self, event=None):
        table = self.table_dropdown.get()
        try:
            self.cursor.execute(f"DESCRIBE {table}")
            columns = [col[0] for col in self.cursor.fetchall()]
            self.tree["columns"] = columns

            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor=tk.W, width=100)

            self.cursor.execute(f"SELECT * FROM {table}")
            rows = self.cursor.fetchall()

            if not rows:
                messagebox.showinfo(
                    "No Data", "No rows found in the selected table.")

            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", tk.END, values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to load table: {err}")

    def edit_row(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        values = self.tree.item(selected_item, "values")
        column_ids = self.tree["columns"]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Row")

        entries = {}
        for i, col in enumerate(column_ids):
            tk.Label(edit_window, text=col).grid(
                row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(edit_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entry.insert(0, values[i])
            entries[col] = entry

        def save_changes():
            updated_values = {col: entries[col].get() for col in column_ids}
            placeholders = ", ".join(f"{col}=%s" for col in column_ids)
            query = f"UPDATE {self.table_dropdown.get()} SET {placeholders} WHERE {column_ids[0]}=%s"
            try:
                self.cursor.execute(query, list(
                    updated_values.values()) + [values[0]])
                self.conn.commit()
                self.load_table()
                edit_window.destroy()
                messagebox.showinfo("Success", "Row updated successfully.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to update row: {err}")

        save_button = tk.Button(edit_window, text="Save", command=save_changes)
        save_button.grid(row=len(column_ids), column=1, pady=10)

    def add_row(self):
        table = self.table_dropdown.get()
        if not table:
            messagebox.showerror("Error", "No table selected.")
            return

        columns = self.tree["columns"]

        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Row")

        entries = {}
        for i, col in enumerate(columns):
            tk.Label(add_window, text=col).grid(
                row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(add_window)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries[col] = entry

        def save_new_row():
            values = [entries[col].get() for col in columns]
            placeholders = ", ".join(["%s"] * len(columns))
            query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
            try:
                self.cursor.execute(query, values)
                self.conn.commit()
                self.load_table()
                add_window.destroy()
                messagebox.showinfo("Success", "Row added successfully.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to add row: {err}")

        save_button = tk.Button(add_window, text="Save", command=save_new_row)
        save_button.grid(row=len(columns), column=1, pady=10)


    def delete_row(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning(
                "Select Row", "Please select a row to delete.")
            return

        values = self.tree.item(selected_item, "values")
        column_ids = self.tree["columns"]
        primary_key = column_ids[0]
        primary_key_value = values[0]

        confirm = messagebox.askyesno(
            "Confirm Delete", f"Are you sure you want to delete the row with {primary_key} = {primary_key_value}?")

        if confirm:
            table = self.table_dropdown.get()
            try:
                query = f"DELETE FROM {table} WHERE {primary_key} = %s"
                self.cursor.execute(query, (primary_key_value,))
                self.conn.commit()
                self.load_table()
                messagebox.showinfo("Success", "Row deleted successfully.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to delete row: {err}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DBVisualizerApp(root)
    root.mainloop()

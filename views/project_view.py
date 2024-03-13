import tkinter as tk
from tooltip import create_tooltip
from tkinter import ttk


class ProjectView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_button = None
        self.project_name_entry = None
        self.project_name_label = None
        self.data_entry_frame = None
        self.new_project_button = None
        self.ci_type_combo = None
        self.ci_type_values = None
        self.ci_type_var = None
        self.ci_type_label = None
        self.parent = parent

        # Initialize the GUI components
        self.setup_ui()

    def setup_ui(self):
        self.new_project_button = tk.Button(self, text="New Project", command=self.new_project)
        self.new_project_button.grid(row=0, column=0, padx=10, pady=10)

    def new_project(self):
        # Create a data entry frame within the sidebar frame
        self.data_entry_frame = tk.Frame(self.parent.sidebar, bg=self.parent.sidebar_color)
        self.data_entry_frame.place(relx=0, rely=0.2, relwidth=1, relheight=0.2)

        # Create a label for "Project Name"
        self.project_name_label = tk.Label(self.data_entry_frame, text="Project Name:", bg=self.parent.sidebar_color,
                                           fg="white",
                                           font=("", 12, "bold"))
        self.project_name_label.grid(row=0, column=0, padx=10, pady=10)

        # Create an entry widget for entering project name
        self.project_name_entry = tk.Entry(self.data_entry_frame)
        self.project_name_entry.grid(row=0, column=1, padx=10, pady=10)

        # Add tooltip to the project name label
        create_tooltip(self.project_name_label, "Enter the name of your project here")

        # Create a label for "CI Type"
        self.ci_type_label = tk.Label(self.data_entry_frame, text="CI Type:", bg=self.parent.sidebar_color,
                                      fg="white",
                                      font=("", 12, "bold"))
        self.ci_type_label.grid(row=1, column=0, padx=0, pady=10)

        # Create a Combobox for selecting CI Type
        self.ci_type_var = tk.StringVar(self.data_entry_frame)
        self.ci_type_values = ["Power Grids", "Financial Institutions", "Communication Networks",
                               "Water Treatment Plants"]
        self.ci_type_combo = ttk.Combobox(self.data_entry_frame, textvariable=self.ci_type_var,
                                          values=self.ci_type_values)
        self.ci_type_combo.grid(row=1, column=1, padx=10, pady=10)

        # Add tooltip to the CI Type label
        create_tooltip(self.ci_type_label, "Select the type of critical infrastructure")

        # Create a "Create" button
        self.create_button = tk.Button(self.data_entry_frame, text="Create", bg="green", fg="white",
                                       font=("", 12, "bold"), state="disabled",
                                       command=self.create_project)
        self.create_button.grid(row=2, column=0)

        # Validate function for the Entry and Combobox
        self.project_name_entry['validate'] = 'all'
        self.project_name_entry['validatecommand'] = self.validate_create_button
        self.ci_type_combo['validate'] = 'all'
        self.ci_type_combo['validatecommand'] = self.validate_create_button

    def validate_create_button(self):
        # Check if both project name entry and CI type combobox are not empty
        project_name = self.project_name_entry.get()
        ci_type = self.ci_type_var.get()
        if project_name.strip() and ci_type:
            self.create_button['state'] = 'normal'
        else:
            self.create_button['state'] = 'disabled'
        return True

    def create_project(self):
        # Add code here to handle project creation
        pass  # Placeholder

    def load_existing_projects(self):
        # Add code here to load existing projects from file
        pass  # Placeholder

    def update_project_tree(self):
        # Add code here to update the project treeview with loaded projects
        pass  # Placeholder

    def show_loaded_projects(self):
        # Add code here to show loaded projects
        pass  # Placeholder

    def hide_loaded_projects(self):
        # Add code here to hide loaded projects
        pass  # Placeholder

    def on_project_selected(self, event):
        # Add code here to handle selection of a project
        pass  # Placeholder

    def proceed_to_analysis(self):
        # Add code here to proceed to project analysis
        pass  # Placeholder

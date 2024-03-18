import tkinter as tk
from tooltip import create_tooltip
from tkinter import ttk
from controllers.project_controller import ProjectController


class ProjectView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.method_var = None
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
        self.create_analysis_method_radio_buttons(self)

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
                                          values=self.ci_type_values, state="readonly")
        self.ci_type_combo.grid(row=1, column=1, padx=10, pady=10)

        # Add tooltip to the CI Type label
        create_tooltip(self.ci_type_label, "Select the type of critical infrastructure")

        # Create a "Create" button
        self.create_button = tk.Button(self.data_entry_frame, text="Create", bg="#325dba", fg="white",
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
        # Get the user-entered data
        project_name = self.project_name_entry.get()
        ci_type = self.ci_type_var.get()

        # Create an instance of ProjectController
        project_controller = ProjectController()

        # Create the new project using the project controller
        new_project = project_controller.create_project(project_name, ci_type)

        if new_project:
            # Update entry widget with project name and set combo box value
            self.project_name_entry.delete(0, tk.END)
            self.project_name_entry.insert(0, project_name)
            self.ci_type_var.set(ci_type)

            # Hide create button
            self.create_button.grid_forget()

            # Clear the project name and critical infrastructure type entries
            self.project_name_entry.delete(0, tk.END)
            self.ci_type_var.set(self.ci_type_values[0])

            # Display another view showing the project details
            self.show_project_details(new_project)

    def show_project_details(self, project):
        # Clear existing widgets
        self.data_entry_frame.destroy()

        # Create a new frame for displaying project details
        details_frame = tk.Frame(self.parent.sidebar, bg=self.parent.sidebar_color)
        details_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Display project details
        project_name_label = tk.Label(details_frame, text=f"Project Name:", bg=self.parent.sidebar_color,
                                      fg="white", font=("", 12, "bold"))
        project_name_label.grid(row=0, column=0, sticky="w", padx=10, pady=(20, 5))

        project_name_value = tk.Label(details_frame, text=project.project_name, bg=self.parent.sidebar_color,
                                      fg="white", font=("", 12))
        project_name_value.grid(row=0, column=1, sticky="w", padx=(0, 10), pady=(20, 5))

        ci_type_label = tk.Label(details_frame, text=f"CI Type:", bg=self.parent.sidebar_color,
                                 fg="white", font=("", 12, "bold"))
        ci_type_label.grid(row=1, column=0, sticky="w", padx=10, pady=(5, 20))

        ci_type_value = tk.Label(details_frame, text=project.ci_type, bg=self.parent.sidebar_color,
                                 fg="white", font=("", 12))
        ci_type_value.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(5, 20))

        # Add section divider after CI Type details
        ci_type_divider = ttk.Separator(details_frame, orient="horizontal")
        ci_type_divider.grid(row=2, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

        # Add section header
        section_header = tk.Label(details_frame, text="Select Analysis Method", bg=self.parent.sidebar_color,
                                  fg="white", font=("", 13, "bold"))
        section_header.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

        # Create radio buttons for selecting analysis method
        self.create_analysis_method_radio_buttons(details_frame)

    def create_analysis_method_radio_buttons(self, parent):
        analysis_methods = ["Monte Carlo Simulation", "Other Analysis Method"]  # Add more as needed
        self.method_var = tk.StringVar(value=analysis_methods[0])  # Select the first method by default

        for i, method in enumerate(analysis_methods):
            radio_button = tk.Radiobutton(parent, text=method, variable=self.method_var,
                                          value=method, bg="white", font=("", 12),
                                          command=self.analysis_method_selected)
            radio_button.grid(row=4 + i, column=0, columnspan=2, sticky="w", padx=(20, 10), pady=(5, 5))

    def analysis_method_selected(self):
        selected_method = self.method_var.get()
        print("Selected Analysis Method:", selected_method)

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

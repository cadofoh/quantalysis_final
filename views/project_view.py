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
        self.data_entry_frame = None
        self.create_analysis_method_radio_buttons(self)

    def new_project(self):
        self.create_data_entry_frame()

    def create_data_entry_frame(self):
        # Create a data entry frame within the sidebar frame
        self.data_entry_frame = tk.Frame(self.parent.sidebar, bg=self.parent.sidebar_color)
        self.data_entry_frame.place(relx=0, rely=0.15, relwidth=1, relheight=0.2)

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
        project_name_value.grid(row=0, column=0, sticky="w", padx=120, pady=(20, 5))

        ci_type_label = tk.Label(details_frame, text=f"CI Type:", bg=self.parent.sidebar_color,
                                 fg="white", font=("", 12, "bold"))
        ci_type_label.grid(row=1, column=0, sticky="w", padx=10, pady=(5, 20))

        ci_type_value = tk.Label(details_frame, text=project.ci_type, bg=self.parent.sidebar_color,
                                 fg="white", font=("", 12))
        ci_type_value.grid(row=1, column=0, sticky="w", padx=75, pady=(5, 20))

        # Add section divider after CI Type details
        ci_type_divider = ttk.Separator(details_frame, orient="horizontal")
        ci_type_divider.grid(row=2, column=0, columnspan=2, sticky="ew", padx=0, pady=0)

        # Add section header
        section_header = tk.Label(details_frame, text="Select Analysis Method", bg=self.parent.sidebar_color,
                                  fg="white", font=("", 13, "bold"))
        section_header.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=(10, 5))

        # Create radio buttons for selecting analysis method
        self.create_analysis_method_radio_buttons(details_frame)

        # Add section header for Input Parameters
        parameters_header = tk.Label(details_frame, text="Input Parameters", bg=self.parent.sidebar_color,
                                     fg="white", font=("", 13, "bold"))
        parameters_header.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=(20, 5))

        self.generate_parameters(details_frame, project.ci_type)

    def generate_parameters(self, parent, ci_type):
        if ci_type == "Power Grids":
            self.generate_power_grid_parameters(parent)
        elif ci_type == "Financial Institutions":
            self.generate_financial_institutions_parameters(parent)
        elif ci_type == "Communication Networks":
            self.generate_communication_networks_parameters(parent)
        elif ci_type == "Water Treatment Plants":
            self.generate_water_treatment_plants_parameters(parent)

    def generate_financial_institutions_parameters(self, parent):
        pass  # Placeholder

    def generate_communication_networks_parameters(self, parent):
        pass  # Placeholder

    def generate_water_treatment_plants_parameters(self, parent):
        pass  # Placeholder

    def generate_power_grid_parameters(self, parent):
        parameters = ["Failure Rate of Equipment(failures per year)",
                      "Repair Time Distribution(hours,days)",
                      "Load Variability (%)",
                      "Generation Capacity Distribution (MW)", "Weather Severity Index(1-10)",
                      "Human Error Probability(%)",
                      "Investment in Infrastructure (USD,GBP"]

        for i, parameter in enumerate(parameters):
            # Create parameter name label
            param_label = tk.Label(parent, text=parameter + ":", bg=self.parent.sidebar_color,
                                   fg="white", font=("", 12))
            param_label.grid(row=8 + i * 2, column=0, sticky="w", padx=10, pady=(10, 0))

            tooltips = [
                "Enter the frequency of equipment failures per year.",
                "Enter the variability in repair time after an outage, measured in hours or days.",
                "Enter the fluctuations in electricity demand, expressed as a percentage deviation from average load.",
                "Enter the variability in available generation capacity, measured in megawatts (MW).",
                "Enter the intensity of weather conditions impacting the power grid, measured on a scale from 1 to 10.",
                "Enter the likelihood of human errors affecting grid operations, expressed as a percentage.",
                "Enter the amount allocated to grid maintenance and upgrades, measured in currency (e.g., USD, GBP)."
            ]
            create_tooltip(param_label, tooltips[i])

            # Create entry field for parameter value
            entry_var = tk.StringVar()
            entry_field = tk.Entry(parent, textvariable=entry_var, font=("", 11))
            entry_field.grid(row=9 + i * 2, column=0, columnspan=2, sticky="w", padx=(10, 0), pady=(5, 0))

        # Add back button
        back_button = tk.Button(parent, text="Back", bg="#325dba", fg="white",
                                font=("", 12, "bold"), command=self.go_back)
        back_button.grid(row=9 + len(parameters) * 2 + 1, column=0, sticky="w", padx=10, pady=(20, 10))

        # Add "Begin Risk Analysis" button
        begin_analysis_button = tk.Button(parent, text="Begin Risk Analysis", bg="green", fg="white",
                                          font=("", 12, "bold"))
        begin_analysis_button.grid(row=9 + len(parameters) * 2 + 1, column=0, columnspan=2, pady=(20, 10))

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

    def go_back(self):
        # Clear the entire sidebar
        for widget in self.parent.sidebar.winfo_children():
            widget.destroy()

        # Recreate the branding frame
        self.parent.brand_frame = tk.Frame(self.parent.sidebar, bg=self.parent.sidebar_color)
        self.parent.brand_frame.place(relx=0, rely=0, relwidth=1, relheight=0.20)

        # Reconfigure the logo and app name labels
        self.parent.app_logo = tk.PhotoImage(file='images\\logo.png').subsample(9)
        logo = tk.Label(self.parent.brand_frame, image=self.parent.app_logo, bg=self.parent.sidebar_color)
        logo.place(x=5, y=20)

        tool_name = tk.Label(self.parent.brand_frame, text='Quantitative Risk', bg=self.parent.sidebar_color,
                             font=("", 15, "bold"))
        tool_name.place(x=55, y=27, anchor="w")

        tool_name = tk.Label(self.parent.brand_frame, text='Analysis Tool', bg=self.parent.sidebar_color,
                             font=("", 15, "bold"))
        tool_name.place(x=55, y=60, anchor="w")

        # Recreate the new project and load project buttons
        self.parent.project_view.new_project_button = tk.Button(self.parent.brand_frame, text="New Project",
                                                                bg=self.parent.sidebar_color, fg="white",
                                                                font=("", 12, "bold"),
                                                                command=self.new_project)
        self.parent.project_view.new_project_button.place(x=5, y=100, anchor="w")

        self.parent.project_view.load_project_button = tk.Button(self.parent.brand_frame, text="Load Project",
                                                                 bg=self.parent.sidebar_color, fg="white",
                                                                 font=("", 12, "bold"),
                                                                 command=self.load_existing_projects)
        self.parent.project_view.load_project_button.place(x=150, y=100, anchor="w")

        # Recreate the data entry frame
        self.create_data_entry_frame()

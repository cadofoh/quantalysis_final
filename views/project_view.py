import json
import tkinter as tk
from tooltip import create_tooltip
from tkinter import ttk
from controllers.project_controller import ProjectController
import numpy as np
from scipy.stats import poisson, norm, beta, randint


class ProjectView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parameter_entries = None
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
        self.ci_type_values = ["Power Grids", "Financial Institutions", "Telecommunication Networks",
                               "Transportation Systems"]
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
        elif ci_type == "Telecommunication Networks":
            self.generate_telecommunication_networks_parameters(parent)
        elif ci_type == "Transportation Systems":
            self.generate_transportation_systems_parameters(parent)

    def generate_financial_institutions_parameters(self, parent):
        self.parameter_entries = []  # List to store references to Entry widgets
        parameters = ["Liquidity Ratio (0-1)",
                      "Capital Adequacy Ratio (0-1)",
                      "Non-Performing Loans Ration (%)",
                      "Return on Assets (%)",
                      "Compliance Violation Counts",
                      "Cybersecurity Incidents Count",
                      "Operational Efficiency Index"]

        for i, parameter in enumerate(parameters):
            # Create parameter name label
            param_label = tk.Label(parent, text=parameter + ":", bg=self.parent.sidebar_color,
                                   fg="white", font=("", 12))
            param_label.grid(row=8 + i * 2, column=0, sticky="w", padx=10, pady=(10, 0))

            tooltips = [
                "Liquidity ratio measures the ability of a financial institution to meet its short-term obligations. A higher ratio indicates better liquidity and vice versa.",
                "Capital adequacy ratio assesses a financial institution's ability to absorb potential losses and risks. A higher ratio signifies stronger financial stability",
                "Non-performing loans ratio measures the proportion of loans that are in default or are not generating income. A lower ratio suggests healthier loan quality",
                "Return on assets measures the profitability of a financial institution relative to its total assets. A higher percentage reflects efficient asset utilization and profitability",
                "Compliance violations count quantifies the number of regulatory compliance breaches or violations detected within the financial institution. A lower count signifies stronger adherence to regulatory standards",
                "Cybersecurity incidents count measures the number of cybersecurity breaches or incidents encountered by the financial institution. A lower count reflects stronger cybersecurity defenses and resilience",
                "Operational efficiency index evaluates the efficiency and effectiveness of the financial institution's operations and processes. A higher index signifies streamlined operations and resource utilization."
            ]
            create_tooltip(param_label, tooltips[i])

            # Create entry field for parameter value
            entry_var = tk.StringVar()
            entry_field = tk.Entry(parent, textvariable=entry_var, font=("", 11))
            entry_field.grid(row=9 + i * 2, column=0, columnspan=2, sticky="w", padx=(10, 0), pady=(5, 0))

            # Validate the entry field to accept only numeric values
            entry_field.config(validate="key", validatecommand=(entry_field.register(self.validate_numeric), "%P"))

            self.parameter_entries.append(entry_field)

            # Add back button
        back_button = tk.Button(parent, text="Back", bg="#325dba", fg="white",
                                font=("", 12, "bold"), command=self.go_back)
        back_button.grid(row=9 + len(parameters) * 2 + 1, column=0, sticky="w", padx=10, pady=(20, 10))

        # Add "Begin Risk Analysis" button
        begin_analysis_button = tk.Button(parent, text="Begin Risk Analysis", bg="green", fg="white",
                                          font=("", 12, "bold"), command=self.begin_analysis)
        begin_analysis_button.grid(row=9 + len(parameters) * 2 + 1, column=0, columnspan=2, pady=(20, 10))

    def generate_telecommunication_networks_parameters(self, parent):
        self.parameter_entries = []  # List to store references to Entry widgets
        parameters = ["Network Downtime (hours per month)",
                      "Mean Time to Repair (MTTR) (hours)",
                      "Data Loss Rate (%))",
                      "Cybersecurity Incident Frequency (per month)",
                      "Network Performance Degradation Rate (%)",
                      "Service Disruption Frequency (per year)"]

        for i, parameter in enumerate(parameters):
            # Create parameter name label
            param_label = tk.Label(parent, text=parameter + ":", bg=self.parent.sidebar_color,
                                   fg="white", font=("", 12))
            param_label.grid(row=8 + i * 2, column=0, sticky="w", padx=10, pady=(10, 0))

            tooltips = [
                "Total hours of network downtime within a month, including both planned maintenance and unplanned outages.",
                "Average duration required to repair network components and resume normal operations after a failure occurs.",
                "Percentage of data loss or corruption observed during transmission over the network.",
                " Frequency of cybersecurity incidents affecting the network's integrity, confidentiality, or availability.",
                "Rate of decline in network performance over time, indicating the extent of degradation affecting user experience and service quality.",
                "Measure of how often service disruptions or outages occur in the telecommunication network, reflecting its reliability and susceptibility to disruptions."
            ]
            create_tooltip(param_label, tooltips[i])

            # Create entry field for parameter value
            entry_var = tk.StringVar()
            entry_field = tk.Entry(parent, textvariable=entry_var, font=("", 11))
            entry_field.grid(row=9 + i * 2, column=0, columnspan=2, sticky="w", padx=(10, 0), pady=(5, 0))

            # Validate the entry field to accept only numeric values
            entry_field.config(validate="key", validatecommand=(entry_field.register(self.validate_numeric), "%P"))

            self.parameter_entries.append(entry_field)

            # Add back button
        back_button = tk.Button(parent, text="Back", bg="#325dba", fg="white",
                                font=("", 12, "bold"), command=self.go_back)
        back_button.grid(row=9 + len(parameters) * 2 + 1, column=0, sticky="w", padx=10, pady=(20, 10))

        # Add "Begin Risk Analysis" button
        begin_analysis_button = tk.Button(parent, text="Begin Risk Analysis", bg="green", fg="white",
                                          font=("", 12, "bold"), command=self.begin_analysis)
        begin_analysis_button.grid(row=9 + len(parameters) * 2 + 1, column=0, columnspan=2, pady=(20, 10))

    def generate_transportation_systems_parameters(self, parent):
        self.parameter_entries = []  # List to store references to Entry widgets
        parameters = ["Traffic Volume (vehicles per day)",
                      "Infrastructure Age (years)",
                      "Incident Response Time (minutes)",
                      "Weather Sensitivity Index (1-10)",
                      "Road Maintenance Budget (GBP)",
                      "Traffic Accident Rate (accidents per year mile)",
                      ]

        for i, parameter in enumerate(parameters):
            # Create parameter name label
            param_label = tk.Label(parent, text=parameter + ":", bg=self.parent.sidebar_color,
                                   fg="white", font=("", 12))
            param_label.grid(row=8 + i * 2, column=0, sticky="w", padx=10, pady=(10, 0))

            tooltips = [
                "Measure of the intensity of traffic flow on the transportation network. Higher traffic volumes may lead to congestion-related risks and increased likelihood of accidents.",
                "Age of the transportation infrastructure components such as roads, bridges, and tunnels. Older infrastructure may be more susceptible to degradation and require more frequent maintenance or replacement.",
                "Average time taken by emergency response teams to reach accident or incident locations on the transportation network. Faster response times can mitigate the severity of accidents and minimize disruption to traffic flow.",
                "Measure of how sensitive the transportation system is to adverse weather conditions such as snow, rain, fog, or high winds. Higher values indicate greater vulnerability to weather-related disruptions.",
                "Financial allocation for maintaining and repairing roads, bridges, and other infrastructure components within the transportation network. Higher budgets may indicate better infrastructure resilience and lower risks of failures.",
                " Measure of the frequency of traffic accidents occurring along the transportation network. A higher accident rate may indicate higher risks to commuters, potential disruptions to traffic flow, and increased maintenance costs for infrastructure repairs.",
            ]
            create_tooltip(param_label, tooltips[i])

            # Create entry field for parameter value
            entry_var = tk.StringVar()
            entry_field = tk.Entry(parent, textvariable=entry_var, font=("", 11))
            entry_field.grid(row=9 + i * 2, column=0, columnspan=2, sticky="w", padx=(10, 0), pady=(5, 0))

            # Validate the entry field to accept only numeric values
            entry_field.config(validate="key", validatecommand=(entry_field.register(self.validate_numeric), "%P"))

            self.parameter_entries.append(entry_field)

        # Add back button
        back_button = tk.Button(parent, text="Back", bg="#325dba", fg="white",
                                font=("", 12, "bold"), command=self.go_back)
        back_button.grid(row=9 + len(parameters) * 2 + 1, column=0, sticky="w", padx=10, pady=(20, 10))

        # Add "Begin Risk Analysis" button
        begin_analysis_button = tk.Button(parent, text="Begin Risk Analysis", bg="green", fg="white",
                                          font=("", 12, "bold"), command=self.begin_analysis)
        begin_analysis_button.grid(row=9 + len(parameters) * 2 + 1, column=0, columnspan=2, pady=(20, 10))

    def generate_power_grid_parameters(self, parent):
        self.parameter_entries = []  # List to store references to Entry widgets
        parameters = ["Failure Rate of Equipment(failures per year)",
                      "Repair Time Distribution(days)",
                      "Load Variability (%)",
                      "Generation Capacity Distribution (MW)",
                      "Weather Severity Index(1-10)",
                      "Human Error Probability(%)",
                      "Investment in Infrastructure (GBP)"]

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
                "Enter the amount allocated to grid maintenance and upgrades, measured in currency (GBP)."
            ]
            create_tooltip(param_label, tooltips[i])

            # Create entry field for parameter value
            entry_var = tk.StringVar()
            entry_field = tk.Entry(parent, textvariable=entry_var, font=("", 11))
            entry_field.grid(row=9 + i * 2, column=0, columnspan=2, sticky="w", padx=(10, 0), pady=(5, 0))

            # Validate the entry field to accept only numeric values
            entry_field.config(validate="key", validatecommand=(entry_field.register(self.validate_numeric), "%P"))

            self.parameter_entries.append(entry_field)

        # Add back button
        back_button = tk.Button(parent, text="Back", bg="#325dba", fg="white",
                                font=("", 12, "bold"), command=self.go_back)
        back_button.grid(row=9 + len(parameters) * 2 + 1, column=0, sticky="w", padx=10, pady=(20, 10))

        # Add "Begin Risk Analysis" button
        begin_analysis_button = tk.Button(parent, text="Begin Risk Analysis", bg="green", fg="white",
                                          font=("", 12, "bold"), command=self.begin_analysis)
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

    def begin_analysis(self):
        # Check if Monte Carlo simulation is selected
        selected_method = self.method_var.get()
        ci_type = self.ci_type_var.get()
        if selected_method == "Monte Carlo Simulation":
            # Perform Monte Carlo analysis
            self.perform_monte_carlo_analysis(ci_type)
        else:
            # Handle other analysis methods
            pass  # Placeholder for now

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

    def perform_monte_carlo_analysis(self, ci_type):

        # Gather parameter values entered by the user
        parameter_values = self.get_parameter_values()

        # Define distributions for Monte Carlo simulation based on parameter values and CI type
        distributions = self.define_distributions(parameter_values, ci_type)

        # Load parameter weights from configuration file
        parameter_weights = self.load_parameter_weights(ci_type)

        # Generate samples using the defined distributions
        num_samples = 10000  # Adjust as needed
        samples = {}
        for param_name, dist in distributions.items():
            samples[param_name] = dist.rvs(size=num_samples)

        # Calculate risk scores for each parameter
        risk_scores = {}
        for param_name, sample_values in samples.items():
            mean = np.mean(sample_values)
            std_dev = np.std(sample_values)
            parameter_weight = parameter_weights.get(param_name)
            print("Parameter:", param_name)
            print("Parameter Weight:", parameter_weight)
            deviation = np.abs(sample_values - mean) / std_dev
            risk_scores[param_name] = np.mean(deviation) * parameter_weight
            print("Risk Score:", risk_scores[param_name])

        # Calculate overall risk score
        overall_risk_score = sum(risk_scores.values())

        # Classify overall risk level
        if overall_risk_score < 0.3:
            risk_level = "Low"
        elif overall_risk_score < 0.6:
            risk_level = "Medium"
        else:
            risk_level = "High"

        # Display risk analysis results
        print("Risk Analysis Results:")
        print(f"Overall Risk Score: {overall_risk_score}")
        print(f"Risk Level: {risk_level}")

    def get_parameter_values(self):
        parameter_values = [entry.get() for entry in self.parameter_entries]
        return parameter_values

    def load_parameter_weights(self, ci_type):
        config_file = 'config/parameter_weights.json'  # Adjust the path as needed
        with open(config_file, 'r') as f:
            config = json.load(f)
            return config.get(ci_type, {}).get('parameters', {})

    def define_distributions(self, parameter_values, ci_type):
        distributions = {}

        parameter_values = [float(value) for value in parameter_values]

        if ci_type == "Power Grids":
            failure_rate_dist = poisson(mu=parameter_values[0])
            repair_time_dist = norm(loc=parameter_values[1], scale=parameter_values[2])
            load_variability_dist = beta(a=2, b=5)  # Example values for shape parameters
            generation_capacity_dist = norm(loc=parameter_values[3], scale=parameter_values[4])
            weather_severity_dist = randint(low=1, high=11)  # Discrete uniform distribution
            human_error_dist = beta(a=2, b=5)  # Example values for shape parameters
            infrastructure_investment_dist = norm(loc=parameter_values[5], scale=parameter_values[6])

            distributions["Failure Rate of Equipment"] = failure_rate_dist
            distributions["Repair Time Distribution"] = repair_time_dist
            distributions["Load Variability"] = load_variability_dist
            distributions["Generation Capacity Distribution"] = generation_capacity_dist
            distributions["Weather Severity Index"] = weather_severity_dist
            distributions["Human Error Probability"] = human_error_dist
            distributions["Investment in Infrastructure"] = infrastructure_investment_dist

        # Add conditions for other CI types here

        return distributions

    def validate_numeric(self, value):
        # Check if the value is empty or numeric
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

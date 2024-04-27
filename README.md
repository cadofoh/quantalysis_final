# Quantitative Risk Analysis Tool
## Introduction
The Quantitative Risk Analysis Tool is a Python-based application designed to perform risk assessments on various critical infrastructure systems. The tool utilizes Monte Carlo simulations and other analysis methods to evaluate the risk levels of power grids, financial institutions, telecommunication networks, and transportation systems.

## Prerequisites

* Python 3.7 or higher
* Tkinter library (comes bundled with Python)
* NumPy library
* SciPy library

### Running the Project

1. Clone the Repository: Clone the repository to a local directory using Git:

```
git clone https://github.com/your-username/quantitative-risk-analysis-tool.git
```
2. Install Required Libraries: Install the required libraries using pip:

```
pip install numpy scipy
```
3. Run the Application: Run the main.py file to start the application:

```
python app.py
```

### Troubleshooting

If you encounter any issues while running the application, please check the following:

* Ensure that you have Python 3.7 or higher installed on your system.
* Verify that you have installed the required libraries (NumPy and SciPy) using pip.
* Check the code for any syntax errors or typos.
**Note**: This project uses Tkinter for the user interface, which comes bundled with Python. If you encounter any issues with the user interface, please refer to the Tkinter documentation for troubleshooting.

4. Use the Application: Once the application is running, you can create a new project, enter parameter values, and run the analysis by following the instructions provided in the user interface.

## Project Structure
The project consists of the following main components:

1. **Project View**: The main user interface for creating and managing projects, selecting analysis methods, and inputting parameter values.
2. **Project Controller**: The backend logic for creating, loading, and saving projects.
3. **Analysis Methods**: The modules for performing risk analysis, such as Monte Carlo simulations and other methods.
4. **Distributions**: The modules for defining probability distributions used in the analysis methods.
5. **Parameter Weights**: The configuration files for storing parameter weights used in the risk analysis.


## User Interface
The user interface is built using the Tkinter library and consists of the following main components:

1. **Branding Frame**: Displays the application logo and name.
2. **New Project Button**: Creates a new project.
3. **Load Project Button**: Loads an existing project.
4. **Data Entry Frame**: Contains the input fields for entering parameter values.
5. **Analysis Method Frame**: Contains the dropdown menu for selecting the analysis method.
6. **Run Analysis Button**: Runs the selected analysis method with the entered parameter values.
7. **Results Frame**: Displays the results of the analysis.


## Project Creation
To create a new project, follow these steps:

1. Click the "New Project" button.
2. Enter a name for the project.
3. Select the analysis method to be used.
4. Enter the parameter values in the input fields.
5. Click the "Run Analysis" button.

## Project Loading
To load an existing project, follow these steps:

Click the "Load Project" button.
Select the project file to be loaded.
The project will be loaded and the input fields will be populated with the saved parameter values.
Click the "Run Analysis" button to run the analysis.


## Parameter Weights
The parameter weights are stored in configuration files and are used to determine the relative importance of each parameter in the risk analysis. The weights can be adjusted to reflect the specific needs of the analysis.

## Conclusion
The Quantitative Risk Analysis Tool is a powerful and flexible application for performing risk assessments on various critical infrastructure systems. The tool utilizes Monte Carlo simulations and other analysis methods to evaluate the risk levels of power grids, financial institutions, telecommunication networks, and transportation systems. The user interface is intuitive and easy to use, making it accessible to users with varying levels of expertise. The project structure is modular and extensible, allowing for easy integration of new analysis methods and data sources. The tool is a valuable resource for organizations seeking to manage and mitigate risks in their critical infrastructure systems.
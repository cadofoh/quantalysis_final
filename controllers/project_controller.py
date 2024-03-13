# controllers/project_controller.py

import json
from datetime import datetime
from tkinter import filedialog

from models.project_model import Project


class ProjectController:
    def __init__(self, app, project_view):
        self.projects = []
        self.selected_project = None
        self.selected_parameters = {}  # Dictionary to store selected parameters

    def create_project(self, project_name=None, ci_type=None):
        try:
            if project_name is None or ci_type is None:
                # If project_name and ci_type are not provided, it means we need to get them from user input
                return None

            date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            project = Project(project_name, ci_type, date_created)
            self.projects.append(project)
            return project
        except Exception as e:
            print(f"Error creating project: {e}")
            return None

    def get_project_by_name(self, project_name):
        for project in self.projects:
            if project.project_name == project_name:
                return project
        return None

    # def save_projects_to_json(self):
    #     if not self.projects:
    #         print("No projects to save.")
    #         return
    #
    #     file_path = filedialog.asksaveasfilename(
    #         title="Save Projects",
    #         defaultextension=".json",
    #         filetypes=[("JSON files", "*.json")],
    #         initialdir="/",  # Set the initial directory if needed
    #     )
    #
    #     if file_path:
    #         with open(file_path, 'w') as file:
    #             json.dump([project.__dict__ for project in self.projects], file, default=str)
    #             print("Projects saved to file.")

    def load_projects_from_json(self, filename='projects.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.projects = [Project(**project_data) for project_data in data]
        except FileNotFoundError:
            # Handle the case where the file doesn't exist yet
            pass

    def project_exists(self):
        return bool(self.projects)

    def get_projects(self):
        return self.projects

    def set_selected_project(self, project):
        self.selected_project = project

    def set_selected_parameters(self, parameters):
        self.selected_parameters = parameters

    def analyze_selected_project(self):
        # Implement analysis based on the selected project and parameters
        print(f"Analyzing project {self.selected_project.project_name} with parameters {self.selected_parameters}")

# models/project_model.py

class Project:
    def __init__(self, project_name, ci_type, date_created):
        self.project_name = project_name
        self.ci_type = ci_type
        self.date_created = date_created

    def to_dict(self):
        return {
            'project_name': self.project_name,
            'ci_type': self.ci_type,
            'date_created': self.date_created
        }

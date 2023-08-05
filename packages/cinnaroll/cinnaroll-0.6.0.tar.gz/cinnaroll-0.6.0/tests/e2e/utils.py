import os


def get_project_id() -> str:
    if 'PROJECT_ID' in os.environ:
        project_id = os.environ['PROJECT_ID']
    else:
        project_id = "8bc51bf4-77ae-4060-b3dc-bb88b06b8f08"
    return project_id

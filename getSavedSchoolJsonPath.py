import os


def getSavedSchoolJsonPath():
    base_path = os.path.dirname(os.path.abspath(__file__))
    path = base_path.replace('\\', '/') + '/' + 'savedschools.json'
    return path

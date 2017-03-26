import os


def ensure_dir_exists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def get_dir(directory):
    """
    Return a string which contains the complete path to the input directory

    Current directory structure:
    PATinderBot
        src
        img
            like
            match
            nope
        json
        data

    :param directory: string of the directory to search for
    :return: string with the complete path to the searched for directory
    """
    current_dir = os.path.dirname(__file__)
    project_dir = os.path.join(current_dir, '..')
    result = os.path.join(project_dir, directory)
    ensure_dir_exists(result)
    return result

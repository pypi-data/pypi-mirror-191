def get_uniform_path(path, name):
    """Constructs a valid uniform path to a test case from its name and the suite's path"""
    return "/".join(path + [name])
from os import mkdir, path



def trim_ext(file_name):
    """
    Trim the file extension from a given file

    """
    return file_name[:file_name.rindex('.')]

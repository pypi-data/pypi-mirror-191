import os


def dir_size(path):
    """Get size in bytes

    Returns:
        int: size in bytes
    """

    total_size = 0
    for dirpath, dirs, files in os.walk(path, topdown=False):
        for i in files:
            f = os.path.join(dirpath, i)
            total_size += os.path.getsize(f)
    return total_size

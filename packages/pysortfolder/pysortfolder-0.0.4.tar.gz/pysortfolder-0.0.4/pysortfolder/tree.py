import os

SPACE = '    '
BRANCH = '│   '
TEE = '├── '
LAST = '└── '


class PySortFolder:
    def __init__(self, path):
        self.path = path
        self._tree = None

    def make_tree(self, reverse=False):
        """Sort folders and files by size in tree like dict

        # folder = {
        #     'name':,
        #     'path':,
        #     'size':,
        #     'childrens':
        # }

        # files = {
        #     'name':,
        #     'path':,
        #     'size':,
        #     'childrens':
        # }

        Args:
            reverse (bool, optional):
                Descend if True, ascend if false. Defaults to False.

        Returns:
            dict: Folder tree in dict
        """
        dirpaths_buffer = {}
        for dirpath, dirs, files in os.walk(self.path, topdown=False):
            folder_node = {
                'name': os.path.basename(dirpath),
                'path': dirpath,
                'size': 0,
                'childrens': [dirpaths_buffer[os.path.join(dirpath, dir)]
                              for dir in dirs]
            }

            # ?: delete the key in dirpaths_buffer dict after pick?

            folder_node['childrens'].sort(
                key=lambda x: x['size'], reverse=reverse
            )

            file_node = []
            for file_name in files:
                file_path = os.path.join(dirpath, file_name)

                file_node.append({
                    'name': file_name,
                    'path': file_path,
                    'size': os.path.getsize(file_path),
                })

            file_node.sort(
                key=lambda x: x['size'], reverse=reverse
            )

            folder_node['childrens'].extend(file_node)
            folder_node['size'] = sum(i['size']
                                      for i in folder_node['childrens'])

            dirpaths_buffer[dirpath] = folder_node
        self._tree = folder_node

    def print_tree(self, prefix='', level=100, only_directories=False,
                   print_current=True):
        for line in print_tree(self._tree, prefix=prefix, level=level,
                               only_directories=only_directories,
                               print_current=print_current):
            print(line)

    @property
    def tree(self):
        return self._tree


def print_tree(tree_dict, prefix='', level=999, only_directories=False,
               print_current=True):
    """
    Prints a tree-like structure of the given tree_dict.
    The tree_dict should be a dictionary with the following format:
    {
        'name': 'root',
        'size': 0,
        'childrens': [
            {
                'name': 'child1',
                'size': 1,
                'childrens': [...]
            },
            {...}
        ]
    }

    Args:
        tree_dict (dict):
            A dictionary representing the tree structure.
        prefix (str, optional):
            String to be added as a prefix for each line of the tree.
            Defaults to ''.
        level (int, optional):
            The level of the tree to be printed.
            Defaults to 999 (all levels).
        only_directories (bool, optional):
            If set to True, only the directories will be printed.
            Defaults to False.
        print_current (bool, optional):
            If set to True, the current level of the tree will be printed.
            Defaults to True.

    Yields:
        str: A string with the tree structure.

    Examples:
        ```python
        tree_dict = {
            'name': 'root',
            'size': 0,
            'childrens': [
                {'name': 'child1', 'size': 1, 'childrens': []},
                {'name': 'child2', 'size': 2, 'childrens': [
                    {'name': 'subchild1', 'size': 3, 'childrens': []},
                    {'name': 'subchild2', 'size': 4, 'childrens': []}
                ]}
            ]
        }
        for line in print_tree(tree_dict):
            print(line)
        ```

    Reference: https://stackoverflow.com/a/59109706/11671779
    """
    if print_current:
        print(tree_dict['name'] + f", size: {tree_dict['size']}")
    try:
        if only_directories:
            childs = [i for i in tree_dict['childrens'] if 'childrens' in i]
        else:
            childs = tree_dict['childrens']
        pointers = [TEE] * (len(childs) - 1) + [LAST]
        for i, (pointer, child) in enumerate(zip(pointers, childs)):
            if 'childrens' in child:
                if level > 0:
                    yield (prefix
                           + pointer
                           + child['name']
                           + f", size: {child['size']}"
                           )
                if level > 1:
                    if pointer == TEE:
                        extension = BRANCH
                    else:
                        extension = SPACE
                    yield from print_tree(child, prefix=prefix + extension,
                                          level=level - 1,
                                          only_directories=only_directories,
                                          print_current=False)
            elif not only_directories:
                yield (prefix
                       + pointer
                       + child['name']
                       + f", size: {child['size']}"
                       )
    except KeyError:
        pass

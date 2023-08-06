# pysortfolder

Sort folders and files by size and display it in folder tree format.

## Usage

```python
from pysortfolder import PySortFolder

PySortFolder(path='PATH/TO/ROOT/FOLDER')
sf.make_tree(reverse=False)  # support reverse=True
sf.print_tree()

# data, size: 82
# ├── subfolder3, size: 0
# │   └── subsubfolder2, size: 0
# │       └── subsubsubfolder1, size: 0
# │           ├── subsubsubsubfolder1, size: 0
# │           └── subsubsubfolder1_text1.txt, size: 0
# ├── subfolder2, size: 17
# │   └── subfolder2_text1.txt, size: 17
# ├── subfolder1, size: 54
# │   ├── subsubfolder1, size: 20
# │   │   └── subsubfolder1_text1.txt, size: 20
# │   ├── subfolder1_text1.txt, size: 17
# │   └── subfolder1_text2.txt, size: 17
# └── root_text1.txt, size: 11
```

```python
from pysortfolder import dir_size

print(dir_size(path='PATH/TO/ROOT/FOLDER')) # print the size of the root

# 82
```

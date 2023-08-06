# hckmtrx-tools
## installation
`pip install hckmtrx-tools`

## how to use
get current directory of python file
```python
import hckmtrx_tools

# initialize FileSystem
fileSystem = hckmtrx_tools.FileSystem(__file__)

# get files directory with GetDirectory() function
reader = open(fileSystem.GetDirectory() + "data.txt")
```
```
C:
|
|___folder1
|   |   folder1_main.py
|   |   folder1_data.txt
|   |
|   |___folder2
|       |   folder2_main.py
|       |   folder2_data.txt

D:
|
|___folder3
|   |   folder3_main.py
|   |   folder3_data.txt
```
### function return in:
- folder1_main.py -> `C:\folder1\`
- folder2_main.py -> `C:\folder1\folder2\`
- folder3_main.py -> `D:\folder3\`
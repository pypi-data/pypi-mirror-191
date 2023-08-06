import sys as sys
import pathlib as pathlib
import inspect as inspect

def get_path(object, path, resource_path="resources") -> pathlib.Path:
    """
    ```python
    import resources
    import you_module

    path = resources.get_resource_path(you_module, 'icon.png')
    print(path) # ...\you_module_path\\resources\icon.png
    
    o = lambda: None
    path = resources.get_resource_path(o, 'icon.png')
    print(path) # ...\current_path\\resources\icon.png

    # Path -> str
    path_s = str(path)
    ```
    """
    return pathlib.Path(inspect.getfile(object)).parent.joinpath(resource_path).joinpath(path).absolute()
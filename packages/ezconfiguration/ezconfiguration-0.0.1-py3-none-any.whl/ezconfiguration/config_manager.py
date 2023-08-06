# modules for read and write configurations used in development stage
import json ## test push cmd
from typing import Protocol, Dict, List, Optional, Union, Tuple, NewType, Any
import os
from pathlib import Path
import inspect

def get_config_path() -> str:
    """generate a configuration path
    
    Examples
    --------
    >>> os.path.abspath(__file__) # return '/<your working directory>/<your current script or module>'
    '/work_dir/package/package_utils'
    
    >>> os.path.dirname(os.path.abspath(__file__)).split("/")
    ['work_dir', 'package', 'package_utils']
    
    >>> os.path.dirname(os.path.abspath(__file__)).split("/")[:-1]
    ['work_dir', 'package']
    
    >>> "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-1])
    '/work_dir/package'
    
    Returns
    -------
    str
        a path for configuration directory
    """
    PACKAGE_PATH = "/".join(os.path.dirname(os.path.abspath(__file__)).split("/")[:-1])
    CONFIGURATION_PATH = os.path.join(PACKAGE_PATH, "configuration")
    return CONFIGURATION_PATH

def get_module_location(module) -> str:
    """pass a python module and get its location
    
    Examples
    --------
    >>> get_module_location(pandas)
    '/<base_path>/anaconda3/envs/python3/lib/python3.10/site-packages/pandas'
    
    Returns
    -------
    str
        a module path
    """
    if inspect.ismodule(module):
        return os.path.dirname(os.path.abspath(module.__file__))
    else:
        raise ValueError(f"input must be a module object. Not a {type(module)}")

class EzConfig:
    """Use this class to manipulate <your config>.json.
    
    Examples
    --------
    >>> cm = ConfigManager(directory='work_dir', filename='config.json')
    >>> cm.write_config_file(config_dict={'a':1, 'b':[1,2,3]})
    >>> cm.read_config_file()
    {'a':1, 'b':[1,2,3]}
    
    >>> cm.insert_config(config_dict={'c':2}) # if a key exists, set replace=True
    >>> cm.read_config_file()
    {'a':1, 'b':[1,2,3], 'c':2}
    
    >>> cm.update_config(key='c', value=[2,3,4], replace=True)
    >>> cm.read_config_file()
    {'a':1, 'b':[1,2,3], 'c':[2,3,4]}    
    
    >>> cm.delete_config(key='c') # then input 'delete config'
    {'a':1, 'b':[1,2,3]}
    
    
    Attributes
    ----------
    directory : str
        a configuration directory
    filename : str
        a configuration file
    
    """
    def __init__(self, directory:str, filename:str):
        self.directory = directory
        self.filename = filename
        self.path = os.path.join(directory, filename)
        self.is_file_exist = os.path.exists(self.path)
    
    def set_new_path(self, directory:str=None, filename:str=None) -> None:
        self.directory = self.directory if directory==None else directory
        self.filename = self.filename if filename==None else filename
        self.path = os.path.join(self.directory, self.filename)
        self.is_file_exist = os.path.exists(self.path)
    
    def write_config_file(self, config_dict:dict, replace=False) -> str:
        """write a package configuration
        Parameters
        ----------
        config_dict : dict
            configuration in a dictionary format
        filename : str
            a filename in json format
        replace : bool
            if the file already exists, set replace=True to replace it
        Returns
        -------
        str
            The path saved
        """
        if self.is_file_exist:
            if replace==True:
                with open(self.path, "w") as f:
                    f.write(json.dumps(config_dict, ensure_ascii=False))
                print(f"saved successfully")
            else:
                raise Exception(f"{self.path} already exists. If replacing the file is needed, try replace=True")

        else:
            Path(self.directory).mkdir(parents=True, exist_ok=True)
            with open(self.path, "w") as f:
                f.write(json.dumps(config_dict, ensure_ascii=False))
            print(f"saved successfully")
            self.is_file_exist = True
        return self.path
    
    def read_config_file(self) -> dict:
        """read a config and return a dictionary object 
        Returns
        -------
        dict
            a configuration in dictionary format
        """
        if self.is_file_exist == True:
            with open(self.path, 'r') as f:
                json_dict = json.load(f)
            return json_dict
        else:
            raise Exception(f"you must create a configuration file first")
    
    def delete_config_file(self) -> None:
        """delete a configuration file
        
        """        
        if self.is_file_exist == True:
            validation = input(prompt=f"Insert 'permanently delete' if you want to delete {self.filename}")
            if validation == 'permanently delete':
                os.remove(self.path)
                print(f"deleted {self.filename} successfully")
                self.is_file_exist = False
        else:
            raise Exception(f"You must create a configuration file first.")
    
    def insert_config(self, config_dict:dict, replace=False):
        """insert the existing configuration's new element
        Parameters
        ----------
        config_dict : dict
            configuration in a dictionary format
        replace : bool
            if the file already exists, set replace=True to replace it
        Returns
        -------
        str
            The path saved
        """        
        existing_config = self.read_config_file()
        intersect_config = set(existing_config.keys()) & set(config_dict.keys())
        
        if len(intersect_config) == 0 or replace==True:
            updated_config = existing_config | config_dict
            self.write_config_file(config_dict=updated_config, replace=True)
        else:
            raise Exception(f"Your new config already exists {list(intersect_config)} if you want to replace it change 'replace=True'.")
            
    def update_config(self, key:str, value:Any, replace=False):
        """update the existing configuration's element
        
        Notes
        -----
        In the case you want to update the nested configuration, use insert method with the whole nested config instead.
        
        
        Parameters
        ----------
        key : str
            a key string
        value : Any
            a value includes int, str, list, dict
        replace : bool
            if the file already exists, set replace=True to replace it
        Returns
        -------
        str
            The path saved
        """        
        existing_config = self.read_config_file()
        if key not in existing_config or replace==True:
            existing_config[key] = value
            self.write_config_file(config_dict=existing_config, replace=True)    
        else:
            raise Exception(f"Your new config already exists '{key}' if you want to replace it change 'replace=True'.")
    
    def delete_config(self, key:str) -> str:
        """delete the existing configuration's element
        Parameters
        ----------
        key : str
            a key string
            
        Returns
        -------
        str
            delete message
        """        
        existing_config = self.read_config_file()
        if key in existing_config:
            validation = input(prompt=f"Insert 'delete config' if you want to delete {key}")
            if validation == 'delete config':
                existing_config.pop(key)
                self.write_config_file(config_dict=existing_config, replace=True)    
                print(f"deleted '{key}' successfully from {self.filename}")
        else:
            raise Exception(f"Your key '{key}' does not exist.")

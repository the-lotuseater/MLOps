import os
import yaml
from src.datascience import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError

@ensure_annotations
def read_yaml(path: Path)->ConfigBox:
    '''
    Docstring for read_yaml
    
    :param path: Description
    :type path: Path
    :return: Description
    :rtype: Any
    '''
    try:
        with open(path) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f'yaml file: {path} loaded successfully.')
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError('yaml file is empty')
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    for path in path_to_directories:
        os.makedirs(path,exist_ok=True)
        if verbose:
            logger.info(f'Created directory at {path}')

    
@ensure_annotations
def save_json(path: Path, data: dict):
    with open(path,'w') as f:
        json.dump(data,f,indent=4)

    logger.info(f'Saved json at {path}')

@ensure_annotations
def load_json(path:Path)-> ConfigBox:
    with open(path) as f:
        content = json.load(f)
    logger.info(f' Json file loaded successfully from path:{path}')
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    '''
    Docstring for save_bin
    
    :param data: Description
    :type data: Any
    :param path: Description
    :type path: Path
    '''
    joblib.dump(value=data, filename=path)
    logger.info(f'Saved binary file at path {path}')

@ensure_annotations
def load_bin(path: Path):
    '''
    Docstring for save_bin
    
    :param data: Description
    :type data: Any
    :param path: Description
    :type path: Path
    '''
    data= joblib.load(value=path)
    logger.info(f'Successfully loaded data from path {path}')
    return data

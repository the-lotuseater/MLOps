import os
from box.exceptions import BoxValueError
import yaml
from src.text_summarizer.logging import LOGGER
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any

@ensure_annotations
def read_yml(file_path:str) -> ConfigBox:
    try:
        print(f'Reading file at = {file_path}')
        with open(file_path) as f:
            content = yaml.safe_load(f)
            LOGGER.info(f'yaml file at {file_path} loaded successfully')
            return ConfigBox(content)
    except BoxValueError as e:
        raise ValueError('yml file is empty')
    except Exception as e:
        raise e
    
@ensure_annotations
def create_dirs(path_to_dirs:list, verbose=True):
    '''
    
    '''
    for path in path_to_dirs:
        os.makedirs(path,exist_ok=True)
        if verbose:
            LOGGER.info(f'Finished created directories at path: {path_to_dirs}')


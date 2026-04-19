import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name = 'text_summarizer'


def init_project():
    list_of_files=[
        '.github/workflows/.gitkeep',
        f'src/{project_name}/__init__.py',
        f'src/{project_name}/components/__init__.py',
        f'src/{project_name}/utils/__init__.py',
        f'src/{project_name}/utils/common.py',
        f'src/{project_name}/logging/__init__.py',
        f'src/{project_name}/config/__init__.py',
        f'src/{project_name}/config/configuration.py',
        f'src/{project_name}/pipeline/__init__.py',
        f'src/{project_name}/entity/__init__.py',
        f'src/{project_name}/constants/__init__.py',
        'config/config.yml',
        'params.yml',
        'app.py',
        'main.py',
        'Dockerfile',
        'requirements.txt',
        'setup.py',
        'research/research.ipynb'
    ]
    for file in list_of_files:
        file_path = Path(file)
        file_dir,file_name = os.path.split(file_path)
        if file_dir!='':
            os.makedirs(file_dir, exist_ok=True)
            logging.info(f'Creating directory {file_dir} for the file {file_name}')

        if (not os.path.exists(file_path) or os.path.getsize(file_path)==0):
            with open(file_path,'wb'):
                pass
                logging.info(f"Created empty file at filepath: {file_path}")
        else:
            logging.info(f'{file_name} already exists')


if __name__=='__main__':
    init_project()
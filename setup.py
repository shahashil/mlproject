from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path:str) -> List[str]:
    '''
    this function will return the list of requriements
    '''
    HYPHEN_E = "-e ."
    all_requirements = []
    with open(file_path) as f_obj:
        all_requirements = f_obj.readlines()

    all_requirements = [ file.replace("\n","") for file in all_requirements ]

    if HYPHEN_E in all_requirements:
        all_requirements.remove(HYPHEN_E)

    return all_requirements



setup(
    name             = "mlproject",
    version          = "0.0.1",
    author           = "Ashil",
    author_email     = "ashilshah19@gnu.ac.in",
    packages         = find_packages(),
    install_requires = get_requirements("requirements.txt")
)
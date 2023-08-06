import os
from rich.tree import Tree
from rich.text import Text

def init(
    env: str = '',
    project_name: str = '',
    parent_dir: str = '',
):
    from .optipack_project_generator import _ProjectGenerator
    from .optipack_utils import visualize_folder_tree

    assert env, 'Empty environment'
    assert project_name, 'Empty project name'

    # TODO: make project gen to be optional 
    # scenario: user init in-code while running experiments. 
    project_gen = _ProjectGenerator(
        env = env, 
        project_name = project_name, 
        parent_dir = parent_dir
    )
    project_existed = project_gen._generate_folder_structure()
    if not project_existed: 
        project_gen._generate_configs_files()
        project_gen._generate_code_files()
    
    vis_dir = os.path.join(parent_dir, project_name)
    visualize_folder_tree(vis_dir, project_name)

    # 3. generate configuration files: 
    #       - connection files to other tools 
    
    # 4. copy files that does not need generation: 
    #   - hyperparam files
    #   - code files

    # 5. provide tools init
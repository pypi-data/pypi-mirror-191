import typer 

""" 
Optipack can be used in 2 ways: 
    - init via cli: optipack init --env <dev/staging/prod> --project <project_name> 
    - setup in code: 

        import optipack 
        optipack.setup(env, project_name) 
"""

app = typer.Typer(no_args_is_help=True)

@app.command(help = 'Initialize project structure')
def init(
    env: str = '', 
    project_name: str = '', 
    parent_dir: str = '', 
): 
    import optipack
    optipack.init(env = env, project_name = project_name, parent_dir=parent_dir)

@app.command(help='Setup')
def setup(

): 
    ...

@app.command(help= 'View project structure')
def view_project(
    project_name: str = '', 
    parent_dir: str = ''
): 
    import optipack
    optipack.utils.visualize_folder_tree(parent_dir, project_name)
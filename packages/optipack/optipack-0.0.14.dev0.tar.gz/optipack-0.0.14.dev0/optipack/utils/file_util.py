import yaml

def load_yaml(yaml_filepath: str ='') -> dict:
    if not yaml_filepath: 
        raise RuntimeError('Invalid yaml path')

    with open(yaml_filepath, 'r') as f:
        cfg = yaml.full_load(f)
    return cfg

def write_yaml(yaml_filepath: str = '', inp_dict: dict = {}):
    if not yaml_filepath: 
        raise RuntimeError('Invalid yaml path')
    
    with open(yaml_filepath, 'w') as f: 
        yaml.dump(inp_dict, f, default_flow_style=False)

def load_text(txt_path: str = '') -> str: 
    if not txt_path: 
        raise RuntimeError('Invalid text path')

    with open(txt_path, 'r') as f: 
        text = f.read()
    return text

def environment_setup(appstart_file: str ='.config/app_start.yaml') -> bool:

    import os
    reset_after_run = False

    try: 
        import optipack
        optipack_path = optipack.__path__[0]
    except: 
        reset_after_run = True
        optipack_path = './optipack/'
        
    try: 
         # 1. update entire environ dict
        start_file = os.path.join(optipack_path, appstart_file)
        cfg = load_yaml(start_file)['app_start']
        os.environ.update(cfg)

        # 2. manually setup some env
        if not os.environ['OPTIPACK_PATH']: 
            os.environ['OPTIPACK_PATH'] = optipack_path
    except: 
        raise OSError('Cannot setup environment variables')

def environment_reset(appstart_file: str = '.config/app_start.yaml'): 
    
    import os
    
    optipack_path = os.environ['OPTIPACK_PATH']
    start_file = os.path.join(optipack_path, appstart_file)
    cfg = load_yaml(start_file)
    for k in cfg: 
        os.environ[k] = ''
    
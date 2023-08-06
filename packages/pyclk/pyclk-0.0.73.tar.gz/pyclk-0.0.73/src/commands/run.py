import os, yaml
from ..utils.context import Context
from ..utils.utils import check_project

def run():
  config = Context.config
  root_path = Context.root_path
  args = Context.command['args']

  check_project(args)
  activate_script = os.path.join(root_path, "python_modules", "bin", "activate")

  global inner_config
  app_relative_path = os.path.join(root_path, config['services'][args]['path'])
  try:
    with open(os.path.join(app_relative_path, 'reqs.yaml'), 'r') as stream:
      inner_config = yaml.safe_load(stream)
    os.system(
      f"/bin/bash -c \"source {activate_script} && pip -V && cd {app_relative_path}\n{inner_config['scripts']['run']}\""
    )
  except ResourceWarning as e:
    print(e)
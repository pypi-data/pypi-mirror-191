from .context import Context
from .chalk import chalk
import os

def check_project(project_name):  
  if project_name not in Context.config['services']:
    print("Hint: Remember to add your project to pyclk.yaml")
    raise ResourceWarning("Error: Project not found.")


def run_hooks(command_name):
  try:
    total_hooks = len(Context.config['hooks'][command_name])
    print("\n")
    print("Running hooks")
    for c, hook in enumerate(Context.config['hooks'][command_name]):
      chalk.cyan(f"[{c +1}/{total_hooks}]: {hook}")
      print("====================")
      os.system(f"{hook}")
      print("====================\n")
  except:
    # it's okay if there are no hooks
    pass
  print("\n")

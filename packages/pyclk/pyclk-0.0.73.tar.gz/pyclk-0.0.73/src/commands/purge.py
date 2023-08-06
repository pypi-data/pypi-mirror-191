import os
from ..utils.context import Context

def purge():
  r = Context.root_path
  os.system(f"rm -rf {r}/python_modules/*")
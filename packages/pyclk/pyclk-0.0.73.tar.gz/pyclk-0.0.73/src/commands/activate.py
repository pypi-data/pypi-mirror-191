import os,yaml
from ..utils.context import Context
import subprocess

def activate():
  root_path = Context.root_path
  output = subprocess.check_output("pip -V", shell=True).decode('utf-8')
  if not output.__contains__('python_modules'):
    print("Error: You must activate python_modules first")
    print("Hint: ")
    print(" source ./python_modules/bin/activate")
    print("")
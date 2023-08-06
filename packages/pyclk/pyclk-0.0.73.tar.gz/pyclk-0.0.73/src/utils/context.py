class _ServiceContext:
  def __init__(self):
    self.config = {}
    self.root_path = ""
    self.config_file_path = ""
    self.command = {
      'args': [],
      'command': '',
    }
    self.project = {}
    self.args = {}
    self.commands = {}
    self.version = ""

  def get_command(self, cmd):
    return getattr(
      getattr((self.commands), cmd),
    cmd)

Context = _ServiceContext()
class Colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class ColorPrinter:
    @staticmethod
    def red(text):
        print(Colors.RED + text + Colors.END)

    @staticmethod
    def purple(text):
        print(Colors.PURPLE + text + Colors.END)

    @staticmethod
    def cyan(text):
        print(Colors.CYAN + text + Colors.END)

    @staticmethod
    def darkcyan(text):
        print(Colors.DARKCYAN + text + Colors.END)

    @staticmethod
    def blue(text):
        print(Colors.BLUE + text + Colors.END)

    @staticmethod
    def green(text):
        print(Colors.GREEN + text + Colors.END)

chalk = ColorPrinter()
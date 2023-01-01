import sys

class Logger():
    def __init__(self, file_path) -> None:
        self.terminal = sys.stdout
        self.log = open(file_path,"a")
        
    def write(self,message):
        self.terminal.write(message)
        self.log.write(message)
        
    def flush(self):
        pass

        
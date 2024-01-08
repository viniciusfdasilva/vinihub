import os, environ
from vinigit.settings import BASE_DIR
class OSResult():
    
    def __init__(self, exit_code, output):
        
        self.exit_code = exit_code
        self.output    = output        
        
class OS():    
    
    path     = '/tmp/'
    filename = '.os_result'
    
    @staticmethod
    def __readfile() -> str:
        
        output = ''
        
        if not os.path.exists(f'{OS.path}{OS.filename}'):
            os.system(f'touch {OS.path}{OS.filename}')

        file = open(f'{OS.path}{OS.filename}', 'r')
        
        output = file.read()
        output = output[0:len(output)-1]
        
        file.close()
        
        return output
        
    @staticmethod     
    def _system(cmd) -> OSResult:
        
        exit_code = os.system(f"{cmd} > {OS.path}{OS.filename}")
        output    = OS.__readfile()
        return OSResult(exit_code=exit_code, output=output)


class Utils():

    def __init__(self):
        self.env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
        
    def get_domain(self):

        return self.env('DOMAIN')

    def get_user(self):
        return self.env('GIT_USER')
    
    def get_git_path(self):
        return self.env('GIT_PATH')
    
    def get_git_extention(self):
        
        return self.env('REPO_EXTENTION')
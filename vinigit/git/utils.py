import os

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
    
if __name__ == '__main__':
    
    result = OS._system('ping 1.1.1.1')
    
    print(result.exit_code)
    print(result.output)
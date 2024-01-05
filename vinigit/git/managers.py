import os, environ
from vinigit.settings import BASE_DIR
from git.utils import OS
from git.models import Repository, LastInstaWebPath

class GitManager():
    
    def get_branches(rep_name):
        
        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
        
        try:
            os.chdir(f'{env("GIT_PATH")}/{rep_name}.{env("REPO_EXTENTION")}/heads/')
            os_result = OS._system('ls')
        except:
            return []
        
        branches = os_result.output.split('\n')
        return [] if len(branches) == 1 and branches[0] == '' else branches

    def git_push(git_dir, branch):
        
        os.chdir(f'{git_dir}') 
        return True if os.system(f'git push origin {branch}') == 0 else False
        
    def git_clone(rep_name, dst_clone):
        
        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
    
        return os.system(f'git clone {env("GIT_USER")}@{env("DOMAIN")}:{env("GIT_PATH")}/{rep_name}.{env("REPO_EXTENTION")} {dst_clone}{rep_name}')
    
    def git_merge(rep_name, from_branch, to_branch):
        
        GitManager.git_clone(rep_name, '/tmp/')
        
        os.chdir(f'/tmp/{rep_name}')        
        return True if os.system(f'git merge {from_branch} {to_branch}') == 0 else False
        
    def get_git_instaweb(repository_name):
        
        last_instaweb = LastInstaWebPath.objects.all().first()
        
        if last_instaweb:
            
            path = last_instaweb.last_path
            
            if path:
            
                env = environ.Env()
                environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
    
                os.chdir(f'{env("GIT_PATH")}/{path}')
                system_status = os.system(f'git instaweb --port {env("WEB_PORT")} --stop&')
    
            os.chdir(f'{env("GIT_PATH")}/{repository_name}')
    
            chdir_status  = os.chdir(f'{env("GIT_PATH")}/{repository_name}')
            system_status = os.system(f'git instaweb --port {env("WEB_PORT")} --start')
    
            last_path_model = LastInstaWebPath.objects.all().first()
            last_path_model.last_path = repository_name
            last_path_model.save()
    
            if chdir_status == 0 and system_status == 0:
                return True
        else:
            LastInstaWebPath.objects.create().save()
            
        return False

class RepositoryManager():
    
    def remove_dir(dir_path):
        return os.system(f'rm -r {dir_path}')
    
    def remove_repository(id):
        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
        
        rep = Repository.objects.get(pk=id)
        
        try:
           
            path = f'{env("GIT_PATH")}/{rep.nome}.{env("REPO_EXTENTION")}'
            os.system(f'rm -r {path}')
            rep.delete()
        except OSError as e:
            
            rep.delete()

    def new_repository(input_value):
        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

        try:
            if str(input_value).__contains__("ssh-rsa"):

                os.system(f'echo {input_value} >> {env("SSH_PATH")}/{env("SSH_FILE")}')
                return True, True
            else:
    
                directory = f'{env("GIT_PATH")}/{input_value}.{env("REPO_EXTENTION")}'

                os.makedirs(directory, mode=500)
                os.chdir(directory)
                os.system('git init --bare')

                Repository(name=input_value).save()

                return True, False
        except OSError as e:
            return False, False

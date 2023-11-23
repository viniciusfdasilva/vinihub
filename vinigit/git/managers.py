import os, environ
from vinigit.settings import BASE_DIR
from git.models import Repository, LastInstaWebPath

def get_git_instaweb(repository_name):
    
    env = environ.Env()
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

    path = LastInstaWebPath.objects.all().first().last_path

    if path:
        
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
    
    return False

class RepositoryManager():
    
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

                Repository(nome=input_value).save()

                return True, False
        except OSError as e:
            return False, False

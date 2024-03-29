import os, environ
from vinigit.settings import BASE_DIR
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from git.managers import RepositoryManager, GitManager
from git.forms import UserForm, PullRequestForm, ReleaseForm
from git.models import Repository, PullRequest, Release
from git.utils import Utils


class ReleaseDetailView(ListView):
    
    template_name = 'release_detail.html'
    
    def get(self, request, repository, id_release):
        
        repo    = Repository.objects.get(name=repository)
        release = Release.objects.get(id=id_release)

        if repo and release:
            
            context = {
                'name'        : release.release_name,
                'description' : release.description,
                'changelog'   : release.changelog,
                'repository'  : repository
            }
            
            return render(request, self.template_name, context=context)
        
        messages.error(request, 'Repositório ou Release não existe!')
        return render(request, self.template_name, context={})

class PullRequestMergeView(ListView):
    
    template_name = 'pull_request.html'
    
    def get(self, request, repository, id_pullrequest):
        
        pull_request = PullRequest.objects.get(id=id_pullrequest)
        rep          = Repository.objects.get(name=repository)
  
        if pull_request and rep:
            form = PullRequestForm()
            
            rep_name = rep.name

            pull_requests = PullRequest.objects.filter(repository=rep)
            
            context = {
                'pull_requests': pull_requests                    ,
                'branches'     : GitManager.get_branches(rep_name),
                'repository'   : repository                       ,
                'form'         : form                             ,
            }
        
            return render(request, self.template_name, context=context)
        
    def post(self, request, repository, id_pullrequest):
        
        pull_request = PullRequest.objects.get(id=id_pullrequest)
        rep          = Repository.objects.get(name=repository)
        
        if pull_request and rep:
            
            rep_name = rep.name
            
            is_successfully = GitManager.git_push(f'/tmp/{rep_name}', pull_request.to_branch)
            RepositoryManager.remove_dir(f'/tmp/{rep_name}')
            
            pull_request.is_merged = True
            pull_request.save()

            
            pull_requests = PullRequest.objects.filter(repository=rep)
            
            form = PullRequestForm()
            
            if pull_request:
                messages.info(request, 'Pull Request realizado com sucesso!')
            else:
                messages.error(request, 'Erro ao realizar Pull Request!')
                
            context = {
                'pull_requests'        : pull_requests                    ,
                'branches'             : GitManager.get_branches(rep_name),
                'repository'           : repository                       ,
                'form'                 : form                             ,
                'merged_branch'        : True                             ,
                'pull_request_success' : is_successfully
            }
            
            return render(request, self.template_name, context=context)
class PullRequestDetailView(ListView):
    template_name = 'pullrequest_detail.html'

    def get(self, request, repository, id_pullrequest):
          
        rep          = Repository.objects.get(name=repository)
        pull_request = PullRequest.objects.get(id=id_pullrequest)
        
        if rep and pull_request:
            
            context = {
                'title'      : pull_request.title,
                'description': pull_request.description,
                'is_merged'  : pull_request.is_merged,
                'repository' : pull_request.repository.name,
                'to_branch'  : pull_request.to_branch,
                'from_branch': pull_request.from_branch
            }

            return render(request, self.template_name, context=context)
        
        messages.error(request, 'Repositório ou Pull Request não existe!')
        return render(request, self.template_name, context={})

class GitGraphView(ListView):

    def get(self, request, repository):
        
        rep = Repository.objects.get(name=repository)    

        if rep:
            
            commits = GitManager.get_commits(repository)
            return HttpResponse(f'<textarea style="width:100%; height:100%;" readonly>{commits}</textarea>')
        
class ReleaseView(ListView):
    
    template_name = 'release.html'
    
    def get(self, request, repository):
        
        utils = Utils()
        rep = Repository.objects.get(name=repository)
        
        if rep:
            
            form = ReleaseForm()
            releases = Release.objects.filter(repository=rep)

            context = {
                'releases'  : releases                 ,
                'form'      : form                     ,
                'repository': rep.name                 ,
                'domain'    : utils.get_domain()       ,
                'git_user'  : utils.get_user()         ,
                'path'      : utils.get_git_path()     ,
                'extention' : utils.get_git_extention()
            }
                        
            if len(GitManager.get_branches(repository)) > 0:
                return render(request, self.template_name, context=context)
            
            messages.error(request, 'Não foi encontrada nenhuma branch!')
            return render(request, self.template_name, context=context)

    def post(self, request, repository):

        rep = Repository.objects.get(name=repository)

        if rep:
            
            releases = Release.objects.filter(repository=rep)
            form = ReleaseForm()
            
            
            utils = Utils()
            
            context = {
                'releases'  : releases                 ,
                'form'      : form                     ,
                'repository': rep.name                 ,
                'domain'    : utils.get_domain()       ,
                'git_user'  : utils.get_user()         ,
                'path'      : utils.get_git_path()     ,
                'extention' : utils.get_git_extention()
            }

            release_name = request.POST.get('release_name') 
            description  = request.POST.get('description')
            changelog    = request.POST.get('changelog')

            tag_created = GitManager.create_tag(rep.name, release_name)

            if tag_created:
                
                release = Release.objects.create(
                    release_name = release_name ,
                    description  = description  ,
                    changelog    = changelog    ,
                    repository   = rep
                )
           
                if release:
                    messages.info(request,'Versão criada com sucesso!')
                else:
                    messages.error(request, 'Erro ao criar versão!')
                return render(request, self.template_name, context=context)
            
            messages.error(request,'Erro ao criar versão!')
            return render(request, self.template_name, context=context)

class PullRequestView(ListView):
    
    template_name = 'pull_request.html'

    def get(self, request,  repository):
            
        rep = Repository.objects.get(name=repository)
        
        if rep:
        
            rep_name = rep.name
            pull_requests = PullRequest.objects.filter(repository=rep)
            
            form = PullRequestForm()
            
            context = {
                'pull_requests': pull_requests,
                'branches'     : GitManager.get_branches(rep_name),
                'repository'   : repository,
                'form'         : form
            }

            return render(request, self.template_name, context=context)

    def post(self, request, repository):
             
        rep = Repository.objects.get(name=repository)
        
        if rep:
            
            from_branch = request.POST.get('from_branches')
            to_branch   = request.POST.get('to_branches')
            description = request.POST.get('description')
            title       = request.POST.get('title')
            
            form = PullRequestForm()
            
            is_merged_branch = GitManager.git_merge(rep.name, from_branch, to_branch)
            
            if not is_merged_branch:
                RepositoryManager.remove_dir(f'/tmp/{rep.name}')
            
            pull_request = PullRequest.objects.create(
                    from_branch = from_branch     ,
                    to_branch   = to_branch       ,
                    description = description     ,
                    title       = title           ,
                    is_merged   = False           ,
                    repository  = rep             ,        
            )
                            
            pull_requests = PullRequest.objects.filter(repository=rep)
            
            context = {
                'pull_requests' : pull_requests                    ,
                'to_branch'     : to_branch                        ,
                'branches'      : GitManager.get_branches(rep.name),
                'form'          : form                             ,
                'merged_branch' : is_merged_branch                 ,
                'created'       : True if pull_request else False  ,
                'id_pullrequest': pull_request.pk                  ,
                'repository'    : repository                       ,
            }
    
            return render(request, self.template_name, context=context)
    
class LogoutView(ListView):
    template_name = 'auth/login.html'
    model = User

    def get(self, request):

        logout(request=request)
        return redirect('/')
        #return render(request, self.template_name)


class LoginView(ListView):
    template_name = 'auth/login.html'
    model = User
    
    def get(self, request):
        repositorio = Repository.objects.all()

        form = UserForm()
      
        if request.user.is_authenticated:
            #return HttpResponseRedirect(reverse('/git/painel'))
            return render(request, 'painel.html', {'username': request.user.username, "repositorios": repositorio})

        return render(request, self.template_name, {'form': form})


    def post(self, request):

        form = UserForm()
       
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.all().count() > 0:

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect('/painel')

        messages.info(request,'Credenciais incorretas')
        return render(request, self.template_name, {'form': form})


class PainelView(ListView):
    template_name = 'painel.html'

    def get(self, request):

        repositorio = Repository.objects.all()
        context = {'username': request.user.username, "repositorios": repositorio}
       
        return render(request, self.template_name, context)

    def post(self, request):
        name = request.POST.get('id')
        repo = request.POST.get('id_repo')
        repositorio = Repository.objects.all()

        env = environ.Env()
        environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

        if name is None and repo is None:    

            input_value = request.POST.get('value')

            status, is_pupkey = RepositoryManager.new_repository(input_value)

            url = f'{env("GIT_USER")}@{env("DOMAIN")}:{env("GIT_PATH")}/{input_value}.{env("REPO_EXTENTION")}'

            if status and is_pupkey:

                messages.info(request,'Chave pública adicionada com sucesso!')
                return render(request, self.template_name, {'username': request.user.username, "repositorios": repositorio})

            elif status and not is_pupkey:  

                context = {'url': url, 'username': request.user.username, "repositorios": repositorio}

                return render(request, self.template_name, context)

            else:
            
                messages.info(request,'Erro no processo!')
                return render(request, self.template_name, {'username': request.user.username, "repositorios": repositorio})
        
        elif repo is not None and name is None:
        
            RepositoryManager.remove_repository(repo)
            return HttpResponse('Repositório removido com sucesso!')
        else:

            url = f'{env("GIT_USER")}@{env("DOMAIN")}:{env("GIT_PATH")}/{name}.{env("REPO_EXTENTION")}'
            return HttpResponse(url)

def get_repo(request):
    
    repository_name = request.data.get('repository')
    
    repo = Repository.objects.get(name=repository_name)
    
    if repo:
        
        result = GitManager.get_git_instaweb(repository_name)
    else:
        
        repositories = Repository.objects.all()
        
        messages.info(request,'Erro no processo!')
        return render(request, 'painel.html', {'username': request.user.username, "repositorios": repositories})            
# Create your views here.

import os,sys,types,importlib.machinery,shutil
import threading as thread
from pathlib import Path
from huggingface_hub import HfApi
from abc import ABC, abstractmethod
from github import Github
from gitlab import Gitlab
from zipfile import ZipFile
import ruamel.std.zipfile as zipfileextra
# https://pypi.org/project/ruamel.std.zipfile/

def split(a, n):
    """
    https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length

    >>> list(split(range(11), 3))
    [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10]]
    """
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def load_file_as_mod(foil):
    foil_name = str(foil.split('/')[-1]).replace('.py','')

    loader = importlib.machinery.SourceFileLoader(foil_name, os.path.abspath(foil_name))
    module = types.ModuleType(loader.name)
    loader.exec_module(module)
    return module

class mem(object):     
    @abstractmethod
    def url(self):
        pass

    @abstractmethod
    def login(self):
        pass
    
    @abstractmethod
    def logut(self):
        pass

    @abstractmethod
    def files(self):
        pass
    
    @abstractmethod
    def upload(self, path=None,path_in_repo=None):
        pass

    @abstractmethod
    def download(self, file_path=None,download_to=None):
        pass

    @abstractmethod
    def delete_file(self,path_in_repo=None):
        pass
    
    def __enter__(self):
        self.login()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()
        return self
    def __iadd__(self, path):
        self.upload(path)
        return self
    def __getitem__(self,foil):
        return self.download(foil)
    def __setitem__(self,key,value):
        self.upload(value,key)
    def __delitem__(self,item):
        return self.delete_file(item)
    def __str__(self):
        return self.files()
    def __contains__(self, item):
        return item in self.files()
    def __call__(self,item):
        return self.download(item) if item in self else None
    def __len__(self):
        return len(self.files())

    def by(self,ext):
        return [x for x in self.files() if str(x).endswith(ext)]

    def find_all(self,lambda_search):
        return [x for x in self.files() if lambda_search(x)]

    def find(self,lambda_search):
        current = self.find_all(lambda_search,False)
        if len(current) > 1:
            print("There are too many files found")
        elif len(current) == 1:
            return current[0]
        return None

    def impor(self,file):
        if file not in self.files():
            print("FILE IS NOT AVAILABLE")
            return None
        
        import_name = str(file.split('/')[-1]).replace('.py','')
        #https://stackoverflow.com/questions/19009932/import-arbitrary-python-source-file-python-3-3#answer-19011259
        loader = importlib.machinery.SourceFileLoader(import_name, os.path.abspath(self[file]))
        mod = types.ModuleType(loader.name)
        loader.exec_module(mod)

        return mod

    def load_text(self,file):
        if file not in self.files():
            print("FILE IS NOT AVAILABLE")
            return None
        
        cur_path = os.path.abspath(self[file])
        with open(cur_path, 'r') as reader:
            contents = reader.readlines()
        os.remove(cur_path)

        return ''.join(contents)

    def load_json(self,file):
        if file not in self.files():
            print("FILE IS NOT AVAILABLE")
            return None
        
        import json
        
        cur_path = os.path.abspath(self[file])
        with open(cur_path, 'r') as reader:
            contents = json.load(reader)
        os.remove(cur_path)

        return contents

    def load_pkl(self,file):
        if file not in self.files():
            print("FILE IS NOT AVAILABLE")
            return None

        import pandas as pd

        cur_path = os.path.abspath(self[file])
        contents = pd.read_pickle(cur_path)
        os.remove(cur_path)

        return contents

    def load_csv(self,file):
        if file not in self.files():
            print("FILE IS NOT AVAILABLE")
            return None

        import pandas as pd

        cur_path = os.path.abspath(self[file])
        contents = pd.read_csv(cur_path)
        os.remove(cur_path)

        return contents

    def load_sqlite(self,file):
        if file not in self.files():
            print("FILE IS NOT AVAILABLE")
            return None
        
        import xcyl
        
        cur_path = os.path.abspath(self[file])
        contents = xcyl.sqlobj(cur_path)

        return contents

    def load_xcyl(self,file):
        if file not in self.files():
            print("FILE IS NOT AVAILABLE")
            return None
        
        import xcyl
        
        cur_path = os.path.abspath(self[file])
        contents = xcyl.xcylobj(cur_path)

        return contents

    def load_zip(self,file):
        if file not in self.files():
            print("FILE IS NOT AVAILABLE")
            return None

        return zyp(os.path.abspath(self[file]))

    def empty(self,save_files=['README.md','.gitattributes','.gitignore']):
        print('[',end='',flush=True)
        filez = [x for x in self.files() if x not in save_files]
        _range = range(0, len(filez))

        class MyThread(thread.Thread):
            #https://www.tutorialspoint.com/python3/python_multithreading.htm
            def __init__(self,my_range,delete_file_lambda):
                thread.Thread.__init__(self)
                self.my_range = my_range
                self.delete_file_lambda = delete_file_lambda
            def run(self):
                for num in self.my_range:
                    self.delete_file_lambda(num)
                    print('.',end='',flush=True)
                    #delete_msg(self.name,self.bot,self.chat_id,num)

        thread_dyct = []
        ranges = split(_range,self.threads)
        for itr,thread_range in enumerate(ranges):
            thread_dyct += [
                MyThread(thread_range, lambda x:self.delete_file(x))
            ]
        [tred.start() for tred in thread_dyct]
        [tred.join() for tred in thread_dyct]

        """
        for foil in self.files():
            if foil not in save_files:
                self.delete_file(foil)
        """
        print(']')

class face(mem):
    def __init__(self,repo,use_auth=True,repo_type="dataset",clear_cache=False, clear_token=False):
        """
        https://rebrand.ly/hugface

        https://huggingface.co/docs/huggingface_hub/quick-start
        https://huggingface.co/docs/huggingface_hub/how-to-upstream
        https://huggingface.co/docs/huggingface_hub/how-to-downstream
        """
        self.api = HfApi()
        self.repo = repo
        self.repo_type = repo_type
        self.auth = use_auth
        self.downloaded_files = []
        self.opened = False
        self.clear_cache = clear_cache
        self.clear_token = clear_token
        self._pr_ = {}
        self.backup_auth = use_auth
        self.threads = 4

    def get_pull_requests(self, status='open'):
        #https://huggingface.co/docs/huggingface_hub/how-to-discussions-and-pull-requests#retrieve-discussions-and-pull-requests-from-the-hub
        #https://github.com/huggingface/huggingface_hub/blob/v0.9.0/src/huggingface_hub/hf_api.py#L2475
        if not self.opened:
            self.login()

        output = []

        try:
            output = [
                x for x in self.api.get_repo_discussions(repo_id=self.repo,repo_type=self.repo_type,token=self.auth)
                if x.is_pull_request and x.status==status
            ]
        except Exception as e:
            print(e)

        return output
    
    def get_pull_request_info(self, pull_request_num):
        #https://github.com/huggingface/huggingface_hub/blob/v0.9.0/src/huggingface_hub/hf_api.py#L2554
        output = None
        if not self.opened:
            self.login()

        try:
            output = self.api.get_discussion_details(repo_id=self.repo,repo_type=self.repo_type,token=self.auth, discussion_num=pull_request_num)
        except Exception as e:
            print(e)

        return output
    
    def url(self):
        return "https://huggingface.co/datasets/" + str(self.repo)

    @property
    def pr(self):
        if self._pr_ == {}:
            for pr in self.get_pull_requests():
                print(pr)
                self._pr_[pr.num] = pr
        return self._pr_

    def merge_pull_request(self, discussion_id=-1, comment="Auto Merge of the Pull Request"):
        #https://huggingface.co/docs/huggingface_hub/v0.9.0/en/package_reference/hf_api#huggingface_hub.HfApi.merge_pull_request
        #https://github.com/huggingface/huggingface_hub/blob/v0.9.0/src/huggingface_hub/hf_api.py#L3033
        if not self.opened:
            self.login()

        try:
            self.api.merge_pull_request(
                repo_id=self.repo,
                discussion_num=discussion_id,
                comment=comment,
                repo_type=self.repo_type,
                token=self.backup_auth or self.auth
            )
            if discussion_id in self._pr_:
                del self._pr_[discussion_id]
            return True
        except Exception as e:
            print(e)
            return False

    def merge_pull_requests(self, comment="Auto Merge of the Pull Request"):
        #https://huggingface.co/docs/huggingface_hub/v0.9.0/en/package_reference/hf_api#huggingface_hub.HfApi.merge_pull_request
        #https://github.com/huggingface/huggingface_hub/blob/v0.9.0/src/huggingface_hub/hf_api.py#L3033
        """ MULTITHREAD PREP
        threads = 4
        try:
            delete_to = update.message.message_id+1
            delete_from = last_message(delete_to)

            _range = range(delete_from, delete_to)
            print(f"Deleting from {delete_from} to {delete_to}")

            class MyThread(thread.Thread):
                #https://www.tutorialspoint.com/python3/python_multithreading.htm
                def __init__(self,name,bot,chat_id,msg_range):
                    thread.Thread.__init__(self)
                    self.name = name
                    self.bot = bot
                    self.chat_id = chat_id
                    self.msg_range = msg_range
                def run(self):
                    for num in self.msg_range:
                        delete_msg(self.name,self.bot,self.chat_id,num)
            
            thread_dyct = []
            ranges = split(_range,threads)
            print(ranges)
            for itr,thread_range in enumerate(ranges):
                print(f"Range:> {thread_range}")
                thread_dyct += [
                    MyThread(itr, context.bot, update.message.chat_id, thread_range)
                ]
            [tred.start() for tred in thread_dyct]
            [tred.join() for tred in thread_dyct]
        except Exception as e:
            update.message.reply_text(f"failure: {e}")
        """

        if not self.opened:
            self.login()

        try:
            for pr in self.get_pull_requests():
                self.merge_pull_request(
                    discussion_id=pr.num,
                    comment=comment
                )
        except Exception as e:
            print(e)

        return None

    def clearcache(self, force=False, all_sets=False):
        """ MULTITHREAD PREP
        threads = 4
        try:
            delete_to = update.message.message_id+1
            delete_from = last_message(delete_to)

            _range = range(delete_from, delete_to)
            print(f"Deleting from {delete_from} to {delete_to}")

            class MyThread(thread.Thread):
                #https://www.tutorialspoint.com/python3/python_multithreading.htm
                def __init__(self,name,bot,chat_id,msg_range):
                    thread.Thread.__init__(self)
                    self.name = name
                    self.bot = bot
                    self.chat_id = chat_id
                    self.msg_range = msg_range
                def run(self):
                    for num in self.msg_range:
                        delete_msg(self.name,self.bot,self.chat_id,num)
            
            thread_dyct = []
            ranges = split(_range,threads)
            print(ranges)
            for itr,thread_range in enumerate(ranges):
                print(f"Range:> {thread_range}")
                thread_dyct += [
                    MyThread(itr, context.bot, update.message.chat_id, thread_range)
                ]
            [tred.start() for tred in thread_dyct]
            [tred.join() for tred in thread_dyct]
        except Exception as e:
            update.message.reply_text(f"failure: {e}")
        """
        if self.clear_cache or force:
            cache_loc = "/home/"+str(os.getlogin()) + "/.cache/huggingface/hub/"
            user_name, repo_name = self.repo.split('/')

            paths_to_remove = [
                str(cache_loc) + "datasets--{0}--{1}/".format(user_name,repo_name)
            ]

            if all_sets:
                paths_to_remove += [
                    str(cache_loc + x) for x in os.listdir(cache_loc)
                ]

            for y in paths_to_remove:
                try:
                    os.system("yes|rm -r " + str(y))
                except:
                    pass

    def login(self):
        if isinstance(self.auth,str):
            import os

            hugging_face = os.path.join(Path.home(),".huggingface")
            token_path = os.path.join(hugging_face, "token")

            if os.path.exists(token_path) and self.clear_token:
                os.system("rm {0}".format(token_path))

            if not os.path.exists(token_path):
                for cmd in [
                    f"mkdir -p {hugging_face}",
                    f"rm {token_path}",
                    f"touch {token_path}"
                ]:
                    try:
                        os.system(cmd)
                    except:
                        pass

                with open(token_path,"a") as writer:
                    writer.write(self.auth)
            self.auth = True
        self.clearcache()
        self.opened = True
        return

    def logout(self):
        for foil in self.downloaded_files:
            try:
                os.remove(foil)
            except:
                try:
                    os.system("yes|rm " + str(foil))
                except Exception as e:
                    print("Failed to remove the cached file " +str(foil))
                    print(e)
                    pass
        self.clearcache()
        return

    def download(self, file_path=None,download_to=None):
        if not self.opened:
            self.login()
        #https://huggingface.co/docs/huggingface_hub/v0.9.0/en/package_reference/file_download#huggingface_hub.hf_hub_download
        if file_path and isinstance(file_path,str):
            from huggingface_hub import hf_hub_download
            current_file = hf_hub_download(
                repo_id=self.repo,
                filename=file_path,
                repo_type=self.repo_type,
                use_auth_token=self.auth
            )
            if download_to:
                try:
                    shutil.copy(current_file, os.path.basename(current_file))
                    current_file = os.path.basename(current_file)
                except:
                    pass
            return current_file
        return None

    def close_nonchanging_pr(self, pull_request=None):
        """ MULTITHREAD PREP
        threads = 4
        try:
            delete_to = update.message.message_id+1
            delete_from = last_message(delete_to)

            _range = range(delete_from, delete_to)
            print(f"Deleting from {delete_from} to {delete_to}")

            class MyThread(thread.Thread):
                #https://www.tutorialspoint.com/python3/python_multithreading.htm
                def __init__(self,name,bot,chat_id,msg_range):
                    thread.Thread.__init__(self)
                    self.name = name
                    self.bot = bot
                    self.chat_id = chat_id
                    self.msg_range = msg_range
                def run(self):
                    for num in self.msg_range:
                        delete_msg(self.name,self.bot,self.chat_id,num)
            
            thread_dyct = []
            ranges = split(_range,threads)
            print(ranges)
            for itr,thread_range in enumerate(ranges):
                print(f"Range:> {thread_range}")
                thread_dyct += [
                    MyThread(itr, context.bot, update.message.chat_id, thread_range)
                ]
            [tred.start() for tred in thread_dyct]
            [tred.join() for tred in thread_dyct]
        except Exception as e:
            update.message.reply_text(f"failure: {e}")
        """
        #https://huggingface.co/docs/huggingface_hub/main/en/package_reference/hf_api#huggingface_hub.HfApi.change_discussion_status
        for pr in self.get_pull_requests():
            if pull_request is None or pull_request == pr.num:
                pr_details = self.get_pull_request_info(pr.num)
                if pr_details.diff.strip() == '':
                    self.api.change_discussion_status(
                        repo_id=self.repo,
                        repo_type=self.repo_type,
                        token=self.auth,
                        discussion_num=pr.num,
                        new_status='closed'
                    )

    def upload(self, path=None,path_in_repo=None, auto_accept_all_pull_requests=True,use_pull_request = True):
        if not self.opened:
            self.login()
        #Because HuggingFace_hub will get pissed if we don't use it
        if path:
            if isinstance(path,str) and os.path.isfile(path):
                #https://huggingface.co/docs/huggingface_hub/v0.9.0/en/package_reference/hf_api#huggingface_hub.HfApi.upload_file
                self.api.upload_file(
                    path_or_fileobj=path,
                    path_in_repo=path_in_repo or path,
                    repo_id=self.repo,
                    repo_type=self.repo_type,
                    create_pr=use_pull_request #https://huggingface.co/docs/huggingface_hub/v0.10.0.rc0/en/how-to-discussions-and-pull-requests
                )
                if auto_accept_all_pull_requests:
                    self.merge_pull_requests()
            elif isinstance(path,str) and os.path.isdir(path):
                #https://huggingface.co/docs/huggingface_hub/v0.9.0/en/package_reference/hf_api#huggingface_hub.HfApi.upload_folder
                self.api.upload_file(
                    folder_path=path,
                    path_in_repo=path_in_repo or path,
                    repo_id=self.repo,
                    repo_type=self.repo_type,
                    create_pr=use_pull_request
                )
                if auto_accept_all_pull_requests:
                    self.merge_pull_requests()
            else:
                print("Entered path " + str(path) + " is not supported or doesn't exist exists(" +  str(os.path.exists(path)) + ").")
            return True
        return False

    def files(self):
        if not self.opened:
            self.login()
        # https://huggingface.co/docs/huggingface_hub/v0.9.0/en/package_reference/hf_api#huggingface_hub.HfApi.list_repo_files
        return self.api.list_repo_files(
            repo_id=self.repo,
            repo_type=self.repo_type
        )

    def ol_impor(self,file):
        if file not in self.files():
            print("FILE IS NOT AVAILABLE")
            return None
        
        import_name = str(file.split('/')[-1]).replace('.py','')
        #https://stackoverflow.com/questions/19009932/import-arbitrary-python-source-file-python-3-3#answer-19011259
        loader = importlib.machinery.SourceFileLoader(import_name, os.path.abspath(self[file]))
        mod = types.ModuleType(loader.name)
        loader.exec_module(mod)

        return mod
        
    def delete_file(self,path_in_repo=None,use_flag=False):
        if not self.opened:
            self.login()
        # https://huggingface.co/docs/huggingface_hub/v0.9.0/en/package_reference/hf_api#huggingface_hub.HfApi.delete_file
        if path_in_repo:
            self.api.delete_file(
                path_in_repo=path_in_repo,
                repo_id=self.repo,
                repo_type=self.repo_type,
                create_pr=use_flag
            )
            if use_flag:
                self.merge_pull_requests()
        return False
        
    def to_ghub(self, location, access_token):
        if not self.opened:
            self.login()

        ghub_repo = ghub(location, access_token, create=True)

        for foil in self.files():
            ghub_repo[foil] = self[foil]

        return ghub_repo

class fixface(face):
    @staticmethod
    def run(cmd):
        print(cmd);os.system(cmd)

    def __init__(self,repo,use_auth=True,repo_type="dataset",clear_cache=False, clear_token=False, sparse=False):
        super().__init__(repo,use_auth=True,repo_type="dataset",clear_cache=False, clear_token=False)
        #https://github.blog/2020-01-17-bring-your-monorepo-down-to-size-with-sparse-checkout/
        fixface.run("git clone {1} https://huggingface.co/datasets/{0}".format(repo, "--no-checkout" if sparse else ""))
        if sparse:
            fixface.run("cd {0} && git sparse-checkout init --cone".format(repo.split("/")[-1]))

    def __enter__(self):
        return self
    
    def exit(self):
        fixface.run("yes|rm -r {0}/".format(self.repo.split("/")[-1]))

    def __exit__(self,exc_type, exc_val, exc_tb):
        self.exit()
        return self

    def fix_pr(self, num):
        num = str(num)
        def run(cmd):
            print(cmd);os.system(cmd)

        run("git fetch origin refs/pr/{0}:pr/{0}".format(num))

        class pr(object):
            def __init__(self,num,face=None):
                self.num = num
                self.face = face
                run("cd {0}".format(repo.split("/")[-1]))
            def fixattr(self):
                run("git checkout main -- .gitattributes && git add .gitattributes")
            def __enter__(self):
                run("git checkout pr/{0}".format(self.num))
                return self
            def __exit__(self,exc_type, exc_val, exc_tb):
                run("git commit -m \"Fixed the gitattributes\"")
                run("git push origin pr/{0}:refs/pr/{0}".format(self.num))
                run("git checkout main")
                face.merge_pull_request(self.num)
                return self
        return pr(num,self)

#https://pygithub.readthedocs.io/en/latest/
#https://pygithub.readthedocs.io/en/latest/examples/Branch.html#get-a-branch
class ghub(mem):
    @staticmethod
    def create_repo(auth_key, repo_name, private=True):
        req = github.Requester.Requester(auth_key,None,None,"https://api.github.com",15,"PyGithub/Python",30,True,None,None)
        try:
            headers, data = req.requestJsonAndCheck(
                "POST", "https://api.github.com/user/repos", parameters={},headers={
                    "Accept":"application/vnd.github+json",
                    "Authorization":"Bearer {0}".format(auth_key),
                    "X-GitHub-Api-Version":"2022-11-28",
                }, input = {
                    "name":repo_name,
                    "private":private,
                    "auto_init":True,
                }
            )
            output = True
        except:
            output = False

        return output

    def __init__(self,repo,access_token,branch='master',create=False):
        self.github_access = Github(access_token)
        if create:
            try:
                repo = self.github_access.get_repo(repo)
                has_repo = True
            except:
                has_repo = False
            
            if has_repo:
                raise Exception("There already is an repo with this name")
            
            if not ghub.create_repo(access_token, repo):
                raise Exception("Error creating repo")

        if False:
            #create
            #https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#create-a-repository-for-the-authenticated-user

            self.github_access = Github(access_token)

            #search :> https://github.com/PyGithub/PyGithub/blob/master/github/MainClass.py#L410
            #https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#create-an-organization-repository
            if create:
                print('a')
            else:
                self.repo = self.github_access.get_repo(repo)
    
        self.repo = self.github_access.get_repo(repo)

        self.branch = None
        if branch is not None:
            self.branch = branch
        
        if self.branch is None:
            try:
                self.repo.get_branch(branch="main")
                self.branch = "main"
            except Exception as e:
                print(e)
                print("Branch 'main' does not exist")
                pass
        
        if self.branch is None:
            try:
                self.repo.get_branch(branch="master")
                self.branch = "master"
            except Exception as e:
                print(e)
                print("Branch 'master' does not exist")
                pass

        if self.branch is None:
            print("No branch is selected, cannot work")
            self.repo = None
            self = None

    def files(self):
        files = []
        contents = self.repo.get_contents("", ref=self.branch)
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(self.repo.get_contents(file_content.path, ref=self.branch))
            else:
                files += [file_content.path]
        return files

    def url(self):
        return "https://github.com/" + str(self.repo)

    def login(self):
        return
    
    def logout(self):
        return
    
    def has_repo(self, repo):
        try:
            repo = self.github_access.get_repo(repo)
            output = True
        except:
            output = False
        return output
    
    def download(self, file_path=None,download_to=None):
        if download_to is None:
            download_to = os.path.join(os.curdir,file_path.split("/")[-1])
        if file_path and isinstance(file_path,str):
            with open(download_to,"w+") as writer:
                writer.write(self.repo.get_contents(file_path, ref=self.branch).decoded_content.decode("utf-8") )
        return download_to
    
    def upload(self, file_path=None,path_in_repo=None):
        if path_in_repo in self: #Update
            from pathlib import Path
            contents = self.repo.get_contents(path_in_repo, ref=self.branch) #https://github.com/PyGithub/PyGithub/blob/001970d4a828017f704f6744a5775b4207a6523c/github/Repository.py#L1803
            new_contents = Path(file_path).read_text()
            self.repo.update_file(contents.path, "Updating the file {}".format(path_in_repo), new_contents, contents.sha, branch=self.branch) #https://github.com/PyGithub/PyGithub/blob/001970d4a828017f704f6744a5775b4207a6523c/github/Repository.py#L2134
        else: #Create #https://github.com/PyGithub/PyGithub/blob/001970d4a828017f704f6744a5775b4207a6523c/github/Repository.py#L2074
            self.repo.create_file(path_in_repo, "Creating the file {}".format(path_in_repo), file_path, branch=self.branch)
    
    def delete_file(self,path_in_repo=None):
        if path_in_repo in self.files():
            contents = self.repo.get_contents(path_in_repo, ref=self.branch) #https://github.com/PyGithub/PyGithub/blob/001970d4a828017f704f6744a5775b4207a6523c/github/Repository.py#L1803
            self.repo.delete_file(path_in_repo, "Deleting the file {}".format(path_in_repo), contents.sha,branch=self.branch) #https://github.com/PyGithub/PyGithub/blob/001970d4a828017f704f6744a5775b4207a6523c/github/Repository.py#L2198

class glab(mem):
    #https://python-gitlab.readthedocs.io/en/stable/index.html#installation
    #https://python-gitlab.readthedocs.io/en/stable/api-usage.html
    def __init__(self,repo,access_token=None,oauth=None,branch='master'):
        if access_token:
            self.gl = Gitlab(private_token=access_token)
        elif oauth:
            self.gl = Gitlab(oauth_token=oauth)
        else:
            self.gl = Gitlab()

        self.gl.auth()

        if "/" in repo:
            self.reponame = repo.strip("/")[-1]
        else:
            self.reponame = repo

        self.project = None
        self.branch = branch

        for project in self.gl.projects.list(owned=True,get_all=True):
            if project.name == self.reponame:
                self.project = project

    def files(self):
        #https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html?highlight=files#project-files
        #https://stackoverflow.com/questions/60243129/how-can-i-extract-contents-from-a-file-stored-in-gitlab-repos

        files = [
            x['path'] for x in 
            self.project.repository_tree(ref=self.branch,all=True,recursive=True)
        ]

        return files

    def url(self):
        return "https://gitlab.com/" + str(self.repo)

    def login(self):
        return
    
    def logout(self):
        return
    
    def download(self, file_path=None,download_to=None):
        #https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html#id7

        if download_to is None:
            download_to = os.path.join(os.curdir,file_path.split("/")[-1])

        if file_path and isinstance(file_path,str):
            with open(download_to,"wb+") as writer:
                self.project.files.raw(file_path=file_path, ref=self.branch,streamed=True,action=writer.write)
        return download_to
    
    def upload(self, file_path=None,path_in_repo=None):
        #https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html
        with open(file_path, 'r') as my_file:
            file_content = my_file.read()

        if path_in_repo in self: #Update
            f = self.project.files.get(file_path=path_in_repo, ref=self.branch)
            f.content = file_content
            f.save(branch=self.branch, commit_message='Auto Update File')
        else: #Create https://stackoverflow.com/questions/52338343/problem-to-upload-a-file-to-gitlab-using-python-gitlab
            f = self.project.files.create({
                'file_path': path_in_repo,
                'branch': self.branch,
                'content': file_content,
                'author_email': self.gl.user.email,
                'author_name': self.gl.user.name,
                #'encoding': 'utf-8',
                'commit_message': 'Auto Create File'
            })
    
    def delete_file(self,path_in_repo=None):
        if path_in_repo in self.files():
            self.project.files.delete(
                file_path=path_in_repo,
                branch=self.branch,
                commit_message="Auto Delete From Repo"
            )

class localdrive(mem):
    #https://python-gitlab.readthedocs.io/en/stable/index.html#installation
    #https://python-gitlab.readthedocs.io/en/stable/api-usage.html
    def __init__(self,file_location):
        self.location = file_location

    def files(self):
        return [os.path.join(dp, f) for dp, dn, filenames in os.walk(os.curdir) for f in filenames if os.path.isfile(f)]

    def login(self):
        return
    
    def logout(self):
        return
    
    def download(self, file_path=None,download_to=None):
        download_to = download_to or os.path.basename(file_path)
        shutil.copy(file_path, download_to)
        return download_to
    
    def upload(self, file_path=None,path_in_repo=None):
        shutil.copy(file_path, path_in_repo)
        return True
    
    def delete_file(self,path_in_repo=None):
        if path_in_repo in self.files():
            os.remove(path_in_repo)
        return True

class zyp(mem):
    #https://docs.python.org/3/library/zipfile.html
    def __init__(self,zyp_file):
        self.location = zyp_file

    def files(self):
        if not os.path.exists(self.location):
            return []
        return ZipFile(self.location).namelist()

    def login(self):
        return
    
    def logout(self):
        return
    
    def download(self, file_path=None,download_to=None):
        if not os.path.exists(self.location):
            print("Zip File Does Not Exist")
            return

        download_to = download_to or os.path.basename(file_path)
        with ZipFile(self.location) as z:
            print(download_to)
            with open(download_to, 'wb') as f:
                f.write(z.read(file_path))
        return download_to
    
    def upload(self, file_path=None,path_in_repo=None):
        editing_mode = 'a' if os.path.exists(self.location) else 'w'

        if path_in_repo in self.files():
            del self[path_in_repo]

        with ZipFile(self.location,editing_mode) as myzip:
            myzip.write(file_path,path_in_repo)
        return True
    
    def delete_file(self,path_in_repo=None):
        if not os.path.exists(self.location):
            return

        zipfileextra.delete_from_zip_file(self.location, file_names=[path_in_repo])
        return True

def redundant(klass):
    """
    #Example:
    source = hugg.redundant([
        hugg.face(xxx, yyy),
        hugg.ghub(xxx, yyy),
    ])
    #One of the two provided should work, otherwise an exception is thrown
    """
    if not isinstance(klass,list):
        klass = [klass]

    for temp_klass in klass:
        try:
            temp_klass.files()
            return temp_klass
        except: pass
    
    raise Exception("No Mirrors are available")

def sync_two_repos(new_repo, old_repo,delay_sec=2):
    import time
    delay = lambda:time.sleep(delay_sec)

    print("Updating/Creating New Files")
    for foil in new_repo.files():
        try:
            old_repo[foil] = new_repo[foil]
        except: pass
        delay()
        print(".",end='',flush=True)

    print("\nDeleting Old Files")
    for foil in old_repo.files():
        if foil not in new_repo.files():
            del old_repo[foil]
            delay()
        print(".",end='',flush=True)
    
    print("Completed")
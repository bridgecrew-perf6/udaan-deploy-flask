import json
import os
from git import *
'''
WORKING: Program basically creates a remote repo, clones it, transfers the newly created folder(OCR folder) into the repo, 
		 and then pushed changes back into the repo.  
TODO: Please check all path variables to make sure the script functions in your enviroment

'''

#Function to push changes into repo
#git_token = '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'
def git_push( DEST_NAME, prj_name):
    try:
        repo = Repo(DEST_NAME)
        os.chdir(DEST_NAME)
        repo.git.add(update=True)
        repo.git.add('--all') #Project Name
        repo.index.commit('initial commit')
        origin = repo.remote(name='origin')
        origin.push()
    except Exception as e:
        print(e)   

#Function to clone repo from github

def get_repo(DEST_NAME, prj_name):
	HTTPS_REMOTE_URL = 'https://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:x-oauth-basic@github.com/UdaanContentForLogging/' + prj_name
	# DEST_NAME = '/media/sanskar/UBUNTU 18_0/IIT-B/API'
	cloned_repo = Repo.clone_from(HTTPS_REMOTE_URL, DEST_NAME)
	print('Cloned at ', DEST_NAME)


#command to create new repo
def push_to_git(prj_name, copy_from, user_git_id):
    BASH_COMMAND_NEW_REPO = "curl -H \"Authorization: token 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\" --data '{\"name\":\"" + prj_name + "\" , \"private\": true}' https://api.github.com/orgs/UdaanContentForLogging/repos"
    try:
        os.system(BASH_COMMAND_NEW_REPO)
    except Exception:
        pass
    DEST_NAME = './tmp_store/'+prj_name
    if not os.path.exists(DEST_NAME):
      os.mkdir(DEST_NAME)
    get_repo(DEST_NAME, prj_name)

    copy_from = 'cp -r ' + copy_from + '  ' + './tmp_store'
    BASH_COMMAND_COPY_TO_REPO = copy_from #"""cp -r 'SBJ2_JK_AV-VS' 'API'"""
    os.system(BASH_COMMAND_COPY_TO_REPO)
    print('transferred data to repo')
    git_push(DEST_NAME, prj_name)
    print('changes pushed to git!')

    add_collab = 'curl -H "Authorization: token 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" "https://api.github.com/repos/UdaanContentForLogging/' + prj_name + '/collaborators/' + user_git_id + '\" -X PUT -d \'{\"permission\":\"push\"}\''
    BASH_COMMAND_ADD_COLLAB =  add_collab #"""curl -H "Authorization: token <git hub token>" "https://api.github.com/repos/UdaanContentForLogging/API/collaborators/cyfer0618" -X PUT -d '{"permission":"push"}'"""
    os.system(BASH_COMMAND_ADD_COLLAB)
    print('you have been added as a collaborator to the repo')
    return True

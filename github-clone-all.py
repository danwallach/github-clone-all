# github-clone-all.py
# Dan Wallach <dwallach@rice.edu>

import requests
import json
import re
import time
import argparse
import sys
import os
import subprocess

# see installation and usage instructions in README.md

defaultGithubToken = "YOUR_TOKEN_HERE"

# and we're going to need the name of your GitHub "project" in which all your
# students' work lives

defaultGithubProject = "YOUR_PROJECT_HERE" # e.g., "RiceComp215"
defaultPrefix = ""

# command-line argument processing

parser = argparse.ArgumentParser(description='Clone a large number of GitHub repos all at once.')
parser.add_argument('--token',
                        nargs=1,
                        default=defaultGithubToken,
                        help='GitHub API token')
parser.add_argument('--project',
                        nargs=1,
                        default=defaultGithubProject,
                        help='GitHub project to scan, default: ' + defaultGithubProject)
parser.add_argument('--prefix',
                        nargs=1,
                        default=defaultPrefix,
                        help='Prefix on projects to match (default: match all projects)')
parser.add_argument('--out',
                        nargs=1,
                        default=".",
                        help='Destination directory for GitHub clones (default: current directory)')

args = parser.parse_args()

githubPrefix = args.prefix
githubProject = args.project
githubToken = args.token
outDir = args.out

#
# local goodies (for my cron job)
#
from datetime import datetime
from pytz import timezone  
print ""
print ">>>>>>>>>>>>>>"
print ">>>>>>>>>>>>>> Running github-clone-all: " + datetime.now(timezone("US/Central")).strftime('%Y-%m-%d %H:%M:%S %Z%z')
print ">>>>>>>>>>>>>>"
print ""

requestHeaders = {
    "User-Agent": "GitHubCloneAll/1.0",
    "Authorization": "token " + githubToken,
}

allReposList = []

pageNumber = 1
sys.stdout.write('Getting repo list from Github')

while True:
    sys.stdout.write('.')
    sys.stdout.flush()
    
    reposPage = requests.get('https://api.github.com/orgs/' + githubProject +
                             '/repos?page=' + str(pageNumber), headers = requestHeaders) 
    pageNumber = pageNumber + 1

    if reposPage.status_code != 200:
        print "Failed to load repos from GitHub: " + reposPage.content
        exit(1)

    reposPageJson = reposPage.json()
    
    if len(reposPageJson) == 0:
        print " Done."
        break

    allReposList = allReposList + reposPage.json()

# Each repo in the list has the following fields that we care about:
#
# clone_url: starts with https, suitable for checking out from the command-line
#     (e.g., 'https://github.com/RiceComp215/comp215-week01-intro-2017-dwallach.git')
#
# ssh_url: starts with git@github.com (e.g., 'git@github.com:RiceComp215/comp215-week01-intro-2017-dwallach.git')
#
# name: the name of the repo itself (e.g., 'comp215-week01-intro-2017-dwallach')
#
# full_name: the project and repo (e.g., 'RiceComp215/comp215-week01-intro-2017-dwallach')

filteredRepoList = [x for x in allReposList if x['name'].startswith(githubPrefix)]
print "%d of %d repos start with %s" % (len(filteredRepoList), len(allReposList), githubPrefix)

# before we start getting any repos, we need a directory to get them
if outDir != ".":
    try:
        os.makedirs(outDir)
    except OSError:
        # directory probably already exists
        print "directory %s already exists" % outDir
    os.chdir(outDir)

# specific clone instructions here:
# https://github.com/blog/1270-easier-builds-and-deployments-using-git-over-https-and-oauth

for repo in filteredRepoList:
    cloneUrl = 'https://%s@github.com/%s.git' % (githubToken, repo['full_name'])

    # Steps to take, per docs above:
    #
    # mkdir foo
    # cd foo
    # git init
    # git pull https://<token>@github.com/username/bar.git

    os.mkdir(repo['name'])
    os.chdir(repo['name'])
    subprocess.call(["git", "init"])
    subprocess.call(["git", "pull", cloneUrl])
    os.chdir('..')

#
# leftover from an earlier emergency: if you want to make a repo be private, here's the code to do it
#
#         response = requests.patch('https://api.github.com/repos' + githubProject + '/' + name,
#                                   headers = requestHeaders, json={ "private": True })
#

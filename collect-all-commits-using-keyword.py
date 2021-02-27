import sys
import os
import requests
from bs4 import BeautifulSoup
import subprocess
import time

framework = sys.argv[1]

frameworkOrg = {
    'tensorflow' : 'tensorflow',
}

if framework not in frameworkOrg.keys():
    raise Exception("Please enter a valid framework in the command line")

# This method filter all the commits having the mentioned keywords
def collectCommitsContainngKeywords(keyword):
    issuesCommitsById = subprocess.check_output('git log -E -P -i --all --grep="{}"'.format(keyword), cwd='../polygot_in_dl_frameworks/polygot_in_dl_frameworks/repo-clones/{}/{}'.format(framework, framework), stderr=subprocess.STDOUT, shell=True).decode("utf-8").split('\n')
    try:
        f = open('All-Commits-Having-{}-in-{}.txt'.format(keyword, framework), 'w+', encoding='utf-8')
        for commit in issuesCommitsById:
            f.write('{}\n'.format(commit))
    except:
        print('Something went wrong while writing the results')
    finally:
        f.close()


start = time.time()

collectCommitsContainngKeywords('security')
collectCommitsContainngKeywords('crash')
collectCommitsContainngKeywords('exception')

timeTaken = time.time() - start

print('Time taken: {}'.format(timeTaken))

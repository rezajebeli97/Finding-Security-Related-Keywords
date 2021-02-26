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

keywords = '(#|close(d|s)*|fix(ed|es)*|issue|tensorflow\\/tensorflow\\/issues\\/)(\\s)*(\\d+)(\\W|$)'

# This method filter all the commits having the mentioned keywords
def collectCommitsContainngKeywords():
    issuesCommitsById = subprocess.check_output('git log -E -P -i --all --grep="{}"'.format(keywords), cwd='../polygot_in_dl_frameworks/polygot_in_dl_frameworks/repo-clones/{}/{}'.format(framework, framework), stderr=subprocess.STDOUT, shell=True).decode("utf-8").split('\n')
    try:
        f = open('All-Commits-Having-Specific-Keyword-{}.txt'.format(framework), 'w+', encoding='utf-8')
        for commit in issuesCommitsById:
            f.write('{}\n'.format(commit))
    except:
        print('Something went wrong while writing the results')
    finally:
        f.close()


start = time.time()

collectCommitsContainngKeywords()

timeTaken = time.time() - start

print('Time taken: {}'.format(timeTaken))

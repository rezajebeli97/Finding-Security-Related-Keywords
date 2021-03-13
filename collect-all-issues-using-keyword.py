import sys
import os
import requests
from bs4 import BeautifulSoup
import subprocess
import time
import re

def webscrape(issueState, issueList, keywords, status):
    files = []
    print('Number of {} issues to be explored : {}'.format(issueState, len(issueList)))

    for keyword in keywords:
    	if status == 'test':
    		files.append(open('issues/test/{}/All-{}-Issues-Having-{}-in-{}.txt'.format(issueState, issueState, keyword, framework), 'w+', encoding='utf-8'))
    	else:
    		files.append(open('issues/{}/All-{}-Issues-Having-{}-in-{}.txt'.format(issueState, issueState, keyword, framework), 'w+', encoding='utf-8'))

    for issue in issueList:
        with open(issue, 'r', encoding='utf-8') as f:
            #parsing the html file corresponding to the issue
            soup = BeautifulSoup(f.read(), 'html5lib')

            #getting the first post which will correspond to the issue's description
	        # issueDesc = soup.find('td', class_="d-block comment-body markdown-body js-comment-body")

	        #extracting the issue's ID from the bug report
            issueIdMatch = re.search('\\d+', issue)
            issueId = issue[issueIdMatch.start() : issueIdMatch.end()]

            for i, keyword in enumerate(keywords):
	            #check if the html has the keyword
	            stringsContainingTheKeyword = soup.body.findAll(text=re.compile(keyword))
	            NumOfRepeat = len(stringsContainingTheKeyword)
	            if (NumOfRepeat > 0):
	                issueInfo = {
	                'ID' : issueId,
	                # 'Description' : issueDesc,
	                'Num of Repeat': NumOfRepeat
	                }
	                files[i].write('ID: {}\tNum of Repeat: {}\n'.format(issueInfo['ID'], issueInfo['Num of Repeat']))


def writeResults(issueState, issuesInfo, keyword):
    try:
        f = open('All-{}-Issues-Having-{}-in-{}.txt'.format(issueState, keyword, framework), 'w+', encoding='utf-8')
        for issueInfo in issuesInfo:
            f.write('ID: {}\tNum of Repeat: {}\tDescription: {}\n'.format(issueInfo['ID'], issueInfo['Num of Repeat'], issueInfo['Description']))
    except:
        print('Something went wrong while writing the results')
    finally:
        f.close()


issueStates = ['open', 'closed']

frameworkOrg = {
    'tensorflow' : 'tensorflow',
}

framework = sys.argv[1]

if framework not in frameworkOrg.keys():
    raise Exception("Please enter a valid framework in the command line")

issueState = sys.argv[2]

status = sys.argv[3]


start = time.time()

issues = []

if issueState == 'open' and status == 'real':
	issues = ['../polygot_in_dl_frameworks/polygot_in_dl_frameworks/{}/open/{}'.format(framework, f) for f in os.listdir('../polygot_in_dl_frameworks/polygot_in_dl_frameworks/{}/open'.format(framework))]

elif issueState == 'closed' and stauts == 'real':
	issues = ['../polygot_in_dl_frameworks/polygot_in_dl_frameworks/{}/closed/{}'.format(framework, f) for f in os.listdir('../polygot_in_dl_frameworks/polygot_in_dl_frameworks/{}/closed'.format(framework))]

elif issueState == 'open' and status == 'test':
	issues = ['../Test/{}/open/{}'.format(framework, f) for f in os.listdir('../Test/{}/open'.format(framework))]

elif issueState == 'closed' and stauts == 'test':
	issues = ['../Test/{}/closed/{}'.format(framework, f) for f in os.listdir('../Test/{}/closed'.format(framework))]

else:
	raise Exception("Please enter valid inputs in the command line")

keywords = ['exception', 'crash', 'security', 'token', 'secret', 'TODO', 'password', 'vulnerable', 'CSRF', 'random', 'hash', 'HMAC', 'MD5', 'SHA-1', 'SHA-2', 'performance', 'efficiency', 'efficient', 'fast', 'speed', 'slow', 'memory usage']

webscrape(issueState, issues, keywords, status)

timeTaken = time.time() - start

print('Time taken: {}'.format(timeTaken))

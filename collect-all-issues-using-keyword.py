import sys
import os
import requests
from bs4 import BeautifulSoup
import subprocess
import time
import re

issueStates = ['open', 'closed']

framework = sys.argv[1]

frameworkOrg = {
    'tensorflow' : 'tensorflow',
}

if framework not in frameworkOrg.keys():
    raise Exception("Please enter a valid framework in the command line")


def webscrape(issueState, issueList, keywords):
    files = []
    print('Number of {} issues to be explored : {}'.format(issueState, len(issueList)))

    for keyword in keywords:
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



start = time.time()
openIssues = ['../polygot_in_dl_frameworks/polygot_in_dl_frameworks/{}/open/{}'.format(framework, f) for f in os.listdir('../polygot_in_dl_frameworks/polygot_in_dl_frameworks/{}/open'.format(framework))]
closedIssues = ['../polygot_in_dl_frameworks/polygot_in_dl_frameworks/{}/closed/{}'.format(framework, f) for f in os.listdir('../polygot_in_dl_frameworks/polygot_in_dl_frameworks/{}/closed'.format(framework))]
# openIssues = ['../Test/{}/open/{}'.format(framework, f) for f in os.listdir('../Test/{}/open'.format(framework))]
# closedIssues = ['../Test/{}/closed/{}'.format(framework, f) for f in os.listdir('../Test/{}/closed'.format(framework))]

keywords = ['exception', 'crash', 'security', 'token', 'secret', 'TODO', 'password', 'vulnerable', 'CSRF', 'random', 'hash', 'HMAC', 'MD5', 'SHA-1', 'SHA-2', 'performance', 'efficiency', 'efficient', 'fast', 'speed', 'slow', 'memory usage']
# openIssuesHavingTheKeywordInfo = webscrape(issueStates[0], openIssues, keywords)
closedIssuesHavingTheKeywordInfo = webscrape(issueStates[1], closedIssues, keywords)

timeTaken = time.time() - start

print('Time taken: {}'.format(timeTaken))

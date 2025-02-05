import sys
import os
import requests
from bs4 import BeautifulSoup
import subprocess
import time
import re

def webscrape_conncected(issueState, issueList, keywords, status, topic):
    files = []
    print('Number of {} issues to be explored : {}'.format(issueState, len(issueList)))

    for keyword in keywords:
        if status == 'test':
            files.append(open('issues/test/{}/{}/All-{}-Issues-Having-{}-in-{}.txt'.format(topic, issueState, issueState, keyword, framework), 'w+', encoding='utf-8'))
        else:
            files.append(open('issues/{}/{}/All-{}-Issues-Having-{}-in-{}.txt'.format(topic, issueState, issueState, keyword.replace('\\','').replace('/','-'), framework), 'w+', encoding='utf-8'))

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
                issueTitle = soup.find('span', class_="js-issue-title markdown-title")
                issueDescs = soup.findAll('td', class_="d-block comment-body markdown-body js-comment-body")
                issueDesc = '\n'.join(issueDescs)
                issue_title_desc = issueTitle + '\n' + issueDesc
                stringsContainingTheKeyword = issue_title_desc.findAll(text=re.compile(keyword, re.I))
                NumOfRepeat = len(stringsContainingTheKeyword)
                if (NumOfRepeat > 0):
                    issueInfo = {
                    'ID' : issueId,
                    # 'Description' : issueDesc,
                    'Num of Repeat': NumOfRepeat
                    }
                    files[i].write('ID: {}\tNum of Repeat: {}\n'.format(issueInfo['ID'], issueInfo['Num of Repeat']))


def webscrape_separated(issueState, issueList, keywords_set, status, topic):
    files = []
    print('Number of {} issues to be explored : {}'.format(issueState, len(issueList)))

    for keyword_set in keywords_set:
        keyword = '-'.join(keyword_set)
        if status == 'test':
            files.append(open('issues/test/{}/{}/All-{}-Issues-Having-{}-in-{}.txt'.format(topic, issueState, issueState, keyword, framework), 'w+', encoding='utf-8'))
        else:
            files.append(open('issues/{}/{}/All-{}-Issues-Having-{}-in-{}.txt'.format(topic, issueState, issueState, keyword.replace('\\','').replace('/','-'), framework), 'w+', encoding='utf-8'))

    for issue in issueList:
        with open(issue, 'r', encoding='utf-8') as f:
            #parsing the html file corresponding to the issue
            soup = BeautifulSoup(f.read(), 'html5lib')

            #getting the first post which will correspond to the issue's description
            # issueDesc = soup.find('td', class_="d-block comment-body markdown-body js-comment-body")

            #extracting the issue's ID from the bug report
            issueIdMatch = re.search('\\d+', issue)
            issueId = issue[issueIdMatch.start() : issueIdMatch.end()]

            for i, keyword_set in enumerate(keywords_set):
                #check if the html has the keyword
                NumOfRepeats = ''
                issueTitle = soup.find('span', class_="js-issue-title markdown-title")
                issueDescs = soup.findAll('td', class_="d-block comment-body markdown-body js-comment-body")
                issueDesc = '\n'.join(issueDescs)
                issue_title_desc = issueTitle + '\n' + issueDesc
                for keyword_index, keyword in enumerate(keyword_set):
                    stringsContainingTheKeyword = issue_title_desc.findAll(text=re.compile(keyword, re.I))
                    NumOfRepeat = len(stringsContainingTheKeyword)
                    if (NumOfRepeat == 0):
                        break
                    
                    if keyword_index == len(keyword_set) - 1:
                        NumOfRepeats += str(NumOfRepeat)
                        issueInfo = {
                            'ID' : issueId,
                            # 'Description' : issueDesc,
                            'Num of Repeats': NumOfRepeats
                        }
                        files[i].write('ID: {}\tNum of Repeats: {}\n'.format(issueInfo['ID'], issueInfo['Num of Repeats']))

                    else:
                        NumOfRepeats += str(NumOfRepeat) + ','


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

topic = sys.argv[4]

start = time.time()

issues = []

keywords = []


if issueState == 'open' and status == 'real':
    issues = ['../polygot_in_dl_frameworks/polygot_in_dl_frameworks/{}/open/{}'.format(framework, f) for f in os.listdir('../polygot_in_dl_frameworks/polygot_in_dl_frameworks/{}/open'.format(framework))]
    # issues = ['{}/open/{}'.format(framework, f) for f in os.listdir('{}/open'.format(framework))]

elif issueState == 'closed' and status == 'real':
    issues = ['../polygot_in_dl_frameworks/polygot_in_dl_frameworks/{}/closed/{}'.format(framework, f) for f in os.listdir('../polygot_in_dl_frameworks/polygot_in_dl_frameworks/{}/closed'.format(framework))]
    # issues = ['{}/closed/{}'.format(framework, f) for f in os.listdir('{}/closed'.format(framework))]

elif issueState == 'open' and status == 'test':
    issues = ['../Test/{}/open/{}'.format(framework, f) for f in os.listdir('../Test/{}/open'.format(framework))]

elif issueState == 'closed' and stauts == 'test':
    issues = ['../Test/{}/closed/{}'.format(framework, f) for f in os.listdir('../Test/{}/closed'.format(framework))]

else:
    raise Exception("Please enter valid inputs in the command line")

# security_keywords = ['exception', 'crash', 'security', 'token', 'secret', 'TODO', 'password', 'vulnerable', 'hash', 'HMAC', 'MD5', 'SHA-1', 'SHA-2']#attacker, 
# performance_keywords = ['performance', 'efficiency', 'efficient', 'fast', 'speed', 'slow', 'memory usage', 'improve', 'memory leak', 'optimize']
# performance_accuracy_regression = [['accuracy', 'decreas(e|ed)'], ['accuracy', 'degrad(e|ed)'], ['worse', 'accuracy'], ['accuracy', 'dro(p|pped|pping)']]
performance_regression_keywrods = ['accuracy decreas(e|ed)', 'accuracy degrad(e|ed)', 'worse in accuracy', 'accuracy dro(p|pped|pping)', 'memory increas(ed|e|ing)', 'memory usage increase(ed|e|ing)', 'computation time increase(ed|e|ing)', 'got slow', 'performance regression']

if topic == "performance_accuracy_regression":
    webscrape_separated(issueState, issues, performance_accuracy_regression, status, topic)
elif topic == "prediction":
    webscrape_separated(issueState, issues, None, status, topic)
elif topic == "both":
    webscrape_separated(issueState, issues, performance_accuracy_regression, status, 'performance_accuracy_regression')
    webscrape_separated(issueState, issues, None, status, 'prediction')
else:
    raise Exception("Wrong topic")

timeTaken = time.time() - start

print('Time taken: {}'.format(timeTaken))

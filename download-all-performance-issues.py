import sys
import requests
from bs4 import BeautifulSoup
import os
import time
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

issueStates = ['open', 'closed']

frameworkOrg = {
    'tfjs' : 'tensorflow',
    'tensorflow' : 'tensorflow',
}

label_type = 'performance'

framework = sys.argv[1]

if framework not in frameworkOrg.keys():
    raise Exception("Please enter a valid framework in the command line")


if not os.path.exists(framework):
    os.makedirs(framework)

for issueState in issueStates:
    if not os.path.exists('{}/{}'.format(framework, issueState)):
        os.makedirs('{}/{}'.format(framework, issueState))

# pages = []

def webscrape(issueState):
    url = 'https://github.com/{}/{}/issues?q=is%3Aissue+is%3A{}+label%3Atype%3A{}'.format(frameworkOrg[framework], framework, issueState, label_type)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html5lib')

    #getting the number of issues to be investigated so we know when to terminate our loop as we can trust not being able to find a
    #new page anymore because of the potential html dicrepencies
    n_issues = soup.find('a', {'class' : 'btn-link selected'})
    n = int(n_issues.text.replace(',', '').replace(' ', '').replace('\n', '').replace(issueState[0].upper() + issueState[1:].lower(), ''))

    print('Number of {} issues to be explored : {}'.format(issueState, n))

    #getting all the issues in the page
    resultSet = soup.find_all('a', {'class' : "Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title"})
    print(resultSet)
    issueCount = 0
    pageCount = 1
    #we encapsulate the code with a while True and try statement so if the connection is lost, we don't lose our progress
    while True:

        try:

            #if we've investigated all the issues closed, we're done
            while issueCount < n:
                
                print('\nPage {}:\n'.format(pageCount))

                for res in resultSet:

                    issueCount = issueCount + 1
                    issueId = ''

                    #as we progress through the pages, there will exist small html discrepensies. However, at this stage of the code
                    #we know that there's still issues to be explored so we use a while loop to keep retrying untill we get our wanted
                    #results
                    allTags = None
                    issueDesc = None
                    issueSoup = None
                    while allTags == None or issueDesc == None:

                        try:
                            issueUrl = 'https://github.com' + res['href']
                            issuePage = requests.get(issueUrl)
                            issueSoup = BeautifulSoup(issuePage.text, 'html5lib')

                            #in case the issue has a "Load more" section, we use selenium to open it up to make sure to scrape the complete issue page
                            loadMoreButton = issueSoup.find('button', {'class' : 'text-gray pt-2 pb-0 px-4 bg-white border-0'})
                            if loadMoreButton != None:
                                driver = webdriver.Chrome('./selenium-webdrivers/chromedriver')
                                driver.get(issueUrl)
                                while loadMoreButton != None:
                                    loadMoreButtonSelen = wait(driver, 20).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, 'button.bg-white.border-0')))
                                    loadMoreButtonSelen.click()
                                    wait(driver, 5).until(expected_conditions.invisibility_of_element_located(loadMoreButtonSelen))
                                    issueSoup = BeautifulSoup(driver.page_source, 'html5lib')
                                    loadMoreButton = issueSoup.find('button', {'class' : 'text-gray pt-2 pb-0 px-4 bg-white border-0'})

                            #getting the first post which will correspond to the issue's description
                            issueDesc = issueSoup.find('td', class_="d-block comment-body markdown-body js-comment-body")
                            if issueDesc == None:
                                print('descrepency (no issue description found). Retrying...')
                                continue

                            #collecting all the tags from the issue
                            allTags = issueDesc.findAll()
                            if allTags == None:
                                print('descrepency (issue description tags not found). Retrying...')
                                continue

                            issueId = issueUrl[issueUrl.rfind('/') + 1:]
                            
                            try:
                                f = open('{}/{}/issue{}.html'.format(framework, issueState, issueId), 'w+', encoding='utf-8')
                                f.write(issueSoup.prettify())
                            except:
                                print('Something went wrong')
                            finally:
                                f.close()
                            
                        except KeyboardInterrupt:
                            print('Keyboard Interrupt')
                            return

                    print('Number of {} issues written: {}/{}'.format(issueState, issueCount, n))

                #if the past issue was the last issue, we're done (we put '>=' instead or '==' because the number of closed issue
                #increase while our program is running)
                if issueCount >= n:
                    print('Finished')
                    return
                
                pageCount = pageCount + 1

                #if there is a next page, we get its link and we keep going
                url = 'https://github.com/{}/{}/issues?page={}&q=is%3Aissue+is%3A{}+label%3Atype%3A{}'.format(frameworkOrg[framework], framework, pageCount, issueState, label_type)

                #as we progress through the pages, there will exist small html discrepensies. However, at this stage of the code
                #we know that there's still issues to be explored so we use a while loop to keep retrying untill we get our wanted
                #results
                resultSet = None
                while resultSet == None:
                    try:
                        page = requests.get(url)
                        soup = BeautifulSoup(page.text, 'html5lib')

                        pageResult = soup.find('h3')
                        if pageResult != None:
                            if pageResult.text == 'No results matched your search.':
                                print('Error: no more pages (finished).')
                                return

                        #getting all the issues in the page
                        resultSet = soup.find_all('a', {'class' : "Link--primary v-align-middle no-underline h4 js-navigation-open markdown-title"})
                        if resultSet == None or len(resultSet) == 0:
                            print('descrepency (resultset). Retrying...')
                            continue
                    except KeyboardInterrupt:
                        print('Keyboard Interrupt')
                        return
        except KeyboardInterrupt:
            print('Keyboard Interrupt')
            return

        break

start = time.time()

#calling the webscrape method
for issueState in issueStates:
    webscrape(issueState)

timeTaken = time.time() - start

print('Time taken: {}'.format(timeTaken))
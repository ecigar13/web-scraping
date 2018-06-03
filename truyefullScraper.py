from bs4 import BeautifulSoup
import urllib
import requests
from requests.exceptions import HTTPError
import time
import os
import random
import sys

"""
This proram access many stories in truyenyy.com and write to HTML file.
- Change the name to set link to the story
- change the search parameter in extractTitle and extractContent to get those items.
Implemented parts:
- Dealing with server errors
- Added user agent
- Randomized access interval (to avoid anti-scraping)
Possible improvements:
- More spoofing of user agent
- Call flush to disk if can't overcome server errors
- Add referer header 
"""


class TruyenyyScraper(object):

    chapters = []
    chapterNum = 1
    currentChapter = 1
    initialUrl = "http://truyenfull.vn/"

    def __init__(self, storyName, outputFile):
        self.storyUrl = self.initialUrl + str(storyName) + "/chuong-"
        self.outputFile = outputFile

    def openFile(self):
        self.out = open(self.outputFile, "a+")
        self.writeHeadHtml()

    def writeHeadHtml(self):
        """Write the beginning part of HTML file so the written file is not garbled when viewed in browser"""
        if(currentChapter > 1):
            self.out.write("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
                <html>
                <head>
                    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
                    <title></title>
                    <meta name="generator" content="LibreOffice 5.1.6.2 (Linux)"/>
                    <meta name="created" content="00:00:00"/>
                    <meta name="changed" content="00:00:00"/>
                </head>
                <body lang="en-US" dir="ltr">""")

    def writeToFile(self):
        """Flush the buffer to OS then to disk when buffer reaches a certain size in case of a crash """
        for sections in self.chapters:
            #encoded = sections.encode('UTF-8')

            self.out.write(str(sections))
        self.out.flush()
        os.fsync(self.out.fileno())
        print("Flushed to disk")
        self.chapters = []
        self.chapterNum = 0

    def closeFile(self):
        """ Close the tags of the HTML file so I don't have to manually use Libre office to fix it """
        self.out.write("</body></html>")
        self.out.flush()
        os.fsync(self.out.fileno())
        self.out.close()

    def extractTitle(self, soup):
        """ Extract the chapter title of most truyenyy pages."""
        temp = soup.find("title")
        print(temp)
        return temp

    def extractContent(self, soup):
        """ Extract the main content of most truyenyy pages. The tag changes depending on the story series."""
        temp = soup.find("div", {"class": "chapter-c"})
        #print(temp)
        return temp

    def setChapterUrl(self, page):
        """ Set the current chapter URL, can be used to continue scraping if the last scraper crashed."""
        newUrl = self.storyUrl + str(page) + '/'
        self.currentChapter = page
        return newUrl

    # Return requests.model.Response
    def getResponseObject(self, url):
        """ Access the url and attempt to deal with different connection errors."""
        while True:
            try:
                r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
                                 )
                r.raise_for_status()
            except HTTPError as errh:
                print("Http Error:", errh)
                print(
                    "It is likely that the program has reached the end of the story and is not an error.")
                self.closeFile()
                exit(0)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
                print("Retrying in a few seconds.")
                time.sleep(5)
                continue
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
                print("Retrying in a few seconds.")
                time.sleep(5)
                continue
            except requests.exceptions.RequestException as err:
                print("OOps: Something Else", err)
                self.writeToFile()
            else:
                return r

    # parser can be html.parser, lxml or other parsers
    def getSoup(self, requestsObject, parser):
        return BeautifulSoup(requestsObject.content.decode('utf-8', 'ignore'), str(parser))

    def addNextChapter(self, soup):
        self.chapters.append(self.extractTitle(soup))
        self.chapters.append(self.extractContent(soup))
        self.chapterNum += 1
        self.currentChapter += 1

    def cleanUp(self):
        """Call this function every once in a while or after Ctrl+C to flush content to disk"""
        self.writeToFile()
        self.closeFile()


def main(storyName, saveFileName):
    try:
        scraper = TruyenyyScraper(str(storyName), str(saveFileName))
        scraper.openFile()
        url = scraper.setChapterUrl(1211)
        response = scraper.getResponseObject(url)

        while(response.status_code < 300):
            print("Next chapter: " + str(scraper.currentChapter))
            time.sleep(random.uniform(0, 3))
            soup = scraper.getSoup(response, 'html.parser')
            #print(soup)
            scraper.addNextChapter(soup)
            scraper.chapterNum = scraper.chapterNum+1
            if(scraper.chapterNum >= 10):
                scraper.writeToFile()

            url = scraper.setChapterUrl(scraper.currentChapter)
            print(url)
            response = scraper.getResponseObject(url)

    except KeyboardInterrupt:
        scraper.cleanUp()

    print("Done scraping. File saved in : " + str(saveFileName))


if __name__ == "__main__":
main(str(sys.argv[1]), str(sys.argv[2]))
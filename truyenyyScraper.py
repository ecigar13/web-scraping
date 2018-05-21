from bs4 import BeautifulSoup
import urllib
import requests
from requests.exceptions import HTTPError
import time
import os


class TruyenyyScraper(object):

    chapters = []
    chapterNum = 1
    currentChapter = 1
    initialUrl = "https://truyenyy.com/truyen/"

    def __init__(self, storyName, outputFile):
        self.storyUrl = self.initialUrl + str(storyName) + "/chuong-"
        self.outputFile = outputFile

    def openFile(self):
        self.out = open(self.outputFile, "w+")
        self.writeHeadHtml()

    def writeHeadHtml(self):
        self.out.write("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\">")

    def writeToFile(self):
        for sections in self.chapters:
            #encoded = sections.encode('UTF-8')
            
            self.out.write(str(sections))
        self.out.flush()
        os.fsync(self.out.fileno())
        print("Flushed to disk")
        self.chapters = []
        self.chapterNum = 0

    def closeFile(self):
        self.out.close()

    def extractTitle(self, soup):
        return soup.find("h1", class_="chap-title sans-serif-font")

    def extractContent(self, soup):
        return soup.find("div", id="inner_chap_content_1")

    def setChapterUrl(self, page):
        newUrl = self.storyUrl + str(page) + ".html"
        return newUrl

    # Return requests.model.Response
    def getResponseObject(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
        except HTTPError:
            print("Could not download page.")
            self.closeFile()
            exit(0)
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
        self.writeToFile()
        self.closeFile()

def main():
    try:
        scraper = TruyenyyScraper("quan-than", "quan-than.html")
        scraper.openFile()
        url = scraper.setChapterUrl(1)
        response = scraper.getResponseObject(url)
        
        count = 0
        while(count < 20):
        #while(response.status_code <= 399):
            print("Next chapter: " + str(scraper.currentChapter))
            time.sleep(0.25)
            soup = scraper.getSoup(response, "lxml")
            scraper.addNextChapter(soup)
            scraper.chapterNum = scraper.chapterNum+1
            if(scraper.chapterNum >= 10):
                scraper.writeToFile()

            url = scraper.setChapterUrl(scraper.currentChapter)
            response = scraper.getResponseObject(url)
            count+=1
    except KeyboardInterrupt:
        scraper.cleanUp()

if __name__ == "__main__":
    main()

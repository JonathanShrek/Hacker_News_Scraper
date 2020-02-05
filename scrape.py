#!/usr/bin/env python3

import urllib.request as req
from bs4 import BeautifulSoup as bs
import emailFunction
import csv
import time
import os.path as path

'''
This program scapes https://news.ycombinator.com/ for the first 30 articles on the front page. The
program then saves the article title, link, and score in their own seperate columns in a .csv file.

@author: Jonathan Shreckengost (jonathanshrek@gmail.com)
'''

class Scrape:
    
    def __init__(self, url, savePath):
        self.url = url
        self.path = savePath
        self.moment = time.strftime("%Y-%b-%d_%H_%M", time.localtime())
        self.fileName = "hackerNews " + self.moment
        self.completeName = path.join(self.path, self.fileName + ".csv")
        
    def hackScraper(self):
        # Error handling in case initial request fails
        try:
            page = req.urlopen(self.url)

            pageCount = 1
            while True:
                # Parses HTML from site
                soup = bs(page, features="html5lib")

                # Loops each story and collects its title and link in seperate lists
                links = []
                titles = []
                for storyLink in soup.find_all('a', class_="storylink"):
                        link = storyLink.get("href")
                        links.append(link)
                        title = storyLink.string
                        titles.append(title)
                
                # Loops through each article and collects its Hacker News score in a list
                articleScores = []
                for score in soup.find_all('span', class_="score"):
                    scores = score.string
                    articleScores.append(scores)

                # Loops each article and scrapes the age since posted to Hacker News
                # This is specific to when the scrape occurs
                ages = []
                for x in soup.find_all('span', class_='age'):
                    age = x.string
                    ages.append(age)
                
                # Used a variable because this line is used in other blocks and its easier to read
                more = soup.find_all('a', class_="morelink")

                # Loops through more to find morelink and collect href for further page scraping
                for x in more:
                    moreLink = x.get("href")

                # This block allows the scraper to continue scraping if there are more pages to be scraped.
                if bool(more) == True:
                    #time.sleep(30)
                    try:
                        page = req.urlopen("https://news.ycombinator.com/" + moreLink)

                        # Initial page used to set the column headings
                        if pageCount == 1:
                            print(pageCount)
                            pageCount += 1

                            with open(self.completeName, 'a') as f:
                                csv_writer = csv.writer(f)
                                csv_writer.writerow(["TITLES", "LINKS", "SCORE", "AGE"])

                                f.close()

                        else:
                            print(pageCount)
                            pageCount += 1

                            with open(self.completeName, 'a') as f:
                                csv_writer = csv.writer(f)

                                rows = zip(titles, links, articleScores, ages)
                                for row in rows:
                                    csv_writer.writerow(row)

                                f.close()

                            if bool(more) == False:
                                break

                        # Set page count to however many pages you would like to scrape
                        # or comment out this entire block to scrape the entire site
                        #if pageCount == 300:
                            #break

                        #else:
                            #pageCount += 1
                            #continue

                    except:
                        return print("Could not make request!")

                else:
                    with open(self.completeName, 'a') as f:
                        csv_writer = csv.writer(f)

                        rows = zip(titles, links, articleScores, ages)
                        for row in rows:
                            csv_writer.writerow(row)

                        f.close()

                    break

        except:
            return print("Could not make request!")

        try:
            emailFunction.email(self.fileName + ".csv")

        except:
            return print("Could not send email!")
            
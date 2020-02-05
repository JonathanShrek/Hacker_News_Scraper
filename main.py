import scrape

def main():
    url = "https://news.ycombinator.com/"
    savePath = "/home/term1nal/Documents/HackerNews/"
    
    scraper = scrape.Scrape(url, savePath)
    
    # Executes the scrape
    scraper.hackScraper()
    
if __name__ == '__main__':
    main()
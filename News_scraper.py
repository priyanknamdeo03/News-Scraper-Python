import requests
import bs4
import json

URL = 'https://www.ndtv.com/top-stories'
FILE_NAME = 'news.html'  

class News:
    # initializing the class members
    def __init__(self, url: str, filename: str) -> None:
        self.list_of_news_articles = [] 
        self.url = url
        self.filename = filename
        self.response = requests.get(self.url)
        self.soup = bs4.BeautifulSoup(self.response.text, "html.parser") 

    # ----------------------------------------------------------------------

    # Saving the parsed Website code in Local File
    def save_code(self) -> None:
        formatted_text = self.soup.prettify()

        with open(self.filename, "w", encoding="utf-8") as file:
            file.write(formatted_text)

    # ----------------------------------------------------------------------

    #  Extracting The webpage Code ,Parsing and saving the HTTP request data in a Local file
    def news_article_scraping(self) -> None:
        news_article = self.soup.find('div', class_='lisingNews')
        
        for i in news_article.find_all('div', class_='news_Itm adBg'):
            i.decompose()

        news_tags = news_article.find_all('div', class_='news_Itm')
        count = 0

        for news in news_tags:
            article_number = count
            article_name = news.find('h2', class_='newsHdng').text
            news_agency_name = news.find('span', class_='posted-by').text.replace(' ', '').strip().split("|")[0]
            news_published_date = news.find('span', class_='posted-by').text.split("|")[1].strip().split(",")[0]
            news_info = news.find('p', class_='newsCont').text
            news_link = news.find('h2', class_='newsHdng').find('a')['href']
            count += 1
            
            data = {  
                'News Post Number': article_number,
                'Article_Name': article_name,
                'News Publishing Agency Name': news_agency_name,
                'News Published Date': news_published_date,
                'News Info': news_info,
                'News Link': news_link
                }
            self.list_of_news_articles.append(data)

        with open(f'News Articles.json', 'w') as file:  
            json.dump(self.list_of_news_articles, file, indent=4)
        print(f'{count} New Articles Saved In : News Articles.json')


def main() -> None:
    daily_news = News(URL, FILE_NAME)
    daily_news.save_code()
    daily_news.news_article_scraping()


if __name__ == "__main__":
    try:
        main()
    except Exception as e: 
        print("Exception", e)









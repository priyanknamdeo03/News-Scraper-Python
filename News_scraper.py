import requests
import bs4
import json
import time


class News:
    # initializing the class members
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename
        self.response = requests.get(self.url)  # Object
        self.soup = bs4.BeautifulSoup(self.response.text, "html.parser")
        self.list_of_news_articles = []

    # ----------------------------------------------------------------------

    # Saving the parsed Website code in Local File
    def save_code(self):
        formatted_text = self.soup.prettify()
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write(formatted_text)

    # ----------------------------------------------------------------------

    #   Extracting The webpage Code ,Parsing and saving the Http request data in a Local file
    def news_article_scraping(self):

        news_article = self.soup.find('div', class_='lisingNews')
        for i in news_article.find_all('div', class_='news_Itm adBg'):
            i.decompose()

        n = news_article.find_all('div', class_='news_Itm')
        count = 0
        for news in n:
            article_number = count
            article_name = news.find('h2', class_='newsHdng').text
            news_agency_name = news.find('span', class_='posted-by').text.replace(' ', '').split("|")[0]
            news_published_date = news.find('span', class_='posted-by').text.split("|")[0].split(",")[0]
            # news_location = news.find('span', class_='posted-by').text.split("|")[1].split(",")
            # print(news_location)
            news_info = news.find('p', class_='newsCont').text
            news_link = news.find('h2', class_='newsHdng').find('a')['href']
            count += 1
            # print(count)
            data = {'News Post Number': article_number,
                    'Article_Name': article_name,
                    'News Publishing Agency Name': news_agency_name,
                    'News Published Date': news_published_date,
                    # 'News Published Location': news_location,
                    'News Info': news_info,
                    'News Link': news_link
                    }
            self.list_of_news_articles.append(data)
        # print(self.list_of_news_articles)
        with open(f'News Articles.json', 'w') as f:
            json.dump(self.list_of_news_articles, f, indent=4)
        print(f'{count} New Articles Saved In : News Articles.json')


def main():
    url = 'https://www.ndtv.com/top-stories'
    file_name = 'news.html'  # input("Enter Filename with Extension To Store The Parsed News-site : ")
    # while True:
    n = News(url, file_name)
    n.save_code()
    n.news_article_scraping()
    # print("Waiting For 30 Seconds........")
    # time.sleep(30)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
    # main()









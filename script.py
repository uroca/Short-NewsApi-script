import requests
import json
import os
from config import *

'''
Created in python 3.7.7
pip dependencies list present in requirements.txt
'''

amp = '&'
new_line_string: str = "\n"
embedded_quote: str = '"'
comma = ','


class ApiCall:

    @staticmethod
    def get_everything(keywords, keywords_in_title, start_date, end_date):

        string = 'https://newsapi.org/v2/everything'
        if (keywords):
            string = ApiCall._add_keyword(string, keywords)
            if (keywords_in_title):
                string = ApiCall._add_keywords_in_title(string, keywords, False)
        else:
            if (keywords_in_title):
                string = ApiCall._add_keywords_in_title(string, keywords_in_title, True)
            else:
                print('Error! We need either a keyword or title keywords!!!')
                quit()

        if (start_date):
            string = ApiCall._add_start(string, start_date)
        if (end_date):
            string = ApiCall._add_end(string, end_date)
        string = ApiCall._add_apiKey(string)
        print('Url used is ' + string)
        response = requests.get(string)
        process_url_response(response)

    @staticmethod
    def _add_keyword(string, keyword):
        return string + '?q=' + keyword

    @staticmethod
    def _add_keywords_in_title(string, keywords_in_title, is_first_parameter):
        if is_first_parameter:
            return string + '?qInTitle=' + keywords_in_title
        else:
            return string + amp + 'qInTitle=' + keywords_in_title

    @staticmethod
    def _add_start(string, start_date):
        return string + amp + 'from=' + start_date

    @staticmethod
    def _add_end(string, end_date):
        return string + amp + 'end=' + end_date

    @staticmethod
    def _add_apiKey(string):
        return string + amp + 'apiKey=' + api_key


class Article:

    def __init__(self, source_id, source_name, author, title, description, url, published_at, content, url_to_image):
        self.source_id = source_id
        self.source_name = source_name
        self.author = author
        self.title = title
        self.description = description
        self.url = url
        self.published_at = published_at
        self.content = content
        self.url_to_image = url_to_image


def process_url_response(response):
    json_result = json.loads(response.text)
    json_articles = json_result['articles']
    number_of_articles = len(json_articles)

    print('Results for this query: {}'.format(json_result['totalResults']))
    print('Articles returned: {}'.format(number_of_articles))

    list_of_articles = []
    for i in range(0, number_of_articles):
        new_article = convert_json_to_article(json_articles[i])
        list_of_articles.append(new_article)

    csv_lines = create_csv_lines(list_of_articles)
    save_file(csv_lines)

    print('Number of articles created: {}'.format(len(list_of_articles)))


def create_csv_lines(articles):
    titles = 'source_id, source_name, author, title, description, url, published_at, content, url_to_image'
    lines = [titles]
    for article in articles:
        new_line = (add_cell_to_line(article.source_id)
                    + add_cell_to_line(article.source_name)
                    + add_cell_to_line(article.author)
                    + add_cell_to_line(article.title.replace('"', "'"))
                    + add_cell_to_line(article.description.replace('"', "'"))
                    + add_cell_to_line(article.url)
                    + add_cell_to_line(article.published_at)
                    + add_cell_to_line(article.content.replace('"', "'"))
                    + add_cell_to_line(article.url_to_image))
        lines.append(new_line)
    return lines


def add_cell_to_line(cell_content):
    if cell_content is None:
        cell_content = ''
    return embedded_quote + cell_content + embedded_quote + comma


def save_file(lines):
    file_path = 'output.csv'
    if os.path.exists(file_path):
        os.remove(file_path)
    with open(file_path, 'a') as f:
        for one_line in lines:
            f.write(one_line + "\n")
        f.close()


def convert_json_to_article(json_article):
    new_article = Article(json_article['source']['id'],
                          json_article['source']['name'],
                          json_article['author'],
                          json_article['title'],
                          json_article['description'],
                          json_article['url'],
                          json_article['publishedAt'],
                          json_article['content'],
                          json_article['urlToImage'])
    return new_article


if __name__ == "__main__":
    keywords = None  # can be none, only if keywords_in_title contains a value
    keywords_in_title = 'racism'  # can be none, only if keywords contains a value
    start_date = '2020-06-18'  # can be none e.g. start_date = None
    end_date = '2020-06-18'  # can be none e.g. end_date = None

    ApiCall.get_everything(keywords, keywords_in_title, start_date, end_date)

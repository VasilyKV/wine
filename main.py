from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import collections
import datetime 
import pandas


WINERY_CREATED_YEAR = 1920

def get_wines_list(filename):
    wines = pandas.read_excel(filename, sheet_name='Лист1',keep_default_na=False).to_dict('records')
    wine_categorized = collections.defaultdict(list)
    for wine in wines:
        wine_categorized[wine['Категория']].append(wine)
    return wine_categorized


env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('template.html')

winery_age = datetime.datetime.now().year - WINERY_CREATED_YEAR
rendered_page = template.render(
    winery_age = winery_age,
    wines = get_wines_list('wine3.xlsx')
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()

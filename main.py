import collections
import datetime
import os

import pandas
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler

WINERY_CREATED_YEAR = 1920

def get_products(filename):
    products = pandas.read_excel(filename, sheet_name='Лист1',keep_default_na=False).to_dict('records')
    product_categorized = collections.defaultdict(list)
    for product in products:
        product_categorized[product['Категория']].append(product)
    return product_categorized

def main():
    load_dotenv()
    product_catalog_path = os.getenv('CATALOG_PATH', default='product_catalog.xlsx')
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    winery_age = datetime.datetime.now().year - WINERY_CREATED_YEAR
    rendered_page = template.render(
        winery_age = winery_age,
        products = get_products(product_catalog_path)
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()

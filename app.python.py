from flask import Flask, render_template, request, redirect, url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    product_data = fetch_product_data(url)
    if not product_data:
        return "Failed to retrieve data. Please check the URL and try again."

    return render_template('result.html', product=product_data)

@app.route('/compare', methods=['POST'])
def compare():
    urls = request.form.getlist('urls')
    products = [fetch_product_data(url) for url in urls]s
    return render_template('compare.html', products=products)

def fetch_product_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Example scraping logic for a smartphone product
    product_data = {
        'title': soup.find('span', {'id': 'productTitle'}).get_text(strip=True),
        'price': soup.find('span', {'id': 'priceblock_ourprice'}).get_text(strip=True),
        'features': [li.get_text(strip=True) for li in soup.find('div', {'id': 'feature-bullets'}).find_all('li')],
        'image_url': soup.find('img', {'id': 'landingImage'})['src']
    }

    return product_data

if __name__ == '__main__':
    app.run(debug=True)

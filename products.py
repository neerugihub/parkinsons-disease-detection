from flask import Flask, jsonify, request
import requests
from urllib.parse import urlencode

app = Flask(_name_)


TEST_SERVER_URL = "http://20.244.56.144/test/companies/:companyname/categories/:categoryname/products?top=n&minPri ce=p&maxPrice=q"

COMPANY_URLS = {
    "AMZ": "AMZ",
    "FLP": "FLP",
    "SNP": "SNP",
    "MYN": "MYN",
    "AZO": "AZO"
}

@app.route('/categories/<category_name>/products')
def get_top_products(category_name):
    # Extract query parameters
    top_n = request.args.get('top', type=int, default=10)
    min_price = request.args.get('minPrice', type=int, default=None)
    max_price = request.args.get('maxPrice', type=int, default=None)
    sort_by = request.args.get('sortBy', type=str, default=None)
    sort_order = request.args.get('sortOrder', type=str, default=None)
    page = request.args.get('page', type=int, default=1)

 
    params = {
        "top": top_n,
        "minPrice": min_price,
        "maxPrice": max_price
    }
    if sort_by:
        params['sortBy'] = sort_by
    if sort_order:
        params['sortOrder'] = sort_order

    products = []
    for company, url in COMPANY_URLS.items():
        company_url = f"{TEST_SERVER_URL}{url}/categories/{category_name}/products?{urlencode(params)}"
        try:
            response = requests.get(company_url)
            if response.status_code == 200:
                company_products = response.json()
                products.extend(company_products)
        except requests.RequestException as e:
            print(f"Error fetching products from {company}: {e}")


    start_index = (page - 1) * top_n
    end_index = start_index + top_n
    paginated_products = products[start_index:end_index]

    return jsonify(paginated_products)

@app.route('/categories/<category_name>/products/<product_id>')
def get_product_details(category_name, product_id):
    # You can implement this endpoint to fetch details of a specific product using its ID
    # This may involve making additional calls to the test server or using cached data
    pass

if _name_ == '_main_':
    app.run(host='0.0.0.0', port=9876)

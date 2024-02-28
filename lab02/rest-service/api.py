import json
import os

from flask import Flask, request, jsonify, abort, send_file

app = Flask(__name__)

product_db: dict[int, 'Product'] = {}
last_id = 0


def check_exist(product_id):
    if product_id not in product_db:
        abort(404, description="Resource not found")


class Product:
    last_id = 0
    base_path = "rest-service/files/"

    def __init__(self, name=None, description=None):
        self.id = self._id_generator()
        self.name = name if name is not None else "default-name"
        self.description = description if description is not None else "default-description"
        self.image_path = None

    def to_json(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.image_path
        })

    def save_image(self, file):
        if not os.path.exists(Product.base_path + f'{self.id}'):
            os.makedirs(Product.base_path + f'{self.id}')
        file.save(Product.base_path + f'{self.id}/{file.filename}')
        self.image_path = Product.base_path + f'{self.id}/{file.filename}'

    @staticmethod
    def _id_generator():
        Product.last_id += 1
        return Product.last_id


@app.route('/')
def hello_world():
    return "Hello! I'm a budding online retailer!"


@app.route('/product', methods=['POST'])
def new_product():
    if request.is_json:
        name = request.json.get("name")
        description = request.json.get("description")
        product = Product(name, description)
        product_db[product.id] = product
        return product.to_json()
    else:
        return jsonify({"error": "Invalid format"}), 400


@app.route('/product/<product_id>', methods=['GET'])
def get_product(product_id):
    product_id = int(product_id)
    check_exist(product_id)
    return product_db[product_id].to_json()


@app.route('/product/<product_id>', methods=['PUT'])
def update_product(product_id):
    product_id = int(product_id)
    check_exist(product_id)

    data_to_update = request.json
    if new_name := data_to_update.get('name'):
        product_db[product_id].name = new_name
    if new_description := data_to_update.get('description'):
        product_db[product_id].description = new_description
    return product_db[product_id].to_json()


@app.route('/product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    product_id = int(product_id)
    check_exist(product_id)

    product = product_db.pop(product_id)
    return product.to_json()


@app.route('/products', methods=['GET'])
def dump_products():
    return jsonify([p.to_json() for p in product_db.values()])


@app.route('/product/<product_id>/image', methods=['POST'])
def add_product_img(product_id):
    product_id = int(product_id)
    check_exist(product_id)
    if 'icon' not in request.files:
        return 'No file', 400
    file = request.files['icon']
    product_db[product_id].save_image(file)
    return 'File uploaded successfully'


@app.route('/product/<product_id>/image', methods=['GET'])
def get_product_img(product_id):
    product_id = int(product_id)
    check_exist(product_id)
    path = product_db[product_id].image_path
    return send_file(path[path.find('/') + 1:], as_attachment=True)


if __name__ == '__main__':
    app.run()

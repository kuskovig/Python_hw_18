import json


def get_product_info():
    with open("test_data/newproduct.json") as file:
        jsonfile = json.load(file)
    return jsonfile


product = get_product_info()

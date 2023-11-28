import json
from get_database import get_laptop_collection


def load_laptops() -> list:
    f = open("data/6-laptops-dataset.json")
    data = json.load(f)
    f.close()
    return data


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    print("starting script")
    collection_name = get_laptop_collection()
    laptops = load_laptops()
    print("inserting")
    collection_name.insert_many(laptops)
    print("done :)")

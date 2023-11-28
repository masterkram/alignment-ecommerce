import json
from get_database import get_laptop_collection


# Get the collection
collection = get_laptop_collection()

# Get a document from the collection
sample_document = collection.find_one()

# Print the attribute names
if sample_document:
    attribute_names = list(sample_document.keys())
    print("Attribute names in the collection:", attribute_names)
    # Save attribute names to a JSON file
    json_file_path = "data/attribute_names.json"
    with open(json_file_path, "w") as json_file:
        json.dump(attribute_names, json_file)
else:
    print("Collection is empty or does not exist.")

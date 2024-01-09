import elasticsearch
import elasticsearch.helpers
import json
import dotenv
from dotenv import load_dotenv
import os

load_dotenv(verbose=True, override=True)

cloud_id = os.getenv("ES_CLOUD")
api_key = os.getenv("API_KEY")


def read_documents(file_name):
    """
    Returns a generator of documents to be indexed by elastic, read from file_name
    """
    with open(file_name, "r") as json_file:
        data = json.load(json_file)
        for laptop in data:
            doc = {"_index": index_name, "_source": laptop}
            yield doc


def create_index(es, index_name, body={}):
    # delete index when it already exists
    es.indices.delete(index=index_name, ignore=[400, 404])
    # create the index
    es.indices.create(index=index_name, body=body)


def index_documents(es, collection_file_name, index_name, body={}):
    create_index(es, index_name, body)
    # bulk index the documents from file_name
    return elasticsearch.helpers.bulk(
        es,
        read_documents(collection_file_name),
        index=index_name,
        chunk_size=2000,
        request_timeout=30,
    )


def test_query(client):
    count_query = {"query": {"match_all": {}}}

    document_count = client.count(index=index_name, body=count_query)

    num_documents = document_count["count"]

    print(f"Number of documents in index '{index_name}': {num_documents}")


def create_client(local=False):
    if local:
        return elasticsearch.Elasticsearch(["http://localhost:9200"])
    return elasticsearch.Elasticsearch(api_key=api_key, cloud_id=cloud_id)


if __name__ == "__main__":
    index_name = "laptops"
    client = create_client()
    print(client.ping())
    print(client.info())
    body = {}  # no indexing options (leave default)
    index_documents(client, "data/6-laptops-dataset.json", index_name, body)
    test_query(client)

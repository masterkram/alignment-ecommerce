import elasticsearch
import elasticsearch.helpers
import json
import dotenv
from dotenv import load_dotenv
import os

load_dotenv(verbose=True)

es_host = os.getenv("ES_CLOUD")

es = elasticsearch.Elasticsearch(cloud_id=es_host)

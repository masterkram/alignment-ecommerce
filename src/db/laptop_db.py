import elasticsearch
from .Laptop import *
import streamlit as st


class LaptopDatabase:
    def __init__(
        self,
        cloud_based=True,
        cloud_id="Laptops:ZXVyb3BlLXdlc3Q0LmdjcC5lbGFzdGljLWNsb3VkLmNvbSRiNGMwYjBlMDVkMDc0NDJmYjQwNDhkZDljNTFiNTNhZiRjNTk2MmQ5ZDFkZWY0ODY0YThmMmM0M2NhOTRjYThmMg==",
        url="http://localhost:9200",
        api_key=st.secrets["ELASTIC_CLOUD_KEY"],
    ):
        # using local docker container
        if cloud_based:
            self.es = elasticsearch.Elasticsearch(cloud_id=cloud_id, api_key=api_key)
        else:
            self.es = elasticsearch.Elasticsearch([url])

    def search_laptops(self, query: str) -> list[Laptop]:
        """Search ElasticSearch index with a lucene query."""

        # Define the search query
        search_body = {
            "query": {
                "query_string": {
                    "query": query,
                }
            }
        }

        # Perform the search
        result = self.es.search(index="laptops", body=search_body)

        # Return the results
        if result and "hits" in result and "hits" in result["hits"]:
            return [laptopFromJson(x) for x in result["hits"]["hits"]]

        return []

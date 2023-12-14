import elasticsearch


class LaptopDatabase:
    def __init__(self, url="http://localhost:9200"):
        self.es = elasticsearch.Elasticsearch([url])

    def search_laptops(self, query: str) -> list:
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
            return result["hits"]["hits"]

        return []

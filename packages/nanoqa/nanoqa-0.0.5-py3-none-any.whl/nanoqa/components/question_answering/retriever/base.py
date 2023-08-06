from typing import List, Optional, Dict

from ...document_store.lexical import ElasticsearchDocumentStore
from ....schemas import Document


def compose_es_query(weight_text=0.8, weight_title=0.5):
    return """
            {
                "query": {
                    "multi_match": {
                        "query": ${query},
                        "type": "most_fields",
                        "fields": ["title^""" + str(weight_title) + """", "content^""" + str(weight_text) + """"]
                    }
                },
                "highlight": {
                    "fields": {
                        "content": {
                            "fragment_size": 100000000
                        }
                    }
                }
            }"""


class Retriever:
    def __init__(self, document_store: ElasticsearchDocumentStore, top_k: int = 10):
        self.document_store = document_store
        self.top_k = top_k

    def retrieve(
            self, query: str, filters: dict = None, top_k: Optional[int] = None,
            index: Optional[str] = None, fields: Optional[Dict[str, float]] = None) -> List[Document]:
        if top_k is None:
            top_k = self.top_k
        if index is None:
            index = self.document_store.index
        if fields is None:
            fields = {"content": 1.0, "title": 0.0}

        return self.document_store.query(query, filters, top_k, custom_query=compose_es_query(
            weight_text=fields.get("content", 1.0), weight_title=fields.get("title", 0)), index=index)

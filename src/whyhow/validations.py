from dataclasses import dataclass

import pinecone
from neo4j import GraphDatabase


@dataclass
class VerifyConnectivity:
    neo4j_url: str
    neo4j_user: str
    neo4j_password: str
    pinecone_api_key: str

    def __post_init__(self):
        self._verify_neo4j_connectivity()

    def _verify_neo4j_connectivity(self):
        auth = (self.neo4j_user, self.neo4j_password)

        with GraphDatabase.driver(self.neo4j_url, auth=auth) as driver:
            driver.verify_connectivity()

    def _verify_pinecone_connectivity(self):
        pc_client = pinecone.Pinecone(api_key=self.pinecone_api_key)
        pc_client.list_indexes()

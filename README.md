# WhyHow Knowledge Graph Creation SDK

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)
[![PyPI Version](https://img.shields.io/pypi/v/whyhow)](https://pypi.org/project/why/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue)](https://mypy-lang.org/)
[![Whyhow Discord](https://dcbadge.vercel.app/api/server/9bWqrsxgHr?compact=true&style=flat)](https://discord.gg/9bWqrsxgHr)

The WhyHow Knowledge Graph Creation SDK enables you to quickly and easily build automated knowledge graphs tailored to your unique worldview. Instantly build, extend, and query well-scoped KGs using a raw PDF and simple seed concepts in natural language. This version leverages OpenAI for embeddings and NLP, Pinecone serverless for scalable vector search and storage, and Neo4j for graph data storage and management.

# Installation

## Prerequisites

- Python 3.10 or higher
- [OpenAI API key](https://openai.com/)
- [Pinecone API key](https://www.pinecone.io/)
- [Neo4j credentials](https://neo4j.com/cloud/platform/aura-graph-database/) (username, password, and URL)

## Install from PyPI

You can install the SDK directly from PyPI using pip:

```shell
pip install whyhow

export OPENAI_API_KEY=<your openai api key>
export PINECONE_API_KEY=<your pinecone api key>
export NEO4J_URL=<your neo4j url>
export NEO4J_USERNAME=<your neo4j username>
export NEO4J_PASSWORD=<your neo4j password>
```

## Install from Github

Alternatively, you can clone the repo and install the package

```shell

git clone git@github.com:whyhow-ai/whyhow.git
cd whyhow
pip install .

export OPENAI_API_KEY=<your openai api key>
export PINECONE_API_KEY=<your pinecone api key>
export NEO4J_URL=<your neo4j url>
export NEO4J_USERNAME=<your neo4j username>
export NEO4J_PASSWORD=<your neo4j password>
```

# Examples

Navigate to the `examples/`.

# How to

## Initialize SDK

Import the SDK and initialize the client using your WhyHow API key.

```shell
from whyhow import WhyHow

client = WhyHow(api_key=<your whyhow api key>)
```

## Add documents to namespace

Your namespace is a logical grouping of the raw data you upload, the seed concepts you define, and the graphs you create. Namespaces are meant to be tightly scoped to your use case. You can create as many namespaces as you want.

```shell

namespace = "harry-potter"
documents = ["files/harry_potter_and_the_philosophers_stone.pdf","files/harry_potter_and_the_chamber_of_secrets.pdf"]

add_docs_response = client.graph.add_documents(namespace, documents)
print(add_docs_response)
# Adding your documents

```

## Create a graph

Tell the WhyHow SDK what you care about by providing a list of concepts in the form of natural language questions. Using these questions, we create a small ontology to guide extraction of entities and relationships that are most relevant to your use case. We then construct triples and generate a graph.

```shell

questions = ["What does Harry wear?","Who is Harry friends with?"]

create_graph_response = client.graph.create_graph(namespace, questions)
print(create_graph_response)
# Creating your graph

```

## Query a graph

Query your graph using natural language. Using your natural language query, we automatically construct a Cypher query to run against the graph stored in your Neo4j instance.

```shell

query = "What does Harry wear?"

query_response = client.graph.query_graph(namespace, query)
print(query_response)
# {answer: "Harry wears a cloak, glasses, robe, and Dudley's old clothes.", cypher_query: "MATCH (:Entity {name: "Harry"})-[:WEARS]->(clothing:Entity)\nRETURN clothing;"}

```

### Support

WhyHow.AI is building tools to help developers bring more determinism and control to their RAG pipelines using graph structures. If you're thinking about, in the process of, or have already incorporated knowledge graphs in RAG, we’d love to chat at team@whyhow.ai, or follow our newsletter at [WhyHow.AI](https://www.whyhow.ai/). Join our discussions about rules, determinism and knowledge graphs in RAG on our [Discord](https://discord.com/invite/9bWqrsxgHr).

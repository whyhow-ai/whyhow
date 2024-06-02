# Tutorial

This is a straightforward tutorial on how to build and query a knowledge graph using PDF texts of Harry Potter books using WhyHow SDK. This example will guide you through importing documents from the Harry Potter series into the knowledge graph, then querying it for insights related to the series.

## Environment Setup

Ensure you have the following:

- Python 3.10 or higher
- OpenAI API key
- Pinecone API key
- Neo4j credentials (username, password, and URL)

To keep your API keys and credentials secure, set them as environment variables. Open your terminal and run the following commands, substituting the placeholders with your actual data:

```shell
export WHYHOW_API_KEY=<YOUR_WHYHOW_API_KEY>
export PINECONE_API_KEY=<YOUR_PINECONE_API_KEY>
export OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
export NEO4J_USER=<YOUR_NEO4J_USERNAME>
export NEO4J_PASSWORD=<YOUR_NEO4J_PASSWORD>
export NEO4J_URL=<YOUR_NEO4J_DATABASE_URL>
```

## Install WhyHow SDK

If you haven't already, install the `WhyHow SDK` using pip:

```shell
pip install whyhow
```

## Configure the WhyHow Client

With your environment variables set, you can now configure the `WhyHow` client in your Python script. The client will automatically read in your environment variables, or you can override those values by specifying them in the client config.

```shell
import os
from whyhow import WhyHow

client = WhyHow(api_key=<your WhyHow API key>)
```

## Option 1 - Create the Knowledge Graph from a schema

First, you need to define the namespace for your project and specify the paths to your Harry Potter book documents. Your namespace is a logical grouping of the raw data you upload, the schema you define, and the graphs you create. Namespaces are meant to be tightly scoped to your use case. You can create as many namespaces as you want.

```shell
namespace = "harry-potter"
documents = [
    "path/to/harry_potter_and_the_philosophers_stone.pdf",
    "path/to/harry_potter_and_the_chamber_of_secrets.pdf"
    # Add paths to the rest of the Harry Potter series documents
]

# Add documents to your namespace
documents_response = client.graph.add_documents(namespace, documents)
print("Documents Added:", documents_response)

```

Next, you must create a schema which defines the entities, relationships, and patterns you'd like to use to construct the graph. Create this and save it as a JSON file.

```shell

#schema.json

{
  "entities": [
    {
      "name": "character",
      "description": "A person appearing in the book, e.g., Harry Potter, Ron Weasley, Hermione Granger, Albus Dumbledore."
    },
    {
      "name": "object",
      "description": "Inanimate items that characters use or interact with, e.g., wand, Philosopher's Stone, Invisibility Cloak, broomstick."
    }
  ],
  "relations": [
    {
      "name": "friends with",
      "description": "Denotes a friendly relationship between characters."
    },
    {
      "name": "interacts with",
      "description": "Describes a scenario in which a character engages with another character, creature, or object."
    },
  ],
  "patterns": [
    {
      "head": "character",
      "relation": "friends with",
      "tail": "character",
      "description": "One character is friends with another, e.g., Harry Potter is friends with Ron Weasley."
    },
    {
      "head": "character",
      "relation": "interacts with",
      "tail": "object",
      "description": "A character interacting with an object, e.g., Harry Potter interacts with the Invisibility Cloak."
    }
  ]
}

```

Then, create the graph using the schema and the uploaded documents:

```shell
# Create graph from schema

schema = "./schema.json"
create_graph_with_schema_response = client.graph.create_graph_from_schema(namespace, schema)
print(create_graph_with_schema_response)
# Creating your graph

```

## Option 2 - Create the Knowledge Graph from seed questions

Alternatively, you can create a graph using seed concepts in the form of questions written in natural language. We'll create a new namespace and upload the same data.

```shell
namespace = "harry-potter-2"
documents = [
    "path/to/harry_potter_and_the_philosophers_stone.pdf",
    "path/to/harry_potter_and_the_chamber_of_secrets.pdf"
    # Add paths to the rest of the Harry Potter series documents
]

# Add documents to your namespace
documents_response = client.graph.add_documents(namespace, documents)
print("Documents Added:", documents_response)

```

Create the knowledge graph from the seed questions and the uploaded documents:

```shell
questions = ["What does Harry look like?","What does Hermione look like?","What does Ron look like?"]
extracted_graph = client.graph.create_graph(namespace, questions)
print("Extracted Graph:", extracted_graph)

```

## Option 3 - Create the Knowledge Graph from CSV

WhyHow also supports creating a graph from structured data in the form a CSV file. Note, right now we only support creating a graph from one CSV file per namespace. If you upload more than one file, the first will be overwritten.

```shell
namespace = "specialists"
documents = ["../examples/assets/specialists.csv"]
schema_file = "../examples/assets/specialists.json"

# Automatically generate a schema
schema = client.graph.generate_schema(documents=documents)
print(schema)

# Add documents to your namespace
documents_response = client.graph.add_documents(
    namespace=namespace, documents=documents)

```

You can automatically generate a schema from a CSV document using the `generate_schema` method of the `GraphAPI` class.

```python
csv_documents = ["path/to/your/csv/file.csv"]
generated_schema = client.graph.generate_schema(documents=csv_documents)
print(generated_schema)
```

Use the `create_graph_from_csv` function to create a graph from the uploaded CSV file. The function will automatically use the schema provided to generate the graph

```shell
csv_graph = client.graph.create_graph_from_csv(
    namespace=namespace, schema_file=schema_file
)

print(csv_graph)

```

## Querying the Knowledge Graph

With the graphs created, you can now query them to find specific information:

```shell
# Query the graph created from csv using specific entities and relations
query = "Who speaks English and live in Houston?"
entities = ["English","Houston"]
relations = ["SPEAKS","LIVE_IN"]

specific_query_response = client.graph.query_graph_specific(
    namespace=namespace,
    query=query,
    entities=entities,
    relations=relations,
    include_triples=False,
    include_chunks=False,
)

print("Specific Query Response:", specific_query_response)

# Query graph created from schema
query = "Who is Harry friends with?"
namespace = "harry-potter"
schema_query_response = client.graph.query_graph(namespace, query)
print("Query Response:", query_response)

# Query graph created from seed questions
query = "Who wears a Cloak?"
namespace = "harry-potter-2"
seed_questions_query_response = client.graph.query_graph(namespace, query)
print("Query Response:", query_response)

# Include the triples in the return
query = "Who is Harry friends with?"
namespace = "harry-potter"
schema_query_response = client.graph.query_graph(namespace, query, include_triples = True)
print("Query Response:", query_response)

# Include the chunk context in the return
query = "Who is Harry friends with?"
namespace = "harry-potter"
schema_query_response = client.graph.query_graph(namespace, query, include_chunks = True)
print("Query Response:", query_response)
```

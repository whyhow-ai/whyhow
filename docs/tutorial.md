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

## Querying the Knowledge Graph

With the graphs created, you can now query them to find specific information:

```shell
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

```

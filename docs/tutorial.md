# Tutorial

This is a straightforward tutorial on how ot build and query a knowledge graph using PDF texts of Harry Potter books using WhyHow SDK. This example will guide you through importing documents from the Harry Potter series into the knowledge graph, then querying it for insights related to the series.

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

If you haven't already, install the `WhyHow SDK `using pip:

```shell
pip install whyhow
```

## Configure the WhyHow Client

With your environment variables set, you can now configure the `WhyHow` client in your Python script. The client will automatically read in your environment variables, or you can override those values by specifying them in the client config.

```shell
import os
from whyhow import WhyHow

client = WhyHow(api_key=<your WhyHow api key>)
```

## Creating the Knowledge Graph

Define the namespace for your project and specify the paths to your Harry Potter series documents. Your namespace is a logical grouping of the raw data you upload, the seed concepts you define, and the graphs you create. Namespaces are meant to be tightly scoped to your use case. You can create as many namespaces as you want.

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

Create the knowledge graph from the uploaded documents:

```shell
questions = ["What does Harry look like?","What does Hermione look like?","What does Ron look like?"]
extracted_graph = client.graph.create_graph(namespace, questions)
print("Extracted Graph:", extracted_graph)

```

## Querying the Knowledge Graph

With the graph created, you can now query it to find specific information. For example, to find out who wears a cloak:

```shell
query = "Who wears a Cloak?"
query_response = client.graph.query_graph(namespace, query)
print("Query Response:", query_response)

```

This query returns information based on the interactions and mentions of cloaks in the Harry Potter series. Even if you did not explicitly ask the SDK to extract information on cloaks and clothing, we are still able to uncover relevant information like this, illustrating the power of our AI-enabled knowledge graphs creation experience.

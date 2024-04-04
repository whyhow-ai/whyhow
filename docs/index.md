# Welcome to the WhyHow Automated Knowledge Graph Creation SDK Documentation

![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)
![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)

The WhyHow Knowledge Graph Creation SDK enables you to quickly and easily build automated knowledge graphs tailored to your unique worldview. Instantly build, extend, and query well-scoped KGs using a raw PDF and simple seed concepts in natural language.

## Key Features

- Instantaneously knowledge graphs using your documents and seed concepts (currently supports PDF files)
- Simple API for querying your knowledge graphs using natural language
- Bring your own keys for OpenAI, Pinecone, and Neo4j

## Getting Started

1. Install the package by following the [Installation Guide](installation.md)
2. Set up your OpenAI, Pinecone, and Neo4j credential as environment variables
3. Initialize the SDK with your WhyHow API key
4. Create a namespace and add raw documents using `graph.add_documents()`
5. Create a graph for the namespace using `graph.create_graph()` using a list of seed concepts
6. Query the graph with natural language using `graph.query_graph()`

For a detailed walkthrough and code examples, check out the [Tutorial](tutorial.md).

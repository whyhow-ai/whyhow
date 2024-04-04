# Installation

## Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Pinecone API key
- Neo4j credentials (username, password, and URL)

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

## Troubleshooting

If you encounter any issues during installation, please check the following:

- Ensure that you have Python 3.10 or higher installed. You can check your Python version by running `python --version` in your terminal.
- Make sure that you have correctly set the `OPENAI_API_KEY`, `PINECONE_API_KEY`, `NEO4J_URL`, `NEO4J_USERNAME`, `NEO4J_PASSWORD` environment variables with your respective credentials.
- If you are installing from GitHub, ensure that you have cloned the repository correctly and are in the right directory.
- If you are using a virtual environment, make sure that it is activated before running the installation commands.
- If you still face problems, please open an issue on the GitHub repository with detailed information about the error and your environment setup.

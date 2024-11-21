# Repository Contents

## File Structure

```
.github/
  └── ISSUE_TEMPLATE/
    └── 🐞-bug-report.md
    └── 💡-feature-request.md
  └── workflows/
    └── publish.yml
    └── python-package.yml
.gitignore
.vscode/
  └── settings.json
CODE_OF_CONDUCT.md
CONTRIBUTING.md
README.md
examples/
  └── checkpointing.ipynb
  └── custom_llm.py
fast_graphrag/
  └── __init__.py
  └── _exceptions.py
  └── _graphrag.py
  └── _llm/
    └── __init__.py
    └── _base.py
    └── _default.py
    └── _llm_openai.py
  └── _policies/
    └── __init__.py
    └── _base.py
    └── _graph_upsert.py
    └── _ranking.py
  └── _prompt.py
  └── _services/
    └── __init__.py
    └── _base.py
    └── _chunk_extraction.py
    └── _information_extraction.py
    └── _state_manager.py
  └── _storage/
    └── __init__.py
    └── _base.py
    └── _blob_pickle.py
    └── _default.py
    └── _gdb_igraph.py
    └── _ikv_pickle.py
    └── _namespace.py
    └── _vdb_hnswlib.py
  └── _types.py
  └── _utils.py
pyproject.toml
tests/
  └── __init__.py
  └── _graphrag_test.py
  └── _llm/
    └── __init__.py
    └── _base_test.py
    └── _llm_openai_test.py
  └── _policies/
    └── __init__.py
    └── _graph_upsert_test.py
    └── _ranking_test.py
  └── _services/
    └── __init__.py
    └── _chunk_extraction_test.py
    └── _information_extraction_test.py
  └── _storage/
    └── __init__.py
    └── _base_test.py
    └── _blob_pickle_test.py
    └── _gdb_igraph_test.py
    └── _ikv_pickle_test.py
    └── _namespace_test.py
    └── _vdb_hnswlib_test.py
  └── _types_test.py
  └── _utils_test.py```

## File Contents

### .github/ISSUE_TEMPLATE/🐞-bug-report.md

```markdown
---
name: "\U0001F41E Bug report"
about: Create a report to help us improve
title: ''
labels: ''
assignees: ''

---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Screenshots**
If applicable, add screenshots to help explain your problem.

**Additional context**
Add any other context about the problem here.

```

### .github/ISSUE_TEMPLATE/💡-feature-request.md

```markdown
---
name: "\U0001F4A1 Feature request"
about: Suggest an idea for this project
title: ''
labels: ''
assignees: ''

---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or screenshots about the feature request here.

```

### .github/workflows/publish.yml

```yaml
name: Publish Package

on:
    release:
        types: [published]

    workflow_dispatch: # TODO remove

jobs:
    build-n-publish:
        name: Build and publish to PyPI
        runs-on: ubuntu-22.04
        environment:
          name: pypi
          url: https://pypi.org/p/fast-graphrag
        permissions:
          id-token: write
        steps:
            - uses: actions/checkout@master

            - name: Set up Python 3.11
              uses: actions/setup-python@v1
              with:
                  python-version: 3.11

            - name: Install Poetry
              run: pipx install poetry==1.8.*

            - name: Cache Poetry virtual environment
              uses: actions/cache@v3
              with:
                  path: ~/.cache/pypoetry
                  key: ${{ runner.os }}-poetry-${{ hashFiles('**/poetry.lock') }}
                  restore-keys: |
                      ${{ runner.os }}-poetry-

            - name: Build
              run: poetry build

            - name: pypi-publish
              uses: pypa/gh-action-pypi-publish@v1.10.3
```

### .github/workflows/python-package.yml

```yaml
# This workflow will install Python dependencies, run tests and lint with a variety of Python versions
# For more information see: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python

name: Python package

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install ruff
        pipx install poetry
        poetry install
    - name: Lint with ruff
      run: |
        # Stop the build if there are Python syntax errors or undefined names
        ruff check . --select E9,F63,F7,F82 --show-files

        # Check with the same settings as the dev environment
        ruff check . --select E,W,F,I,B,C4,N,D --ignore C901,W191,D401 --show-files
        
        # Treat all errors as warnings with max line length and complexity constraints
        ruff check . --exit-zero --line-length 127 --select C901
    - name: Test with unittest
      run: |
        poetry run python -m unittest discover -s tests/ -p "*_test.py"

```

### .gitignore

```
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/
book_example/
book.txt

```

### .vscode/settings.json

```json
{
    "python.analysis.typeCheckingMode": "strict",
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        ".",
        "-p",
        "*_test.py"
    ],
    "python.testing.pytestEnabled": false,
    "python.testing.unittestEnabled": true
}
```

### CODE_OF_CONDUCT.md

```markdown
# Code of Conduct - Fast GraphRAG

## Our Pledge

In the interest of fostering an open and welcoming environment, we as
contributors and maintainers pledge to make participation in our project and
our community a harassment-free experience for everyone, regardless of age, body
size, disability, ethnicity, sex characteristics, gender identity and expression,
level of experience, education, socio-economic status, nationality, personal
appearance, race, religion, or sexual identity and orientation.

## Our Standards

Examples of behaviour that contributes to a positive environment for our
community include:

* Demonstrating empathy and kindness toward other people
* Being respectful of differing opinions, viewpoints, and experiences
* Giving and gracefully accepting constructive feedback
* Accepting responsibility and apologising to those affected by our mistakes,
and learning from the experience
* Focusing on what is best not just for us as individuals, but for the
overall community

Examples of unacceptable behaviour include:

* The use of sexualised language or imagery, and sexual attention or advances
* Trolling, insulting or derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or email
address, without their explicit permission
* Other conduct which could reasonably be considered inappropriate in a
professional setting

## Our Responsibilities

Project maintainers are responsible for clarifying and enforcing our standards of
acceptable behaviour and will take appropriate and fair corrective action in
response to any instances of unacceptable behaviour.

Project maintainers have the right and responsibility to remove, edit, or reject
comments, commits, code, wiki edits, issues, and other contributions that are
not aligned to this Code of Conduct, or to ban
temporarily or permanently any contributor for other behaviours that they deem
inappropriate, threatening, offensive, or harmful.

## Scope

This Code of Conduct applies within all community spaces, and also applies when
an individual is officially representing the community in public spaces.
Examples of representing our community include using an official e-mail address,
posting via an official social media account, or acting as an appointed
representative at an online or offline event.

## Enforcement

Instances of abusive, harassing, or otherwise unacceptable behaviour may be
reported to the community leaders responsible for enforcement at .
All complaints will be reviewed and investigated promptly and fairly.

All community leaders are obligated to respect the privacy and security of the
reporter of any incident.

## Attribution

This Code of Conduct is adapted from the [Contributor Covenant](https://contributor-covenant.org/), version
[1.4](https://www.contributor-covenant.org/version/1/4/code-of-conduct/code_of_conduct.md) and
[2.0](https://www.contributor-covenant.org/version/2/0/code_of_conduct/code_of_conduct.md),
and was generated by [contributing-gen](https://github.com/bttger/contributing-gen).

```

### CONTRIBUTING.md

```markdown
<!-- omit in toc -->
# Contributing to Fast GraphRAG

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions. 🎉

> And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
> - Star the project
> - Tweet about it
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues

<!-- omit in toc -->
## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Your First Code Contribution](#your-first-code-contribution)
- [Improving The Documentation](#improving-the-documentation)
- [Styleguides](#styleguides)
- [Commit Messages](#commit-messages)
- [Join The Project Team](#join-the-project-team)


## Code of Conduct

This project and everyone participating in it is governed by the
[Fast GraphRAG Code of Conduct](https://github.com/circlemind-ai/fast-graphrag/blob/main/CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to .


## I Have a Question

First off, make sure to join the discord community: https://discord.gg/McpuSEkR

Before you ask a question, it is best to search for existing [Issues](https://github.com/circlemind-ai/fast-graphrag/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/circlemind-ai/fast-graphrag/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (python, os, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

## I Want To Contribute

> ### Legal Notice <!-- omit in toc -->
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project licence.

### Reporting Bugs

<!-- omit in toc -->
#### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions. If you are looking for support, you might want to check Discord first.
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/circlemind-ai/fast-graphrag/issues?q=label%3Abug).
- Also make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
- Collect all important information about the bug

<!-- omit in toc -->
#### How Do I Submit a Good Bug Report?

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public. Instead sensitive bugs must be sent by email to security@circlemind.co

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/circlemind-ai/fast-graphrag/issues/new). (Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs-repro`. Bugs with the `needs-repro` tag will not be addressed until they are reproduced.
- If the team is able to reproduce the issue, it will be marked `needs-fix`, as well as possibly other tags (such as `critical`), and the issue will be left to be [implemented by someone](#your-first-code-contribution).

<!-- You might want to create an issue template for bugs and errors that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->


### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Fast GraphRAG, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

<!-- omit in toc -->
#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Perform a [search](https://github.com/circlemind-ai/fast-graphrag/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on/plugin library.

<!-- omit in toc -->
#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/circlemind-ai/fast-graphrag/issues).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- **Explain why this enhancement would be useful** to most Fast GraphRAG users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

```

### README.md

```markdown
<h1 align="center">
  <img width="800" src="banner.png" alt="circlemind fast-graphrag">
</h1>
<h4 align="center">
  <a href="https://github.com/circlemind-ai/fast-graphrag/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="fast-graphrag is released under the MIT license." />
  </a>
  <a href="https://github.com/circlemind-ai/fast-graphrag/blob/main/CONTRIBUTING.md">
    <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen" alt="PRs welcome!" />
  </a>
  <a href="https://circlemind.co">
    <img src="https://img.shields.io/badge/Project-Page-Green" alt="Circlemind Page" />
  </a>
  <img src="https://img.shields.io/badge/python->=3.10.1-blue">
</h4>
<p align="center">
  <p align="center"><b>Streamlined and promptable Fast GraphRAG framework designed for interpretable, high-precision, agent-driven retrieval workflows. <br> <a href="https://circlemind.co/"> Looking for a Managed Service? » </a> </b> </p>
</p>

<h4 align="center">
  <a href="#install">Install</a> |
  <a href="#quickstart">Quickstart</a> |
  <a href="https://discord.gg/DvY2B8u4sA">Community</a> |
  <a href="https://github.com/circlemind-ai/fast-graphrag/issues/new?assignees=&labels=&projects=&template=%F0%9F%90%9E-bug-report.md&title=">Report Bug</a> |
  <a href="https://github.com/circlemind-ai/fast-graphrag/issues/new?assignees=&labels=&projects=&template=%F0%9F%92%A1-feature-request.md&title=">Request Feature</a>
</h4>

> [!NOTE]
> Using *The Wizard of Oz*, `fast-graphrag` costs $0.08 vs. `graphrag` $0.48 — **a 6x costs saving** that further improves with data size and number of insertions. Stay tuned for the official benchmarks, and join us as a contributor!

## Features

- **Interpretable and Debuggable Knowledge:** Graphs offer a human-navigable view of knowledge that can be queried, visualized, and updated.
- **Fast, Low-cost, and Efficient:** Designed to run at scale without heavy resource or cost requirements.
- **Dynamic Data:** Automatically generate and refine graphs to best fit your domain and ontology needs.
- **Incremental Updates:** Supports real-time updates as your data evolves.
- **Intelligent Exploration:** Leverages PageRank-based graph exploration for enhanced accuracy and dependability.
- **Asynchronous & Typed:** Fully asynchronous, with complete type support for robust and predictable workflows.

Fast GraphRAG is built to fit seamlessly into your retrieval pipeline, giving you the power of advanced RAG, without the overhead of building and designing agentic workflows.

## Install

**Install from PyPi (recommended)**

```bash
pip install fast-graphrag
```

**Install from source**

```bash
# clone this repo first
cd fast_graphrag
poetry install
```

## Quickstart

Set the OpenAI API key in the environment:

```bash
export OPENAI_API_KEY="sk-..."
```

Download a copy of *A Christmas Carol* by Charles Dickens:

```bash
curl https://raw.githubusercontent.com/circlemind-ai/fast-graphrag/refs/heads/main/mock_data.txt > ./book.txt
```

Use the Python snippet below:

```python
from fast_graphrag import GraphRAG

DOMAIN = "Analyze this story and identify the characters. Focus on how they interact with each other, the locations they explore, and their relationships."

EXAMPLE_QUERIES = [
    "What is the significance of Christmas Eve in A Christmas Carol?",
    "How does the setting of Victorian London contribute to the story's themes?",
    "Describe the chain of events that leads to Scrooge's transformation.",
    "How does Dickens use the different spirits (Past, Present, and Future) to guide Scrooge?",
    "Why does Dickens choose to divide the story into \"staves\" rather than chapters?"
]

ENTITY_TYPES = ["Character", "Animal", "Place", "Object", "Activity", "Event"]

grag = GraphRAG(
    working_dir="./book_example",
    domain=DOMAIN,
    example_queries="\n".join(EXAMPLE_QUERIES),
    entity_types=ENTITY_TYPES
)

with open("./book.txt") as f:
    grag.insert(f.read())

print(grag.query("Who is Scrooge?").response)
```

The next time you initialize fast-graphrag from the same working directory, it will retain all the knowledge automatically.

## Examples
Please refer to the `examples` folder for a list of tutorial on common use cases of the library:
- `custom_llm.py`: a brief example on how to configure fast-graphrag to run with different OpenAI API compatible language models and embedders.

## Contributing

Whether it's big or small, we love contributions. Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated. Check out our [guide](https://github.com/circlemind-ai/fast-graphrag/blob/main/CONTRIBUTING.md) to see how to get started.

Not sure where to get started? You can join our [Discord](https://discord.gg/DvY2B8u4sA) and ask us any questions there.

## Philosophy

Our mission is to increase the number of successful GenAI applications in the world. To do that, we build memory and data tools that enable LLM apps to leverage highly specialized retrieval pipelines without the complexity of setting up and maintaining agentic workflows.

## Open-source or Managed Service

This repo is under the MIT License. See [LICENSE.txt](https://github.com/circlemind-ai/fast-graphrag/blob/main/LICENSE) for more information.

The fastest and most reliable way to get started with Fast GraphRAG is using our managed service. Your first 100 requests are free every month, after which you pay based on usage.

<h1 align="center">
  <img width="800" src="demo.gif" alt="circlemind fast-graphrag demo">
</h1>

To learn more about our managed service, [book a demo](https://circlemind.co/demo) or see our [docs](https://docs.circlemind.co/quickstart).

```

### examples/checkpointing.ipynb

```
{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Checkpointing in Fast GraphRAG\n",
    "\n",
    "To properly function, fast-graphrag mantains a state synchronised among different types of databases. It is highly unlikely, but it can happend that during any reading/writing operation any of these storages can get corrupted. So, we are introducing checkpointing to signficiantly reduce the impact of this unpleasant situation. To enable checkpointing, simply set `n_checkpoints = k`, with `k > 0`:"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from fast_graphrag import GraphRAG\n",
    "\n",
    "DOMAIN = \"Analyze this story and identify the characters. Focus on how they interact with each other, the locations they explore, and their relationships.\"\n",
    "\n",
    "EXAMPLE_QUERIES = [\n",
    "    \"What is the significance of Christmas Eve in A Christmas Carol?\",\n",
    "    \"How does the setting of Victorian London contribute to the story's themes?\",\n",
    "    \"Describe the chain of events that leads to Scrooge's transformation.\",\n",
    "    \"How does Dickens use the different spirits (Past, Present, and Future) to guide Scrooge?\",\n",
    "    \"Why does Dickens choose to divide the story into \\\"staves\\\" rather than chapters?\"\n",
    "]\n",
    "\n",
    "ENTITY_TYPES = [\"Character\", \"Animal\", \"Place\", \"Object\", \"Activity\", \"Event\"]\n",
    "\n",
    "grag = GraphRAG(\n",
    "    working_dir=\"./book_example\",\n",
    "    n_checkpoints=2,  # Number of checkpoints to keep\n",
    "    domain=DOMAIN,\n",
    "    example_queries=\"\\n\".join(EXAMPLE_QUERIES),\n",
    "    entity_types=ENTITY_TYPES\n",
    ")\n",
    "\n",
    "with open(\"./book.txt\") as f:\n",
    "    grag.insert(f.read())\n",
    "\n",
    "print(grag.query(\"Who is Scrooge?\").response)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "DONE! Now the library will automatically keep in memory the `k` most recent checkpoints and rollback to them if necessary."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "NOTES:\n",
    "- if you want to migrate a project from no checkpoints to checkpoints, simply set the flag and run a insert operation (even an empty one should do the job). Check that the checkpoint was created succesfully by querying the graph. If eveything worked correctly, you should see a new directory in you storage working dir (in the case above, it would be something like `./book_example/1731555907`). You can now safely remove all the files in the root dir `./book_example/*.*`.\n",
    "- if you want to stop using checkpoints, simply copy all the files from the most recent checkpoints folder in the root dir, delete all the \"number\" folders and unset `n_checkpoints`."
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "cm",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

```

### examples/custom_llm.py

```python
"""Example usage of GraphRAG with custom LLM and Embedding services compatible with the OpenAI API."""
from typing import List

from dotenv import load_dotenv

from fast_graphrag import GraphRAG
from fast_graphrag._llm import OpenAIEmbeddingService, OpenAILLMService

load_dotenv()

DOMAIN = ""
QUERIES: List[str] = []
ENTITY_TYPES: List[str] = []

working_dir = "./examples/ignore/hp"
grag = GraphRAG(
    working_dir=working_dir,
    domain=DOMAIN,
    example_queries="\n".join(QUERIES),
    entity_types=ENTITY_TYPES,
    config=GraphRAG.Config(
        llm_service=OpenAILLMService(model="your-llm-model", base_url="api.url.com", api_key="your-api-key"),
        embedding_service=OpenAIEmbeddingService(
            model="your-embedding-model",
            base_url="api.url.com",
            api_key="your-api-key",
            embedding_dim=512,  # the output embedding dim of the chosen model
        ),
    ),
)

```

### fast_graphrag/__init__.py

```python
"""Top-level package for GraphRAG."""

__all__ = ["GraphRAG", "QueryParam"]

from dataclasses import dataclass, field
from typing import Type

from fast_graphrag._llm import DefaultEmbeddingService, DefaultLLMService
from fast_graphrag._llm._base import BaseEmbeddingService
from fast_graphrag._llm._llm_openai import BaseLLMService
from fast_graphrag._policies._base import BaseGraphUpsertPolicy
from fast_graphrag._policies._graph_upsert import (
    DefaultGraphUpsertPolicy,
    EdgeUpsertPolicy_UpsertIfValidNodes,
    EdgeUpsertPolicy_UpsertValidAndMergeSimilarByLLM,
    NodeUpsertPolicy_SummarizeDescription,
)
from fast_graphrag._policies._ranking import RankingPolicy_TopK, RankingPolicy_WithThreshold
from fast_graphrag._services import (
    BaseChunkingService,
    BaseInformationExtractionService,
    BaseStateManagerService,
    DefaultChunkingService,
    DefaultInformationExtractionService,
    DefaultStateManagerService,
)
from fast_graphrag._storage import (
    DefaultGraphStorage,
    DefaultGraphStorageConfig,
    DefaultIndexedKeyValueStorage,
    DefaultVectorStorage,
    DefaultVectorStorageConfig,
)
from fast_graphrag._storage._namespace import Workspace
from fast_graphrag._types import TChunk, TEmbedding, TEntity, THash, TId, TIndex, TRelation

from ._graphrag import BaseGraphRAG, QueryParam


@dataclass
class GraphRAG(BaseGraphRAG[TEmbedding, THash, TChunk, TEntity, TRelation, TId]):
    """A class representing a Graph-based Retrieval-Augmented Generation system."""

    @dataclass
    class Config:
        """Configuration for the GraphRAG class."""

        chunking_service_cls: Type[BaseChunkingService[TChunk]] = field(default=DefaultChunkingService)
        information_extraction_service_cls: Type[BaseInformationExtractionService[TChunk, TEntity, TRelation, TId]] = (
            field(default=DefaultInformationExtractionService)
        )
        information_extraction_upsert_policy: BaseGraphUpsertPolicy[TEntity, TRelation, TId] = field(
            default_factory=lambda: DefaultGraphUpsertPolicy(
                config=NodeUpsertPolicy_SummarizeDescription.Config(),
                nodes_upsert_cls=NodeUpsertPolicy_SummarizeDescription,
                edges_upsert_cls=EdgeUpsertPolicy_UpsertIfValidNodes,
            )
        )
        state_manager_cls: Type[BaseStateManagerService[TEntity, TRelation, THash, TChunk, TId, TEmbedding]] = field(
            default=DefaultStateManagerService
        )

        llm_service: BaseLLMService = field(default_factory=lambda: DefaultLLMService())
        embedding_service: BaseEmbeddingService = field(default_factory=lambda: DefaultEmbeddingService())

        graph_storage: DefaultGraphStorage[TEntity, TRelation, TId] = field(
            default_factory=lambda: DefaultGraphStorage(DefaultGraphStorageConfig(node_cls=TEntity, edge_cls=TRelation))
        )
        entity_storage: DefaultVectorStorage[TIndex, TEmbedding] = field(
            default_factory=lambda: DefaultVectorStorage(
                DefaultVectorStorageConfig()
            )
        )
        chunk_storage: DefaultIndexedKeyValueStorage[THash, TChunk] = field(
            default_factory=lambda: DefaultIndexedKeyValueStorage(None)
        )

        entity_ranking_policy: RankingPolicy_WithThreshold = field(
            default_factory=lambda: RankingPolicy_WithThreshold(RankingPolicy_WithThreshold.Config(threshold=0.005))
        )
        relation_ranking_policy: RankingPolicy_TopK = field(
            default_factory=lambda: RankingPolicy_TopK(RankingPolicy_TopK.Config(top_k=32))
        )
        chunk_ranking_policy: RankingPolicy_TopK = field(
            default_factory=lambda: RankingPolicy_TopK(RankingPolicy_TopK.Config(top_k=8))
        )
        node_upsert_policy: NodeUpsertPolicy_SummarizeDescription = field(
            default_factory=lambda: NodeUpsertPolicy_SummarizeDescription()
        )
        edge_upsert_policy: EdgeUpsertPolicy_UpsertValidAndMergeSimilarByLLM = field(
            default_factory=lambda: EdgeUpsertPolicy_UpsertValidAndMergeSimilarByLLM()
        )

        def __post_init__(self):
            """Initialize the GraphRAG Config class."""
            self.entity_storage.embedding_dim = self.embedding_service.embedding_dim

    config: Config = field(default_factory=Config)

    def __post_init__(self):
        """Initialize the GraphRAG class."""
        self.llm_service = self.config.llm_service
        self.embedding_service = self.config.embedding_service
        self.chunking_service = self.config.chunking_service_cls()
        self.information_extraction_service = self.config.information_extraction_service_cls(
            graph_upsert=self.config.information_extraction_upsert_policy
        )
        self.state_manager = self.config.state_manager_cls(
            workspace=Workspace.new(self.working_dir, keep_n=self.n_checkpoints),
            embedding_service=self.embedding_service,
            graph_storage=self.config.graph_storage,
            entity_storage=self.config.entity_storage,
            chunk_storage=self.config.chunk_storage,
            entity_ranking_policy=self.config.entity_ranking_policy,
            chunk_ranking_policy=self.config.chunk_ranking_policy,
            node_upsert_policy=self.config.node_upsert_policy,
            edge_upsert_policy=self.config.edge_upsert_policy,
        )

```

### fast_graphrag/_exceptions.py

```python
class InvalidStorageError(Exception):
    """Exception raised for errors in the storage operations."""

    def __init__(self, message: str = "Invalid storage operation"):
        self.message = message
        super().__init__(self.message)


class InvalidStorageUsageError(Exception):
    """Exception raised for errors in the usage of the storage."""

    def __init__(self, message: str = "Invalid usage of the storage"):
        self.message = message
        super().__init__(self.message)


class LLMServiceNoResponseError(Exception):
    """Exception raised when the LLM service does not provide a response."""

    def __init__(self, message: str = "LLM service did not provide a response"):
        self.message = message
        super().__init__(self.message)

```

### fast_graphrag/_graphrag.py

```python
"""This module implements a Graph-based Retrieval-Augmented Generation (GraphRAG) system."""

from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, Optional, Tuple, Union

from fast_graphrag._llm import BaseLLMService, format_and_send_prompt
from fast_graphrag._llm._base import BaseEmbeddingService
from fast_graphrag._policies._base import BaseEdgeUpsertPolicy, BaseGraphUpsertPolicy, BaseNodeUpsertPolicy
from fast_graphrag._prompt import PROMPTS
from fast_graphrag._services._chunk_extraction import BaseChunkingService
from fast_graphrag._services._information_extraction import BaseInformationExtractionService
from fast_graphrag._services._state_manager import BaseStateManagerService
from fast_graphrag._storage._base import BaseGraphStorage, BaseIndexedKeyValueStorage, BaseVectorStorage
from fast_graphrag._types import GTChunk, GTEdge, GTEmbedding, GTHash, GTId, GTNode, TContext, TDocument, TQueryResponse
from fast_graphrag._utils import TOKEN_TO_CHAR_RATIO, get_event_loop, logger


@dataclass
class InsertParam:
    pass


@dataclass
class QueryParam:
    with_references: bool = False
    only_context: bool = False
    entities_max_tokens: int = 4000
    relationships_max_tokens: int = 3000
    chunks_max_tokens: int = 9000


@dataclass
class BaseGraphRAG(Generic[GTEmbedding, GTHash, GTChunk, GTNode, GTEdge, GTId]):
    """A class representing a Graph-based Retrieval-Augmented Generation system."""

    working_dir: str = field()
    domain: str = field()
    example_queries: str = field()
    entity_types: List[str] = field()
    n_checkpoints: int = field(default=0)

    llm_service: BaseLLMService = field(init=False, default_factory=lambda: BaseLLMService())
    chunking_service: BaseChunkingService[GTChunk] = field(init=False, default_factory=lambda: BaseChunkingService())
    information_extraction_service: BaseInformationExtractionService[GTChunk, GTNode, GTEdge, GTId] = field(
        init=False,
        default_factory=lambda: BaseInformationExtractionService(
            graph_upsert=BaseGraphUpsertPolicy(
                config=None,
                nodes_upsert_cls=BaseNodeUpsertPolicy,
                edges_upsert_cls=BaseEdgeUpsertPolicy,
            )
        ),
    )
    state_manager: BaseStateManagerService[GTNode, GTEdge, GTHash, GTChunk, GTId, GTEmbedding] = field(
        init=False,
        default_factory=lambda: BaseStateManagerService(
            workspace=None,
            graph_storage=BaseGraphStorage[GTNode, GTEdge, GTId](config=None),
            entity_storage=BaseVectorStorage[GTId, GTEmbedding](config=None),
            chunk_storage=BaseIndexedKeyValueStorage[GTHash, GTChunk](config=None),
            embedding_service=BaseEmbeddingService(),
            node_upsert_policy=BaseNodeUpsertPolicy(config=None),
            edge_upsert_policy=BaseEdgeUpsertPolicy(config=None),
        ),
    )

    def insert(
        self,
        content: Union[str, List[str]],
        metadata: Union[List[Optional[Dict[str, Any]]], Optional[Dict[str, Any]]] = None,
        params: Optional[InsertParam] = None,
        show_progress: bool = True
    ) -> Tuple[int, int, int]:
        return get_event_loop().run_until_complete(self.async_insert(content, metadata, params, show_progress))

    async def async_insert(
        self,
        content: Union[str, List[str]],
        metadata: Union[List[Optional[Dict[str, Any]]], Optional[Dict[str, Any]]] = None,
        params: Optional[InsertParam] = None,
        show_progress: bool = True
    ) -> Tuple[int, int, int]:
        """Insert a new memory or memories into the graph.

        Args:
            content (str | list[str]): The data to be inserted. Can be a single string or a list of strings.
            metadata (dict, optional): Additional metadata associated with the data. Defaults to None.
            params (InsertParam, optional): Additional parameters for the insertion. Defaults to None.
            show_progress (bool, optional): Whether to show the progress bar. Defaults to True.
        """
        if params is None:
            params = InsertParam()

        if isinstance(content, str):
            content = [content]
        if isinstance(metadata, dict):
            metadata = [metadata]

        if metadata is None or isinstance(metadata, dict):
            data = (TDocument(data=c, metadata=metadata or {}) for c in content)
        else:
            data = (TDocument(data=c, metadata=m or {}) for c, m in zip(content, metadata))

        await self.state_manager.insert_start()
        try:
            # Chunk the data
            chunked_documents = await self.chunking_service.extract(data=data)

            # Filter the chunks checking for duplicates
            new_chunks_per_data = await self.state_manager.filter_new_chunks(chunks_per_data=chunked_documents)

            # Extract entities and relationships from the new chunks only
            subgraphs = self.information_extraction_service.extract(
                llm=self.llm_service,
                documents=new_chunks_per_data,
                prompt_kwargs={
                    "domain": self.domain,
                    "example_queries": self.example_queries,
                    "entity_types": ",".join(self.entity_types),
                },
                entity_types=self.entity_types,
            )
            if len(subgraphs) == 0:
                logger.info("No new entities or relationships extracted from the data.")

            # Update the graph with the new entities, relationships, and chunks
            await self.state_manager.upsert(
                llm=self.llm_service, subgraphs=subgraphs, documents=new_chunks_per_data, show_progress=show_progress
            )

            # Return the total number of entities, relationships, and chunks
            return (
                await self.state_manager.get_num_entities(),
                await self.state_manager.get_num_relations(),
                await self.state_manager.get_num_chunks(),
            )
        except Exception as e:
            logger.error(f"Error during insertion: {e}")
            raise e
        finally:
            await self.state_manager.insert_done()

    def query(self, query: str, params: Optional[QueryParam] = None) -> TQueryResponse[GTNode, GTEdge, GTHash, GTChunk]:
        async def _query() -> TQueryResponse[GTNode, GTEdge, GTHash, GTChunk]:
            try:
                await self.state_manager.query_start()
                answer = await self.async_query(query, params)
                return answer
            except Exception as e:
                logger.error(f"Error during query: {e}")
                raise e
            finally:
                await self.state_manager.query_done()

        return get_event_loop().run_until_complete(_query())

    async def async_query(
        self, query: str, params: Optional[QueryParam] = None
    ) -> TQueryResponse[GTNode, GTEdge, GTHash, GTChunk]:
        """Query the graph with a given input.

        Args:
            query (str): The query string to search for in the graph.
            params (QueryParam, optional): Additional parameters for the query. Defaults to None.

        Returns:
            TQueryResponse: The result of the query (response + context).
        """
        if params is None:
            params = QueryParam()

        # Extract entities from query
        extracted_entities = await self.information_extraction_service.extract_entities_from_query(
            llm=self.llm_service, query=query, prompt_kwargs={}
        )

        # Retrieve relevant state
        relevant_state = await self.state_manager.get_context(query=query, entities=extracted_entities)
        if relevant_state is None:
            return TQueryResponse[GTNode, GTEdge, GTHash, GTChunk](
                response=PROMPTS["fail_response"], context=TContext([], [], [])
            )

        # Ask LLM
        if params.only_context:
            llm_response = ""
        else:
            llm_response, _ = await format_and_send_prompt(
                prompt_key="generate_response_query_with_references"
                if params.with_references
                else "generate_response_query_no_references",
                llm=self.llm_service,
                format_kwargs={
                    "query": query,
                    "context": relevant_state.to_str(
                        {
                            "entities": params.entities_max_tokens * TOKEN_TO_CHAR_RATIO,
                            "relationships": params.relationships_max_tokens * TOKEN_TO_CHAR_RATIO,
                            "chunks": params.chunks_max_tokens * TOKEN_TO_CHAR_RATIO,
                        }
                    ),
                },
                response_model=str,
            )

        return TQueryResponse[GTNode, GTEdge, GTHash, GTChunk](response=llm_response, context=relevant_state)

```

### fast_graphrag/_llm/__init__.py

```python
__all__ = [
    "BaseLLMService",
    "BaseEmbeddingService",
    "DefaultEmbeddingService",
    "DefaultLLMService",
    "format_and_send_prompt",
    "OpenAIEmbeddingService",
    "OpenAILLMService",
]

from ._base import BaseEmbeddingService, BaseLLMService, format_and_send_prompt
from ._default import DefaultEmbeddingService, DefaultLLMService
from ._llm_openai import OpenAIEmbeddingService, OpenAILLMService

```

### fast_graphrag/_llm/_base.py

```python
"""LLM Services module."""

from dataclasses import dataclass, field
from typing import Any, Optional, Tuple, Type

import numpy as np

from fast_graphrag._prompt import PROMPTS
from fast_graphrag._types import GTResponseModel


async def format_and_send_prompt(
    prompt_key: str,
    llm: "BaseLLMService",
    format_kwargs: dict[str, Any],
    response_model: Type[GTResponseModel] | None = None,
    **args: Any,
) -> Tuple[GTResponseModel, list[dict[str, str]]]:
    """Get a prompt, format it with the supplied args, and send it to the LLM.

    Args:
        prompt_key (str): The key for the prompt in the PROMPTS dictionary.
        llm (BaseLLMService): The LLM service to use for sending the message.
        response_model (Type[GTResponseModel]): The expected response model.
        format_kwargs (dict[str, Any]): Dictionary of arguments to format the prompt.
        model (str | None): The model to use for the LLM. Defaults to None.
        max_tokens (int | None): The maximum number of tokens for the response. Defaults to None.
        **args (Any): Additional keyword arguments to pass to the LLM.

    Returns:
        GTResponseModel: The response from the LLM.
    """
    # Get the prompt from the PROMPTS dictionary
    prompt = PROMPTS[prompt_key]

    # Format the prompt with the supplied arguments
    formatted_prompt = prompt.format(**format_kwargs)

    # Send the formatted prompt to the LLM
    return await llm.send_message(prompt=formatted_prompt, response_model=response_model, **args)


@dataclass
class BaseLLMService:
    """Base class for Language Model implementations."""

    model: Optional[str] = field(default=None)
    base_url: Optional[str] = field(default=None)
    api_key: Optional[str] = field(default=None)
    llm_async_client: Any = field(init=False, default=None)

    async def send_message(
        self,
        prompt: str,
        model: str | None = None,
        system_prompt: str | None = None,
        history_messages: list[dict[str, str]] | None = None,
        response_model: Type[GTResponseModel] | None = None,
        **kwargs: Any,
    ) -> Tuple[GTResponseModel, list[dict[str, str]]]:
        """Send a message to the language model and receive a response.

        Args:
            prompt (str): The input message to send to the language model.
            model (str): The name of the model to use.
            system_prompt (str, optional): The system prompt to set the context for the conversation. Defaults to None.
            history_messages (list, optional): A list of previous messages in the conversation. Defaults to empty.
            response_model (Type[T], optional): The Pydantic model to parse the response. Defaults to None.
            **kwargs: Additional keyword arguments that may be required by specific LLM implementations.

        Returns:
            str: The response from the language model.
        """
        raise NotImplementedError


@dataclass
class BaseEmbeddingService:
    """Base class for Language Model implementations."""

    embedding_dim: int = field(default=1536)
    model: Optional[str] = field(default="text-embedding-3-small")
    base_url: Optional[str] = field(default=None)
    api_key: Optional[str] = field(default=None)

    embedding_async_client: Any = field(init=False, default=None)

    async def get_embedding(
        self, texts: list[str], model: Optional[str] = None
    ) -> np.ndarray[Any, np.dtype[np.float32]]:
        """Get the embedding representation of the input text.

        Args:
            texts (str): The input text to embed.
            model (str): The name of the model to use.

        Returns:
            list[float]: The embedding vector as a list of floats.
        """
        raise NotImplementedError

```

### fast_graphrag/_llm/_default.py

```python
__all__ = ['DefaultLLMService', 'DefaultEmbeddingService']

from ._llm_openai import OpenAIEmbeddingService, OpenAILLMService


class DefaultLLMService(OpenAILLMService):
    pass
class DefaultEmbeddingService(OpenAIEmbeddingService):
    pass

```

### fast_graphrag/_llm/_llm_openai.py

```python
"""LLM Services module."""

import asyncio
from dataclasses import dataclass, field
from itertools import chain
from typing import Any, List, Optional, Tuple, Type, cast

import instructor
import numpy as np
from openai import APIConnectionError, AsyncOpenAI, RateLimitError
from pydantic import BaseModel
from tenacity import (
    AsyncRetrying,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from fast_graphrag._exceptions import LLMServiceNoResponseError
from fast_graphrag._types import BTResponseModel, GTResponseModel
from fast_graphrag._utils import TOKEN_TO_CHAR_RATIO, logger, throttle_async_func_call

from ._base import BaseEmbeddingService, BaseLLMService

TIMEOUT_SECONDS = 180.0


@dataclass
class OpenAILLMService(BaseLLMService):
    """LLM Service for OpenAI LLMs."""

    model: Optional[str] = field(default="gpt-4o-mini")

    def __post_init__(self):
        logger.debug("Initialized OpenAILLMService with patched OpenAI client.")
        self.llm_async_client: instructor.AsyncInstructor = instructor.from_openai(
            AsyncOpenAI(base_url=self.base_url, api_key=self.api_key, timeout=TIMEOUT_SECONDS)
        )

    @throttle_async_func_call(max_concurrent=256, stagger_time=0.001, waitting_time=0.001)
    async def send_message(
        self,
        prompt: str,
        model: str | None = None,
        system_prompt: str | None = None,
        history_messages: list[dict[str, str]] | None = None,
        response_model: Type[GTResponseModel] | None = None,
        **kwargs: Any,
    ) -> Tuple[GTResponseModel, list[dict[str, str]]]:
        """Send a message to the language model and receive a response.

        Args:
            prompt (str): The input message to send to the language model.
            model (str): The name of the model to use. Defaults to the model provided in the config.
            system_prompt (str, optional): The system prompt to set the context for the conversation. Defaults to None.
            history_messages (list, optional): A list of previous messages in the conversation. Defaults to empty.
            response_model (Type[T], optional): The Pydantic model to parse the response. Defaults to None.
            **kwargs: Additional keyword arguments that may be required by specific LLM implementations.

        Returns:
            str: The response from the language model.
        """
        logger.debug(f"Sending message with prompt: {prompt}")
        model = model or self.model
        if model is None:
            raise ValueError("Model name must be provided.")
        messages: list[dict[str, str]] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            logger.debug(f"Added system prompt: {system_prompt}")

        if history_messages:
            messages.extend(history_messages)
            logger.debug(f"Added history messages: {history_messages}")

        messages.append({"role": "user", "content": prompt})

        llm_response: GTResponseModel = await self.llm_async_client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore
            response_model=response_model.Model
            if response_model and issubclass(response_model, BTResponseModel)
            else response_model,
            **kwargs,
            max_retries=AsyncRetrying(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)),
        )

        if not llm_response:
            logger.error("No response received from the language model.")
            raise LLMServiceNoResponseError("No response received from the language model.")

        messages.append(
            {
                "role": "assistant",
                "content": llm_response.model_dump_json() if isinstance(llm_response, BaseModel) else str(llm_response),
            }
        )
        logger.debug(f"Received response: {llm_response}")

        if response_model and issubclass(response_model, BTResponseModel):
            llm_response = cast(GTResponseModel, cast(BTResponseModel.Model, llm_response).to_dataclass(llm_response))

        return llm_response, messages


@dataclass
class OpenAIEmbeddingService(BaseEmbeddingService):
    """Base class for Language Model implementations."""

    embedding_dim: int = field(default=1536)
    max_request_tokens: int = 8000
    model: Optional[str] = field(default="text-embedding-3-small")

    def __post_init__(self):
        self.embedding_async_client: AsyncOpenAI = AsyncOpenAI(
            base_url=self.base_url, api_key=self.api_key, timeout=TIMEOUT_SECONDS
        )
        logger.debug("Initialized OpenAIEmbeddingService with OpenAI client.")

    async def get_embedding(
        self, texts: list[str], model: Optional[str] = None
    ) -> np.ndarray[Any, np.dtype[np.float32]]:
        """Get the embedding representation of the input text.

        Args:
            texts (str): The input text to embed.
            model (str, optional): The name of the model to use. Defaults to the model provided in the config.

        Returns:
            list[float]: The embedding vector as a list of floats.
        """
        logger.debug(f"Getting embedding for texts: {texts}")
        model = model or self.model
        if model is None:
            raise ValueError("Model name must be provided.")

        # Chunk the requests to size limits
        max_chunk_length = self.max_request_tokens * TOKEN_TO_CHAR_RATIO
        text_chunks: List[List[str]] = []

        current_chunk: List[str] = []
        current_chunk_length = 0
        for text in texts:
            text_length = len(text)
            if text_length + current_chunk_length > max_chunk_length:
                text_chunks.append(current_chunk)
                current_chunk = []
                current_chunk_length = 0
            current_chunk.append(text)
            current_chunk_length += text_length
        text_chunks.append(current_chunk)

        response = await asyncio.gather(*[self._embedding_request(chunk, model) for chunk in text_chunks])

        data = chain(*[r.data for r in response])
        embeddings = np.array([dp.embedding for dp in data])
        logger.debug(f"Received embedding response: {len(embeddings)} embeddings")

        return embeddings

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((RateLimitError, APIConnectionError, TimeoutError)),
    )
    async def _embedding_request(self, input: List[str], model: str) -> Any:
        return await self.embedding_async_client.embeddings.create(model=model, input=input, encoding_format="float")

```

### fast_graphrag/_policies/__init__.py

```python

```

### fast_graphrag/_policies/_base.py

```python
from dataclasses import dataclass, field
from typing import Any, Generic, Iterable, Tuple, Type

from scipy.sparse import csr_matrix

from fast_graphrag._llm._llm_openai import BaseLLMService
from fast_graphrag._storage._base import BaseGraphStorage
from fast_graphrag._types import GTEdge, GTId, GTNode, TIndex


@dataclass
class BasePolicy:
    config: Any = field()


####################################################################################################
# GRAPH UPSERT POLICIES
####################################################################################################


@dataclass
class BaseNodeUpsertPolicy(BasePolicy, Generic[GTNode, GTId]):
    async def __call__(
        self, llm: BaseLLMService, target: BaseGraphStorage[GTNode, GTEdge, GTId], source_nodes: Iterable[GTNode]
    ) -> Tuple[BaseGraphStorage[GTNode, GTEdge, GTId], Iterable[Tuple[TIndex, GTNode]]]:
        raise NotImplementedError


@dataclass
class BaseEdgeUpsertPolicy(BasePolicy, Generic[GTEdge, GTId]):
    async def __call__(
        self, llm: BaseLLMService, target: BaseGraphStorage[GTNode, GTEdge, GTId], source_edges: Iterable[GTEdge]
    ) -> Tuple[BaseGraphStorage[GTNode, GTEdge, GTId], Iterable[Tuple[TIndex, GTEdge]]]:
        raise NotImplementedError


@dataclass
class BaseGraphUpsertPolicy(BasePolicy, Generic[GTNode, GTEdge, GTId]):
    nodes_upsert_cls: Type[BaseNodeUpsertPolicy[GTNode, GTId]] = field()
    edges_upsert_cls: Type[BaseEdgeUpsertPolicy[GTEdge, GTId]] = field()
    _nodes_upsert: BaseNodeUpsertPolicy[GTNode, GTId] = field(init=False)
    _edges_upsert: BaseEdgeUpsertPolicy[GTEdge, GTId] = field(init=False)

    def __post_init__(self):
        self._nodes_upsert = self.nodes_upsert_cls(self.config)
        self._edges_upsert = self.edges_upsert_cls(self.config)

    async def __call__(
        self,
        llm: BaseLLMService,
        target: BaseGraphStorage[GTNode, GTEdge, GTId],
        source_nodes: Iterable[GTNode],
        source_edges: Iterable[GTEdge],
    ) -> Tuple[
        BaseGraphStorage[GTNode, GTEdge, GTId],
        Iterable[Tuple[TIndex, GTNode]],
        Iterable[Tuple[TIndex, GTEdge]],
    ]:
        raise NotImplementedError


####################################################################################################
# RANKING POLICIES
####################################################################################################


class BaseRankingPolicy(BasePolicy):
    def __call__(self, scores: csr_matrix) -> csr_matrix:
        assert scores.shape[0] == 1, "Ranking policies only supports batch size of 1"
        return scores

```

### fast_graphrag/_policies/_graph_upsert.py

```python
import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import chain
from typing import Counter, Dict, Iterable, List, Optional, Set, Tuple, Union

from fast_graphrag._llm._base import format_and_send_prompt
from fast_graphrag._llm._llm_openai import BaseLLMService
from fast_graphrag._prompt import PROMPTS
from fast_graphrag._storage._base import BaseGraphStorage
from fast_graphrag._types import GTEdge, GTId, GTNode, TEditRelationList, TEntity, THash, TId, TIndex, TRelation
from fast_graphrag._utils import logger

from ._base import BaseEdgeUpsertPolicy, BaseGraphUpsertPolicy, BaseNodeUpsertPolicy


async def summarize_entity_description(
    prompt: str, description: str, llm: BaseLLMService, max_tokens: Optional[int] = None
) -> str:
    """Summarize the given entity description."""
    if max_tokens is not None:
        raise NotImplementedError("Summarization with max tokens is not yet supported.")
    # Prompt
    entity_description_summarization_prompt = prompt

    # Extract entities and relationships
    formatted_entity_description_summarization_prompt = entity_description_summarization_prompt.format(
        description=description
    )
    new_description, _ = await llm.send_message(
        prompt=formatted_entity_description_summarization_prompt, response_model=str, max_tokens=max_tokens
    )

    return new_description


####################################################################################################
# DEFAULT GRAPH UPSERT POLICIES
####################################################################################################


@dataclass
class DefaultNodeUpsertPolicy(BaseNodeUpsertPolicy[GTNode, GTId]):
    async def __call__(
        self, llm: BaseLLMService, target: BaseGraphStorage[GTNode, GTEdge, GTId], source_nodes: Iterable[GTNode]
    ) -> Tuple[BaseGraphStorage[GTNode, GTEdge, GTId], Iterable[Tuple[TIndex, GTNode]]]:
        upserted: Dict[TIndex, GTNode] = {}
        for node in source_nodes:
            _, index = await target.get_node(node)
            if index is not None:
                await target.upsert_node(node=node, node_index=index)
            else:
                index = await target.upsert_node(node=node, node_index=None)
            upserted[index] = node

        return target, upserted.items()


@dataclass
class DefaultEdgeUpsertPolicy(BaseEdgeUpsertPolicy[GTEdge, GTId]):
    async def __call__(
        self, llm: BaseLLMService, target: BaseGraphStorage[GTNode, GTEdge, GTId], source_edges: Iterable[GTEdge]
    ) -> Tuple[BaseGraphStorage[GTNode, GTEdge, GTId], Iterable[Tuple[TIndex, GTEdge]]]:
        indices = await target.insert_edges(source_edges)

        r: Iterable[Tuple[TIndex, GTEdge]]
        if len(indices):
            r = zip(indices, source_edges)
        else:
            r = []
        return target, r


@dataclass
class DefaultGraphUpsertPolicy(BaseGraphUpsertPolicy[GTNode, GTEdge, GTId]):  # noqa: N801
    async def __call__(
        self,
        llm: BaseLLMService,
        target: BaseGraphStorage[GTNode, GTEdge, GTId],
        source_nodes: Iterable[GTNode],
        source_edges: Iterable[GTEdge],
    ) -> Tuple[
        BaseGraphStorage[GTNode, GTEdge, GTId],
        Iterable[Tuple[TIndex, GTNode]],
        Iterable[Tuple[TIndex, GTEdge]],
    ]:
        target, upserted_nodes = await self._nodes_upsert(llm, target, source_nodes)
        target, upserted_edges = await self._edges_upsert(llm, target, source_edges)

        return target, upserted_nodes, upserted_edges


####################################################################################################
# NODE UPSERT POLICIES
####################################################################################################


@dataclass
class NodeUpsertPolicy_SummarizeDescription(BaseNodeUpsertPolicy[TEntity, TId]):  # noqa: N801
    @dataclass
    class Config:
        max_node_description_size: int = field(default=512)
        node_summarization_ratio: float = field(default=0.5)
        node_summarization_prompt: str = field(default=PROMPTS["summarize_entity_descriptions"])
        is_async: bool = field(default=True)

    config: Config = field(default_factory=Config)

    async def __call__(
        self, llm: BaseLLMService, target: BaseGraphStorage[TEntity, GTEdge, TId], source_nodes: Iterable[TEntity]
    ) -> Tuple[BaseGraphStorage[TEntity, GTEdge, TId], Iterable[Tuple[TIndex, TEntity]]]:
        upserted: List[Tuple[TIndex, TEntity]] = []

        async def _upsert_node(node_id: TId, nodes: List[TEntity]) -> Optional[Tuple[TIndex, TEntity]]:
            existing_node, index = await target.get_node(node_id)
            if existing_node:
                nodes.append(existing_node)

            # Resolve descriptions
            node_description = "  ".join((node.description for node in nodes))

            if len(node_description) > self.config.max_node_description_size:
                node_description = await summarize_entity_description(
                    self.config.node_summarization_prompt,
                    node_description,
                    llm,
                    # int(
                    #     self.config.max_node_description_size
                    #     * self.config.node_summarization_ratio
                    #     / TOKEN_TO_CHAR_RATIO
                    # ),
                )
                node_description = node_description.replace("\n", "  ")

            # Resolve types (pick most frequent)
            node_type = Counter((node.type for node in nodes)).most_common(1)[0][0]

            node = TEntity(name=node_id, description=node_description, type=node_type)
            index = await target.upsert_node(node=node, node_index=index)

            upserted.append((index, node))

        # Group nodes by name
        grouped_nodes: Dict[TId, List[TEntity]] = defaultdict(lambda: [])
        for node in source_nodes:
            grouped_nodes[node.name].append(node)

        if self.config.is_async:
            node_upsert_tasks = (_upsert_node(node_id, nodes) for node_id, nodes in grouped_nodes.items())
            await asyncio.gather(*node_upsert_tasks)
        else:
            for node_id, nodes in grouped_nodes.items():
                await _upsert_node(node_id, nodes)

        return target, upserted


####################################################################################################
# EDGE UPSERT POLICIES
####################################################################################################


@dataclass
class EdgeUpsertPolicy_UpsertIfValidNodes(BaseEdgeUpsertPolicy[TRelation, TId]):  # noqa: N801
    @dataclass
    class Config:
        is_async: bool = field(default=True)

    config: Config = field(default_factory=Config)

    async def __call__(
        self, llm: BaseLLMService, target: BaseGraphStorage[GTNode, TRelation, TId], source_edges: Iterable[TRelation]
    ) -> Tuple[BaseGraphStorage[GTNode, TRelation, TId], Iterable[Tuple[TIndex, TRelation]]]:
        new_edges: List[TRelation] = []

        async def _upsert_edge(edge: TRelation) -> Optional[Tuple[TIndex, TRelation]]:
            source_node, _ = await target.get_node(edge.source)
            target_node, _ = await target.get_node(edge.target)

            if source_node and target_node:
                new_edges.append(edge)

        if self.config.is_async:
            edge_upsert_tasks = (_upsert_edge(edge) for edge in source_edges)
            await asyncio.gather(*edge_upsert_tasks)
        else:
            for edge in source_edges:
                await _upsert_edge(edge)
        indices = await target.insert_edges(new_edges)

        r: Iterable[Tuple[TIndex, TRelation]]
        if len(indices):
            r = zip(indices, new_edges)
        else:
            r = []

        return target, r


@dataclass
class EdgeUpsertPolicy_UpsertValidAndMergeSimilarByLLM(BaseEdgeUpsertPolicy[TRelation, TId]):  # noqa: N801
    @dataclass
    class Config:
        edge_merge_threshold: int = field(default=5)
        is_async: bool = field(default=True)

    config: Config = field(default_factory=Config)

    async def _upsert_edge(
        self,
        llm: BaseLLMService,
        target: BaseGraphStorage[GTNode, TRelation, TId],
        edges: List[TRelation],
        source_entity: TId,
        target_entity: TId,
    ) -> Tuple[List[Tuple[TIndex, TRelation]], List[TRelation], List[TIndex]]:
        existing_edges = list(await target.get_edges(source_entity, target_entity))

        # Check if we need to run edges maintenance
        if (len(existing_edges) + len(edges)) > self.config.edge_merge_threshold:
            upserted_eges, new_edges, to_delete_edges = await self._merge_similar_edges(
                llm, target, existing_edges, edges
            )
        else:
            upserted_eges = []
            new_edges = edges
            to_delete_edges = []

        return upserted_eges, new_edges, to_delete_edges

    async def _merge_similar_edges(
        self,
        llm: BaseLLMService,
        target: BaseGraphStorage[GTNode, TRelation, TId],
        existing_edges: List[Tuple[TRelation, TIndex]],
        edges: List[TRelation],
    ) -> Tuple[List[Tuple[TIndex, TRelation]], List[TRelation], List[TIndex]]:
        """Merge similar edges between the same pair of nodes.

        Args:
            llm (BaseLLMService): The language model that is called to determine the similarity between edges.
            target (BaseGraphStorage[GTNode, TRelation, TId]): the graph storage to upsert the edges to.
            existing_edges (List[Tuple[TRelation, TIndex]]): list of existing edges in the main graph storage.
            edges (List[TRelation]): list of new edges to be upserted.

        Returns:
            Tuple[List[Tuple[TIndex, TRelation]], List[TIndex]]: return the pairs of inserted (index, edge),
            the new edges that were not merged, and the indices of the edges that are to be deleted.
        """
        updated_edges: List[Tuple[TIndex, TRelation]] = []
        new_edges: List[TRelation] = []
        map_incremental_to_edge: Dict[int, Tuple[TRelation, Union[TIndex, None]]] = {
            **dict(enumerate(existing_edges)),
            **{idx + len(existing_edges): (edge, None) for idx, edge in enumerate(edges)},
        }

        # Extract entities and relationships
        edge_grouping, _ = await format_and_send_prompt(
            prompt_key="edges_group_similar",
            llm=llm,
            format_kwargs={
                "edge_list": "\n".join(
                    (f"{idx}, {edge.description}" for idx, (edge, _) in map_incremental_to_edge.items())
                )
            },
            response_model=TEditRelationList,
        )

        visited_edges: Dict[TIndex, Union[TIndex, None]] = {}
        for edges_group in edge_grouping.groups:
            relation_indices = [
                index
                for index in edges_group.ids
                if index < len(existing_edges) + len(edges)  # Only consider valid indices
            ]
            if len(relation_indices) < 2:
                logger.info("LLM returned invalid index for edge maintenance, ignoring.")
                continue

            chunks: Set[THash] = set()

            for second in relation_indices[1:]:
                edge, index = map_incremental_to_edge[second]

                # Set visited edges only the first time we see them.
                # In this way, if an existing edge is marked for "not deletion" later, we do not overwrite it.
                if second not in visited_edges:
                    visited_edges[second] = index
                if edge.chunks:
                    chunks.update(edge.chunks)

            first_index = relation_indices[0]
            edge, index = map_incremental_to_edge[first_index]
            edge.description = edges_group.description.replace("\n", "  ")
            visited_edges[first_index] = None  # None means it was visited but not marked for deletion.
            if edge.chunks:
                chunks.update(edge.chunks)
            edge.chunks = list(chunks)
            if index is not None:
                updated_edges.append((await target.upsert_edge(edge, index), edge))
            else:
                new_edges.append(edge)

        for idx, edge in enumerate(edges):
            # If the edge was not visited, it means it was not grouped and must be inserted as new.
            if idx + len(existing_edges) not in visited_edges:
                new_edges.append(edge)
                # upserted_eges.append((await target.upsert_edge(edge, None), edge))

        # Only existing edges that were marked for deletion have non-None value which corresponds to their real index.
        return updated_edges, new_edges, [v for v in visited_edges.values() if v is not None]

    async def __call__(
        self, llm: BaseLLMService, target: BaseGraphStorage[GTNode, TRelation, TId], source_edges: Iterable[TRelation]
    ) -> Tuple[BaseGraphStorage[GTNode, TRelation, TId], Iterable[Tuple[TIndex, TRelation]]]:
        grouped_edges: Dict[Tuple[TId, TId], List[TRelation]] = defaultdict(lambda: [])
        upserted_edges: List[List[Tuple[TIndex, TRelation]]] = []
        new_edges: List[List[TRelation]] = []
        to_delete_edges: List[List[TIndex]] = []
        for edge in source_edges:
            grouped_edges[(edge.source, edge.target)].append(edge)

        if self.config.is_async:
            edge_upsert_tasks = (
                self._upsert_edge(llm, target, edges, source_entity, target_entity)
                for (source_entity, target_entity), edges in grouped_edges.items()
            )
            tasks = await asyncio.gather(*edge_upsert_tasks)
            if len(tasks):
                upserted_edges, new_edges, to_delete_edges = zip(*tasks)
        else:
            tasks = [
                await self._upsert_edge(llm, target, edges, source_entity, target_entity)
                for (source_entity, target_entity), edges in grouped_edges.items()
            ]
            if len(tasks):
                upserted_edges, new_edges, to_delete_edges = zip(*tasks)
        await target.delete_edges_by_index(chain(*to_delete_edges))
        new_indices = await target.insert_edges(chain(*new_edges))
        return target, chain(*upserted_edges, zip(new_indices, chain(*new_edges)))

```

### fast_graphrag/_policies/_ranking.py

```python
from dataclasses import dataclass, field

import numpy as np
from scipy.sparse import csr_matrix

from ._base import BaseRankingPolicy


class RankingPolicy_WithThreshold(BaseRankingPolicy):  # noqa: N801
    @dataclass
    class Config:
        threshold: float = field(default=0.05)

    config: Config = field()

    def __call__(self, scores: csr_matrix) -> csr_matrix:
        # Remove scores below threshold
        scores.data[scores.data < self.config.threshold] = 0
        scores.eliminate_zeros()

        return scores


class RankingPolicy_TopK(BaseRankingPolicy):  # noqa: N801
    @dataclass
    class Config:
        top_k: int = field(default=10)

    top_k: Config = field()

    def __call__(self, scores: csr_matrix) -> csr_matrix:
        assert scores.shape[0] == 1, "TopK policy only supports batch size of 1"
        if scores.nnz <= self.config.top_k:
            return scores

        smallest_indices = np.argpartition(scores.data, -self.config.top_k)[:-self.config.top_k]
        scores.data[smallest_indices] = 0
        scores.eliminate_zeros()

        return scores


class RankingPolicy_Elbow(BaseRankingPolicy):  # noqa: N801
    def __call__(self, scores: csr_matrix) -> csr_matrix:
        assert scores.shape[0] == 1, "Elbow policy only supports batch size of 1"
        if scores.nnz <= 1:
            return scores

        sorted_scores = np.sort(scores.data)

        # Compute elbow
        diff = np.diff(sorted_scores)
        elbow = np.argmax(diff) + 1

        smallest_indices = np.argpartition(scores.data, elbow)[:elbow]
        scores.data[smallest_indices] = 0
        scores.eliminate_zeros()

        return scores


class RankingPolicy_WithConfidence(BaseRankingPolicy):  # noqa: N801
    def __call__(self, scores: csr_matrix) -> csr_matrix:
        raise NotImplementedError("Confidence policy is not supported yet.")

```

### fast_graphrag/_prompt.py

```python
"""Prompts."""

from typing import Any, Dict

PROMPTS: Dict[str, Any] = {}

## NEW
PROMPTS["entity_relationship_extraction"] = """You are a helpful assistant that helps a human analyst perform information discovery in the following domain.

# DOMAIN
{domain}

# GOAL
Given a document and a list of types, first, identify all present entities of those types and, then, all relationships among the identified entities.
Your goal is to highlight information that is relevant to the domain and the questions that may be asked on it.

Examples of possible questions:
{example_queries}

# STEPS
1. Identify all entities of the given types. Make sure to extract all and only the entities that are of one of the given types, ignore the others. Use singular names and split compound concepts when necessary (for example, from the sentence "they are movie and theater directors", you should extract the entities "movie director" and "theater director").
2. Identify all relationships between the entities found in step 1. Clearly resolve pronouns to their specific names to maintain clarity.
3. Double check that each entity identified in step 1 appears in at least one relationship. If not, add the missing relationships.

# EXAMPLE DATA
Types: [location, organization, person, communication]
Document: Radio City: Radio City is India's first private FM radio station and was started on 3 July 2001. It plays Hindi, English and regional songs. Radio City recently forayed into New Media in May 2008 with the launch of a music portal - PlanetRadiocity.com that offers music related news, videos, songs, and other music-related features."

Output:
{{
	"entities": [
	{{"name": "Radio City", "type": "organization", "desc": "Radio City is India's first private FM radio station."}},
	{{"name": "India", "type": "location", "desc": "The country of India."}},
	{{"name": "FM radio station", "type": "communication", "desc": "A radio station that broadcasts using frequency modulation."}},
	{{"name": "English", "type": "communication", "desc": "The English language."}},
	{{"name": "Hindi", "type": "communication", "desc": "The Hindi language."}},
	{{"name": "New Media", "type": "communication", "desc": "New Media is a term for all forms of media that are digital and/or interactive."}},
	{{"name": "PlanetRadiocity.com", "type": "organization", "desc": "PlanetRadiocity.com is an online music portal."}},
	{{"name": "music portal", "type": "communication", "desc": "A website that offers music related information."}},
	{{"name": "news", "type": "communication", "desc": "The concept of news."}},
	{{"name": "video", "type": "communication", "desc": "The concept of a video."}},
	{{"name": "song", "type": "communication", "desc": "The concept of a song."}}
	],
	"relationships": [
	{{"source": "Radio City", "target": "India", "desc": "Radio City is located in India."}},
	{{"source": "Radio City", "target": "FM radio station", "desc": "Radio City is a private FM radio station started on 3 July 2001."}},
	{{"source": "Radio City", "target": "English", "desc": "Radio City broadcasts English songs."}},
	{{"source": "Radio City", "target": "Hindi", "desc": "Radio City broadcasts songs in the Hindi language."}},
	{{"source": "Radio City", "target": "PlanetRadiocity.com", "desc": "Radio City launched PlanetRadiocity.com in May 2008."}},
	{{"source": "PlanetRadiocity.com", "target": "music portal", "desc": "PlanetRadiocity.com is a music portal that offers music related news, videos and more."}}
	],
	"other_relationships": [
	{{"source": "Radio City", "target": "New Media", "desc": "Radio City forayed into New Media in May 2008."}},
	{{"source": "PlanetRadiocity.com", "target": "news", "desc": "PlanetRadiocity.com offers music related news."}},
	{{"source": "PlanetRadiocity.com", "target": "video", "desc": "PlanetRadiocity.com offers music related videos."}},
	{{"source": "PlanetRadiocity.com", "target": "song", "desc": "PlanetRadiocity.com offers songs."}}
	]
}}

# REAL DATA
Types: {entity_types}
Document: {input_text}

Output:
"""

PROMPTS["entity_relationship_continue_extraction"] = "MANY entities were missed in the last extraction.  Add them below using the same format:"

PROMPTS["entity_relationship_gleaning_done_extraction"] = "Retrospectively check if all entities have been correctly identified: answer done if so, or continue if there are still entities that need to be added."

PROMPTS["entity_extraction_query"] = """You are a helpful assistant that helps a human analyst identify all the named entities present in the input query that are important for answering the query.

# Example 1
Query: Do the magazines Arthur's Magazine or First for Women have the same publisher?
Ouput: {{"entities": ["Arthur's Magazine", "First for Women"], "n": 2}}

# Example 2
Query: Which film has the director who was born earlier, Avatar II: The Return or The Interstellar?
Ouput: {{"entities": ["Avatar II: The Return", "The Interstellar"], "n": 2}}

# INPUT
Query: {query}
Output:
"""


PROMPTS[
	"summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given the current description, summarize it in a shorter but comprehensive description. Make sure to include all important information.
If the provided description is contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.

Current description:
{description}

Updated description:
"""


PROMPTS[
	"edges_group_similar"
] = """You are a helpful assistant responsible for maintaining a list of facts describing the relations between two entities so that information is not redundant.
Given a list of ids and facts, identify any facts that should be grouped together as they contain similar or duplicated information and provide a new summarized description for the group.

# EXAMPLE
Facts (id, description):
0, Mark is the dad of Luke
1, Luke loves Mark
2, Mark is always ready to help Luke
3, Mark is the father of Luke
4, Mark loves Luke very much

Ouput:
{{
	grouped_facts: [
	{{
		'ids': [0, 3],
		'description': 'Mark is the father of Luke'
	}},
	{{
		'ids': [1, 4],
		'description': 'Mark and Luke love each other very much'
	}}
	]
}}

# INPUT:
Facts:
{edge_list}

Ouput:
"""

PROMPTS["generate_response_query_with_references"] = """You are a helpful assistant analyzing the given input data to provide an helpful response to the user query.

# INPUT DATA
{context}

# USER QUERY
{query}

# INSTRUCTIONS
Your goal is to provide a response to the user query using the relevant information in the input data:
- the "Entities" and "Relationships" tables contain high-level information. Use these tables to identify the most important entities and relationships to respond to the query.
- the "Sources" list contains raw text sources to help answer the query. It may contain noisy data, so pay attention when analyzing it.

Follow these steps:
1. Read and understand the user query.
2. Look at the "Entities" and "Relationships" tables to get a general sense of the data and understand which information is the most relevant to answer the query.
3. Carefully analyze all the "Sources" to get more detailed information. Information could be scattered across several sources, use the identified relevant entities and relationships to guide yourself through the analysis of the sources.
4. While you write the response, you must include inline references to the all the sources you are using by appending `[<source_id>]` at the end of each sentence, where `source_id` is the corresponding source ID from the "Sources" list.
5. Write the response to the user query - which must include the inline references - based on the information you have gathered. Be very concise and answer the user query directly. If the response cannot be inferred from the input data, just say no relevant information was found. Do not make anything up or add unrelevant information.

Answer:
"""

PROMPTS["generate_response_query_no_references"] = """You are a helpful assistant analyzing the given input data to provide an helpful response to the user query.

# INPUT DATA
{context}

# USER QUERY
{query}

# INSTRUCTIONS
Your goal is to provide a response to the user query using the relevant information in the input data:
- the "Entities" and "Relationships" tables contain high-level information. Use these tables to identify the most important entities and relationships to respond to the query.
- the "Sources" list contains raw text sources to help answer the query. It may contain noisy data, so pay attention when analyzing it.

Follow these steps:
1. Read and understand the user query.
2. Look at the "Entities" and "Relationships" tables to get a general sense of the data and understand which information is the most relevant to answer the query.
3. Carefully analyze all the "Sources" to get more detailed information. Information could be scattered across several sources, use the identified relevant entities and relationships to guide yourself through the analysis of the sources.
4. Write the response to the user query based on the information you have gathered. Be very concise and answer the user query directly. If the response cannot be inferred from the input data, just say no relevant information was found. Do not make anything up or add unrelevant information.

Answer:
"""

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

```

### fast_graphrag/_services/__init__.py

```python
__all__ = [
    'BaseChunkingService',
    'BaseInformationExtractionService',
    'BaseStateManagerService',
    'DefaultChunkingService',
    'DefaultInformationExtractionService',
    'DefaultStateManagerService'
]

from ._base import BaseChunkingService, BaseInformationExtractionService, BaseStateManagerService
from ._chunk_extraction import DefaultChunkingService
from ._information_extraction import DefaultInformationExtractionService
from ._state_manager import DefaultStateManagerService

```

### fast_graphrag/_services/_base.py

```python
import asyncio
from dataclasses import dataclass, field
from typing import Dict, Generic, Iterable, List, Optional, Type

from scipy.sparse import csr_matrix

from fast_graphrag._llm import BaseEmbeddingService, BaseLLMService
from fast_graphrag._policies._base import (
    BaseEdgeUpsertPolicy,
    BaseGraphUpsertPolicy,
    BaseNodeUpsertPolicy,
    BaseRankingPolicy,
)
from fast_graphrag._storage import BaseBlobStorage, BaseGraphStorage, BaseIndexedKeyValueStorage, BaseVectorStorage
from fast_graphrag._storage._namespace import Workspace
from fast_graphrag._types import (
    GTChunk,
    GTEdge,
    GTEmbedding,
    GTHash,
    GTId,
    GTNode,
    TContext,
    TDocument,
    TEntity,
    TIndex,
)


@dataclass
class BaseChunkingService(Generic[GTChunk]):
    """Base class for chunk extractor."""

    def __post__init__(self):
        pass

    async def extract(self, data: Iterable[TDocument]) -> Iterable[Iterable[GTChunk]]:
        """Extract unique chunks from the given data."""
        raise NotImplementedError


@dataclass
class BaseInformationExtractionService(Generic[GTChunk, GTNode, GTEdge, GTId]):
    """Base class for entity and relationship extractors."""

    graph_upsert: BaseGraphUpsertPolicy[GTNode, GTEdge, GTId]
    max_gleaning_steps: int = 0

    def extract(
        self,
        llm: BaseLLMService,
        documents: Iterable[Iterable[GTChunk]],
        prompt_kwargs: Dict[str, str],
        entity_types: List[str],
    ) -> List[asyncio.Future[Optional[BaseGraphStorage[GTNode, GTEdge, GTId]]]]:
        """Extract both entities and relationships from the given data."""
        raise NotImplementedError

    async def extract_entities_from_query(
        self, llm: BaseLLMService, query: str, prompt_kwargs: Dict[str, str]
    ) -> Iterable[TEntity]:
        """Extract entities from the given query."""
        raise NotImplementedError


@dataclass
class BaseStateManagerService(Generic[GTNode, GTEdge, GTHash, GTChunk, GTId, GTEmbedding]):
    """A class for managing state operations."""

    workspace: Optional[Workspace] = field()

    graph_storage: BaseGraphStorage[GTNode, GTEdge, GTId] = field()
    entity_storage: BaseVectorStorage[TIndex, GTEmbedding] = field()
    chunk_storage: BaseIndexedKeyValueStorage[GTHash, GTChunk] = field()

    embedding_service: BaseEmbeddingService = field()

    node_upsert_policy: BaseNodeUpsertPolicy[GTNode, GTId] = field()
    edge_upsert_policy: BaseEdgeUpsertPolicy[GTEdge, GTId] = field()

    entity_ranking_policy: BaseRankingPolicy = field(default_factory=lambda: BaseRankingPolicy(None))
    relation_ranking_policy: BaseRankingPolicy = field(default_factory=lambda: BaseRankingPolicy(None))
    chunk_ranking_policy: BaseRankingPolicy = field(default_factory=lambda: BaseRankingPolicy(None))

    node_specificity: bool = field(default=False)

    blob_storage_cls: Type[BaseBlobStorage[csr_matrix]] = field(default=BaseBlobStorage)

    async def insert_start(self) -> None:
        """Prepare the storage for indexing before adding new data."""
        raise NotImplementedError

    async def insert_done(self) -> None:
        """Commit the storage operations after indexing."""
        raise NotImplementedError

    async def query_start(self) -> None:
        """Prepare the storage for indexing before adding new data."""
        raise NotImplementedError

    async def query_done(self) -> None:
        """Commit the storage operations after indexing."""
        raise NotImplementedError

    async def filter_new_chunks(self, chunks_per_data: Iterable[Iterable[GTChunk]]) -> List[List[GTChunk]]:
        """Filter the chunks to check for duplicates.

        This method takes a sequence of chunks and returns a sequence of new chunks
        that are not already present in the storage. It uses a hashing mechanism to
        efficiently identify duplicates.

        Args:
            chunks_per_data (Iterable[Iterable[TChunk]]): A sequence of chunks to be filtered.

        Returns:
            Iterable[Iterable[TChunk]]: A sequence of chunks that are not in the storage.
        """
        raise NotImplementedError

    async def upsert(
        self,
        llm: BaseLLMService,
        subgraphs: List[asyncio.Future[Optional[BaseGraphStorage[GTNode, GTEdge, GTId]]]],
        documents: Iterable[Iterable[GTChunk]],
        show_progress: bool = True
    ) -> None:
        """Clean and upsert entities, relationships, and chunks into the storage."""
        raise NotImplementedError

    async def get_context(
        self, query: str, entities: Iterable[TEntity]
    ) -> Optional[TContext[GTNode, GTEdge, GTHash, GTChunk]]:
        """Retrieve relevant state from the storage."""
        raise NotImplementedError

    async def get_num_entities(self) -> int:
        """Get the number of entities in the storage."""
        raise NotImplementedError

    async def get_num_relations(self) -> int:
        """Get the number of relations in the storage."""
        raise NotImplementedError

    async def get_num_chunks(self) -> int:
        """Get the number of chunks in the storage."""
        raise NotImplementedError

```

### fast_graphrag/_services/_chunk_extraction.py

```python
import re
from dataclasses import dataclass, field
from itertools import chain
from typing import Iterable, List, Set, Tuple

import xxhash

from fast_graphrag._types import TChunk, TDocument, THash
from fast_graphrag._utils import TOKEN_TO_CHAR_RATIO

from ._base import BaseChunkingService

DEFAULT_SEPARATORS = [
    # Paragraph and page separators
    "\n\n\n",
    "\n\n",
    "\r\n\r\n",
    # Sentence ending punctuation
    "。",  # Chinese period
    "．",  # Full-width dot
    ".",  # English period
    "！",  # Chinese exclamation mark
    "!",  # English exclamation mark
    "？",  # Chinese question mark
    "?",  # English question mark
]


@dataclass
class DefaultChunkingServiceConfig:
    separators: List[str] = field(default_factory=lambda: DEFAULT_SEPARATORS)
    chunk_token_size: int = field(default=1024)
    chunk_token_overlap: int = field(default=128)


@dataclass
class DefaultChunkingService(BaseChunkingService[TChunk]):
    """Default class for chunk extractor."""

    config: DefaultChunkingServiceConfig = field(default_factory=DefaultChunkingServiceConfig)

    def __post_init__(self):
        self._split_re = re.compile(f"({'|'.join(re.escape(s) for s in self.config.separators or [])})")
        self._chunk_size = self.config.chunk_token_size * TOKEN_TO_CHAR_RATIO
        self._chunk_overlap = self.config.chunk_token_overlap * TOKEN_TO_CHAR_RATIO

    async def extract(self, data: Iterable[TDocument]) -> Iterable[Iterable[TChunk]]:
        """Extract unique chunks from the given data."""
        chunks_per_data: List[List[TChunk]] = []

        for d in data:
            unique_chunk_ids: Set[THash] = set()
            extracted_chunks = await self._extract_chunks(d)
            chunks: List[TChunk] = []
            for chunk in extracted_chunks:
                if chunk.id not in unique_chunk_ids:
                    unique_chunk_ids.add(chunk.id)
                    chunks.append(chunk)
            chunks_per_data.append(chunks)

        return chunks_per_data

    async def _extract_chunks(self, data: TDocument) -> List[TChunk]:
        # Sanitise input data:
        data.data = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", data.data)
        if len(data.data) <= self._chunk_size:
            chunks = [data.data]
        else:
            chunks = self._split_text(data.data)

        return [
            TChunk(
                id=THash(xxhash.xxh3_64_intdigest(chunk)),
                content=chunk,
                metadata=data.metadata,
            )
            for chunk in chunks
        ]

    def _split_text(self, text: str) -> List[str]:
        return self._merge_splits(self._split_re.split(text))

    def _merge_splits(self, splits: List[str]) -> List[str]:
        if not splits:
            return []

        # Add empty string to the end to have a separator at the end of the last chunk
        splits.append("")

        merged_splits: List[List[Tuple[str, int]]] = []
        current_chunk: List[Tuple[str, int]] = []
        current_chunk_length: int = 0

        for i, split in enumerate(splits):
            split_length: int = len(split)
            # Ignore splitting if it's a separator
            if (i % 2 == 1) or (
                current_chunk_length + split_length <= self._chunk_size - (self._chunk_overlap if i > 0 else 0)
            ):
                current_chunk.append((split, split_length))
                current_chunk_length += split_length
            else:
                merged_splits.append(current_chunk)
                current_chunk = [(split, split_length)]
                current_chunk_length = split_length

        merged_splits.append(current_chunk)

        if self._chunk_overlap > 0:
            return self._enforce_overlap(merged_splits)
        else:
            r = ["".join((c[0] for c in chunk)) for chunk in merged_splits]

        return r

    def _enforce_overlap(self, chunks: List[List[Tuple[str, int]]]) -> List[str]:
        result: List[str] = []
        for i, chunk in enumerate(chunks):
            if i == 0:
                result.append("".join((c[0] for c in chunk)))
            else:
                # Compute overlap
                overlap_length: int = 0
                overlap: List[str] = []
                for text, length in reversed(chunks[i - 1]):
                    if overlap_length + length > self._chunk_overlap:
                        break
                    overlap_length += length
                    overlap.append(text)
                result.append("".join(chain(reversed(overlap), (c[0] for c in chunk))))
        return result

```

### fast_graphrag/_services/_information_extraction.py

```python
"""Entity-Relationship extraction module."""

import asyncio
import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Literal, Optional

from pydantic import BaseModel, Field

from fast_graphrag._llm import BaseLLMService, format_and_send_prompt
from fast_graphrag._storage._base import BaseGraphStorage
from fast_graphrag._storage._gdb_igraph import IGraphStorage, IGraphStorageConfig
from fast_graphrag._types import GTId, TChunk, TEntity, TGraph, TQueryEntities, TRelation
from fast_graphrag._utils import logger

from ._base import BaseInformationExtractionService


class TGleaningStatus(BaseModel):
    status: Literal["done", "continue"] = Field(
        description="done if all entities and relationship have been extracted, continue otherwise"
    )


@dataclass
class DefaultInformationExtractionService(BaseInformationExtractionService[TChunk, TEntity, TRelation, GTId]):
    """Default entity and relationship extractor."""

    def extract(
        self,
        llm: BaseLLMService,
        documents: Iterable[Iterable[TChunk]],
        prompt_kwargs: Dict[str, str],
        entity_types: List[str],
    ) -> List[asyncio.Future[Optional[BaseGraphStorage[TEntity, TRelation, GTId]]]]:
        """Extract both entities and relationships from the given data."""
        return [
            asyncio.create_task(self._extract(llm, document, prompt_kwargs, entity_types)) for document in documents
        ]

    async def extract_entities_from_query(
        self, llm: BaseLLMService, query: str, prompt_kwargs: Dict[str, str]
    ) -> Iterable[TEntity]:
        """Extract entities from the given query."""
        prompt_kwargs["query"] = query
        entities, _ = await format_and_send_prompt(
            prompt_key="entity_extraction_query",
            llm=llm,
            format_kwargs=prompt_kwargs,
            response_model=TQueryEntities,
        )

        return [TEntity(name=name, type="", description="") for name in entities.entities]

    async def _extract(
        self, llm: BaseLLMService, chunks: Iterable[TChunk], prompt_kwargs: Dict[str, str], entity_types: List[str]
    ) -> Optional[BaseGraphStorage[TEntity, TRelation, GTId]]:
        """Extract both entities and relationships from the given chunks."""
        # Extract entities and relatioships from each chunk
        try:
            chunk_graphs = await asyncio.gather(
                *[self._extract_from_chunk(llm, chunk, prompt_kwargs, entity_types) for chunk in chunks]
            )
            if len(chunk_graphs) == 0:
                return None

            # Combine chunk graphs in document graph
            return await self._merge(llm, chunk_graphs)
        except Exception as e:
            logger.error(f"Error during information extraction from document: {e}")
            return None

    async def _gleaning(
        self, llm: BaseLLMService, initial_graph: TGraph, history: list[dict[str, str]]
    ) -> Optional[TGraph]:
        """Do gleaning steps until the llm says we are done or we reach the max gleaning steps."""
        # Prompts
        current_graph = initial_graph

        try:
            for gleaning_count in range(self.max_gleaning_steps):
                # Do gleaning step
                gleaning_result, history = await format_and_send_prompt(
                    prompt_key="entity_relationship_continue_extraction",
                    llm=llm,
                    format_kwargs={},
                    response_model=TGraph,
                    history_messages=history,
                )

                # Combine new entities, relationships with previously obtained ones
                current_graph.entities.extend(gleaning_result.entities)
                current_graph.relationships.extend(gleaning_result.relationships)

                # Stop gleaning if we don't need to keep going
                if gleaning_count == self.max_gleaning_steps - 1:
                    break

                # Ask llm if we are done extracting entities and relationships
                gleaning_status, _ = await format_and_send_prompt(
                    prompt_key="entity_relationship_gleaning_done_extraction",
                    llm=llm,
                    format_kwargs={},
                    response_model=TGleaningStatus,
                    history_messages=history,
                )

                # If we are done parsing, stop gleaning
                if gleaning_status.status == Literal["done"]:
                    break
        except Exception as e:
            logger.error(f"Error during gleaning: {e}")

            return None

        return current_graph

    async def _extract_from_chunk(
        self, llm: BaseLLMService, chunk: TChunk, prompt_kwargs: Dict[str, str], entity_types: List[str]
    ) -> TGraph:
        """Extract entities and relationships from the given chunk."""
        prompt_kwargs["input_text"] = chunk.content

        chunk_graph, history = await format_and_send_prompt(
            prompt_key="entity_relationship_extraction",
            llm=llm,
            format_kwargs=prompt_kwargs,
            response_model=TGraph,
        )

        # Do gleaning
        chunk_graph_with_gleaning = await self._gleaning(llm, chunk_graph, history)
        if chunk_graph_with_gleaning:
            chunk_graph = chunk_graph_with_gleaning

        _clean_entity_types = [re.sub("[ _]", "", entity_type).upper() for entity_type in entity_types]
        for entity in chunk_graph.entities:
            if re.sub("[ _]", "", entity.type).upper() not in _clean_entity_types:
                entity.type = "UNKNOWN"

        # Assign chunk ids to relationships
        for relationship in chunk_graph.relationships:
            relationship.chunks = [chunk.id]

        return chunk_graph

    async def _merge(self, llm: BaseLLMService, graphs: List[TGraph]) -> BaseGraphStorage[TEntity, TRelation, GTId]:
        """Merge the given graphs into a single graph storage."""
        graph_storage = IGraphStorage[TEntity, TRelation, GTId](config=IGraphStorageConfig(TEntity, TRelation))

        await graph_storage.insert_start()

        try:
            # This is synchronous since each sub graph is inserted into the graph storage and conflicts are resolved
            for graph in graphs:
                await self.graph_upsert(llm, graph_storage, graph.entities, graph.relationships)
        finally:
            await graph_storage.insert_done()

        return graph_storage

```

### fast_graphrag/_services/_state_manager.py

```python
import asyncio
from dataclasses import dataclass, field
from itertools import chain
from typing import Any, Awaitable, Dict, Iterable, List, Optional, Tuple, Type, cast

import numpy as np
import numpy.typing as npt
from scipy.sparse import csr_matrix
from tqdm import tqdm

from fast_graphrag._llm import BaseLLMService
from fast_graphrag._storage._base import (
    BaseBlobStorage,
    BaseGraphStorage,
    BaseStorage,
)
from fast_graphrag._storage._blob_pickle import PickleBlobStorage
from fast_graphrag._storage._namespace import Workspace
from fast_graphrag._types import (
    TChunk,
    TContext,
    TEmbedding,
    TEntity,
    THash,
    TId,
    TIndex,
    TRelation,
    TScore,
)
from fast_graphrag._utils import csr_from_indices_list, extract_sorted_scores, logger

from ._base import BaseStateManagerService


@dataclass
class DefaultStateManagerService(BaseStateManagerService[TEntity, TRelation, THash, TChunk, TId, TEmbedding]):
    blob_storage_cls: Type[BaseBlobStorage[csr_matrix]] = field(default=PickleBlobStorage)
    similarity_score_threshold: float = field(default=0.8)

    def __post_init__(self):
        assert self.workspace is not None, "Workspace must be provided."

        self.graph_storage.namespace = self.workspace.make_for("graph")
        self.entity_storage.namespace = self.workspace.make_for("entities")
        self.chunk_storage.namespace = self.workspace.make_for("chunks")

        self._entities_to_relationships: BaseBlobStorage[csr_matrix] = self.blob_storage_cls(
            namespace=self.workspace.make_for("map_e2r"), config=None
        )
        self._relationships_to_chunks: BaseBlobStorage[csr_matrix] = self.blob_storage_cls(
            namespace=self.workspace.make_for("map_r2c"), config=None
        )

    async def get_num_entities(self) -> int:
        return await self.graph_storage.node_count()

    async def get_num_relations(self) -> int:
        return await self.graph_storage.edge_count()

    async def get_num_chunks(self) -> int:
        return await self.chunk_storage.size()

    async def filter_new_chunks(self, chunks_per_data: Iterable[Iterable[TChunk]]) -> List[List[TChunk]]:
        flattened_chunks = [chunk for chunks in chunks_per_data for chunk in chunks]
        if len(flattened_chunks) == 0:
            return []

        new_chunks_mask = await self.chunk_storage.mask_new(keys=[c.id for c in flattened_chunks])

        i = iter(new_chunks_mask)
        new_chunks = [[chunk for chunk in chunks if next(i)] for chunks in chunks_per_data]

        return new_chunks

    async def upsert(
        self,
        llm: BaseLLMService,
        subgraphs: List[asyncio.Future[Optional[BaseGraphStorage[TEntity, TRelation, TId]]]],
        documents: Iterable[Iterable[TChunk]],
        show_progress: bool = True
    ) -> None:
        nodes: Iterable[List[TEntity]]
        edges: Iterable[List[TRelation]]

        # STEP: Extracting subgraphs
        async def _get_graphs(
            fgraph: asyncio.Future[Optional[BaseGraphStorage[TEntity, TRelation, TId]]],
        ) -> Optional[Tuple[List[TEntity], List[TRelation]]]:
            graph = await fgraph
            if graph is None:
                return None

            nodes = [t for i in range(await graph.node_count()) if (t := await graph.get_node_by_index(i)) is not None]
            edges = [t for i in range(await graph.edge_count()) if (t := await graph.get_edge_by_index(i)) is not None]

            return (nodes, edges)

        graphs = [r for graph in tqdm(
            asyncio.as_completed([_get_graphs(fgraph) for fgraph in subgraphs]),
            total=len(subgraphs),
            desc="Extracting data",
            disable=not show_progress,
        ) if (r := await graph) is not None]

        if len(graphs) == 0:
            return

        progress_bar = tqdm(total=7, disable=not show_progress, desc="Building...")
        # STEP (2): Upserting nodes and edges
        nodes, edges = zip(*graphs)
        progress_bar.set_description("Building... [upserting graphs]")

        _, upserted_nodes = await self.node_upsert_policy(llm, self.graph_storage, chain(*nodes))
        progress_bar.update(1)
        _, _ = await self.edge_upsert_policy(llm, self.graph_storage, chain(*edges))
        progress_bar.update(1)

        # STEP (2): Computing entity embeddings
        progress_bar.set_description("Building... [computing embeddings]")
        # Insert entities in entity_storage
        embeddings = await self.embedding_service.get_embedding(texts=[d.to_str() for _, d in upserted_nodes])
        progress_bar.update(1)
        await self.entity_storage.upsert(ids=(i for i, _ in upserted_nodes), embeddings=embeddings)
        progress_bar.update(1)

        # STEP: Entity deduplication
        # Note that get_knn will very likely return the same entity as the most similar one, so we remove it
        # when selecting the index order.
        progress_bar.set_description("Building... [entity deduplication]")
        upserted_indices = np.array([i for i, _ in upserted_nodes]).reshape(-1, 1)
        similar_indices, scores = await self.entity_storage.get_knn(embeddings, top_k=5)
        similar_indices = np.array(similar_indices)
        scores = np.array(scores)

        # Create matrix with the indices with a score higher than the threshold
        # We use the fact that similarity scores are symmetric between entity pairs,
        # so we only select half of that by index order
        similar_indices[
            (scores < self.similarity_score_threshold)
            | (similar_indices <= upserted_indices)  # remove indices smaller or equal the entity
        ] = 0  # 0 can be used here (not 100% sure, but 99% sure)
        progress_bar.update(1)

        # | entity_index  | similar_indices[] |
        # |---------------|------------------------|
        # | 1             | 0, 7, 12, 0, 9         |

        # STEP: insert identity edges
        progress_bar.set_description("Building... [identity edges]")
        async def _insert_identiy_edges(
            source_index: TIndex, target_indices: npt.NDArray[np.int32]
        ) -> Iterable[Tuple[TIndex, TIndex]]:
            return [
                (source_index, idx)
                for idx in target_indices
                if idx != 0 and not await self.graph_storage.are_neighbours(source_index, idx)
            ]

        new_edge_indices = list(
            chain(
                *await asyncio.gather(*[_insert_identiy_edges(i, indices) for i, indices in enumerate(similar_indices)])
            )
        )
        new_edges_attrs: Dict[str, Any] = {
            "description": ["is"] * len(new_edge_indices),
            "chunks": [[]] * len(new_edge_indices),
        }
        await self.graph_storage.insert_edges(indices=new_edge_indices, attrs=new_edges_attrs)
        progress_bar.update(1)

        # STEP: Save chunks
        # Insert chunks in chunk_storage
        progress_bar.set_description("Building... [saving chunks]")
        flattened_chunks = [chunk for chunks in documents for chunk in chunks]
        await self.chunk_storage.upsert(keys=[chunk.id for chunk in flattened_chunks], values=flattened_chunks)
        progress_bar.update(1)
        progress_bar.set_description("Building [done]")

    async def get_context(
        self, query: str, entities: Iterable[TEntity]
    ) -> Optional[TContext[TEntity, TRelation, THash, TChunk]]:
        try:
            entity_names = [entity.name for entity in entities]
            if len(entity_names) == 0:
                return None

            query_embeddings = await self.embedding_service.get_embedding(entity_names + [query])
            # query_embeddings = await self.embedding_service.get_embedding([query])

            # Similarity-search over entities
            vdb_entity_scores_by_name = await self._score_entities_by_vectordb(
                query_embeddings=query_embeddings[:-1], top_k=1
            )
            vdb_entity_scores_by_query = await self._score_entities_by_vectordb(
                query_embeddings=query_embeddings[-1:], top_k=16
            )

            vdb_entity_scores = vdb_entity_scores_by_name + vdb_entity_scores_by_query

            if vdb_entity_scores.nnz == 0:
                return None
        except Exception as e:
            logger.error(f"Error during information extraction and scoring for query entities {entities}.\n{e}")
            raise e

        # Score entities
        try:
            graph_entity_scores = self.entity_ranking_policy(
                await self._score_entities_by_graph(entity_scores=vdb_entity_scores)
            )
        except Exception as e:
            logger.error(f"Error during graph scoring for entities. Non-zero elements: {vdb_entity_scores.nnz}.\n{e}")
            raise e

        try:
            # All score vectors should be row vectors
            indices, scores = extract_sorted_scores(graph_entity_scores)
            relevant_entities: List[Tuple[TEntity, TScore]] = []
            for i, s in zip(indices, scores):
                entity = await self.graph_storage.get_node_by_index(i)
                if entity is not None:
                    relevant_entities.append((entity, s))

            # Extract relevant relationships
            relation_scores = self.relation_ranking_policy(
                await self._score_relationships_by_entities(entity_scores=graph_entity_scores)
            )

            indices, scores = extract_sorted_scores(relation_scores)
            relevant_relationships: List[Tuple[TRelation, TScore]] = []
            for i, s in zip(indices, scores):
                relationship = await self.graph_storage.get_edge_by_index(i)
                if relationship is not None:
                    relevant_relationships.append((relationship, s))

            # Extract relevant chunks
            chunk_scores = self.chunk_ranking_policy(
                await self._score_chunks_by_relations(relationships_score=relation_scores)
            )
            indices, scores = extract_sorted_scores(chunk_scores)
            relevant_chunks: List[Tuple[TChunk, TScore]] = []
            for chunk, s in zip(await self.chunk_storage.get_by_index(indices), scores):
                if chunk is not None:
                    relevant_chunks.append((chunk, s))

            return TContext(entities=relevant_entities, relationships=relevant_relationships, chunks=relevant_chunks)
        except Exception as e:
            logger.error(f"Error during scoring of chunks and relationships.\n{e}")
            raise e

    async def _get_entities_to_num_docs(self) -> Any:
        raise NotImplementedError

    async def _score_entities_by_vectordb(self, query_embeddings: Iterable[TEmbedding], top_k: int = 1) -> csr_matrix:
        # TODO: check this
        # if top_k != 1:
        #     logger.warning(f"Top-k > 1 is not tested yet. Using top_k={top_k}.")
        if self.node_specificity:
            raise NotImplementedError("Node specificity is not supported yet.")

        all_entity_probs_by_query_entity = await self.entity_storage.score_all(
            np.array(query_embeddings), top_k=top_k
        )  # (#query_entities, #all_entities)

        # TODO: if top_k > 1, we need to aggregate the scores here
        if all_entity_probs_by_query_entity.shape[1] == 0:
            return all_entity_probs_by_query_entity
        all_entity_weights: csr_matrix = all_entity_probs_by_query_entity.max(axis=0)  # (1, #all_entities)

        # Normalize the scores
        all_entity_weights /= all_entity_weights.sum()

        if self.node_specificity:
            all_entity_weights = all_entity_weights.multiply(1.0 / await self._get_entities_to_num_docs())

        return all_entity_weights

    async def _score_entities_by_graph(self, entity_scores: Optional[csr_matrix]) -> csr_matrix:
        graph_weighted_scores = await self.graph_storage.score_nodes(entity_scores)
        node_scores = csr_matrix(graph_weighted_scores)  # (1, #entities)
        return node_scores

    async def _score_relationships_by_entities(self, entity_scores: csr_matrix) -> csr_matrix:
        e2r = await self._entities_to_relationships.get()
        if e2r is None:
            logger.warning("No entities to relationships map was loaded.")
            return csr_matrix((1, await self.graph_storage.edge_count()))

        return entity_scores.dot(e2r)  # (1, #entities) x (#entities, #relationships) => (1, #relationships)

    async def _score_chunks_by_relations(self, relationships_score: csr_matrix) -> csr_matrix:
        c2r = await self._relationships_to_chunks.get()
        if c2r is None:
            logger.warning("No relationships to chunks map was loaded.")
            return csr_matrix((1, await self.chunk_storage.size()))
        return relationships_score.dot(c2r)  # (1, #relationships) x (#relationships, #chunks) => (1, #chunks)

    ####################################################################################################

    # I/O management
    ####################################################################################################

    async def query_start(self):
        storages: List[BaseStorage] = [
            self.graph_storage,
            self.entity_storage,
            self.chunk_storage,
            self._relationships_to_chunks,
            self._entities_to_relationships,
        ]

        def _fn():
            tasks: List[Awaitable[Any]] = []
            for storage_inst in storages:
                tasks.append(storage_inst.query_start())
            return asyncio.gather(*tasks)

        await cast(Workspace, self.workspace).with_checkpoints(_fn)

        for storage_inst in storages:
            storage_inst.set_in_progress(True)

    async def query_done(self):
        tasks: List[Awaitable[Any]] = []
        storages: List[BaseStorage] = [
            self.graph_storage,
            self.entity_storage,
            self.chunk_storage,
            self._relationships_to_chunks,
            self._entities_to_relationships,
        ]
        for storage_inst in storages:
            tasks.append(storage_inst.query_done())
        await asyncio.gather(*tasks)

        for storage_inst in storages:
            storage_inst.set_in_progress(False)

    async def insert_start(self):
        storages: List[BaseStorage] = [
            self.graph_storage,
            self.entity_storage,
            self.chunk_storage,
            self._relationships_to_chunks,
            self._entities_to_relationships,
        ]

        def _fn():
            tasks: List[Awaitable[Any]] = []
            for storage_inst in storages:
                tasks.append(storage_inst.insert_start())
            return asyncio.gather(*tasks)

        await cast(Workspace, self.workspace).with_checkpoints(_fn)

        for storage_inst in storages:
            storage_inst.set_in_progress(True)

    async def insert_done(self):
        await self._entities_to_relationships.set(await self.graph_storage.get_entities_to_relationships_map())

        raw_relationships_to_chunks = await self.graph_storage.get_relationships_attrs(key="chunks")
        # Map Chunk IDs to indices
        raw_relationships_to_chunks = [
            [i for i in await self.chunk_storage.get_index(chunk_ids) if i is not None]
            for chunk_ids in raw_relationships_to_chunks
        ]
        await self._relationships_to_chunks.set(
            csr_from_indices_list(
                raw_relationships_to_chunks, shape=(len(raw_relationships_to_chunks), await self.chunk_storage.size())
            )
        )

        tasks: List[Awaitable[Any]] = []
        storages: List[BaseStorage] = [
            self.graph_storage,
            self.entity_storage,
            self.chunk_storage,
            self._relationships_to_chunks,
            self._entities_to_relationships,
        ]
        for storage_inst in storages:
            tasks.append(storage_inst.insert_done())
        await asyncio.gather(*tasks)

        for storage_inst in storages:
            storage_inst.set_in_progress(False)

```

### fast_graphrag/_storage/__init__.py

```python
__all__ = [
    'Namespace',
    'BaseBlobStorage',
    'BaseIndexedKeyValueStorage',
    'BaseVectorStorage',
    'BaseGraphStorage',
    'DefaultBlobStorage',
    'DefaultIndexedKeyValueStorage',
    'DefaultVectorStorage',
    'DefaultGraphStorage',
    'DefaultGraphStorageConfig',
    'DefaultVectorStorageConfig',
]

from ._base import BaseBlobStorage, BaseGraphStorage, BaseIndexedKeyValueStorage, BaseVectorStorage, Namespace
from ._default import (
    DefaultBlobStorage,
    DefaultGraphStorage,
    DefaultGraphStorageConfig,
    DefaultIndexedKeyValueStorage,
    DefaultVectorStorage,
    DefaultVectorStorageConfig,
)

```

### fast_graphrag/_storage/_base.py

```python
from dataclasses import dataclass, field
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Literal,
    Mapping,
    Optional,
    Tuple,
    Union,
    final,
)

from scipy.sparse import csr_matrix  # type: ignore

from fast_graphrag._types import GTBlob, GTEdge, GTEmbedding, GTId, GTKey, GTNode, GTValue, TIndex, TScore
from fast_graphrag._utils import logger

from ._namespace import Namespace


@dataclass
class BaseStorage:
    config: Optional[Any] = field()
    namespace: Optional[Namespace] = field(default=None)
    _mode: Optional[Literal["insert", "query"]] = field(init=False, default=None)
    _in_progress: Optional[bool] = field(init=False, default=None)

    def set_in_progress(self, in_progress: bool) -> None:
        self._in_progress = in_progress

    @final
    async def insert_start(self):
        if self._mode == "query":
            logger.info("Switching from query to insert mode.")
            if self._in_progress is not False:
                t = (
                    f"[{self.__class__.__name__}] Cannot being insert before committing query operations."
                    "Committing query operations now."
                )
                logger.error(t)
                await self._query_done()
                self._in_progress = False
        self._mode = "insert"

        if self._in_progress is not True:
            await self._insert_start()

    @final
    async def query_start(self):
        if self._mode == "insert":
            logger.info("Switching from insert to query mode.")
            if self._in_progress is not False:
                t = (
                    f"[{self.__class__.__name__}] Cannot being query before commiting insert operations."
                    "Committing insert operations now."
                )
                logger.error(t)
                await self._insert_done()
                self._in_progress = False
        self._mode = "query"

        if self._in_progress is not True:
            await self._query_start()

    @final
    async def insert_done(self) -> None:
        if self._mode == "query":
            t = f"[{self.__class__.__name__}] Trying to commit insert operations in query mode."
            logger.error(t)
        else:
            if self._in_progress is not False:
                await self._insert_done()
            else:
                logger.warning(f"[{self.__class__.__name__}] No insert operations to commit.")

    @final
    async def query_done(self) -> None:
        if self._mode == "insert":
            t = f"[{self.__class__.__name__}] Trying to commit query operations in insert mode."
            logger.error(t)
        else:
            if self._in_progress is not False:
                await self._query_done()
            else:
                logger.warning(f"[{self.__class__.__name__}] No query operations to commit.")

    async def _insert_start(self):
        """Prepare the storage for inserting."""
        pass

    async def _insert_done(self):
        """Commit the storage operations after inserting."""
        if self._mode == "query":
            logger.error("Trying to commit insert operations in query mode.")

    async def _query_start(self):
        """Prepare the storage for querying."""
        pass

    async def _query_done(self):
        """Release the storage after querying."""
        if self._mode == "insert":
            logger.error("Trying to commit query operations in insert mode.")


####################################################################################################
# Blob Storage
####################################################################################################


@dataclass
class BaseBlobStorage(BaseStorage, Generic[GTBlob]):
    async def get(self) -> Optional[GTBlob]:
        raise NotImplementedError

    async def set(self, blob: GTBlob) -> None:
        raise NotImplementedError


####################################################################################################
# Key-Value Storage
####################################################################################################


@dataclass
class BaseIndexedKeyValueStorage(BaseStorage, Generic[GTKey, GTValue]):
    async def size(self) -> int:
        raise NotImplementedError

    async def get(self, keys: Iterable[GTKey]) -> Iterable[Optional[GTValue]]:
        raise NotImplementedError

    async def get_by_index(self, indices: Iterable[TIndex]) -> Iterable[Optional[GTValue]]:
        raise NotImplementedError

    async def get_index(self, keys: Iterable[GTKey]) -> Iterable[Optional[TIndex]]:
        raise NotImplementedError

    async def upsert(self, keys: Iterable[GTKey], values: Iterable[GTValue]) -> None:
        raise NotImplementedError

    async def upsert_by_index(self, indices: Iterable[TIndex], values: Iterable[GTValue]) -> None:
        raise NotImplementedError

    async def delete(self, keys: Iterable[GTKey]) -> None:
        raise NotImplementedError

    async def delete_by_index(self, indices: Iterable[TIndex]) -> None:
        raise NotImplementedError

    async def mask_new(self, keys: Iterable[GTKey]) -> Iterable[bool]:
        raise NotImplementedError


####################################################################################################
# Vector Storage
####################################################################################################


@dataclass
class BaseVectorStorage(BaseStorage, Generic[GTId, GTEmbedding]):
    embedding_dim: int = field(default=0)

    async def get_knn(
        self, embeddings: Iterable[GTEmbedding], top_k: int
    ) -> Tuple[Iterable[Iterable[GTId]], Iterable[Iterable[TScore]]]:
        raise NotImplementedError

    async def upsert(
        self,
        ids: Iterable[GTId],
        embeddings: Iterable[GTEmbedding],
        metadata: Union[Iterable[Dict[str, Any]], None] = None,
    ) -> None:
        raise NotImplementedError

    async def score_all(
        self, embeddings: Iterable[GTEmbedding], top_k: int = 1, confidence_threshold: float = 0.0
    ) -> csr_matrix:
        """Score all embeddings against the given queries.

        Return a (#queries, #all_embeddings) matrix containing the relevancy scores of each embedding given each query.
        """
        raise NotImplementedError


####################################################################################################
# Graph Storage
####################################################################################################


@dataclass
class BaseGraphStorage(BaseStorage, Generic[GTNode, GTEdge, GTId]):
    @staticmethod
    def from_tgraph(graph: Any, namespace: Optional[Namespace] = None) -> "BaseGraphStorage[GTNode, GTEdge, GTId]":
        raise NotImplementedError

    async def node_count(self) -> int:
        raise NotImplementedError

    async def edge_count(self) -> int:
        raise NotImplementedError

    async def get_edge_ids(self) -> Iterable[GTId]:
        raise NotImplementedError

    async def get_node(self, node: Union[GTNode, GTId]) -> Union[Tuple[GTNode, TIndex], Tuple[None, None]]:
        raise NotImplementedError

    async def get_all_edges(self) -> Iterable[GTEdge]:
        raise NotImplementedError

    async def get_edges(
        self, source_node: Union[GTId, TIndex], target_node: Union[GTId, TIndex]
    ) -> Iterable[Tuple[GTEdge, TIndex]]:
        raise NotImplementedError

    async def get_edge_indices(
        self, source_node: Union[GTId, TIndex], target_node: Union[GTId, TIndex]
    ) -> Iterable[TIndex]:
        raise NotImplementedError

    async def get_node_by_index(self, index: TIndex) -> Union[GTNode, None]:
        raise NotImplementedError

    async def get_edge_by_index(self, index: TIndex) -> Union[GTEdge, None]:
        raise NotImplementedError

    async def upsert_node(self, node: GTNode, node_index: Union[TIndex, None]) -> TIndex:
        raise NotImplementedError

    async def upsert_edge(self, edge: GTEdge, edge_index: Union[TIndex, None]) -> TIndex:
        raise NotImplementedError

    async def insert_edges(
        self,
        edges: Optional[Iterable[GTEdge]] = None,
        indices: Optional[Iterable[Tuple[TIndex, TIndex]]] = None,
        attrs: Optional[Mapping[str, Iterable[Any]]] = None,
    ) -> List[TIndex]:
        raise NotImplementedError

    async def are_neighbours(self, source_node: Union[GTId, TIndex], target_node: Union[GTId, TIndex]) -> bool:
        raise NotImplementedError

    async def delete_edges_by_index(self, indices: Iterable[TIndex]) -> None:
        raise NotImplementedError

    async def get_entities_to_relationships_map(self) -> csr_matrix:
        raise NotImplementedError

    async def get_relationships_to_chunks_map(
        self, key: str, key_to_index_fn: Callable[[Iterable[GTKey]], Awaitable[Iterable[TIndex]]], num_chunks: int
    ) -> csr_matrix:
        raise NotImplementedError

    async def get_relationships_attrs(self, key: str) -> List[List[Any]]:
        raise NotImplementedError

    async def score_nodes(self, initial_weights: Optional[csr_matrix]) -> csr_matrix:
        """Score nodes based on the initial weights."""
        raise NotImplementedError

```

### fast_graphrag/_storage/_blob_pickle.py

```python
import pickle
from dataclasses import dataclass, field
from typing import Optional

from fast_graphrag._exceptions import InvalidStorageError
from fast_graphrag._types import GTBlob
from fast_graphrag._utils import logger

from ._base import BaseBlobStorage


@dataclass
class PickleBlobStorage(BaseBlobStorage[GTBlob]):
    RESOURCE_NAME = "blob_data.pkl"
    _data: Optional[GTBlob] = field(init=False, default=None)

    async def get(self) -> Optional[GTBlob]:
        return self._data

    async def set(self, blob: GTBlob) -> None:
        self._data = blob

    async def _insert_start(self):
        if self.namespace:
            data_file_name = self.namespace.get_load_path(self.RESOURCE_NAME)
            if data_file_name:
                try:
                    with open(data_file_name, "rb") as f:
                        self._data = pickle.load(f)
                except Exception as e:
                    t = f"Error loading data file for blob storage {data_file_name}: {e}"
                    logger.error(t)
                    raise InvalidStorageError(t) from e
            else:
                logger.info(f"No data file found for blob storage {data_file_name}. Loading empty storage.")
                self._data = None
        else:
            self._data = None
            logger.debug("Creating new volatile blob storage.")

    async def _insert_done(self):
        if self.namespace:
            data_file_name = self.namespace.get_save_path(self.RESOURCE_NAME)
            try:
                with open(data_file_name, "wb") as f:
                    pickle.dump(self._data, f)
                logger.debug(
                    f"Saving blob storage '{data_file_name}'."
                )
            except Exception as e:
                logger.error(f"Error saving data file for blob storage {data_file_name}: {e}")

    async def _query_start(self):
        assert self.namespace, "Loading a blob storage requires a namespace."

        data_file_name = self.namespace.get_load_path(self.RESOURCE_NAME)
        if data_file_name:
            try:
                with open(data_file_name, "rb") as f:
                    self._data = pickle.load(f)
            except Exception as e:
                t = f"Error loading data file for blob storage {data_file_name}: {e}"
                logger.error(t)
                raise InvalidStorageError(t) from e
        else:
            logger.warning(f"No data file found for blob storage {data_file_name}. Loading empty blob.")
            self._data = None

    async def _query_done(self):
        pass

```

### fast_graphrag/_storage/_default.py

```python
__all__ = [
    "DefaultVectorStorage",
    "DefaultVectorStorageConfig",
    "DefaultBlobStorage",
    "DefaultIndexedKeyValueStorage",
    "DefaultGraphStorage",
    "DefaultGraphStorageConfig",
]

from fast_graphrag._storage._blob_pickle import PickleBlobStorage
from fast_graphrag._storage._gdb_igraph import IGraphStorage, IGraphStorageConfig
from fast_graphrag._storage._ikv_pickle import PickleIndexedKeyValueStorage
from fast_graphrag._storage._vdb_hnswlib import HNSWVectorStorage, HNSWVectorStorageConfig
from fast_graphrag._types import GTBlob, GTEdge, GTEmbedding, GTId, GTKey, GTNode, GTValue


# Storage
class DefaultVectorStorage(HNSWVectorStorage[GTId, GTEmbedding]):
    pass
class DefaultVectorStorageConfig(HNSWVectorStorageConfig):
    pass
class DefaultBlobStorage(PickleBlobStorage[GTBlob]):
    pass
class DefaultIndexedKeyValueStorage(PickleIndexedKeyValueStorage[GTKey, GTValue]):
    pass
class DefaultGraphStorage(IGraphStorage[GTNode, GTEdge, GTId]):
    pass
class DefaultGraphStorageConfig(IGraphStorageConfig[GTNode, GTEdge]):
    pass

```

### fast_graphrag/_storage/_gdb_igraph.py

```python
from dataclasses import asdict, dataclass, field
from typing import Any, Generic, Iterable, List, Mapping, Optional, Tuple, Type, Union

import igraph as ig  # type: ignore
import numpy as np
from scipy.sparse import csr_matrix

from fast_graphrag._exceptions import InvalidStorageError
from fast_graphrag._types import GTEdge, GTId, GTNode, TIndex
from fast_graphrag._utils import csr_from_indices_list, logger

from ._base import BaseGraphStorage


@dataclass
class IGraphStorageConfig(Generic[GTNode, GTEdge]):
    node_cls: Type[GTNode] = field()
    edge_cls: Type[GTEdge] = field()
    ppr_damping: float = field(default=0.85)


@dataclass
class IGraphStorage(BaseGraphStorage[GTNode, GTEdge, GTId]):
    RESOURCE_NAME = "igraph_data.pklz"
    config: IGraphStorageConfig[GTNode, GTEdge] = field()
    _graph: Optional[ig.Graph] = field(init=False, default=None)  # type: ignore

    async def node_count(self) -> int:
        return self._graph.vcount()  # type: ignore

    async def edge_count(self) -> int:
        return self._graph.ecount()  # type: ignore

    async def get_node(self, node: Union[GTNode, GTId]) -> Union[Tuple[GTNode, TIndex], Tuple[None, None]]:
        if isinstance(node, self.config.node_cls):
            node_id = node.name
        else:
            node_id = node

        try:
            vertex = self._graph.vs.find(name=node_id)  # type: ignore
        except ValueError:
            vertex = None

        return (self.config.node_cls(**vertex.attributes()), vertex.index) if vertex else (None, None)  # type: ignore

    async def get_edges(
        self, source_node: Union[GTId, TIndex], target_node: Union[GTId, TIndex]
    ) -> Iterable[Tuple[GTEdge, TIndex]]:
        indices = await self.get_edge_indices(source_node, target_node)
        edges: List[Tuple[GTEdge, TIndex]] = []
        for index in indices:
            edge = await self.get_edge_by_index(index)
            if edge:
                edges.append((edge, index))
        return edges

    async def get_edge_indices(
        self, source_node: Union[GTId, TIndex], target_node: Union[GTId, TIndex]
    ) -> Iterable[TIndex]:
        if type(source_node) is TIndex:
            source_node = self._graph.vs.find(name=source_node).index  # type: ignore
        if type(target_node) is TIndex:
            target_node = self._graph.vs.find(name=target_node).index  # type: ignore
        edges = self._graph.es.select(_source=source_node, _target=target_node)  # type: ignore

        return (edge.index for edge in edges)  # type: ignore

    async def get_node_by_index(self, index: TIndex) -> Union[GTNode, None]:
        node = self._graph.vs[index] if index < self._graph.vcount() else None  # type: ignore
        return self.config.node_cls(**node.attributes()) if index < self._graph.vcount() else None  # type: ignore

    async def get_edge_by_index(self, index: TIndex) -> Union[GTEdge, None]:
        edge = self._graph.es[index] if index < self._graph.ecount() else None  # type: ignore
        return (
            self.config.edge_cls(
                source=self._graph.vs[edge.source]["name"],  # type: ignore
                target=self._graph.vs[edge.target]["name"],  # type: ignore
                **edge.attributes(),  # type: ignore
            )
            if edge
            else None
        )

    async def upsert_node(self, node: GTNode, node_index: Union[TIndex, None]) -> TIndex:
        if node_index is not None:
            if node_index >= self._graph.vcount():  # type: ignore
                logger.error(
                    f"Trying to update node with index {node_index} but graph has only {self._graph.vcount()} nodes."  # type: ignore
                )
                raise ValueError(f"Index {node_index} is out of bounds")
            already_node = self._graph.vs[node_index]  # type: ignore
            already_node.update_attributes(**asdict(node))  # type: ignore

            return already_node.index  # type: ignore
        else:
            return self._graph.add_vertex(**asdict(node)).index  # type: ignore

    async def upsert_edge(self, edge: GTEdge, edge_index: Union[TIndex, None]) -> TIndex:
        if edge_index is not None:
            if edge_index >= self._graph.ecount():  # type: ignore
                logger.error(
                    f"Trying to update edge with index {edge_index} but graph has only {self._graph.ecount()} edges."  # type: ignore
                )
                raise ValueError(f"Index {edge_index} is out of bounds")
            already_edge = self._graph.es[edge_index]  # type: ignore
            already_edge.update_attributes(**edge.to_attrs(edge=edge))  # type: ignore

            return already_edge.index  # type: ignore
        else:
            return self._graph.add_edge(  # type: ignore
                **asdict(edge)
            ).index  # type: ignore

    async def insert_edges(
        self,
        edges: Optional[Iterable[GTEdge]] = None,
        indices: Optional[Iterable[Tuple[TIndex, TIndex]]] = None,
        attrs: Optional[Mapping[str, Iterable[Any]]] = None,
    ) -> List[TIndex]:
        if indices is not None:
            assert edges is None, "Cannot provide both indices and edges."

            indices = list(indices)
            if len(indices) == 0:
                return []
            self._graph.add_edges(  # type: ignore
                indices,
                attributes=attrs,
            )
            # TODO: not sure if this is the best way to get the indices of the new edges
            return list(range(self._graph.ecount() - len(indices), self._graph.ecount()))  # type: ignore
        elif edges is not None:
            assert indices is None and attrs is None, "Cannot provide both indices and edges."
            edges = list(edges)
            if len(edges) == 0:
                return []
            self._graph.add_edges(  # type: ignore
                ((edge.source, edge.target) for edge in edges),
                attributes=type(edges[0]).to_attrs(edges=edges),
            )

            # TODO: not sure if this is the best way to get the indices of the new edges
            return list(range(self._graph.ecount() - len(edges), self._graph.ecount()))  # type: ignore
        else:
            return []

    async def are_neighbours(self, source_node: Union[GTId, TIndex], target_node: Union[GTId, TIndex]) -> bool:
        return self._graph.get_eid(source_node, target_node, directed=False, error=False) != -1  # type: ignore

    async def delete_edges_by_index(self, indices: Iterable[TIndex]) -> None:
        self._graph.delete_edges(indices)  # type: ignore

    async def score_nodes(self, initial_weights: Optional[csr_matrix]) -> csr_matrix:
        if self._graph.vcount() == 0:  # type: ignore
            logger.info("Trying to score nodes in an empty graph.")
            return csr_matrix((1, 0))

        reset_prob = initial_weights.toarray().flatten() if initial_weights is not None else None

        ppr_scores = self._graph.personalized_pagerank(  # type: ignore
            damping=self.config.ppr_damping, directed=False, reset=reset_prob
        )
        ppr_scores = np.array(ppr_scores, dtype=np.float32)  # type: ignore

        return csr_matrix(
            ppr_scores.reshape(1, -1)  # type: ignore
        )

    async def get_entities_to_relationships_map(self) -> csr_matrix:
        if len(self._graph.vs) == 0:  # type: ignore
            return csr_matrix((0, 0))

        return csr_from_indices_list(
            [
                [edge.index for edge in vertex.incident()]  # type: ignore
                for vertex in self._graph.vs  # type: ignore
            ],
            shape=(await self.node_count(), await self.edge_count()),
        )

    async def get_relationships_attrs(self, key: str) -> List[List[Any]]:
        if len(self._graph.es) == 0:  # type: ignore
            return []

        lists_of_attrs: List[List[TIndex]] = []
        for attr in self._graph.es[key]:  # type: ignore
            lists_of_attrs.append(list(attr))  # type: ignore

        return lists_of_attrs

    async def _insert_start(self):
        if self.namespace:
            graph_file_name = self.namespace.get_load_path(self.RESOURCE_NAME)

            if graph_file_name:
                try:
                    self._graph = ig.Graph.Read_Picklez(graph_file_name)  # type: ignore
                    logger.debug(f"Loaded graph storage '{graph_file_name}'.")
                except Exception as e:
                    t = f"Error loading graph from {graph_file_name}: {e}"
                    logger.error(t)
                    raise InvalidStorageError(t) from e
            else:
                logger.info(f"No data file found for graph storage '{graph_file_name}'. Loading empty graph.")
                self._graph = ig.Graph(directed=False)
        else:
            self._graph = ig.Graph(directed=False)
            logger.debug("Creating new volatile graphdb storage.")

    async def _insert_done(self):
        if self.namespace:
            graph_file_name = self.namespace.get_save_path(self.RESOURCE_NAME)
            try:
                ig.Graph.write_picklez(self._graph, graph_file_name)  # type: ignore
            except Exception as e:
                t = f"Error saving graph to {graph_file_name}: {e}"
                logger.error(t)
                raise InvalidStorageError(t) from e

    async def _query_start(self):
        assert self.namespace, "Loading a graph requires a namespace."
        graph_file_name = self.namespace.get_load_path(self.RESOURCE_NAME)
        if graph_file_name:
            try:
                self._graph = ig.Graph.Read_Picklez(graph_file_name)  # type: ignore
                logger.debug(f"Loaded graph storage '{graph_file_name}'.")
            except Exception as e:
                t = f"Error loading graph from '{graph_file_name}': {e}"
                logger.error(t)
                raise InvalidStorageError(t) from e
        else:
            logger.warning(f"No data file found for graph storage '{graph_file_name}'. Loading empty graph.")
            self._graph = ig.Graph(directed=False)

    async def _query_done(self):
        pass

```

### fast_graphrag/_storage/_ikv_pickle.py

```python
import pickle
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Union

import numpy as np
import numpy.typing as npt

from fast_graphrag._exceptions import InvalidStorageError
from fast_graphrag._types import GTKey, GTValue, TIndex
from fast_graphrag._utils import logger

from ._base import BaseIndexedKeyValueStorage


@dataclass
class PickleIndexedKeyValueStorage(BaseIndexedKeyValueStorage[GTKey, GTValue]):
    RESOURCE_NAME = "kv_data.pkl"
    _data: Dict[Union[None, TIndex], GTValue] = field(init=False, default_factory=dict)
    _key_to_index: Dict[GTKey, TIndex] = field(init=False, default_factory=dict)
    _free_indices: List[TIndex] = field(init=False, default_factory=list)
    _np_keys: Optional[npt.NDArray[np.object_]] = field(init=False, default=None)

    async def size(self) -> int:
        return len(self._data)

    async def get(self, keys: Iterable[GTKey]) -> Iterable[Optional[GTValue]]:
        return (self._data.get(self._key_to_index.get(key, None), None) for key in keys)

    async def get_by_index(self, indices: Iterable[TIndex]) -> Iterable[Optional[GTValue]]:
        return (self._data.get(index, None) for index in indices)

    async def get_index(self, keys: Iterable[GTKey]) -> Iterable[Optional[TIndex]]:
        return (self._key_to_index.get(key, None) for key in keys)

    async def upsert(self, keys: Iterable[GTKey], values: Iterable[GTValue]) -> None:
        for key, value in zip(keys, values):
            index = self._key_to_index.get(key, None)
            if index is None:
                if len(self._free_indices) > 0:
                    index = self._free_indices.pop()
                else:
                    index = TIndex(len(self._data))
                self._key_to_index[key] = index

                # Invalidate cache
                self._np_keys = None
            self._data[index] = value

    async def delete(self, keys: Iterable[GTKey]) -> None:
        for key in keys:
            index = self._key_to_index.pop(key, None)
            if index is not None:
                self._free_indices.append(index)
                self._data.pop(index, None)

                # Invalidate cache
                self._np_keys = None
            else:
                logger.warning(f"Key '{key}' not found in indexed key-value storage.")

    async def mask_new(self, keys: Iterable[GTKey]) -> Iterable[bool]:
        keys = list(keys)

        if len(keys) == 0:
            return np.array([], dtype=bool)

        if self._np_keys is None:
            self._np_keys = np.fromiter(
                self._key_to_index.keys(),
                count=len(self._key_to_index),
                dtype=type(keys[0]),
            )
        keys_array = np.array(keys, dtype=type(keys[0]))

        return ~np.isin(keys_array, self._np_keys)

    async def _insert_start(self):
        if self.namespace:
            data_file_name = self.namespace.get_load_path(self.RESOURCE_NAME)

            if data_file_name:
                try:
                    with open(data_file_name, "rb") as f:
                        self._data, self._free_indices, self._key_to_index = pickle.load(f)
                        logger.debug(
                            f"Loaded {len(self._data)} elements from indexed key-value storage '{data_file_name}'."
                        )
                except Exception as e:
                    t = f"Error loading data file for key-vector storage '{data_file_name}': {e}"
                    logger.error(t)
                    raise InvalidStorageError(t) from e
            else:
                logger.info(f"No data file found for key-vector storage '{data_file_name}'. Loading empty storage.")
                self._data = {}
                self._free_indices = []
                self._key_to_index = {}
        else:
            self._data = {}
            self._free_indices = []
            self._key_to_index = {}
            logger.debug("Creating new volatile indexed key-value storage.")
        self._np_keys = None

    async def _insert_done(self):
        if self.namespace:
            data_file_name = self.namespace.get_save_path(self.RESOURCE_NAME)
            try:
                with open(data_file_name, "wb") as f:
                    pickle.dump((self._data, self._free_indices, self._key_to_index), f)
                    logger.debug(f"Saving {len(self._data)} elements to indexed key-value storage '{data_file_name}'.")
            except Exception as e:
                t = f"Error saving data file for key-vector storage '{data_file_name}': {e}"
                logger.error(t)
                raise InvalidStorageError(t) from e

    async def _query_start(self):
        assert self.namespace, "Loading a kv storage requires a namespace."
        data_file_name = self.namespace.get_load_path(self.RESOURCE_NAME)
        if data_file_name:
            try:
                with open(data_file_name, "rb") as f:
                    self._data, self._free_indices, self._key_to_index = pickle.load(f)
                    logger.debug(
                        f"Loaded {len(self._data)} elements from indexed key-value storage '{data_file_name}'."
                    )
            except Exception as e:
                t = f"Error loading data file for key-vector storage {data_file_name}: {e}"
                logger.error(t)
                raise InvalidStorageError(t) from e
        else:
            logger.warning(f"No data file found for key-vector storage '{data_file_name}'. Loading empty storage.")
            self._data = {}
            self._free_indices = []
            self._key_to_index = {}

    async def _query_done(self):
        pass

```

### fast_graphrag/_storage/_namespace.py

```python
import os
import shutil
import time
from typing import Any, Callable, List, Optional

from fast_graphrag._exceptions import InvalidStorageError
from fast_graphrag._utils import logger


class Workspace:
    @staticmethod
    def new(working_dir: str, checkpoint: int = 0, keep_n: int = 0) -> "Workspace":
        return Workspace(working_dir, checkpoint, keep_n)

    @staticmethod
    def get_path(working_dir: str, checkpoint: Optional[int] = None) -> Optional[str]:
        if checkpoint is None:
            return None
        elif checkpoint == 0:
            return working_dir
        return os.path.join(working_dir, str(checkpoint))

    def __init__(self, working_dir: str, checkpoint: int = 0, keep_n: int = 0):
        self.working_dir: str = working_dir
        self.keep_n: int = keep_n
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)

        self.checkpoints = sorted(
            (int(x.name) for x in os.scandir(self.working_dir) if x.is_dir() and not x.name.startswith("0__err_")),
            reverse=True,
        )
        if self.checkpoints:
            self.current_load_checkpoint = checkpoint if checkpoint else self.checkpoints[0]
        else:
            self.current_load_checkpoint = checkpoint
        self.save_checkpoint: Optional[int] = None
        self.failed_checkpoints: List[str] = []

    def __del__(self):
        for checkpoint in self.failed_checkpoints:
            old_path = os.path.join(self.working_dir, checkpoint)
            new_path = os.path.join(self.working_dir, f"0__err_{checkpoint}")
            os.rename(old_path, new_path)

        if self.keep_n > 0:
            checkpoints = sorted((x.name for x in os.scandir(self.working_dir) if x.is_dir()), reverse=True)
            for checkpoint in checkpoints[self.keep_n + 1 :]:
                shutil.rmtree(os.path.join(self.working_dir, str(checkpoint)))

    def make_for(self, namespace: str) -> "Namespace":
        return Namespace(self, namespace)

    def get_load_path(self) -> Optional[str]:
        load_path = self.get_path(self.working_dir, self.current_load_checkpoint)
        if load_path == self.working_dir and len([x for x in os.scandir(load_path) if x.is_file()]) == 0:
            return None
        return load_path


    def get_save_path(self) -> str:
        if self.save_checkpoint is None:
            if self.keep_n > 0:
                self.save_checkpoint = int(time.time())
            else:
                self.save_checkpoint = 0
        save_path = self.get_path(self.working_dir, self.save_checkpoint)

        assert save_path is not None, "Save path cannot be None."

        if not os.path.exists(save_path):
            os.makedirs(save_path)
        return os.path.join(save_path)

    def _rollback(self) -> bool:
        if self.current_load_checkpoint is None:
            return False
        # List all directories in the working directory and select the one
        # with the smallest number greater then the current load checkpoint.
        try:
            self.current_load_checkpoint = next(x for x in self.checkpoints if x < self.current_load_checkpoint)
            logger.warning("Rolling back to checkpoint: %s", self.current_load_checkpoint)
        except (StopIteration, ValueError):
            self.current_load_checkpoint = None
            logger.warning("No checkpoints to rollback to. Last checkpoint tried: %s", self.current_load_checkpoint)

        return True

    async def with_checkpoints(self, fn: Callable[[], Any]) -> Any:
        while True:
            try:
                return await fn()
            except Exception as e:
                logger.warning("Error occurred loading checkpoint: %s", e)
                if self.current_load_checkpoint is not None:
                    self.failed_checkpoints.append(str(self.current_load_checkpoint))
                if self._rollback() is False:
                    break
        raise InvalidStorageError("No valid checkpoints to load or default storages cannot be created.")


class Namespace:
    def __init__(self, workspace: Workspace, namespace: Optional[str] = None):
        self.namespace = namespace
        self.workspace = workspace

    def get_load_path(self, resource_name: str) -> Optional[str]:
        assert self.namespace is not None, "Namespace must be set to get resource load path."
        load_path = self.workspace.get_load_path()
        if load_path is None:
            return None
        return os.path.join(load_path, f"{self.namespace}_{resource_name}")

    def get_save_path(self, resource_name: str) -> str:
        assert self.namespace is not None, "Namespace must be set to get resource save path."
        return os.path.join(self.workspace.get_save_path(), f"{self.namespace}_{resource_name}")

```

### fast_graphrag/_storage/_vdb_hnswlib.py

```python
import pickle
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Tuple, Union

import hnswlib
import numpy as np
import numpy.typing as npt
from scipy.sparse import csr_matrix

from fast_graphrag._exceptions import InvalidStorageError
from fast_graphrag._types import GTEmbedding, GTId, TScore
from fast_graphrag._utils import logger

from ._base import BaseVectorStorage


@dataclass
class HNSWVectorStorageConfig:
    ef_construction: int = field(default=64)
    M: int = field(default=48)
    max_elements: int = field(default=1000000)
    ef_search: int = field(default=64)
    num_threads: int = field(default=-1)


@dataclass
class HNSWVectorStorage(BaseVectorStorage[GTId, GTEmbedding]):
    RESOURCE_NAME = "hnsw_index_{}.bin"
    RESOURCE_METADATA_NAME = "hnsw_metadata.pkl"
    config: HNSWVectorStorageConfig = field()  # type: ignore
    _index: Any = field(init=False, default=None)  # type: ignore
    _metadata: Dict[GTId, Dict[str, Any]] = field(default_factory=dict)
    _current_elements: int = field(init=False, default=0)

    async def upsert(
        self,
        ids: Iterable[GTId],
        embeddings: Iterable[GTEmbedding],
        metadata: Union[Iterable[Dict[str, Any]], None] = None,
    ) -> None:
        ids = list(ids)
        embeddings = np.array(list(embeddings), dtype=np.float32)
        metadata = list(metadata) if metadata else None

        assert (len(ids) == len(embeddings)) and (
            metadata is None or (len(metadata) == len(ids))
        ), "ids, embeddings, and metadata (if provided) must have the same length"

        # TODO: this should expand the index
        if self._current_elements + len(embeddings) > self.config.max_elements:
            logger.error(f"HNSW index is full. Cannot insert {len(embeddings)} elements.")
            raise NotImplementedError(f"Cannot insert {len(embeddings)} elements. Full index.")

        if metadata:
            self._metadata.update(dict(zip(ids, metadata)))
        self._index.add_items(data=embeddings, ids=ids, num_threads=self.config.num_threads)
        self._current_elements = self._index.get_current_count()

    async def get_knn(
        self, embeddings: Iterable[GTEmbedding], top_k: int
    ) -> Tuple[Iterable[Iterable[GTId]], npt.NDArray[TScore]]:
        if self._current_elements == 0:
            empty_list: List[List[GTId]] = []
            logger.info("Querying knns in empty index.")
            return empty_list, np.array([], dtype=TScore)

        top_k = min(top_k, self._current_elements)

        if top_k > self.config.ef_search:
            self._index.set_ef(top_k)

        ids, distances = self._index.knn_query(data=embeddings, k=top_k, num_threads=self.config.num_threads)

        return ids, 1.0 - np.array(distances, dtype=TScore)

    async def score_all(
        self, embeddings: Iterable[GTEmbedding], top_k: int = 1, confidence_threshold: float = 0.0
    ) -> csr_matrix:
        if confidence_threshold > 0.0:
            raise NotImplementedError("Confidence threshold is not supported yet.")
        if not isinstance(embeddings, np.ndarray):
            embeddings = np.array(list(embeddings), dtype=np.float32)

        if embeddings.size == 0 or self._current_elements == 0:
            logger.warning(f"No provided embeddings ({embeddings.size}) or empty index ({self._current_elements}).")
            return csr_matrix((0, self._current_elements))

        top_k = min(top_k, self._current_elements)
        if top_k > self.config.ef_search:
            self._index.set_ef(top_k)

        ids, distances = self._index.knn_query(data=embeddings, k=top_k, num_threads=self.config.num_threads)

        ids = np.array(ids)
        scores = np.array(distances, dtype=TScore)

        # Create sparse distance matrix with shape (#embeddings, #all_embeddings)
        flattened_ids = ids.ravel()
        flattened_scores = scores.ravel()

        scores = csr_matrix(
            (flattened_scores, (np.repeat(np.arange(len(ids)), top_k), flattened_ids)),
            shape=(len(ids), self._current_elements),
        )

        scores.data = (2.0 - scores.data) * 0.5

        return scores

    async def _insert_start(self):
        self._index = hnswlib.Index(space="cosine", dim=self.embedding_dim)  # type: ignore

        if self.namespace:
            index_file_name = self.namespace.get_load_path(self.RESOURCE_NAME.format(self.embedding_dim))
            metadata_file_name = self.namespace.get_load_path(self.RESOURCE_METADATA_NAME)

            if index_file_name and metadata_file_name:
                try:
                    self._index.load_index(index_file_name, max_elements=self.config.max_elements)
                    with open(metadata_file_name, "rb") as f:
                        self._metadata, self._current_elements = pickle.load(f)
                        logger.debug(
                            f"Loaded {self._current_elements} elements from vectordb storage '{index_file_name}'."
                        )
                    return  # All good
                except Exception as e:
                    t = f"Error loading metadata file for vectordb storage '{metadata_file_name}': {e}"
                    logger.error(t)
                    raise InvalidStorageError(t) from e
            else:
                logger.info(f"No data file found for vectordb storage '{index_file_name}'. Loading empty vectordb.")
        else:
            logger.debug("Creating new volatile vectordb storage.")
        self._index.init_index(
            max_elements=self.config.max_elements,
            ef_construction=self.config.ef_construction,
            M=self.config.M,
        )
        self._index.set_ef(self.config.ef_search)
        self._metadata = {}
        self._current_elements = 0

    async def _insert_done(self):
        if self.namespace:
            index_file_name = self.namespace.get_save_path(self.RESOURCE_NAME.format(self.embedding_dim))
            metadata_file_name = self.namespace.get_save_path(self.RESOURCE_METADATA_NAME)

            try:
                self._index.save_index(index_file_name)
                with open(metadata_file_name, "wb") as f:
                    pickle.dump((self._metadata, self._current_elements), f)
                logger.debug(f"Saving {self._current_elements} elements from vectordb storage '{index_file_name}'.")
            except Exception as e:
                t = f"Error saving vectordb storage from {index_file_name}: {e}"
                logger.error(t)
                raise InvalidStorageError(t) from e

    async def _query_start(self):
        assert self.namespace, "Loading a vectordb requires a namespace."
        self._index = hnswlib.Index(space="cosine", dim=self.embedding_dim)  # type: ignore

        index_file_name = self.namespace.get_load_path(self.RESOURCE_NAME.format(self.embedding_dim))
        metadata_file_name = self.namespace.get_load_path(self.RESOURCE_METADATA_NAME)
        if index_file_name and metadata_file_name:
            try:
                self._index.load_index(index_file_name, max_elements=self.config.max_elements)
                with open(metadata_file_name, "rb") as f:
                    self._metadata, self._current_elements = pickle.load(f)
                logger.debug(f"Loaded {self._current_elements} elements from vectordb storage '{index_file_name}'.")
            except Exception as e:
                t = f"Error loading vectordb storage from {index_file_name}: {e}"
                logger.error(t)
                raise InvalidStorageError(t) from e
        else:
            logger.warning(f"No data file found for vectordb storage '{index_file_name}'. Loading empty vectordb.")
            self._metadata = {}
            self._current_elements = 0

    async def _query_done(self):
        pass

```

### fast_graphrag/_types.py

```python
from dataclasses import dataclass, field
from itertools import chain
from typing import Any, Dict, Generic, Iterable, List, Optional, Tuple, TypeAlias, TypeVar, Union

import numpy as np
import numpy.typing as npt
from pydantic import BaseModel, Field, field_validator
from pydantic._internal import _model_construction

####################################################################################################
# GENERICS
####################################################################################################

# Blob
GTBlob = TypeVar("GTBlob")

# KeyValue
GTKey = TypeVar("GTKey")
GTValue = TypeVar("GTValue")

# Vectordb
GTEmbedding = TypeVar("GTEmbedding")
GTHash = TypeVar("GTHash")

# Graph
GTGraph = TypeVar("GTGraph")
GTId = TypeVar("GTId")


@dataclass
class BTNode:
    name: Any


GTNode = TypeVar("GTNode", bound=BTNode)


@dataclass
class BTEdge:
    source: Any
    target: Any

    @staticmethod
    def to_attrs(edge: Optional[Any] = None, edges: Optional[Iterable[Any]] = None, **kwargs: Any) -> Dict[str, Any]:
        raise NotImplementedError


GTEdge = TypeVar("GTEdge", bound=BTEdge)
GTChunk = TypeVar("GTChunk")


# LLM
def _schema_no_title(schema: dict[str, Any]) -> None:
    schema.pop("required")
    for prop in schema.get("properties", {}).values():
        prop.pop("title", None)


class MetaModel(_model_construction.ModelMetaclass):
    def __new__(
        cls, name: str, bases: tuple[type[Any], ...], dct: Dict[str, Any], alias: Optional[str] = None, **kwargs: Any
    ) -> type:
        if alias:
            dct["__qualname__"] = alias
        if "BaseModel" not in [base.__name__ for base in bases]:
            bases = bases + (BaseModel,)
        return super().__new__(cls, name, bases, dct, json_schema_extra=_schema_no_title, **kwargs)


class BTResponseModel:
    class Model(BaseModel):
        @staticmethod
        def to_dataclass(pydantic: Any) -> Any:
            raise NotImplementedError

    def to_str(self) -> str:
        raise NotImplementedError


GTResponseModel = TypeVar("GTResponseModel", bound=Union[str, BaseModel, BTResponseModel])

####################################################################################################
# TYPES
####################################################################################################


def dump_to_csv(
    data: Iterable[object],
    fields: List[str],
    separator: str = "\t",
    with_header: bool = False,
    **values: Dict[str, List[Any]],
) -> List[str]:
    rows = list(
        chain(
            (separator.join(chain(fields, values.keys())),) if with_header else (),
            chain(
                separator.join(
                    chain(
                        (str(getattr(d, field)).replace("\t", "    ") for field in fields),
                        (str(v).replace("\t", "    ") for v in vs),
                    )
                )
                for d, *vs in zip(data, *values.values())
            ),
        )
    )
    return rows


def dump_to_reference_list(data: Iterable[object], separator: str = "\n=====\n\n"):
    return [f"[{i + 1}]  {d}{separator}" for i, d in enumerate(data)]


# Embedding types
TEmbeddingType: TypeAlias = np.float32
TEmbedding: TypeAlias = npt.NDArray[TEmbeddingType]

THash: TypeAlias = np.uint64
TScore: TypeAlias = np.float32
TIndex: TypeAlias = int
TId: TypeAlias = str


@dataclass
class TDocument:
    """A class for representing a piece of data."""

    data: str = field()
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TChunk:
    """A class for representing a chunk."""

    id: THash = field()
    content: str = field()
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return self.content


# Graph types
@dataclass
class TEntity(BTResponseModel, BTNode):
    name: str = field()
    type: str = Field()
    description: str = Field()

    def to_str(self) -> str:
        s = f"[NAME] {self.name}"
        if len(self.description):
            s += f"  [DESCRIPTION] {self.description}"
        return s

    class Model(BTResponseModel.Model, metaclass=MetaModel, alias="Entity"):
        name: str = Field(..., description="The name of the entity")
        type: str = Field(..., description="The type of the entity")
        desc: str = Field(..., description="The description of the entity")

        @staticmethod
        def to_dataclass(pydantic: "TEntity.Model") -> "TEntity":
            return TEntity(name=pydantic.name, type=pydantic.type, description=pydantic.desc)

        @field_validator("name", mode="before")
        @classmethod
        def uppercase_name(cls, value: str):
            return value.upper() if value else value

        @field_validator("type", mode="before")
        @classmethod
        def uppercase_type(cls, value: str):
            return value.upper() if value else value


class TQueryEntities(BaseModel):
    entities: List[str] = Field(
        ...,
        description=("The list of entities extracted from the query in the format 'name [type]'"),
    )
    n: int = Field(..., description="The number of named entities found")  # So that the LLM can answer 0.

    @field_validator("entities", mode="before")
    @classmethod
    def uppercase_source(cls, value: List[str]):
        return [e.upper() for e in value] if value else value


@dataclass
class TRelation(BTResponseModel, BTEdge):
    source: str = field()
    target: str = field()
    description: str = field()
    chunks: List[THash] | None = field(default=None)

    @staticmethod
    def to_attrs(
        edge: Optional["TRelation"] = None,
        edges: Optional[Iterable["TRelation"]] = None,
        include_source_target: bool = False,
        **_,
    ) -> Dict[str, Any]:
        if edge is not None:
            assert edges is None, "Either edge or edges should be provided, not both"
            return {
                "description": edge.description,
                "chunks": edge.chunks,
                **(
                    {
                        "source": edge.source,
                        "target": edge.target,
                    }
                    if include_source_target
                    else {}
                ),
            }
        elif edges is not None:
            return {
                "description": [e.description for e in edges],
                "chunks": [e.chunks for e in edges],
                **(
                    {
                        "source": [e.source for e in edges],
                        "target": [e.target for e in edges],
                    }
                    if include_source_target
                    else {}
                ),
            }
        else:
            return {}

    class Model(BTResponseModel.Model, metaclass=MetaModel, alias="Relation"):
        source: str = Field(..., description="The name of the source entity")
        target: str = Field(..., description="The name of the target entity")
        desc: str = Field(..., description="The description of the relationship between the source and target entity")

        @staticmethod
        def to_dataclass(pydantic: "TRelation.Model") -> "TRelation":
            return TRelation(source=pydantic.source, target=pydantic.target, description=pydantic.desc)

        @field_validator("source", mode="before")
        @classmethod
        def uppercase_source(cls, value: str):
            return value.upper() if value else value

        @field_validator("target", mode="before")
        @classmethod
        def uppercase_target(cls, value: str):
            return value.upper() if value else value


@dataclass
class TGraph(BTResponseModel):
    entities: List[TEntity] = field()
    relationships: List[TRelation] = field()

    class Model(BTResponseModel.Model, metaclass=MetaModel, alias="Graph"):
        entities: List[TEntity.Model] = Field(description="The list of extracted entities")
        relationships: List[TRelation.Model] = Field(description="The relationships between the entities")
        other_relationships: List[TRelation.Model] = Field(
            description=(
                "Other and missed relationships between the extracted entities"
                " (likely involving more generic entities)"
            )
        )

        @staticmethod
        def to_dataclass(pydantic: "TGraph.Model") -> "TGraph":
            return TGraph(
                entities=[p.to_dataclass(p) for p in pydantic.entities],
                relationships=[p.to_dataclass(p) for p in pydantic.relationships]
                + [p.to_dataclass(p) for p in pydantic.other_relationships],
            )


class TEditRelation(BaseModel):
    ids: List[int] = Field(..., description="The ids of the facts that you are combining into one.")
    description: str = Field(
        ..., description="The summarized description of the combined facts, in detail and comprehensive."
    )


class TEditRelationList(BaseModel):
    groups: List[TEditRelation] = Field(
        ...,
        description="The list of new fact groups. Include only groups of more than one fact.",
        alias="grouped_facts",
    )


@dataclass
class TContext(Generic[GTNode, GTEdge, GTHash, GTChunk]):
    """A class for representing the context used to generate a query response."""

    entities: List[Tuple[GTNode, TScore]]
    relationships: List[Tuple[GTEdge, TScore]]
    chunks: List[Tuple[GTChunk, TScore]]

    def to_str(self, max_chars: Dict[str, int]) -> str:
        """Convert the context to a string representation."""
        csv_tables: Dict[str, List[str]] = {
            "entities": dump_to_csv([e for e, _ in self.entities], ["name", "description"], with_header=True),
            "relationships": dump_to_csv(
                [r for r, _ in self.relationships], ["source", "target", "description"], with_header=True
            ),
            "chunks": dump_to_reference_list([str(c) for c, _ in self.chunks]),
        }
        csv_tables_row_length = {k: [len(row) for row in table] for k, table in csv_tables.items()}

        include_up_to = {
            "entities": 0,
            "relationships": 0,
            "chunks": 0,
        }

        # Truncate each csv to the maximum number of assigned tokens
        chars_remainder = 0
        while True:
            last_char_remainder = chars_remainder
            # Keep augmenting the context until feasible
            for table in csv_tables:
                for i in range(include_up_to[table], len(csv_tables_row_length[table])):
                    length = csv_tables_row_length[table][i] + 1  # +1 for the newline character
                    if length <= chars_remainder:  # use up the remainder
                        include_up_to[table] += 1
                        chars_remainder -= length
                    elif length <= max_chars[table]:  # use up the assigned tokens
                        include_up_to[table] += 1
                        max_chars[table] -= length
                    else:
                        break

                if max_chars[table] >= 0:  # if the assigned tokens are not used up store in the remainder
                    chars_remainder += max_chars[table]
                    max_chars[table] = 0

            # Truncate the csv
            if chars_remainder == last_char_remainder:
                break

        data: List[str] = []
        if len(self.entities):
            data.extend(
                [
                    "\n## Entities",
                    "```csv",
                    *csv_tables["entities"][: include_up_to["entities"]],
                    "```",
                ]
            )
        else:
            data.append("\n#Entities: None\n")

        if len(self.relationships):
            data.extend(
                [
                    "\n## Relationships",
                    "```csv",
                    *csv_tables["relationships"][: include_up_to["relationships"]],
                    "```",
                ]
            )
        else:
            data.append("\n## Relationships: None\n")

        if len(self.chunks):
            data.extend(
                [
                    "\n## Sources\n",
                    *csv_tables["chunks"][: include_up_to["chunks"]],
                ]
            )
        else:
            data.append("\n## Sources: None\n")
        return "\n".join(data)


@dataclass
class TQueryResponse(Generic[GTNode, GTEdge, GTHash, GTChunk]):
    """A class for representing a query response."""

    response: str
    context: TContext[GTNode, GTEdge, GTHash, GTChunk]

```

### fast_graphrag/_utils.py

```python
import asyncio
import logging
import time
from functools import wraps
from typing import Any, Callable, List, Optional, Tuple, TypeVar, Union

import numpy as np
import numpy.typing as npt
from scipy.sparse import csr_matrix

from fast_graphrag._types import TIndex

logger = logging.getLogger("graphrag")
TOKEN_TO_CHAR_RATIO = 4

def timeit(func: Callable[..., Any]):
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start
        wrapper.execution_times.append(duration)  # type: ignore
        return result

    wrapper.execution_times = []  # type: ignore
    return wrapper


def throttle_async_func_call(max_concurrent: int = 2048, stagger_time: Optional[float] = None, waitting_time: float = 0.001):
    _wrappedFn = TypeVar("_wrappedFn", bound=Callable[..., Any])
    def decorator(func: _wrappedFn) -> _wrappedFn:
        __current_exes = 0
        __current_queued = 0

        @wraps(func)
        async def wait_func(*args: Any, **kwargs: Any) -> Any:
            nonlocal __current_exes, __current_queued
            while __current_exes >= max_concurrent:
                await asyncio.sleep(waitting_time)

            # __current_queued += 1
            # await asyncio.sleep(stagger_time * (__current_queued - 1))
            # __current_queued -= 1
            __current_exes += 1
            result = await func(*args, **kwargs)
            __current_exes -= 1
            return result

        return wait_func  # type: ignore

    return decorator

def get_event_loop() -> asyncio.AbstractEventLoop:
    try:
        # If there is already an event loop, use it.
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If in a sub-thread, create a new event loop.
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


def extract_sorted_scores(row_vector: csr_matrix) -> Tuple[npt.NDArray[np.int64], npt.NDArray[np.float32]]:
    """Take a sparse row vector and return a list of non-zero (index, score) pairs sorted by score."""
    assert row_vector.shape[0] <= 1, "The input matrix must be a row vector."
    if row_vector.shape[0] == 0:
        return np.array([], dtype=np.int64), np.array([], dtype=np.float32)

    # Step 1: Get the indices of non-zero elements
    non_zero_indices = row_vector.nonzero()[1]

    # Step 2: Extract the probabilities of these indices
    probabilities = row_vector.data

    # Step 3: Use NumPy to create arrays for indices and probabilities
    indices_array = np.array(non_zero_indices)
    probabilities_array = np.array(probabilities)

    # Step 4: Sort the probabilities and get the sorted indices
    sorted_indices = np.argsort(probabilities_array)[::-1]

    # Step 5: Create sorted arrays for indices and probabilities
    sorted_indices_array = indices_array[sorted_indices]
    sorted_probabilities_array = probabilities_array[sorted_indices]

    return sorted_indices_array, sorted_probabilities_array


def csr_from_indices_list(
    data: List[List[Union[int, TIndex]]], shape: Tuple[int, int]
) -> csr_matrix:
    """Create a CSR matrix from a list of lists."""
    num_rows = len(data)

    # Flatten the list of lists and create corresponding row indices
    row_indices = np.repeat(np.arange(num_rows), [len(row) for row in data])
    col_indices = np.concatenate(data) if num_rows > 0 else np.array([], dtype=np.int64)

    # Data values (all ones in this case)
    values = np.broadcast_to(1, len(row_indices))

    # Create the CSR matrix
    return csr_matrix((values, (row_indices, col_indices)), shape=shape)

```

### pyproject.toml

```
[tool.poetry]
name = "fast-graphrag"
version = "0.0.3"
description = ""
authors = ["Luca Pinchetti <luca@circlemind.co>", "Antonio Vespoli <antonio@circlemind.co>", "Yuhang Song <yuhang@circlemind.co>"]
packages = [{include = "fast_graphrag" }]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.10.1"
igraph = "^0.11.6"
xxhash = "^3.5.0"
pydantic = "^2.9.2"
scipy = "^1.14.1"
scikit-learn = "^1.5.2"
tenacity = "^9.0.0"
openai = "^1.52.1"
scipy-stubs = "^1.14.1.3"
hnswlib = "^0.8.0"
instructor = "^1.6.3"
requests = "^2.32.3"
python-dotenv = "^1.0.1"


[tool.poetry.group.dev.dependencies]
ruff = "^0.7.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.ruff]
line-length = 120

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "N",  # PEP8 naming convetions
    "D"  # pydocstyle
]
ignore = [
    "C901",  # too complex
    "W191",  # indentation contains tabs
    "D401"  # imperative mood
]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.per-file-ignores]
"_prompt.py" = ["E501"]

```

### tests/__init__.py

```python
"""Testing."""

```

### tests/_graphrag_test.py

```python
# type: ignore
import unittest
from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, patch

from fast_graphrag._graphrag import BaseGraphRAG
from fast_graphrag._types import TContext, TQueryResponse


class TestBaseGraphRAG(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.llm_service = AsyncMock()
        self.chunking_service = AsyncMock()
        self.information_extraction_service = MagicMock()
        self.information_extraction_service.extract_entities_from_query = AsyncMock()
        self.state_manager = AsyncMock()
        self.state_manager.embedding_service.embedding_dim = self.state_manager.entity_storage.embedding_dim = 1

        @dataclass
        class BaseGraphRAGNoEmbeddingValidation(BaseGraphRAG):
            def __post_init__(self):
                pass

        self.graph_rag = BaseGraphRAGNoEmbeddingValidation(
            working_dir="test_dir",
            domain="test_domain",
            example_queries="test_query",
            entity_types=["type1", "type2"],
        )
        self.graph_rag.llm_service = self.llm_service
        self.graph_rag.chunking_service = self.chunking_service
        self.graph_rag.information_extraction_service = self.information_extraction_service
        self.graph_rag.state_manager = self.state_manager

    async def test_async_insert(self):
        self.chunking_service.extract = AsyncMock(return_value=["chunked_data"])
        self.state_manager.filter_new_chunks = AsyncMock(return_value=["new_chunks"])
        self.information_extraction_service.extract = MagicMock(return_value=["subgraph"])
        self.state_manager.upsert = AsyncMock()

        await self.graph_rag.async_insert("test_content", {"meta": "data"})

        self.chunking_service.extract.assert_called_once()
        self.state_manager.filter_new_chunks.assert_called_once()
        self.information_extraction_service.extract.assert_called_once()
        self.state_manager.upsert.assert_called_once()

    @patch("fast_graphrag._graphrag.format_and_send_prompt", new_callable=AsyncMock)
    async def test_async_query(self, format_and_send_prompt):
        self.information_extraction_service.extract_entities_from_query = AsyncMock(return_value=["entities"])
        self.state_manager.get_context = AsyncMock(return_value=TContext([], [], []))
        format_and_send_prompt.return_value=("response", None)

        response = await self.graph_rag.async_query("test_query")

        self.information_extraction_service.extract_entities_from_query.assert_called_once()
        self.state_manager.get_context.assert_called_once()
        format_and_send_prompt.assert_called_once()
        self.assertIsInstance(response, TQueryResponse)


if __name__ == "__main__":
    unittest.main()

```

### tests/_llm/__init__.py

```python

```

### tests/_llm/_base_test.py

```python
# type: ignore
import unittest
from unittest.mock import AsyncMock, patch

from fast_graphrag._llm._base import BaseLLMService, format_and_send_prompt

# Assuming these are defined somewhere in your codebase
PROMPTS = {
    "example_prompt": "Hello, {name}!"
}

class TestFormatAndSendPrompt(unittest.IsolatedAsyncioTestCase):

    @patch("fast_graphrag._llm._base.PROMPTS", PROMPTS)
    async def test_format_and_send_prompt(self):
        mock_llm = AsyncMock(spec=BaseLLMService())
        mock_response = (str(), [{"key": "value"}])
        mock_llm.send_message = AsyncMock(return_value=mock_response)

        result = await format_and_send_prompt(
            prompt_key="example_prompt",
            llm=mock_llm,
            format_kwargs={"name": "World"},
            response_model=str
        )

        mock_llm.send_message.assert_called_once_with(
            prompt="Hello, World!",
            response_model=str
        )
        self.assertEqual(result, mock_response)

    @patch("fast_graphrag._llm._base.PROMPTS", PROMPTS)
    async def test_format_and_send_prompt_with_additional_args(self):
        mock_llm = AsyncMock(spec=BaseLLMService())
        mock_response = (str(), [{"key": "value"}])
        mock_llm.send_message = AsyncMock(return_value=mock_response)

        result = await format_and_send_prompt(
            prompt_key="example_prompt",
            llm=mock_llm,
            format_kwargs={"name": "World"},
            response_model=str,
            model="test_model",
            max_tokens=100
        )

        mock_llm.send_message.assert_called_once_with(
            prompt="Hello, World!",
            response_model=str,
            model="test_model",
            max_tokens=100
        )
        self.assertEqual(result, mock_response)

if __name__ == "__main__":
    unittest.main()

```

### tests/_llm/_llm_openai_test.py

```python
# type: ignore
import os
import unittest
from unittest.mock import AsyncMock, MagicMock

import instructor
from openai import APIConnectionError, AsyncOpenAI, RateLimitError
from tenacity import RetryError

from fast_graphrag._exceptions import LLMServiceNoResponseError
from fast_graphrag._llm._llm_openai import OpenAIEmbeddingService, OpenAILLMService

os.environ["OPENAI_API_KEY"] = ""


RateLimitError429 = RateLimitError(message="Rate limit exceeded", response=MagicMock(), body=None)


class TestOpenAILLMService(unittest.IsolatedAsyncioTestCase):
    async def test_send_message_success(self):
        service = OpenAILLMService(api_key="test")
        mock_response = str("Hi!")
        service.llm_async_client = AsyncMock()
        service.llm_async_client.chat.completions.create = AsyncMock(return_value=mock_response)

        response, messages = await service.send_message(prompt="Hello", model="gpt-4o-mini")

        self.assertEqual(response, mock_response)
        self.assertEqual(messages[-1]["role"], "assistant")

    async def test_send_message_no_response(self):
        service = OpenAILLMService(api_key="test")
        service.llm_async_client = AsyncMock()
        service.llm_async_client.chat.completions.create.return_value = None

        with self.assertRaises(LLMServiceNoResponseError):
            await service.send_message(prompt="Hello", model="gpt-4o-mini")

    async def test_send_message_rate_limit_error(self):
        service = OpenAILLMService()
        mock_response = str("Hi!")
        async_open_ai = AsyncOpenAI(api_key="test")
        async_open_ai.chat.completions.create = AsyncMock(
            side_effect=(RateLimitError429, mock_response)
        )
        service.llm_async_client: instructor.AsyncInstructor = instructor.from_openai(
            async_open_ai
        )

        response, messages = await service.send_message(prompt="Hello", model="gpt-4o-mini", response_model=None)

        self.assertEqual(response, mock_response)
        self.assertEqual(messages[-1]["role"], "assistant")

    async def test_send_message_api_connection_error(self):
        service = OpenAILLMService()
        mock_response = str("Hi!")
        async_open_ai = AsyncOpenAI(api_key="test")
        async_open_ai.chat.completions.create = AsyncMock(
            side_effect=(APIConnectionError(request=MagicMock()), mock_response)
        )
        service.llm_async_client: instructor.AsyncInstructor = instructor.from_openai(
            async_open_ai
        )

        response, messages = await service.send_message(prompt="Hello", model="gpt-4o-mini")

        self.assertEqual(response, mock_response)
        self.assertEqual(messages[-1]["role"], "assistant")

    async def test_send_message_with_system_prompt(self):
        service = OpenAILLMService(api_key="test")
        mock_response = str("Hi!")
        service.llm_async_client = AsyncMock()
        service.llm_async_client.chat.completions.create = AsyncMock(return_value=mock_response)

        response, messages = await service.send_message(
            prompt="Hello", system_prompt="System prompt", model="gpt-4o-mini"
        )

        self.assertEqual(response, mock_response)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[0]["content"], "System prompt")

    async def test_send_message_with_history(self):
        service = OpenAILLMService(api_key="test")
        mock_response = str("Hi!")
        service.llm_async_client = AsyncMock()
        service.llm_async_client.chat.completions.create = AsyncMock(return_value=mock_response)

        history = [{"role": "user", "content": "Previous message"}]
        response, messages = await service.send_message(prompt="Hello", history_messages=history, model="gpt-4o-mini")

        self.assertEqual(response, mock_response)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[0]["content"], "Previous message")


class TestOpenAIEmbeddingService(unittest.IsolatedAsyncioTestCase):
    async def test_get_embedding_success(self):
        service = OpenAIEmbeddingService(api_key="test")
        mock_response = AsyncMock()
        mock_response.data = [AsyncMock(embedding=[0.1, 0.2, 0.3])]
        service.embedding_async_client.embeddings.create = AsyncMock(return_value=mock_response)

        embeddings = await service.get_embedding(texts=["test"], model="text-embedding-3-small")

        self.assertEqual(embeddings.shape, (1, 3))
        self.assertEqual(embeddings[0][0], 0.1)

    async def test_get_embedding_rate_limit_error(self):
        service = OpenAIEmbeddingService(api_key="test")
        mock_response = AsyncMock()
        mock_response.data = [AsyncMock(embedding=[0.1, 0.2, 0.3])]
        service.embedding_async_client.embeddings.create = AsyncMock(side_effect=(RateLimitError429, mock_response))

        embeddings = await service.get_embedding(texts=["test"], model="text-embedding-3-small")

        self.assertEqual(embeddings.shape, (1, 3))
        self.assertEqual(embeddings[0][0], 0.1)

    async def test_get_embedding_api_connection_error(self):
        service = OpenAIEmbeddingService(api_key="test")
        mock_response = AsyncMock()
        mock_response.data = [AsyncMock(embedding=[0.1, 0.2, 0.3])]
        service.embedding_async_client.embeddings.create = AsyncMock(
            side_effect=(APIConnectionError(request=MagicMock()), mock_response)
        )
        embeddings = await service.get_embedding(texts=["test"], model="text-embedding-3-small")

        self.assertEqual(embeddings.shape, (1, 3))
        self.assertEqual(embeddings[0][0], 0.1)

    async def test_get_embedding_retry_failure(self):
        service = OpenAIEmbeddingService(api_key="test")
        service.embedding_async_client.embeddings.create = AsyncMock(
            side_effect=RateLimitError429
        )

        with self.assertRaises(RetryError):
            await service.get_embedding(texts=["test"], model="text-embedding-3-small")

    async def test_get_embedding_with_different_model(self):
        service = OpenAIEmbeddingService(api_key="test")
        mock_response = AsyncMock()
        mock_response.data = [AsyncMock(embedding=[0.4, 0.5, 0.6])]
        service.embedding_async_client.embeddings.create = AsyncMock(return_value=mock_response)

        embeddings = await service.get_embedding(texts=["test"], model="text-embedding-3-large")

        self.assertEqual(embeddings.shape, (1, 3))
        self.assertEqual(embeddings[0][0], 0.4)


if __name__ == "__main__":
    unittest.main()

```

### tests/_policies/__init__.py

```python

```

### tests/_policies/_graph_upsert_test.py

```python
# type: ignore
import copy
import unittest
from unittest.mock import AsyncMock, MagicMock, call, patch

from fast_graphrag._llm._llm_openai import BaseLLMService
from fast_graphrag._policies._graph_upsert import (
    DefaultEdgeUpsertPolicy,
    # DefaultGraphUpsertPolicy,
    DefaultNodeUpsertPolicy,
    EdgeUpsertPolicy_UpsertIfValidNodes,
    EdgeUpsertPolicy_UpsertValidAndMergeSimilarByLLM,
    NodeUpsertPolicy_SummarizeDescription,
)
from fast_graphrag._storage._base import BaseGraphStorage


class TestNodeUpsertPolicy_SummarizeDescription(unittest.IsolatedAsyncioTestCase):  # noqa: N801
    async def test_call_same_node_summarize(self):
        # Mock dependencies
        llm = AsyncMock(spec=BaseLLMService)
        target = AsyncMock(spec=BaseGraphStorage)
        node1 = MagicMock()
        node1.name = "node1"
        node1.description = "This is a lengthy random description."
        node2 = MagicMock()
        node2.name = "node1"
        node2.description = "This is a lengthy random description that is being used to test the summarization."
        source_nodes = [node1, node2]

        # Mock methods
        llm.send_message.return_value = ("This is a summary.", None)
        target.get_node = AsyncMock(return_value=(None, None))
        target.upsert_node.side_effect = lambda node, node_index: node_index or 0

        # Create policy instance
        policy = NodeUpsertPolicy_SummarizeDescription(
            config=NodeUpsertPolicy_SummarizeDescription.Config(
                max_node_description_size=len(node1.description) + 4,
            )
        )

        # Call the method
        _, upserted_nodes = await policy(llm, target, source_nodes)
        self.assertEqual(upserted_nodes[0][1].name, "node1")
        self.assertEqual(upserted_nodes[0][1].description, "This is a summary.")

    async def test_call_same_node_no_summarize(self):
        # Mock dependencies
        llm = AsyncMock(spec=BaseLLMService)
        target = AsyncMock(spec=BaseGraphStorage)
        node1 = MagicMock()
        node1.name = "node1"
        node1.description = "This is a short random description 1."
        node2 = MagicMock()
        node2.name = "node1"
        node2.description = "This is a short random description 2."
        source_nodes = [node1, node2]

        # Mock methods
        llm.send_message.return_value = ("This is a summary.", None)
        target.get_node.side_effect = [(None, None), (node1, 0)]
        target.upsert_node.side_effect = lambda node, node_index: node_index or 0

        # Create policy instance
        policy = NodeUpsertPolicy_SummarizeDescription(
            config=NodeUpsertPolicy_SummarizeDescription.Config(
                max_node_description_size=(len(node1.description) * 2) + 4
            )
        )

        # Call the method
        _, upserted_nodes = await policy(llm, target, source_nodes)

        self.assertEqual(
            upserted_nodes[0][1].description,
            "This is a short random description 1.  This is a short random description 2.",
        )

        # Assertions
        llm.send_message.assert_not_called()

    async def test_call_two_nodes(self):
        # Mock dependencies
        llm = AsyncMock(spec=BaseLLMService)
        target = AsyncMock(spec=BaseGraphStorage)
        node1 = MagicMock()
        node1.name = "node1"
        node1.description = "Description for node1."
        node2 = MagicMock()
        node2.name = "node2"
        node2.description = "Description for node2."
        source_nodes = [node1, node2]

        # Mock methods
        llm.send_message.return_value = ("This is a summary.", None)
        target.get_node.side_effect = [(None, None), (None, None)]
        target.upsert_node.side_effect = lambda node, node_index: node_index or 0

        # Create policy instance
        policy = NodeUpsertPolicy_SummarizeDescription(
            config=NodeUpsertPolicy_SummarizeDescription.Config(
                max_node_description_size=len(node1.description) + 4,
            )
        )

        # Call the method
        _, upserted_nodes = await policy(llm, target, source_nodes)

        self.assertEqual(upserted_nodes[0][1].description, "Description for node1.")
        self.assertEqual(upserted_nodes[1][1].description, "Description for node2.")


class TestEdgeUpsertPolicy_UpsertIfValidNodes(unittest.IsolatedAsyncioTestCase):  # noqa: N801
    async def test_call(self):
        # Mock dependencies
        llm = AsyncMock(spec=BaseLLMService)
        target = AsyncMock(spec=BaseGraphStorage)
        edge1 = MagicMock()
        edge1.source = "source1"
        edge1.target = "target1"
        edge2 = MagicMock()
        edge2.source = "source1"
        edge2.target = "target2"
        source_edges = [edge1, edge2]

        # Mock methods
        target.get_node.side_effect = lambda x: (MagicMock(), None) if x in ["source1", "target1"] else (None, None)
        target.upsert_edge = AsyncMock()
        target.insert_edges = AsyncMock()

        # Create policy instance
        policy = EdgeUpsertPolicy_UpsertIfValidNodes(config=EdgeUpsertPolicy_UpsertIfValidNodes.Config())

        # Call the method
        await policy(llm, target, source_edges)

        # Assertions
        target.get_node.assert_has_calls([call("source1"), call("target1"), call("source1"), call("target2")])
        target.upsert_edge.assert_not_called()
        target.insert_edges.assert_called_once_with([edge1])


class TestDefaultNodeUpsertPolicy(unittest.IsolatedAsyncioTestCase):  # noqa: N801
    async def test_call_same_id(self):
        # Mock dependencies
        llm = AsyncMock(spec=BaseLLMService)
        target = AsyncMock(spec=BaseGraphStorage)
        node1 = MagicMock()
        node1.name = "node1"
        node1.description = "Description for node1."
        node2 = MagicMock()
        node2.name = "node1"
        node2.description = "Description for node2."
        source_nodes = [node1, node2]

        # Mock methods
        target.get_node = AsyncMock()
        target.get_node.side_effect = [(None, None), (node1, 0)]
        target.upsert_node = AsyncMock()
        target.upsert_node.side_effect = lambda node, node_index: node_index or 0

        # Create policy instance
        policy = DefaultNodeUpsertPolicy(config=None)

        # Call the method
        _, upserted = await policy(llm, target, source_nodes)
        upserted = list(upserted)

        self.assertEqual(len(upserted), 1)
        self.assertEqual(upserted[0][1].description, "Description for node2.")

        # Assertions
        target.get_node.assert_has_calls([call(node1), call(node2)])
        target.upsert_node.assert_has_calls([call(node=node1, node_index=None), call(node=node2, node_index=0)])

    async def test_call_different_id(self):
        # Mock dependencies
        llm = AsyncMock(spec=BaseLLMService)
        target = AsyncMock(spec=BaseGraphStorage)
        node1 = MagicMock()
        node1.name = "node1"
        node1.description = "Description for node1."
        node2 = MagicMock()
        node2.name = "node2"
        node2.description = "Description for node2."
        source_nodes = [node1, node2]

        # Mock methods
        target.get_node = AsyncMock()
        target.get_node.side_effect = [(None, None), (None, None)]
        target.upsert_node = AsyncMock()
        target.upsert_node.side_effect = [0, 1]  # type: ignore

        # Create policy instance
        policy = DefaultNodeUpsertPolicy(config=None)

        # Call the method
        _, upserted = await policy(llm, target, source_nodes)
        upserted = list(upserted)
        self.assertEqual(len(upserted), 2)

        # Assertions
        target.get_node.assert_has_calls([call(node1), call(node2)])
        target.upsert_node.assert_has_calls([call(node=node1, node_index=None), call(node=node2, node_index=None)])


class TestEdgeUpsertPolicy_UpsertValidAndMergeSimilarByLLM(unittest.IsolatedAsyncioTestCase):  # noqa: N801
    async def asyncSetUp(self):
        self.mock_llm = AsyncMock(spec=BaseLLMService)
        self.mock_target = AsyncMock(spec=BaseGraphStorage)

    async def test_call_edges_below_threshold(self):
        edge_upsert_policy = EdgeUpsertPolicy_UpsertValidAndMergeSimilarByLLM(
            EdgeUpsertPolicy_UpsertValidAndMergeSimilarByLLM.Config(edge_merge_threshold=1)
        )
        sources = ["node1", "node2", "node3"]
        targets = ["node4", "node5", "node6"]

        edges = [
            MagicMock(source=source, target=target, description=source + target)
            for source in sources
            for target in targets
        ]
        self.mock_target.get_edges = AsyncMock(return_value=[])

        insert_index = 0

        def _upsert_edge(edge, edge_index):
            nonlocal insert_index
            if edge_index is not None:
                return edge_index
            insert_index += 1
            return insert_index

        def _insert_edges(edges):
            return [_upsert_edge(edge, None) for edge in edges]

        self.mock_target.upsert_edge = AsyncMock(side_effect=_upsert_edge)
        self.mock_target.insert_edges = AsyncMock(side_effect=_insert_edges)
        self.mock_target.delete_edges_by_index = AsyncMock()

        target, upserted_edges = await edge_upsert_policy(self.mock_llm, self.mock_target, edges)
        self.assertEqual(len(list(upserted_edges)), 9)
        self.assertEqual(len(list(self.mock_target.delete_edges_by_index.call_args[0][0])), 0)
        self.assertEqual(insert_index, 9)
        self.mock_target.delete_edges_by_index.assert_called_once()

    @patch("fast_graphrag._policies._graph_upsert.format_and_send_prompt", new_callable=AsyncMock)
    async def test_call_edges_above_threshold(self, mock_format_and_send_prompt):
        edge_upsert_policy = EdgeUpsertPolicy_UpsertValidAndMergeSimilarByLLM(
            EdgeUpsertPolicy_UpsertValidAndMergeSimilarByLLM.Config(edge_merge_threshold=1)
        )
        sources = ["node1", "node2"]
        targets = ["node4", "node5"]

        edges = [
            MagicMock(source=source, target=target, description=source + target)
            for source in sources
            for target in targets
        ]
        existing_edges = {
            "node1node4": [(copy.copy(edges[0]), 1)],
            "node1node5": [
                (copy.copy(edges[1]), 0),
                (copy.copy(edges[1]), 2),
                (copy.copy(edges[1]), 3),
                (copy.copy(edges[1]), 4),
            ],
        }
        edges = [copy.copy(edges[0])] + edges  # add a duplicate for first edge
        self.mock_target.get_edges = AsyncMock(
            side_effect=lambda source_node, target_node: existing_edges.get(source_node + target_node, [])
        )

        def _format_and_send_prompt(format_kwargs, **kwargs):
            if "node4" in format_kwargs["edge_list"]:
                mock_result = MagicMock()
                mock_group = MagicMock()
                mock_group.ids = [0, 1]
                mock_group.description = "Summary"
                mock_result.groups = [mock_group]
                return mock_result, None
            elif "node5" in format_kwargs["edge_list"]:
                mock_result = MagicMock()
                mock_group1 = MagicMock()
                mock_group1.ids = [1, 2, 0]
                mock_group1.description = "Summary1"
                mock_group2 = MagicMock()
                mock_group2.ids = [4, 3]
                mock_group2.description = "Summary2"
                mock_result.groups = [mock_group1, mock_group2]
                return mock_result, None

        mock_format_and_send_prompt.side_effect = _format_and_send_prompt

        insert_index = 5  # number of existing edges

        def _upsert_edge(edge, edge_index):
            if edge_index is not None:
                return edge_index
            nonlocal insert_index
            i = insert_index
            insert_index += 1
            return i

        def _insert_edges(edges):
            return [_upsert_edge(edge, None) for edge in edges]

        self.mock_target.upsert_edge = AsyncMock(side_effect=_upsert_edge)
        self.mock_target.insert_edges = AsyncMock(side_effect=_insert_edges)
        self.mock_target.delete_edges_by_index = AsyncMock()

        target, upserted_edges = await edge_upsert_policy(self.mock_llm, self.mock_target, edges)
        upserted_edges = list(upserted_edges)
        edges = [e[1].description for e in upserted_edges]
        self.assertEqual(
            set(edges),
            {"Summary", "Summary1", "node1node4", "Summary2", "node2node4", "node2node5"}
        )
        self.assertEqual({e[0] for e in upserted_edges}, {1, 5, 2, 6, 7, 8})
        self.assertEqual(set(self.mock_target.delete_edges_by_index.call_args[0][0]), {0, 3, 4})


class TestDefaultEdgeUpsertPolicy(unittest.IsolatedAsyncioTestCase):  # noqa: N801
    async def test_call(self):
        # Mock dependencies
        llm = AsyncMock(spec=BaseLLMService)
        target = AsyncMock(spec=BaseGraphStorage)
        edge = MagicMock()
        source_edges = [edge]

        # Mock methods
        target.upsert_edge = AsyncMock()
        target.insert_edges = AsyncMock()

        # Create policy instance
        policy = DefaultEdgeUpsertPolicy(config=None)

        # Call the method
        await policy(llm, target, source_edges)

        # Assertions
        target.upsert_edge.assert_not_called()
        target.insert_edges.assert_called_once_with(source_edges)


# class TestDefaultGraphUpsertPolicy(unittest.IsolatedAsyncioTestCase):
#     async def test_call(self):
#         # Mock dependencies
#         llm = AsyncMock(spec=BaseLLMService)
#         source = AsyncMock(spec=BaseGraphStorage)
#         target_nodes = AsyncMock(spec=BaseGraphStorage)
#         target_edges = AsyncMock(spec=BaseGraphStorage)
#         node = MagicMock()
#         edge = MagicMock()
#         source_nodes = [node]
#         source_edges = [edge]

#         # Mock methods
#         policy = DefaultGraphUpsertPolicy[TEntity, TRelation, TId](
#             config=None,
#             nodes_upsert_cls=DefaultNodeUpsertPolicy[TEntity, TId],
#             edges_upsert_cls=DefaultEdgeUpsertPolicy[TRelation, TId],
#         )
#         policy._nodes_upsert = AsyncMock(return_value=target_nodes)
#         policy._edges_upsert = AsyncMock(return_value=target_edges)

#         # Call the method
#         result = await policy(llm, source, source_nodes, source_edges)

#         # Assertions
#         policy._nodes_upsert.assert_called_once_with(llm, source, source_nodes)
#         policy._edges_upsert.assert_called_once_with(llm, target_nodes, source_edges)
#         self.assertEqual(result, target_edges)

#     async def test_call_with_default(self):
#         pass


if __name__ == "__main__":
    unittest.main()

```

### tests/_policies/_ranking_test.py

```python
import unittest

import numpy as np
from scipy.sparse import csr_matrix

from fast_graphrag._policies._ranking import (
    RankingPolicy_Elbow,
    RankingPolicy_TopK,
    # RankingPolicy_WithConfidence,
    RankingPolicy_WithThreshold,
)


class TestRankingPolicyWithThreshold(unittest.TestCase):
    def test_threshold(self):
        policy = RankingPolicy_WithThreshold(RankingPolicy_WithThreshold.Config(0.1))
        scores = csr_matrix([0.05, 0.2, 0.15, 0.05])
        result = policy(scores)
        expected = csr_matrix([0, 0.2, 0.15, 0])
        np.testing.assert_array_equal(result.toarray(), expected.toarray())

    def test_all_below_threshold(self):
        policy = RankingPolicy_WithThreshold(RankingPolicy_WithThreshold.Config(0.1))
        scores = csr_matrix([0.05, 0.05, 0.05, 0.05])
        result = policy(scores)
        expected = csr_matrix([], shape=(1, 4))
        np.testing.assert_array_equal(result.toarray(), expected.toarray())

    def test_explicit_batch_size_1(self):
        policy = RankingPolicy_WithThreshold(RankingPolicy_WithThreshold.Config(0.1))
        scores = csr_matrix([[0.05, 0.2, 0.15, 0.05]])
        result = policy(scores)
        expected = csr_matrix([[0, 0.2, 0.15, 0]])
        np.testing.assert_array_equal(result.toarray(), expected.toarray())

    def test_all_above_threshold(self):
        policy = RankingPolicy_WithThreshold(RankingPolicy_WithThreshold.Config(0.1))
        scores = csr_matrix([0.15, 0.2, 0.25, 0.35])
        result = policy(scores)
        expected = csr_matrix([0.15, 0.2, 0.25, 0.35])
        np.testing.assert_array_equal(result.toarray(), expected.toarray())


class TestRankingPolicyTopK(unittest.TestCase):
    def test_top_k(self):
        policy = RankingPolicy_TopK(RankingPolicy_TopK.Config(2))
        scores = csr_matrix([0.05, 0.05, 0.2, 0.15, 0.25])
        result = policy(scores)
        expected = csr_matrix([0, 0, 0.2, 0.0, 0.25])
        np.testing.assert_array_equal(result.toarray(), expected.toarray())

        policy = RankingPolicy_TopK(RankingPolicy_TopK.Config(1))
        result = policy(scores)
        expected = csr_matrix([0, 0, 0.0, 0.0, 0.25])
        np.testing.assert_array_equal(result.toarray(), expected.toarray())

    def test_top_k_less_than_k(self):
        policy = RankingPolicy_TopK(RankingPolicy_TopK.Config(5))
        scores = csr_matrix([0.05, 0.2, 0.0, 0.15])
        result = policy(scores)
        expected = csr_matrix([0.05, 0.2, 0.0, 0.15])
        np.testing.assert_array_equal(result.toarray(), expected.toarray())

    def test_top_k_is_zero(self):
        policy = RankingPolicy_TopK(RankingPolicy_TopK.Config(0))
        scores = csr_matrix([0.05, 0.2, 0.15, 0.25])
        result = policy(scores)
        expected = csr_matrix([0.05, 0.2, 0.15, 0.25])
        np.testing.assert_array_equal(result.toarray(), expected.toarray())

    def test_top_k_all_zero(self):
        policy = RankingPolicy_TopK(RankingPolicy_TopK.Config(2))
        scores = csr_matrix([0, 0, 0, 0, 0])
        result = policy(scores)
        expected = csr_matrix([0, 0, 0, 0, 0])
        np.testing.assert_array_equal(result.toarray(), expected.toarray())


class TestRankingPolicyElbow(unittest.TestCase):
    def test_elbow(self):
        policy = RankingPolicy_Elbow(config=None)
        scores = csr_matrix([0.05, 0.2, 0.1, 0.25, 0.1])
        result = policy(scores)
        expected = csr_matrix([0, 0.2, 0.0, 0.25, 0])
        np.testing.assert_array_equal(result.toarray(), expected.toarray())

    def test_elbow_all_zero(self):
        policy = RankingPolicy_Elbow(config=None)
        scores = csr_matrix([0, 0, 0, 0, 0])
        result = policy(scores)
        expected = csr_matrix([0, 0, 0, 0, 0])
        np.testing.assert_array_equal(result.toarray(), expected.toarray())

    def test_elbow_all_same(self):
        policy = RankingPolicy_Elbow(config=None)
        scores = csr_matrix([0.05, 0.05, 0.05, 0.05, 0.05])
        result = policy(scores)
        expected = csr_matrix([0, 0.05, 0.05, 0.05, 0.05])
        np.testing.assert_array_equal(result.toarray(), expected.toarray())

# class TestRankingPolicyWithConfidence(unittest.TestCase):
#     def test_not_implemented(self):
#         policy = RankingPolicy_WithConfidence()
#         scores = csr_matrix([0.05, 0.2, 0.15, 0.25, 0.1])
#         with self.assertRaises(NotImplementedError):
#             policy(scores)

if __name__ == '__main__':
    unittest.main()

```

### tests/_services/__init__.py

```python

```

### tests/_services/_chunk_extraction_test.py

```python
# type: ignore
import unittest
from dataclasses import dataclass
from typing import Any, Dict
from unittest.mock import patch

import xxhash

from fast_graphrag._services._chunk_extraction import DefaultChunkingService
from fast_graphrag._types import THash


@dataclass
class MockDocument:
    data: str
    metadata: Dict[str, Any]


@dataclass
class MockChunk:
    id: THash
    content: str
    metadata: Dict[str, Any]


class TestDefaultChunkingService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.chunking_service = DefaultChunkingService()

    async def test_extract(self):
        doc1 = MockDocument(data="test data 1", metadata={"meta": "data1"})
        doc2 = MockDocument(data="test data 2", metadata={"meta": "data2"})
        documents = [doc1, doc2]

        with patch.object(
            self.chunking_service,
            "_extract_chunks",
            return_value=[
                MockChunk(id=THash(xxhash.xxh3_64_intdigest(doc1.data)), content=doc1.data, metadata=doc1.metadata)
            ],
        ) as mock_extract_chunks:
            chunks = await self.chunking_service.extract(documents)

        self.assertEqual(len(chunks), 2)
        self.assertEqual(len(chunks[0]), 1)
        self.assertEqual(chunks[0][0].content, "test data 1")
        self.assertEqual(chunks[0][0].metadata, {"meta": "data1"})
        mock_extract_chunks.assert_called()

    async def test_extract_with_duplicates(self):
        doc1 = MockDocument(data="test data 1", metadata={"meta": "data1"})
        doc2 = MockDocument(data="test data 1", metadata={"meta": "data1"})
        documents = [doc1, doc2]

        with patch.object(
            self.chunking_service,
            "_extract_chunks",
            return_value=[
                MockChunk(id=THash(xxhash.xxh3_64_intdigest(doc1.data)), content=doc1.data, metadata=doc1.metadata)
            ],
        ) as mock_extract_chunks:
            chunks = await self.chunking_service.extract(documents)

        self.assertEqual(len(chunks), 2)
        self.assertEqual(len(chunks[0]), 1)
        self.assertEqual(len(chunks[1]), 1)
        self.assertEqual(chunks[0][0].content, "test data 1")
        self.assertEqual(chunks[0][0].metadata, {"meta": "data1"})
        self.assertEqual(chunks[1][0].content, "test data 1")
        self.assertEqual(chunks[1][0].metadata, {"meta": "data1"})
        mock_extract_chunks.assert_called()

    async def test_extract_chunks(self):
        doc = MockDocument(data="test data", metadata={"meta": "data"})
        chunk = MockChunk(id=THash(xxhash.xxh3_64_intdigest(doc.data)), content=doc.data, metadata=doc.metadata)

        chunks = await self.chunking_service._extract_chunks(doc)
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].id, chunk.id)
        self.assertEqual(chunks[0].content, chunk.content)
        self.assertEqual(chunks[0].metadata, chunk.metadata)


if __name__ == "__main__":
    unittest.main()

```

### tests/_services/_information_extraction_test.py

```python
# type: ignore
import asyncio
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from fast_graphrag._llm._base import BaseLLMService
from fast_graphrag._policies._graph_upsert import BaseGraphUpsertPolicy
from fast_graphrag._services import DefaultInformationExtractionService
from fast_graphrag._storage._base import BaseGraphStorage
from fast_graphrag._types import TGraph, TQueryEntities


class TestDefaultInformationExtractionService(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.llm_service = MagicMock(spec=BaseLLMService)
        self.llm_service.send_message = AsyncMock()
        self.chunk = MagicMock()
        self.chunk.content = "test content"
        self.chunk.id = "chunk_id"
        self.document = [self.chunk]
        self.entity_types = [ "entity_type"]
        self.prompt_kwargs = {"domain": "test_domain"}
        self.service = DefaultInformationExtractionService(
            graph_upsert=None
        )
        self.service.graph_upsert = AsyncMock(spec=BaseGraphUpsertPolicy)

    @patch('fast_graphrag._services._information_extraction.format_and_send_prompt', new_callable=AsyncMock)
    async def test_extract_entities_from_query(self, mock_format_and_send_prompt):
        mock_format_and_send_prompt.return_value = (TQueryEntities(entities=["entity1", "entity2"], n=2), None)
        entities = await self.service.extract_entities_from_query(self.llm_service, "test query", self.prompt_kwargs)
        self.assertEqual(len(entities), 2)
        self.assertEqual(entities[0].name, "ENTITY1")
        self.assertEqual(entities[1].name, "ENTITY2")


    @patch('fast_graphrag._services._information_extraction.format_and_send_prompt', new_callable=AsyncMock)
    async def test_extract(self, mock_format_and_send_prompt):
        mock_format_and_send_prompt.return_value = (TGraph(entities=[], relationships=[]), [])
        tasks = self.service.extract(self.llm_service, [self.document], self.prompt_kwargs, self.entity_types)
        results = await asyncio.gather(*tasks)
        self.assertEqual(len(results), 1)
        self.assertIsInstance(results[0], BaseGraphStorage)

if __name__ == '__main__':
    unittest.main()

```

### tests/_storage/__init__.py

```python

```

### tests/_storage/_base_test.py

```python
# type: ignore
import unittest
from unittest.mock import AsyncMock, patch

from fast_graphrag._storage._base import BaseStorage


class TestBaseStorage(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.storage = BaseStorage(config=None)

    @patch.object(BaseStorage, '_insert_start', new_callable=AsyncMock)
    @patch.object(BaseStorage, '_query_done', new_callable=AsyncMock)
    @patch("fast_graphrag._storage._base.logger")
    async def test_insert_start_from_query_mode(self, mock_logger, mock_query_done, mock_insert_start):
        self.storage._mode = "query"
        self.storage._in_progress = True

        await self.storage.insert_start()

        mock_query_done.assert_called_once()
        mock_insert_start.assert_called_once()
        mock_logger.error.assert_called_once()
        self.assertEqual(self.storage._mode, "insert")
        self.assertFalse(self.storage._in_progress)

    @patch.object(BaseStorage, '_insert_start', new_callable=AsyncMock)
    async def test_insert_start_from_none_mode(self, mock_insert_start):
        self.storage._mode = None
        self.storage._in_progress = False

        await self.storage.insert_start()

        mock_insert_start.assert_called_once()
        self.assertEqual(self.storage._mode, "insert")
        self.assertFalse(self.storage._in_progress)

    @patch.object(BaseStorage, '_insert_done', new_callable=AsyncMock)
    async def test_insert_done_in_insert_mode(self, mock_insert_done):
        self.storage._mode = "insert"
        self.storage._in_progress = True

        await self.storage.insert_done()

        mock_insert_done.assert_called_once()

    @patch("fast_graphrag._storage._base.logger")
    async def test_insert_done_in_query_mode(self, mock_logger):
        self.storage._mode = "query"
        self.storage._in_progress = True

        await self.storage.insert_done()
        mock_logger.error.assert_called_once()

    @patch.object(BaseStorage, '_query_start', new_callable=AsyncMock)
    @patch.object(BaseStorage, '_insert_done', new_callable=AsyncMock)
    @patch("fast_graphrag._storage._base.logger")
    async def test_query_start_from_insert_mode(self, mock_logger, mock_insert_done, mock_query_start):
        self.storage._mode = "insert"
        self.storage._in_progress = True

        await self.storage.query_start()

        mock_insert_done.assert_called_once()
        mock_query_start.assert_called_once()
        mock_logger.error.assert_called_once()
        self.assertEqual(self.storage._mode, "query")
        self.assertFalse(self.storage._in_progress)

    @patch.object(BaseStorage, '_query_start', new_callable=AsyncMock)
    async def test_query_start_from_none_mode(self, mock_query_start):
        self.storage._mode = None
        self.storage._in_progress = False

        await self.storage.query_start()

        mock_query_start.assert_called_once()
        self.assertEqual(self.storage._mode, "query")

    @patch.object(BaseStorage, '_query_done', new_callable=AsyncMock)
    async def test_query_done_in_query_mode(self, mock_query_done):
        self.storage._mode = "query"
        self.storage._in_progress = True

        await self.storage.query_done()

        mock_query_done.assert_called_once()

    @patch("fast_graphrag._storage._base.logger")
    async def test_query_done_in_insert_mode(self, mock_logger):
        self.storage._mode = "insert"
        self.storage._in_progress = True

        await self.storage.query_done()
        mock_logger.error.assert_called_once()

if __name__ == "__main__":
    unittest.main()

```

### tests/_storage/_blob_pickle_test.py

```python
# type: ignore
import pickle
import unittest
from unittest.mock import MagicMock, mock_open, patch

from fast_graphrag._exceptions import InvalidStorageError
from fast_graphrag._storage._blob_pickle import PickleBlobStorage


class TestPickleBlobStorage(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.namespace = MagicMock()
        self.namespace.get_load_path.return_value = "blob_data.pkl"
        self.namespace.get_save_path.return_value = "blob_data.pkl"
        self.storage = PickleBlobStorage(namespace=self.namespace, config=None)

    async def test_get(self):
        self.storage._data = {"key": "value"}
        result = await self.storage.get()
        self.assertEqual(result, {"key": "value"})

    async def test_set(self):
        blob = {"key": "value"}
        await self.storage.set(blob)
        self.assertEqual(self.storage._data, blob)

    @patch("builtins.open", new_callable=mock_open, read_data=pickle.dumps({"key": "value"}))
    async def test_insert_start_with_existing_file(self, mock_open):
        await self.storage._insert_start()
        self.assertEqual(self.storage._data, {"key": "value"})
        mock_open.assert_called_once_with("blob_data.pkl", "rb")

    @patch("os.path.exists", return_value=False)
    async def test_insert_start_without_existing_file(self, mock_exists):
        self.namespace.get_load_path.return_value = None
        await self.storage._insert_start()
        self.assertIsNone(self.storage._data)

    @patch("builtins.open", new_callable=mock_open)
    async def test_insert_done(self, mock_open):
        self.storage._data = {"key": "value"}
        await self.storage._insert_done()
        mock_open.assert_called_once_with("blob_data.pkl", "wb")
        mock_open().write.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data=pickle.dumps({"key": "value"}))
    async def test_query_start_with_existing_file(self, mock_open):
        await self.storage._query_start()
        self.assertEqual(self.storage._data, {"key": "value"})
        mock_open.assert_called_once_with("blob_data.pkl", "rb")

    @patch("fast_graphrag._storage._blob_pickle.logger")
    async def test_query_start_without_existing_file(self, mock_logger):
        self.namespace.get_load_path.return_value = None
        await self.storage._query_start()
        self.assertIsNone(self.storage._data)
        mock_logger.warning.assert_called_once()

    @patch("fast_graphrag._storage._blob_pickle.logger")
    async def test_insert_start_with_invalid_file(self, mock_logger):
        with self.assertRaises(InvalidStorageError):
            await self.storage._insert_start()
        mock_logger.error.assert_called_once()

    @patch("fast_graphrag._storage._blob_pickle.logger")
    async def test_query_start_with_invalid_file(self, mock_logger):
        with self.assertRaises(InvalidStorageError):
            await self.storage._query_start()
        mock_logger.error.assert_called_once()

    async def test_query_done(self):
        await self.storage._query_done()  # Should not raise any exceptions


if __name__ == "__main__":
    unittest.main()

```

### tests/_storage/_gdb_igraph_test.py

```python
# type: ignore

import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import numpy as np

from fast_graphrag._storage._gdb_igraph import IGraphStorage, IGraphStorageConfig
from fast_graphrag._types import TEntity, TRelation


class TestIGraphStorage(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.config = IGraphStorageConfig(node_cls=TEntity, edge_cls=TRelation)
        self.storage = IGraphStorage(config=self.config)
        self.storage._graph = MagicMock()

    async def test_node_count(self):
        self.storage._graph.vcount.return_value = 10
        count = await self.storage.node_count()
        self.assertEqual(count, 10)

    async def test_edge_count(self):
        self.storage._graph.ecount.return_value = 20
        count = await self.storage.edge_count()
        self.assertEqual(count, 20)

    async def test_get_node(self):
        node = MagicMock()
        node.name = "node1"
        node.attributes.return_value = {"name": "foo", "description": "value"}
        self.storage._graph.vs.find.return_value = node

        result = await self.storage.get_node("node1")
        self.assertEqual(result, (TEntity(**node.attributes()), node.index))

    async def test_get_node_not_found(self):
        self.storage._graph.vs.find.side_effect = ValueError
        result = await self.storage.get_node("node1")
        self.assertEqual(result, (None, None))

    async def test_get_edges(self):
        self.storage.get_edge_indices = AsyncMock(return_value=[0, 1])
        self.storage.get_edge_by_index = AsyncMock(
            side_effect=[TRelation(source="node1", target="node2", description="txt"), None]
        )

        edges = await self.storage.get_edges("node1", "node2")
        self.assertEqual(edges, [(TRelation(source="node1", target="node2", description="txt"), 0)])

    async def test_get_edge_indices(self):
        self.storage._graph.vs.find.side_effect = lambda name: MagicMock(index=name)
        self.storage._graph.es.select.return_value = [MagicMock(index=0), MagicMock(index=1)]

        indices = await self.storage.get_edge_indices("node1", "node2")
        self.assertEqual(list(indices), [0, 1])

    async def test_get_node_by_index(self):
        node = MagicMock()
        node.attributes.return_value = {"name": "foo", "description": "value"}
        self.storage._graph.vs.__getitem__.return_value = node
        self.storage._graph.vcount.return_value = 1

        result = await self.storage.get_node_by_index(0)
        self.assertEqual(result, TEntity(**node.attributes()))

    async def test_get_edge_by_index(self):
        edge = MagicMock()
        edge.source = "node0"
        edge.target = "node1"
        edge.attributes.return_value = {"description": "value"}
        self.storage._graph.es.__getitem__.return_value = edge
        self.storage._graph.vs.__getitem__.side_effect = lambda idx: {"name": idx}
        self.storage._graph.ecount.return_value = 1

        result = await self.storage.get_edge_by_index(0)
        self.assertEqual(result, TRelation(source="node0", target="node1", **edge.attributes()))

    async def test_upsert_node(self):
        node = TEntity(name="node1", description="value")
        self.storage._graph.vcount.return_value = 1
        self.storage._graph.vs.__getitem__.return_value = MagicMock(index=0)

        index = await self.storage.upsert_node(node, 0)
        self.assertEqual(index, 0)

    async def test_upsert_edge(self):
        edge = TRelation(source="node1", target="node2", description="desc", chunks=[])
        self.storage._graph.ecount.return_value = 1
        self.storage._graph.es.__getitem__.return_value = MagicMock(index=0)

        index = await self.storage.upsert_edge(edge, 0)
        self.assertEqual(index, 0)

    async def test_delete_edges_by_index(self):
        self.storage._graph.delete_edges = MagicMock()
        indices = [0, 1]
        await self.storage.delete_edges_by_index(indices)
        self.storage._graph.delete_edges.assert_called_with(indices)

    @patch("fast_graphrag._storage._gdb_igraph.logger")
    async def test_score_nodes_empty_graph(self, mock_logger):
        self.storage._graph.vcount.return_value = 0
        scores = await self.storage.score_nodes(None)
        self.assertEqual(scores.shape, (1, 0))
        mock_logger.info.assert_called_with("Trying to score nodes in an empty graph.")

    async def test_score_nodes(self):
        self.storage._graph.vcount.return_value = 3
        self.storage._graph.personalized_pagerank.return_value = [0.1, 0.2, 0.7]

        scores = await self.storage.score_nodes(None)
        self.assertTrue(np.array_equal(scores.toarray(), np.array([[0.1, 0.2, 0.7]], dtype=np.float32)))

    async def test_get_entities_to_relationships_map_empty_graph(self):
        self.storage._graph.vs = []
        result = await self.storage.get_entities_to_relationships_map()
        self.assertEqual(result.shape, (0, 0))

    @patch("fast_graphrag._storage._gdb_igraph.csr_from_indices_list")
    async def test_get_entities_to_relationships_map(self, mock_csr_from_indices_list):
        self.storage._graph.vs = [MagicMock(incident=lambda: [MagicMock(index=0), MagicMock(index=1)])]
        self.storage.node_count = AsyncMock(return_value=1)
        self.storage.edge_count = AsyncMock(return_value=2)

        await self.storage.get_entities_to_relationships_map()
        mock_csr_from_indices_list.assert_called_with([[0, 1]], shape=(1, 2))

    async def test_get_relationships_attrs_empty_graph(self):
        self.storage._graph.es = []
        result = await self.storage.get_relationships_attrs("key")
        self.assertEqual(result, [])

    async def test_get_relationships_attrs(self):
        self.storage._graph.es.__getitem__.return_value = [[1, 2], [3, 4]]
        self.storage._graph.es.__len__.return_value = 2
        result = await self.storage.get_relationships_attrs("key")
        self.assertEqual(result, [[1, 2], [3, 4]])

    @patch("igraph.Graph.Read_Picklez")
    @patch("fast_graphrag._storage._gdb_igraph.logger")
    async def test_insert_start_with_existing_file(self, mock_logger, mock_read_picklez):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_load_path.return_value = "dummy_path"

        await self.storage._insert_start()

        mock_read_picklez.assert_called_with("dummy_path")
        mock_logger.debug.assert_called_with("Loaded graph storage 'dummy_path'.")

    @patch("igraph.Graph")
    @patch("fast_graphrag._storage._gdb_igraph.logger")
    async def test_insert_start_with_no_file(self, mock_logger, mock_graph):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_load_path.return_value = None

        await self.storage._insert_start()

        mock_graph.assert_called_with(directed=False)
        mock_logger.info.assert_called_with("No data file found for graph storage 'None'. Loading empty graph.")

    @patch("igraph.Graph")
    @patch("fast_graphrag._storage._gdb_igraph.logger")
    async def test_insert_start_with_no_namespace(self, mock_logger, mock_graph):
        self.storage.namespace = None

        await self.storage._insert_start()

        mock_graph.assert_called_with(directed=False)
        mock_logger.debug.assert_called_with("Creating new volatile graphdb storage.")

    @patch("igraph.Graph.write_picklez")
    @patch("fast_graphrag._storage._gdb_igraph.logger")
    async def test_insert_done(self, mock_logger, mock_write_picklez):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_save_path.return_value = "dummy_path"

        await self.storage._insert_done()

        mock_write_picklez.assert_called_with(self.storage._graph, "dummy_path")

    @patch("igraph.Graph.Read_Picklez")
    @patch("fast_graphrag._storage._gdb_igraph.logger")
    async def test_query_start_with_existing_file(self, mock_logger, mock_read_picklez):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_load_path.return_value = "dummy_path"

        await self.storage._query_start()

        mock_read_picklez.assert_called_with("dummy_path")
        mock_logger.debug.assert_called_with("Loaded graph storage 'dummy_path'.")

    @patch("igraph.Graph")
    @patch("fast_graphrag._storage._gdb_igraph.logger")
    async def test_query_start_with_no_file(self, mock_logger, mock_graph):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_load_path.return_value = None

        await self.storage._query_start()

        mock_graph.assert_called_with(directed=False)
        mock_logger.warning.assert_called_with(
            "No data file found for graph storage 'None'. Loading empty graph."
        )


if __name__ == "__main__":
    unittest.main()

```

### tests/_storage/_ikv_pickle_test.py

```python
# type: ignore
import pickle
import unittest
from unittest.mock import MagicMock, mock_open, patch

import numpy as np

from fast_graphrag._exceptions import InvalidStorageError
from fast_graphrag._storage._ikv_pickle import PickleIndexedKeyValueStorage


class TestPickleIndexedKeyValueStorage(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.storage = PickleIndexedKeyValueStorage(namespace=None, config=None)
        await self.storage._insert_start()

    async def test_size(self):
        self.storage._data = {1: "value1", 2: "value2"}
        size = await self.storage.size()
        self.assertEqual(size, 2)

    async def test_get(self):
        self.storage._data = {1: "value1", 2: "value2"}
        self.storage._key_to_index = {"key1": 1, "key2": 2}
        result = await self.storage.get(["key1", "key2", "key3"])
        self.assertEqual(list(result), ["value1", "value2", None])

    async def test_get_by_index(self):
        self.storage._data = {1: "value1", 2: "value2"}
        result = await self.storage.get_by_index([1, 2, 3])
        self.assertEqual(list(result), ["value1", "value2", None])

    async def test_get_index(self):
        self.storage._key_to_index = {"key1": 1, "key2": 2}
        result = await self.storage.get_index(["key1", "key2", "key3"])
        self.assertEqual(list(result), [1, 2, None])

    async def test_upsert(self):
        await self.storage.upsert(["key1", "key2"], ["value1", "value2"])
        self.assertEqual(self.storage._data, {0: "value1", 1: "value2"})
        self.assertEqual(self.storage._key_to_index, {"key1": 0, "key2": 1})

    async def test_delete(self):
        self.storage._data = {0: "value1", 1: "value2"}
        self.storage._key_to_index = {"key1": 0, "key2": 1}
        await self.storage.delete(["key1"])
        self.assertEqual(self.storage._data, {1: "value2"})
        self.assertEqual(self.storage._key_to_index, {"key2": 1})
        self.assertEqual(self.storage._free_indices, [0])

    async def test_mask_new(self):
        self.storage._key_to_index = {"key1": 0, "key2": 1}
        result = await self.storage.mask_new([["key1", "key3"]])
        self.assertTrue(np.array_equal(result, [[False, True]]))

    @patch("builtins.open", new_callable=mock_open, read_data=pickle.dumps(({0: "value"}, [1, 2, 3], {"key": 0})))
    @patch("os.path.exists", return_value=True)
    @patch("fast_graphrag._storage._ikv_pickle.logger")
    async def test_insert_start_with_existing_file(self, mock_logger, mock_exists, mock_open):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_load_path.return_value = "dummy_path"

        # Call the function
        await self.storage._insert_start()

        # Check if data was loaded correctly
        self.assertEqual(self.storage._data, {0: "value"})
        self.assertEqual(self.storage._free_indices, [1, 2, 3])
        self.assertEqual(self.storage._key_to_index, {"key": 0})
        mock_logger.debug.assert_called_once()

    @patch("fast_graphrag._storage._ikv_pickle.logger")
    async def test_insert_start_with_no_file(self, mock_logger):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_load_path.return_value = "dummy_path"

        # Call the function
        with self.assertRaises(InvalidStorageError):
            await self.storage._insert_start()

    @patch("fast_graphrag._storage._ikv_pickle.logger")
    async def test_insert_start_with_no_namespace(self, mock_logger):
        self.storage.namespace = None

        # Call the function
        await self.storage._insert_start()

        # Check if data was initialized correctly
        self.assertEqual(self.storage._data, {})
        self.assertEqual(self.storage._free_indices, [])
        mock_logger.debug.assert_called_with("Creating new volatile indexed key-value storage.")

    @patch("builtins.open", new_callable=mock_open)
    @patch("fast_graphrag._storage._ikv_pickle.logger")
    async def test_insert_done(self, mock_logger, mock_open):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_save_path.return_value = "dummy_path"
        self.storage._data = {0: "value"}
        self.storage._free_indices = [1, 2, 3]
        self.storage._key_to_index = {"key": 0}

        # Call the function
        await self.storage._insert_done()

        # Check if data was saved correctly
        mock_open.assert_called_with("dummy_path", "wb")
        mock_logger.debug.assert_called_with("Saving 1 elements to indexed key-value storage 'dummy_path'.")

    @patch("builtins.open", new_callable=mock_open, read_data=pickle.dumps(({0: "value"}, [1, 2, 3], {"key": 0})))
    @patch("os.path.exists", return_value=True)
    @patch("fast_graphrag._storage._ikv_pickle.logger")
    async def test_query_start_with_existing_file(self, mock_logger, mock_exists, mock_open):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_load_path.return_value = "dummy_path"

        # Call the function
        await self.storage._query_start()

        # Check if data was loaded correctly
        self.assertEqual(self.storage._data, {0: "value"})
        self.assertEqual(self.storage._free_indices, [1, 2, 3])
        self.assertEqual(self.storage._key_to_index, {"key": 0})
        mock_logger.debug.assert_called_with("Loaded 1 elements from indexed key-value storage 'dummy_path'.")

    @patch("os.path.exists", return_value=False)
    @patch("fast_graphrag._storage._ikv_pickle.logger")
    async def test_query_start_with_no_file(self, mock_logger, mock_exists):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_load_path.return_value = None

        # Call the function
        await self.storage._query_start()

        # Check if data was initialized correctly
        self.assertEqual(self.storage._data, {})
        self.assertEqual(self.storage._free_indices, [])
        mock_logger.warning.assert_called_with(
            "No data file found for key-vector storage 'None'. Loading empty storage."
        )


if __name__ == "__main__":
    unittest.main()

```

### tests/_storage/_namespace_test.py

```python
import gc
import os
import shutil
import unittest
from typing import cast

from fast_graphrag._exceptions import InvalidStorageError
from fast_graphrag._storage._namespace import Namespace, Workspace


class TestWorkspace(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        def _(self: Workspace) -> None:
            pass

        Workspace.__del__ = _
        self.test_dir = "test_workspace"
        self.workspace = Workspace(self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_new_workspace(self):
        ws = Workspace.new(self.test_dir)
        self.assertIsInstance(ws, Workspace)
        self.assertEqual(ws.working_dir, self.test_dir)

    def test_get_load_path_no_checkpoint(self):
        self.assertEqual(self.workspace.get_load_path(), None)

    def test_get_save_path_creates_directory(self):
        save_path = self.workspace.get_save_path()
        self.assertTrue(os.path.exists(save_path))

    async def test_with_checkpoint_failures(self):
        for checkpoint in [1, 2, 3]:
            os.makedirs(os.path.join(self.test_dir, str(checkpoint)))
        self.workspace = Workspace(self.test_dir)

        async def sample_fn():
            if "1" not in cast(str, self.workspace.get_load_path()):
                raise Exception("Checkpoint not loaded")
            return "success"

        result = await self.workspace.with_checkpoints(sample_fn)
        self.assertEqual(result, "success")
        self.assertEqual(self.workspace.current_load_checkpoint, 1)
        self.assertEqual(self.workspace.failed_checkpoints, ["3", "2"])

    async def test_with_checkpoint_no_failure(self):
        for checkpoint in [1, 2, 3]:
            os.makedirs(os.path.join(self.test_dir, str(checkpoint)))
        self.workspace = Workspace(self.test_dir)

        async def sample_fn():
            return "success"

        result = await self.workspace.with_checkpoints(sample_fn)
        self.assertEqual(result, "success")
        self.assertEqual(self.workspace.current_load_checkpoint, 3)
        self.assertEqual(self.workspace.failed_checkpoints, [])

    async def test_with_checkpoint_all_failures(self):
        for checkpoint in [1, 2, 3]:
            os.makedirs(os.path.join(self.test_dir, str(checkpoint)))
        self.workspace = Workspace(self.test_dir)

        async def sample_fn():
            raise Exception("Checkpoint not loaded")

        with self.assertRaises(InvalidStorageError):
            await self.workspace.with_checkpoints(sample_fn)
        self.assertEqual(self.workspace.current_load_checkpoint, None)
        self.assertEqual(self.workspace.failed_checkpoints, ["3", "2", "1"])

    async def test_with_checkpoint_all_failures_accept_none(self):
        for checkpoint in [1, 2, 3]:
            os.makedirs(os.path.join(self.test_dir, str(checkpoint)))
        self.workspace = Workspace(self.test_dir)

        async def sample_fn():
            if self.workspace.get_load_path() is not None:
                raise Exception("Checkpoint not loaded")

        result = await self.workspace.with_checkpoints(sample_fn)
        self.assertEqual(result, None)
        self.assertEqual(self.workspace.current_load_checkpoint, None)
        self.assertEqual(self.workspace.failed_checkpoints, ["3", "2", "1"])


class TestNamespace(unittest.TestCase):
    def setUp(self):
        def _(self: Workspace) -> None:
            pass

        Workspace.__del__ = _

    def test_get_load_path_no_checkpoint_no_file(self):
        self.test_dir = "test_workspace"
        self.workspace = Workspace(self.test_dir)
        self.workspace.__del__ = lambda: None
        self.namespace = Namespace(self.workspace, "test_namespace")
        self.assertEqual(None, self.namespace.get_load_path("resource"))
        del self.workspace
        gc.collect()
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_get_load_path_no_checkpoint_with_file(self):
        self.test_dir = "test_workspace"
        self.workspace = Workspace(self.test_dir)
        self.workspace.__del__ = lambda: None
        self.namespace = Namespace(self.workspace, "test_namespace")

        with open(os.path.join(self.test_dir, "test_namespace_resource"), "w") as f:
            f.write("test")
        self.assertEqual(
            os.path.join("test_workspace", "test_namespace_resource"), self.namespace.get_load_path("resource")
        )
        del self.workspace
        gc.collect()
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_get_load_path_with_checkpoint(self):
        self.test_dir = "test_workspace"
        self.workspace = Workspace(self.test_dir)
        self.namespace = Namespace(self.workspace, "test_namespace")
        self.workspace.current_load_checkpoint = 1
        load_path = self.namespace.get_load_path("resource")
        self.assertEqual(load_path, os.path.join(self.test_dir, "1", "test_namespace_resource"))

        del self.workspace
        gc.collect()
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_get_save_path_creates_directory(self):
        self.test_dir = "test_workspace"
        self.workspace = Workspace(self.test_dir)
        self.namespace = Namespace(self.workspace, "test_namespace")
        save_path = self.namespace.get_save_path("resource")
        self.assertTrue(os.path.exists(os.path.join(*os.path.split(save_path)[:-1])))

        del self.workspace
        gc.collect()
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)


if __name__ == "__main__":
    unittest.main()

```

### tests/_storage/_vdb_hnswlib_test.py

```python
# type: ignore
import pickle
import unittest
from unittest.mock import MagicMock, mock_open, patch

import numpy as np

from fast_graphrag._storage._vdb_hnswlib import HNSWVectorStorage, HNSWVectorStorageConfig, InvalidStorageError


class TestHNSWVectorStorage(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.config = HNSWVectorStorageConfig()
        self.storage = HNSWVectorStorage(config=self.config, embedding_dim=128)
        self.storage._index = MagicMock()
        self.storage._index.get_current_count.return_value = 0

    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_upsert(self, mock_logger):
        ids = [1, 2, 3]
        embeddings = np.random.rand(3, 128).astype(np.float32)
        metadata = [{"meta1": "data1"}, {"meta2": "data2"}, {"meta3": "data3"}]

        self.storage._current_elements = 0
        self.storage._index.get_current_count.return_value = 3

        await self.storage.upsert(ids, embeddings, metadata)

        self.assertEqual(self.storage._current_elements, 3)
        self.assertEqual(self.storage._metadata[1], {"meta1": "data1"})
        self.assertEqual(self.storage._metadata[2], {"meta2": "data2"})
        self.assertEqual(self.storage._metadata[3], {"meta3": "data3"})

    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_upsert_full_index(self, mock_logger):
        ids = [1, 2, 3]
        embeddings = np.random.rand(3, 128).astype(np.float32)

        self.storage._current_elements = self.config.max_elements

        with self.assertRaises(NotImplementedError):
            await self.storage.upsert(ids, embeddings)

        mock_logger.error.assert_called_with("HNSW index is full. Cannot insert 3 elements.")

    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_get_knn_empty_index(self, mock_logger):
        embeddings = np.random.rand(1, 128).astype(np.float32)

        ids, distances = await self.storage.get_knn(embeddings, top_k=5)

        self.assertEqual(ids, [])
        self.assertTrue(np.array_equal(distances, np.array([], dtype=np.float32)))
        mock_logger.info.assert_called_with("Querying knns in empty index.")

    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_get_knn(self, mock_logger):
        embeddings = np.random.rand(2, 128).astype(np.float32)
        self.storage._current_elements = 10
        self.storage._index.knn_query.return_value = ([[1, 2, 3], [4, 5, 6]], [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]])

        ids, distances = await self.storage.get_knn(embeddings, top_k=3)

        self.storage._index.knn_query.assert_called_once_with(data=embeddings, k=3, num_threads=self.config.num_threads)
        self.assertEqual(ids, [[1, 2, 3], [4, 5, 6]])
        np.testing.assert_almost_equal(distances, np.array([[0.9, 0.8, 0.7], [0.6, 0.5, 0.4]], dtype=np.float32))

    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_score_all_empty_index(self, mock_logger):
        embeddings = np.random.rand(1, 128).astype(np.float32)

        scores = await self.storage.score_all(embeddings, top_k=1)

        self.assertEqual(scores.shape, (0, 0))
        mock_logger.warning.assert_called_with("No provided embeddings (128) or empty index (0).")

    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_score_all(self, mock_logger):
        embeddings = np.random.rand(2, 128).astype(np.float32)
        self.storage._current_elements = 10
        self.storage._index.knn_query.return_value = ([[1, 2, 3]], [[0.1, 0.2, 0.3]])

        scores = await self.storage.score_all(embeddings, top_k=3)

        self.storage._index.knn_query.assert_called_once_with(data=embeddings, k=3, num_threads=self.config.num_threads)
        self.assertEqual(scores.shape, (1, 10))
        np.testing.assert_almost_equal(scores.data, np.array([0.95, 0.9, 0.85], dtype=np.float32))

    @patch("fast_graphrag._storage._vdb_hnswlib.hnswlib.Index")
    @patch("builtins.open", new_callable=mock_open, read_data=pickle.dumps(({"key": "value"}, 3)))
    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_insert_start_with_existing_files(self, mock_logger, mock_open, mock_index):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_load_path.side_effect = lambda x: f"dummy_path_{x}"

        await self.storage._insert_start()

        mock_index.assert_called_with(space="cosine", dim=self.storage.embedding_dim)
        self.storage._index.load_index.assert_called_with(
            "dummy_path_hnsw_index_128.bin", max_elements=self.config.max_elements
        )
        self.assertEqual(self.storage._metadata, {"key": "value"})
        self.assertEqual(self.storage._current_elements, 3)
        mock_logger.debug.assert_called_with("Loaded 3 elements from vectordb storage 'dummy_path_hnsw_index_128.bin'.")

    @patch("fast_graphrag._storage._vdb_hnswlib.hnswlib.Index")
    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_insert_start_with_no_files(self, mock_logger, mock_index):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_load_path.return_value = None

        await self.storage._insert_start()

        mock_index.assert_called_with(space="cosine", dim=self.storage.embedding_dim)
        self.storage._index.init_index.assert_called_with(
            max_elements=self.config.max_elements,
            ef_construction=self.config.ef_construction,
            M=self.config.M,
        )
        self.storage._index.set_ef.assert_called_with(self.config.ef_search)
        self.assertEqual(self.storage._metadata, {})
        self.assertEqual(self.storage._current_elements, 0)

    @patch("fast_graphrag._storage._vdb_hnswlib.hnswlib.Index")
    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_insert_start_with_no_namespace(self, mock_logger, mock_index):
        self.storage.namespace = None

        await self.storage._insert_start()

        mock_index.assert_called_with(space="cosine", dim=self.storage.embedding_dim)
        self.storage._index.init_index.assert_called_with(
            max_elements=self.config.max_elements,
            ef_construction=self.config.ef_construction,
            M=self.config.M,
        )
        self.storage._index.set_ef.assert_called_with(self.config.ef_search)
        self.assertEqual(self.storage._metadata, {})
        self.assertEqual(self.storage._current_elements, 0)
        mock_logger.debug.assert_called_with("Creating new volatile vectordb storage.")

    @patch("fast_graphrag._storage._vdb_hnswlib.hnswlib.Index")
    @patch("builtins.open", new_callable=mock_open)
    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_insert_done(self, mock_logger, mock_open, mock_index):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_save_path.side_effect = lambda x: f"dummy_path_{x}"
        self.storage._metadata = {"key": "value"}
        self.storage._current_elements = 3

        await self.storage._insert_done()

        self.storage._index.save_index.assert_called_with("dummy_path_hnsw_index_128.bin")
        mock_open.assert_called_with("dummy_path_hnsw_metadata.pkl", "wb")
        mock_logger.debug.assert_called_with("Saving 3 elements from vectordb storage 'dummy_path_hnsw_index_128.bin'.")

    @patch("fast_graphrag._storage._vdb_hnswlib.hnswlib.Index")
    @patch("builtins.open", new_callable=mock_open, read_data=pickle.dumps(({"key": "value"}, 3)))
    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_query_start_with_existing_files(self, mock_logger, mock_open, mock_index):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_load_path.side_effect = lambda x: f"dummy_path_{x}"

        await self.storage._query_start()

        mock_index.assert_called_with(space="cosine", dim=self.storage.embedding_dim)
        self.storage._index.load_index.assert_called_with(
            "dummy_path_hnsw_index_128.bin", max_elements=self.config.max_elements
        )
        self.assertEqual(self.storage._metadata, {"key": "value"})
        self.assertEqual(self.storage._current_elements, 3)
        mock_logger.debug.assert_called_with("Loaded 3 elements from vectordb storage 'dummy_path_hnsw_index_128.bin'.")

    @patch("fast_graphrag._storage._vdb_hnswlib.hnswlib.Index")
    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_query_start_with_no_files(self, mock_logger, mock_index):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_load_path.return_value = None

        await self.storage._query_start()

        mock_index.assert_called_with(space="cosine", dim=self.storage.embedding_dim)
        self.assertEqual(self.storage._metadata, {})
        self.assertEqual(self.storage._current_elements, 0)
        mock_logger.warning.assert_called_with(
            "No data file found for vectordb storage 'None'. Loading empty vectordb."
        )

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_insert_start_with_invalid_file(self, mock_logger, mock_open, mock_exists):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_resource_path.side_effect = lambda x: f"dummy_path_{x}"
        with self.assertRaises(InvalidStorageError):
            await self.storage._insert_start()
        mock_logger.error.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open)
    @patch("fast_graphrag._storage._vdb_hnswlib.logger")
    async def test_query_start_with_invalid_file(self, mock_logger, mock_open, mock_exists):
        self.storage.namespace = MagicMock()
        self.storage.namespace.get_resource_path.side_effect = lambda x: f"dummy_path_{x}"
        with self.assertRaises(InvalidStorageError):
            await self.storage._query_start()
        mock_logger.error.assert_called_once()


if __name__ == "__main__":
    unittest.main()

```

### tests/_types_test.py

```python
# type: ignore
import re
import unittest
from dataclasses import asdict

from pydantic import ValidationError

from fast_graphrag._types import (
    TChunk,
    TContext,
    TDocument,
    TEditRelation,
    TEditRelationList,
    TEntity,
    TGraph,
    TQueryEntities,
    TQueryResponse,
    TRelation,
    TScore,
    dump_to_csv,
)


class TestTypes(unittest.TestCase):
    def test_tdocument(self):
        doc = TDocument(data="Sample data", metadata={"key": "value"})
        self.assertEqual(doc.data, "Sample data")
        self.assertEqual(doc.metadata, {"key": "value"})

    def test_tchunk(self):
        chunk = TChunk(id=123, content="Sample content", metadata={"key": "value"})
        self.assertEqual(chunk.id, 123)
        self.assertEqual(chunk.content, "Sample content")
        self.assertEqual(chunk.metadata, {"key": "value"})

    def test_tentity(self):
        entity = TEntity(name="Entity1", type="Type1", description="Description1")
        self.assertEqual(entity.name, "Entity1")
        self.assertEqual(entity.type, "Type1")
        self.assertEqual(entity.description, "Description1")

        pydantic_entity = TEntity.Model(name="Entity1", type="Type1", desc="Description1")
        entity.name = entity.name.upper()
        entity.type = entity.type.upper()
        self.assertEqual(asdict(entity), asdict(pydantic_entity.to_dataclass(pydantic_entity)))

    def test_tqueryentities(self):
        query_entities = TQueryEntities(entities=["Entity1", "Entity2"], n=2)
        self.assertEqual(query_entities.entities, ["ENTITY1", "ENTITY2"])
        self.assertEqual(query_entities.n, 2)

        with self.assertRaises(ValidationError):
            TQueryEntities(entities=["Entity1", "Entity2"], n="two")

    def test_trelation(self):
        relation = TRelation(source="Entity1", target="Entity2", description="Relation description")
        self.assertEqual(relation.source, "Entity1")
        self.assertEqual(relation.target, "Entity2")
        self.assertEqual(relation.description, "Relation description")

        pydantic_relation = TRelation.Model(
            source="Entity1", target="Entity2", desc="Relation description"
        )

        relation.source = relation.source.upper()
        relation.target = relation.target.upper()
        self.assertEqual(asdict(relation), asdict(pydantic_relation.to_dataclass(pydantic_relation)))

    def test_tgraph(self):
        entity = TEntity(name="Entity1", type="Type1", description="Description1")
        relation = TRelation(source="Entity1", target="Entity2", description="Relation description")
        graph = TGraph(entities=[entity], relationships=[relation])
        self.assertEqual(graph.entities, [entity])
        self.assertEqual(graph.relationships, [relation])

        pydantic_graph = TGraph.Model(
            entities=[TEntity.Model(name="Entity1", type="Type1", desc="Description1")],
            relationships=[
                TRelation.Model(source="Entity1", target="Entity2", desc="Relation description")
            ],
            other_relationships=[]
        )

        for entity in graph.entities:
            entity.name = entity.name.upper()
            entity.type = entity.type.upper()
        for relation in graph.relationships:
            relation.source = relation.source.upper()
            relation.target = relation.target.upper()
        self.assertEqual(asdict(graph), asdict(pydantic_graph.to_dataclass(pydantic_graph)))

    def test_teditrelationship(self):
        edit_relationship = TEditRelation(ids=[1, 2], description="Combined relationship description")
        self.assertEqual(edit_relationship.ids, [1, 2])
        self.assertEqual(edit_relationship.description, "Combined relationship description")

    def test_teditrelationshiplist(self):
        edit_relationship = TEditRelation(ids=[1, 2], description="Combined relationship description")
        edit_relationship_list = TEditRelationList(grouped_facts=[edit_relationship])
        self.assertEqual(edit_relationship_list.groups, [edit_relationship])

    def test_tcontext(self):
        entities = [TEntity(name="Entity1", type="Type1", description="Sample description 1")] * 8 + [
            TEntity(name="Entity2", type="Type2", description="Sample description 2")
        ] * 8
        relationships = [TRelation(source="Entity1", target="Entity2", description="Relation description 12")] * 8 + [
            TRelation(source="Entity2", target="Entity1", description="Relation description 21")
        ] * 8
        chunks = [
            TChunk(id=i, content=f"Long and repeated chunk content {i}" * 4, metadata={"key": f"value {i}"})
            for i in range(16)
        ]

        for r, c in zip(relationships, chunks):
            r.chunks = [c.id]
        context = TContext(
            entities=[(e, TScore(0.9)) for e in entities],
            relationships=[(r, TScore(0.8)) for r in relationships],
            chunks=[(c, TScore(0.7)) for c in chunks],
        )
        max_chars = {"entities": 128, "relationships": 128, "chunks": 512}
        csv = context.to_str(max_chars.copy())

        csv_entities = re.findall(r"## Entities\n```csv\n(.*?)\n```", csv, re.DOTALL)
        csv_relationships = re.findall(r"## Relationships\n```csv\n(.*?)\n```", csv, re.DOTALL)
        csv_chunks = re.findall(r"## Sources\n.*=====", csv, re.DOTALL)

        self.assertEqual(len(csv_entities), 1)
        self.assertEqual(len(csv_relationships), 1)
        self.assertEqual(len(csv_chunks), 1)

        self.assertGreaterEqual(
            sum(max_chars.values()) + 16, len(csv_entities[0]) + len(csv_relationships[0]) + len(csv_chunks[0])
        )

    def test_tqueryresponse(self):
        context = TContext(
            entities=[("Entity1", TScore(0.9))],
            relationships=[("Relation1", TScore(0.8))],
            chunks=[("Chunk1", TScore(0.7))],
        )
        query_response = TQueryResponse(response="Sample response", context=context)
        self.assertEqual(query_response.response, "Sample response")
        self.assertEqual(query_response.context, context)

    def test_dump_to_csv(self):
        data = [TEntity(name="Sample name", type="SAMPLE TYPE", description="Sample description")]
        fields = ["name", "type"]
        values = {"score": [0.9]}
        csv_output = dump_to_csv(data, fields, with_header=True, **values)
        expected_output = ["name\ttype\tscore", "Sample name\tSAMPLE TYPE\t0.9"]
        self.assertEqual(csv_output, expected_output)


if __name__ == "__main__":
    unittest.main()

```

### tests/_utils_test.py

```python
# tests/test_utils.py

import asyncio
import threading
import unittest
from typing import List

import numpy as np
from scipy.sparse import csr_matrix

from fast_graphrag._utils import csr_from_indices_list, extract_sorted_scores, get_event_loop


class TestGetEventLoop(unittest.TestCase):
    def test_get_existing_event_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.assertEqual(get_event_loop(), loop)
        loop.close()

    def test_get_event_loop_in_sub_thread(self):
        def target():
            loop = get_event_loop()
            self.assertIsInstance(loop, asyncio.AbstractEventLoop)
            loop.close()

        thread = threading.Thread(target=target)
        thread.start()
        thread.join()


# Not checked
class TestExtractSortedScores(unittest.TestCase):
    def test_non_zero_elements(self):
        row_vector = csr_matrix([[0, 0.1, 0, 0.7, 0.5, 0]])
        indices, scores = extract_sorted_scores(row_vector)
        np.testing.assert_array_equal(indices, np.array([3, 4, 1]))
        np.testing.assert_array_equal(scores, np.array([0.7, 0.5, 0.1]))

    def test_empty(self):
        row_vector = csr_matrix((0, 0))
        indices, scores = extract_sorted_scores(row_vector)
        np.testing.assert_array_equal(indices, np.array([], dtype=np.int64))
        np.testing.assert_array_equal(scores, np.array([], dtype=np.float32))

    def test_empty_row_vector(self):
        row_vector = csr_matrix([[]])
        indices, scores = extract_sorted_scores(row_vector)
        np.testing.assert_array_equal(indices, np.array([], dtype=np.int64))
        np.testing.assert_array_equal(scores, np.array([], dtype=np.float32))

    def test_single_element(self):
        row_vector = csr_matrix([[0.5]])
        indices, scores = extract_sorted_scores(row_vector)
        np.testing.assert_array_equal(indices, np.array([0]))
        np.testing.assert_array_equal(scores, np.array([0.5]))

    def test_all_zero_elements(self):
        row_vector = csr_matrix([[0, 0, 0, 0, 0]])
        indices, scores = extract_sorted_scores(row_vector)
        np.testing.assert_array_equal(indices, np.array([], dtype=np.int64))
        np.testing.assert_array_equal(scores, np.array([], dtype=np.float32))

    def test_duplicate_elements(self):
        row_vector = csr_matrix([[0, 0.1, 0, 0.7, 0.5, 0.7]])
        indices, scores = extract_sorted_scores(row_vector)
        expected_indices_1 = np.array([5, 3, 4, 1])
        expected_indices_2 = np.array([3, 5, 4, 1])
        self.assertTrue(
            np.array_equal(indices, expected_indices_1) or np.array_equal(indices, expected_indices_2),
            f"indices {indices} do not match either {expected_indices_1} or {expected_indices_2}"
        )
        np.testing.assert_array_equal(scores, np.array([0.7, 0.7, 0.5, 0.1]))


class TestCsrFromListOfLists(unittest.TestCase):
    def test_repeated_elements(self):
        data: List[List[int]] = [[0, 0], [], []]
        expected_matrix = csr_matrix(([1, 1, 0], ([0, 0, 0], [0, 0, 0])), shape=(3, 3))
        result_matrix = csr_from_indices_list(data, shape=(3, 3))
        np.testing.assert_array_equal(result_matrix.toarray(), expected_matrix.toarray())

    def test_non_zero_elements(self):
        data = [[0, 1, 2], [2, 3], [0, 3]]
        expected_matrix = csr_matrix([[1, 1, 1, 0, 0], [0, 0, 1, 1, 0], [1, 0, 0, 1, 0]], shape=(3, 5))
        result_matrix = csr_from_indices_list(data, shape=(3, 5))
        np.testing.assert_array_equal(result_matrix.toarray(), expected_matrix.toarray())

    def test_empty_list_of_lists(self):
        data: List[List[int]] = []
        expected_matrix = csr_matrix((0, 0))
        result_matrix = csr_from_indices_list(data, shape=(0, 0))
        np.testing.assert_array_equal(result_matrix.toarray(), expected_matrix.toarray())

    def test_empty_list_of_lists_with_unempty_shape(self):
        data: List[List[int]] = []
        expected_matrix = csr_matrix((1, 1))
        result_matrix = csr_from_indices_list(data, shape=(1, 1))
        np.testing.assert_array_equal(result_matrix.toarray(), expected_matrix.toarray())

    def test_list_with_empty_sublists(self):
        data: List[List[int]] = [[], [], []]
        expected_matrix = csr_matrix((3, 0))
        result_matrix = csr_from_indices_list(data, shape=(3, 0))
        np.testing.assert_array_equal(result_matrix.toarray(), expected_matrix.toarray())


if __name__ == "__main__":
    unittest.main()

```


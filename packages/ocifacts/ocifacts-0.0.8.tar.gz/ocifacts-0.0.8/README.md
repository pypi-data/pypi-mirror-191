# Ocifacts

A lazy Python utility to store arbitrary artifacts in any docker image repository

# Install

```sh
pip install ocifacts
```

## Prerequisites
* Working authentication to your image registry of choice e.g. `~/.docker/config.json`

# Quick Start

Push some files to a docker repository and add labels to the artifact
```python
import ocifacts

ocifacts.push("myrepo/foo:v1", file="./tests/data/test.yaml", labels={"qux": "baz"})
```

Pull them back out
```python
ocifacts.pull("myrepo/foo:v1", "./out/")
```

More complete examples can be found in the [tests](./tests/test_api.py)

# FAQ

__What about OCI artifacts?__

OCI artifacts are amazing and will be the future, but many registries don't support them yet, this tool will work with any docker registry. 



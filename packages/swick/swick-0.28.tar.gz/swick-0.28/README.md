# ![swick Logo](https://github.com/nathantspencer/swick/raw/main/assets/logo_cropped_small.png)
`swick` is the slick way to process [SWC files](http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html)—which contain tree-like representations of neuron structures—in Python.

Reading, writing, combining, splitting, and validating SWC files can be done in just a few lines. Objects to represent SWC files are also provided, laying the groundwork for custom analysis or modification of SWCs in Python.

# Installation

To install `swick` via [pip](https://pip.pypa.io/en/stable/), simply:

```
pip install swick
```

Or to upgrade an existing installation:

```
pip install swick --upgrade
```

Python wheels can also be manually downloaded via the [PyPI page](https://pypi.org/project/swick/).

# Usage & Documentation

Documentation is automatically built via a [Github Actions workflow](https://github.com/nathantspencer/swick/blob/main/.github/workflows/build-docs.yml) and hosted on Github Pages. Reading it is the best way to get started with `swick`. For any questions not addressed there, please feel free to [open an issue](https://github.com/nathantspencer/swick/issues/new)!

Here are some links to relevant documentation:

 - [Documentation Homepage](https://nathantspencer.github.io/swick/index.html)
 - [User Guide](https://nathantspencer.github.io/swick/user_guide/index.html)
 - [API Reference](https://nathantspencer.github.io/swick/api_documentation/index.html)

# Testing

Tests can be run via this command from the root directory of the repository:

```
python -m unittest discover
```

In the near future, tests will be automated via Github Actions in order to evaluate pull requests as well as the current head of the `main` branch.
# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['transformer_embeddings']

package_data = \
{'': ['*']}

install_requires = \
['s3fs>=2022.10.0,<2023.0.0',
 'torch>=1.9.1,<2.0.0',
 'transformers>=4.23.1,<5.0.0']

setup_kwargs = {
    'name': 'transformer-embeddings',
    'version': '3.0.5',
    'description': 'Transformer Embeddings',
    'long_description': '# Transformer Embeddings\n\n[![PyPI](https://img.shields.io/pypi/v/transformer-embeddings.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/transformer-embeddings.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/transformer-embeddings)][python version]\n[![License](https://img.shields.io/pypi/l/transformer-embeddings)][license]\n\n[![Tests](https://github.com/ginger-io/transformer-embeddings/workflows/Tests/badge.svg?branch=main)][tests]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/transformer-embeddings/\n[status]: https://pypi.org/project/transformer-embeddings/\n[python version]: https://pypi.org/project/transformer-embeddings\n[read the docs]: https://transformer-embeddings.readthedocs.io/\n[tests]: https://github.com/ginger-io/transformer-embeddings/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/ginger-io/transformer-embeddings\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\nThis library simplifies and streamlines the usage of encoder transformer models supported by [HuggingFace\'s `transformers` library](https://github.com/huggingface/transformers/) ([model hub](https://huggingface.co/models) or local) to generate embeddings for string inputs, similar to the way `sentence-transformers` does.\n\n## Why use this over HuggingFace\'s `transformers` or `sentence-transformers`?\n\nUnder the hood, we take care of:\n\n1. Can be used with any model on the HF model hub, with sensible defaults for inference.\n2. Setting the PyTorch model to `eval` mode.\n3. Using `no_grad()` when doing the forward pass.\n4. Batching, and returning back output in the format produced by HF transformers.\n5. Padding / truncating to model defaults.\n6. Moving to and from GPUs if available.\n\n## Installation\n\nYou can install _Transformer Embeddings_ via [pip] from [PyPI]:\n\n```console\n$ pip install transformer-embeddings\n```\n\n## Usage\n\n```python\nfrom transformer_embeddings import TransformerEmbeddings\n\ntransformer = TransformerEmbeddings("model_name")\n```\n\nIf you have a previously instantiated `model` and / or `tokenizer`, you can pass that in.\n\n```python\ntransformer = TransformerEmbeddings(model=model, tokenizer=tokenizer)\n```\n\n```python\ntransformer = TransformerEmbeddings(model_name="model_name", model=model)\n```\n\nor\n\n```python\ntransformer = TransformerEmbeddings(model_name="model_name", tokenizer=tokenizer)\n```\n\n**Note:** The `model_name` should be included if only 1 of model or tokenizer are passed in.\n\n### Embeddings\n\nTo get output embeddings:\n\n```python\nembeddings = transformer.encode(["Lorem ipsum dolor sit amet",\n                                 "consectetur adipiscing elit",\n                                 "sed do eiusmod tempor incididunt",\n                                 "ut labore et dolore magna aliqua."])\nembeddings.output\n```\n\n### Pooled Output\n\nTo get pooled outputs:\n\n```python\nfrom transformer_embeddings import TransformerEmbeddings, mean_pooling\n\ntransformer = TransformerEmbeddings("model_name", return_output=False, pooling_fn=mean_pooling)\n\nembeddings = transformer.encode(["Lorem ipsum dolor sit amet",\n                                "consectetur adipiscing elit",\n                                "sed do eiusmod tempor incididunt",\n                                "ut labore et dolore magna aliqua."])\n\nembeddings.pooled\n```\n\n### Exporting the Model\n\nOnce you are done testing and training the model, it can be exported into a single tarball that can be uploaded to S3 using:\n\n```python\nfrom transformer_embeddings import TransformerEmbeddings\n\ntransformer = TransformerEmbeddings("model_name")\ntransformer.export(\n    additional_files=["/path/to/other/files/to/include/in/tarball.pickle"],\n    s3_path="s3://bucket/models/model-name/date-version/",\n)\n```\n\n## Contributing\n\nContributions are very welcome. To learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [Apache 2.0 license][license], _Transformer Embeddings_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems, please [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was partly generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/ginger-io/transformer-embeddings/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/ginger-io/transformer-embeddings/blob/main/LICENSE\n[contributor guide]: https://github.com/ginger-io/transformer-embeddings/blob/main/CONTRIBUTING.md\n[command-line reference]: https://transformer-embeddings.readthedocs.io/en/latest/usage.html\n',
    'author': 'Headspace Health',
    'author_email': 'transformer-embeddings@headspace.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ginger-io/transformer-embeddings',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)

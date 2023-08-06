# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aws_codeartifact_poetry',
 'aws_codeartifact_poetry.aws',
 'aws_codeartifact_poetry.commands',
 'aws_codeartifact_poetry.helpers']

package_data = \
{'': ['*']}

install_requires = \
['boto3==1.20.5', 'click>=8.0.3,<9.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['aws-codeartifact-poetry = '
                     'aws_codeartifact_poetry.cli:cli']}

setup_kwargs = {
    'name': 'aws-codeartifact-poetry',
    'version': '1.2.0',
    'description': 'AWS CodeArtifact Poetry CLI',
    'long_description': '# AWS CodeArtifact Poetry\n\n## SonarCloud Status\n\n[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=lucasvieirasilva_aws-codeartifact-poetry)\n[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=bugs)](https://sonarcloud.io/dashboard?id=lucasvieirasilva_aws-codeartifact-poetry)\n[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=code_smells)](https://sonarcloud.io/dashboard?id=lucasvieirasilva_aws-codeartifact-poetry)\n[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=sqale_index)](https://sonarcloud.io/dashboard?id=lucasvieirasilva_aws-codeartifact-poetry)\n[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=ncloc)](https://sonarcloud.io/dashboard?id=lucasvieirasilva_aws-codeartifact-poetry)\n\n[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=lucasvieirasilva_aws-codeartifact-poetry)\n[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=lucasvieirasilva_aws-codeartifact-poetry)\n[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=security_rating)](https://sonarcloud.io/dashboard?id=lucasvieirasilva_aws-codeartifact-poetry)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=lucasvieirasilva_aws-codeartifact-poetry&metric=alert_status)](https://sonarcloud.io/dashboard?id=lucasvieirasilva_aws-codeartifact-poetry)\n\nAWS CodeArtifact Poetry CLI is a CLI designed to perform Poetry login with AWS CodeArtifact Private PyPi.\n\n## Install\n\n`pip install aws-codeartifact-poetry`\n\n## Documentation\n\n- See our [Documentation](https://aws-codeartifact-poetry.readthedocs.io/)\n\n## Contributing\n\n- See our [Contributing Guide](CONTRIBUTING.md)\n\n## CLI Documentation\n\n- See our [CLI Documentation](docs/CLI.md)\n\n## Change Log\n\n- See our [Change Log](CHANGELOG.md)\n',
    'author': 'Lucas Vieira',
    'author_email': 'lucas.vieira94@outlook.com',
    'maintainer': 'Lucas Vieira',
    'maintainer_email': 'lucas.vieira94@outlook.com',
    'url': 'https://github.com/lucasvieirasilva/aws-codeartifact-poetry',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)

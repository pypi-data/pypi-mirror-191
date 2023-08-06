# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nvd_api',
 'nvd_api.low_api',
 'nvd_api.low_api.api',
 'nvd_api.low_api.apis',
 'nvd_api.low_api.model',
 'nvd_api.low_api.models']

package_data = \
{'': ['*']}

install_requires = \
['certifi>=2022.12.7,<2023.0.0',
 'frozendict>=2.3.4,<3.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'setuptools>=67.2.0,<68.0.0',
 'typing-extensions>=4.4.0,<5.0.0',
 'urllib3>=1.26.13,<2.0.0']

entry_points = \
{'console_scripts': ['push = tools.push:main',
                     'release = tools.release:main',
                     'sbom = tools.sbom:main',
                     'sphinx = tools.sphinx:main']}

setup_kwargs = {
    'name': 'nvd-api',
    'version': '0.7.0',
    'description': 'NVD API 2.0 Python API',
    'long_description': '=================\nNVD API Client\n=================\n\n\nNVD API client is a community driven NVD API 2.0 client. \nThis client support `Vulnerabilities`_ API and `Products`_ API.\n\n.. _Vulnerabilities: https://nvd.nist.gov/developers/vulnerabilities\n.. _Products: https://nvd.nist.gov/developers/products\n\n.. image:: https://badge.fury.io/py/nvd-api.svg\n    :target: https://badge.fury.io/py/nvd-api\n\n.. image:: https://github.com/kannkyo/nvd-api/actions/workflows/python-ci.yml/badge.svg\n    :target: https://github.com/kannkyo/nvd-api/actions/workflows/python-ci.yml\n\n.. image:: https://codecov.io/gh/kannkyo/nvd-api/branch/main/graph/badge.svg?token=ASYLVG3X9O\n    :target: https://codecov.io/gh/kannkyo/nvd-api\n\n.. image:: https://github.com/kannkyo/nvd-api/actions/workflows/scorecards.yml/badge.svg\n    :target: https://github.com/kannkyo/nvd-api/actions/workflows/scorecards.yml\n\n.. image:: https://bestpractices.coreinfrastructure.org/projects/6889/badge\n    :target: https://bestpractices.coreinfrastructure.org/projects/6889\n\nGetting Start\n=============\n\nProducts / CPE API\n---------------------\n\nThis API\'s simple example is bellow.\n\n.. code-block:: python\n\n    from client import NvdApiClient\n    from pprint import pprint\n\n    client = NvdApiClient()\n\n    response = client.get_cpes(\n        cpe_name_id="87316812-5F2C-4286-94FE-CC98B9EAEF53",\n        results_per_page=1,\n        start_index=0\n    )\n    pprint(response)\n\n`get_cpes` method check API\'s all constraints and limitations.\n\n* cpeNameId and matchCriteriaId must be uuid format.\n* cpeMatchString must be CPEv2.3 format.\n* If filtering by keywordExactMatch, keywordSearch is REQUIRED.\n* If filtering by the last modified date, both lastModStartDate and lastModEndDate are REQUIRED.\n* resultsPerPage\'s maximum allowable limit is 10,000.\n* The maximum allowable range when using any date range parameters is 120 consecutive days.\n\nProducts / Match Criteria API\n-----------------------------\n\nThis API\'s simple example is bellow.\n\n.. code-block:: python\n\n    from nvd_api import NvdApiClient\n    from pprint import pprint\n\n    client = NvdApiClient()\n\n    response = client.get_cpe_match(\n        cve_id="CVE-2022-32223",\n        results_per_page=1,\n        start_index=0\n    )\n    pprint(response)\n\n`get_cpe_match` method check API\'s all constraints and limitations.\n\n* cveId is must be CVE ID format.\n* If filtering by the last modified date, both lastModStartDate and lastModEndDate are REQUIRED.\n* matchCriteriaId must be uuid format.\n* resultsPerPage\'s maximum allowable limit is 5,000.\n* The maximum allowable range when using any date range parameters is 120 consecutive days.\n* cpeName must be CPEv2.3 format.\n\nVulnerabilities / CVE API\n---------------------------\n\nThis API\'s simple example is bellow.\n\n.. code-block:: python\n\n    from nvd_api import NvdApiClient\n    from pprint import pprint\n\n    client = NvdApiClient()\n\n    response = client.get_cves(\n        cpe_name="cpe:2.3:o:debian:debian_linux:3.0:*:*:*:*:*:*:*",\n        cvss_v2_metrics="AV:L/AC:L/Au:N/C:C/I:C/A:C",\n        cvss_v2_severity="HIGH",\n        results_per_page=1,\n        start_index=1\n    )\n    pprint(response)\n\n* cpeName must be CPEv2.3 format.\n* cveId is must be CVE ID format.\n* cvssV2Severity, cvssV2Metrics is must be CVSS v2 format.\n* cvssV3Severity, cvssV3Metrics is must be CVSS v3 format.\n* cweId is must be CWE ID format.\n* resultsPerPage\'s maximum allowable limit is 2,000.\n* If filtering by keywordExactMatch, keywordSearch is REQUIRED.\n* If filtering by the last modified date, both lastModStartDate and lastModEndDate are REQUIRED.\n* If filtering by the last modified date, both pubStartDate and pubEndDate are REQUIRED.\n* The maximum allowable range when using any date range parameters is 120 consecutive days.\n* cvssV2Metrics cannot be used in requests that include cvssV3Metrics.\n* cvssV3Metrics cannot be used in requests that include cvssV2Metrics.\n* cvssV2Severity cannot be used in requests that include cvssV3Severity.\n* cvssV3Severity cannot be used in requests that include cvssV2Severity.\n\nVulnerabilities / CVE Change History API\n-------------------------------------------\n\nThis API\'s simple example is bellow.\n\n.. code-block:: python\n\n    from nvd_api import NvdApiClient\n    from pprint import pprint\n\n    client = NvdApiClient()\n\n    response = client.get_cve_history(\n        change_start_date="2021-08-04T00:00:00.000",\n        change_end_date="2021-10-23T00:00:00.000",\n        event_name="CVE Rejected",\n        results_per_page=1,\n        start_index=1\n    )\n    pprint(response)\n\n`get_cve_history` method check API\'s all constraints and limitations.\n\n* If filtering by the change date, both changeStartDate and changeEndDate are REQUIRED.\n* cveId is must be CVE ID format.\n* resultsPerPage\'s maximum allowable limit is 5,000.\n* The maximum allowable range when using any date range parameters is 120 consecutive days.\n\nWith API Key\n---------------------\n\nIf you have the nvd api key, you can set key to client.\n\n.. code-block:: python\n\n    from nvd_api import NvdApiClient\n    from pprint import pprint\n\n    client = NvdApiClient(wait_time=1 * 1000, api_key=\'THIS IS API KEY\')\n\n    response = client.get_cves(\n        cpe_name="cpe:2.3:o:debian:debian_linux:3.0:*:*:*:*:*:*:*",\n        cvss_v2_metrics="AV:L/AC:L/Au:N/C:C/I:C/A:C",\n        cvss_v2_severity="HIGH",\n        results_per_page=1,\n        start_index=1\n    )\n    pprint(response)\n\n* api_key : api key published by nvd.\n* wait_time : interval time to execute api (with api key is 50 requests in a rolling 30s window, without api key is 5 requests in a rolling 30s window)\n',
    'author': 'kannkyo',
    'author_email': '15080890+kannkyo@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kannkyo/nvd-api',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

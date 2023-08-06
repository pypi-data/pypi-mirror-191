# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tungsten',
 'tungsten.globally_harmonized_system',
 'tungsten.parsers',
 'tungsten.parsers.supplier',
 'tungsten.parsers.supplier.sigma_aldrich']

package_data = \
{'': ['*']}

install_requires = \
['pdfminer.six>=20220524,<20220525', 'tabula-py>=2.5.1,<3.0.0']

setup_kwargs = {
    'name': 'tungsten-sds',
    'version': '0.6.2',
    'description': 'An MSDS parser.',
    'long_description': '<div align="center">\n    <a align="center" href="https://pypi.org/project/tungsten-sds/">\n        <img src="https://raw.githubusercontent.com/Den4200/tungsten/main/assets/tungsten-wide-dark-bg-pad.png" align="center" alt="Tungsten" />\n    </a>\n    <h1 align="center">Tungsten</h1>\n    <p align="center">A material safety data sheet parser.</p>\n</div>\n\n## Installation\n\nTungsten is available on PyPi via pip. To install, run the following command:\n\n```sh\npip install tungsten-sds\n```\n\n## Usage Example\n\n```python\nimport json\nfrom pathlib import Path\n\nfrom tungsten import SigmaAldrichSdsParser, SdsQueryFieldName, \\\n    SigmaAldrichFieldMapper\n\nsds_parser = SigmaAldrichSdsParser()\nsds_path = Path("CERILLIAN_L-001.pdf")\n\n# Convert PDF file to parsed data\nwith open(sds_path, "rb") as f:\n    sds = sds_parser.parse_to_ghs_sds(f)\n\nfield_mapper = SigmaAldrichFieldMapper()\n\nfields = [\n    SdsQueryFieldName.PRODUCT_NAME,\n    SdsQueryFieldName.PRODUCT_NUMBER,\n    SdsQueryFieldName.CAS_NUMBER,\n    SdsQueryFieldName.PRODUCT_BRAND,\n    SdsQueryFieldName.RECOMMENDED_USE_AND_RESTRICTIONS,\n    SdsQueryFieldName.SUPPLIER_ADDRESS,\n    SdsQueryFieldName.SUPPLIER_TELEPHONE,\n    SdsQueryFieldName.SUPPLIER_FAX,\n    SdsQueryFieldName.EMERGENCY_TELEPHONE,\n    SdsQueryFieldName.IDENTIFICATION_OTHER,\n    SdsQueryFieldName.SUBSTANCE_CLASSIFICATION,\n    SdsQueryFieldName.PICTOGRAM,\n    SdsQueryFieldName.SIGNAL_WORD,\n    SdsQueryFieldName.HNOC_HAZARD,\n]\n\n# Serialize parsed data to JSON and dump to a file\nwith open(sds_path.stem + ".json", "w") as f:\n    sds.dump(f)\n    # Also print out mapped fields\n    for field in fields:\n        print(field.name, field_mapper.getField(field, json.loads(sds.dumps())))\n\n```\n\n## License\n\nThis work is licensed under MIT. Media assets in the `assets` directory are licensed under a\nCreative Commons Attribution-NoDerivatives 4.0 International Public License.\n\n## Notes\n\nThis library currently comes bundled with a new build of `tabula-java`, which is also licensed\nunder MIT, to see the full license, see https://github.com/tabulapdf/tabula-java/blob/master/LICENSE.\n',
    'author': 'Dennis Pham',
    'author_email': 'dennis@dennispham.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Den4200/tungsten',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cimlab',
 'cimlab.data_profile',
 'cimlab.data_profile.cimext_2022',
 'cimlab.data_profile.rc4_2021',
 'cimlab.loaders',
 'cimlab.loaders.blazegraph',
 'cimlab.loaders.gridappsd',
 'cimlab.loaders.sparql.rc4_2021',
 'cimlab.models']

package_data = \
{'': ['*']}

install_requires = \
['SPARQLWrapper>=2.0.0,<3.0.0', 'xsdata>=22.5,<23.0']

extras_require = \
{':extra == "gridappsd"': ['gridappsd-python>=2.7.230209,<3.0.0']}

setup_kwargs = {
    'name': 'gridappsd-cim-lab',
    'version': '0.11.20230210193727a0',
    'description': 'CIM models used within gridappsd.',
    'long_description': '# GridAPPS-D CIM-Lab Library\nPython library for parsing CIM power system models in distributed ADMS applications. It creates Python object instances in memory using a data profile exported from a specified CIM profile (e.g. GridAPPS-D CIM100 RC4_2021 profile).\n\nThe library is being expanded to cover centralized applications, transmission models, and real-time editing of CIM XML models natively.\n\n## Requirements\nThe gridappsd-cim-lab requires a python version >=3.8 and <4. No testing has been done with other versions.\n\nIt also requires a connection to a Blazegraph TripleStore Database or the GridAPPS-D Platform. Support for other databases may be added in future releases.\n\nThe DistributedModel class also requires the output for GridAPPS-D Topology Processor, which may be obtained by importing the topology processor library or passing an API call to the `goss.gridappsd.request.data.topology` queue in the GridAPPS-D platform.\n\n## Installation\nThe CIM-Lab library should be installed in same virtual environment as the ADMS application. \n```\npip install gridappsd-cim-lab\n```\nIt is also included in the gridappsd-python library, which can be installed using\n```\npip install gridappsd-python\n```\n\n## Specifying the CIM Profile\nThe CIM-Lab library supports multiple CIM profiles, which can be exported using CIMtool or Enterprise Architect Schema Composer as a .xsd data profile. The data profiles are ingested using the xsdata python library and saved in the cimlab/data_profile directory.\n\nWhen importing the library, the CIM profile must be specified using the gridappsd-python constructor or directly as\n```\nimport cimlab.data_profile.rc4_2021 as cim\n```\nor by using `importlib`:\n```\nimport importlib\ncim_profile = \'rc4_2021\'\ncim = importlib.import_module(\'cimlab.data_profile.\' + cim_profile)\n```\n\n\n## Model Initialization\n\nThe CIM-Lab library creates object instances populated with the attributes of `name` and `mRID` for all addressable and unaddressable equipment in each distributed area. All other attributes are `None` or `[]` by default.\n\n### Usage with GridAPPS-D Context Manager\nIf an application is built using the GridAPPS-D Context Manager and Field Interface in gridappsd-python, initialization of the `DistributedModel`, `SwitchArea`, and `SecondaryArea` classes is performed automatically.\n\n### Standalone Usage\nInitialization of the `DistributedModel`, `SwitchArea`, and `SecondaryArea` classes requires the distributed topology message from GridAPPS-D Topology Processor, which may be called through the GridAPPS-D API or by import the topology library:\n```\ntopic = "goss.gridappsd.request.data.topology"\n\nmessage = {\n   "requestType": "GET_SWITCH_AREAS",\n   "modelID":  "_FEEDER_MRID_1234_ABCD,\n   "resultFormat": "JSON"\n}\n\ntopology_response = gapps.get_response(topic, message, timeout=30)\n```\n```\nfrom topology_processor import DistributedTopology\ngapps = GridappsdConnection(feeder_mrid)\nTopology = DistributedTopology(gapps, feeder_mrid)\ntopology_response = Topology.create_switch_areas(feeder_mrid)\ntopology_response = json.loads(topology_response)\n```\nThe distributed network model can then be initialized using\n```\nfeeder = cim.Feeder(mRID=feeder_mrid)\nnetwork = DistributedModel(connection=bg, feeder=feeder, topology=topology_response[\'feeders\'])\n```\n\n## Core Library Methods\nThe CIM power system model can then be parsed by invoking the `.get_all_attributes(cim.ClassName)` method. The method populates all available attributes of the given attribute and creates default instances of all associated class object instances that are one association away in the CIM UML. Associated default instances are only populated with `mRID` attribute. The `.get_all_attributes` method must be invoked in sequential order following the inheritance hierarchy in the CIM UML, starting with the particular equiment class (e.g. ACLineSegment) and then each child class inheriting from the previous class. \n\nThe Python object instances can be accessed using the `typed_catalog` dictionary of each distributed area class instance. The typed catalog is organized by the class type and then mRID of each object. The attributes of each class can be accessed directly or through any associated class. These two call are equivalent:\n```\nbus_name = switch_area.typed_catalog[cim.ConnectivityNode][node_mrid].name\n```\n```\nbus_name = switch_area.typed_catalog[cim.ACLineSegment][line_mrid].Terminals[0].ConnectivityNode.name\n```\n\nNote that all classes and attributes are case sensitive and follow the CIM UML conventions for each class.\n\nAll instances of all given CIM class can also be exported as JSON text using the `.__dumps__(cim.ClassName)` method of the distributed area classes:\n```\nLines = switch_area.__dumps__(cim.ACLineSegment)\n```\n\nAdditional examples of usage for specified CIM classes are inlcuded in model_example.py\n',
    'author': 'C. Allwardt',
    'author_email': '3979063+craig8@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.9,<4.0',
}


setup(**setup_kwargs)

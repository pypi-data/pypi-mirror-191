import setuptools
import os

pwd = os.path.abspath(os.path.dirname(__file__))

# Returns the README.md content
with open(os.path.join(pwd, "README.md"), mode="r", encoding="utf-8") as f:
    readme: str = f.read()

with open(os.path.join(pwd, "requirements.txt"), mode="r", encoding="utf-8") as f:
    required: list[str] = f.read().splitlines()


VERSION = '0.1.1 '
PACKAGE_NAME = 'owl_model_extractor'
AUTHOR = 'KnowledgeFactory'
URL = ''

LICENSE = 'MIT'
DESCRIPTION = 'Librería que nos permite acceder a un fichero OWL tanto local como remoto y modelar la información que contiene'
LONG_DESCRIPTION = "TEST"
LONG_DESC_TYPE = "text/markdown"


setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author=AUTHOR,
    maintainer=AUTHOR,
    description=DESCRIPTION,
    long_description=readme,
    long_description_content_type=LONG_DESC_TYPE,
    license=LICENSE,
    packages=[
        "owl_model_extractor"
    ],
    python_requires=">=3.6",
    install_requires=required,
    url=URL,
    keywords=["kfsembu", "knowledge-factory", "helpers", "utils", "utilities", "useful-methods"]
)

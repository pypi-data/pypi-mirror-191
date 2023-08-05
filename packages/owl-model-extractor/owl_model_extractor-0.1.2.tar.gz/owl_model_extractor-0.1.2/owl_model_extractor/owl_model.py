from owlready2 import *


class OwlModel:
    __ontology: Ontology
    is_loaded: bool

    def __init__(self, ontology_url):
        try:
            self.__ontology = get_ontology(ontology_url).load()
            self.is_loaded = True
        except Exception as ex:
            self.is_loaded = False

    def get_base_iri(self):
        if hasattr(self.__ontology, "base_iri"):
            return self.__ontology.base_iri
        else:
            return ""

    def get_license(self):
        if hasattr(self.__ontology.metadata, "license"):
            return self.__ontology.metadata.license
        else:
            return ""

    def get_backward_compatibility(self):
        if hasattr(self.__ontology.metadata, "backwardCompatibleWith"):
            return self.__ontology.metadata.backwardCompatibleWith
        else:
            return ""

    def get_creator(self):
        if hasattr(self.__ontology.metadata, "creator"):
            return self.__ontology.metadata.creator
        else:
            return ""

    def get_created(self):
        if hasattr(self.__ontology.metadata, "created"):
            return self.__ontology.metadata.created
        else:
            return ""

    def get_modified(self):
        if hasattr(self.__ontology.metadata, "modified"):
            return self.__ontology.metadata.modified
        else:
            return ""

    def get_preferred_namespace_prefix(self):
        if hasattr(self.__ontology.metadata, "preferredNamespacePrefix"):
            return self.__ontology.metadata.preferredNamespacePrefix
        else:
            return ""

    def get_preferred_namespace_uri(self):
        if hasattr(self.__ontology.metadata, "preferredNamespaceUri"):
            return self.__ontology.metadata.preferredNamespaceUri
        else:
            return ""

    def get_version_iri(self):
        if hasattr(self.__ontology.metadata, "versionIRI"):
            return self.__ontology.metadata.versionIRI
        else:
            return ""

    def get_citation(self):
        if hasattr(self.__ontology.metadata, "citation"):
            return self.__ontology.metadata.citation
        else:
            return ""

    def get_title(self):
        if hasattr(self.__ontology.metadata, "title"):
            return self.__ontology.metadata.title
        else:
            return ""

    def get_metadata(self) -> list:
        if self.__ontology.metadata:
            return self.__ontology.metadata
        else:
            return None

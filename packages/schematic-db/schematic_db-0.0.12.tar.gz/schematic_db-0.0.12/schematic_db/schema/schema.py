"""Schema class"""

from typing import Optional, Callable, Union
from dataclasses import dataclass
import warnings
import networkx
import pandas as pd
from schematic_db.db_config import (
    DBConfig,
    DBObjectConfig,
    DBForeignKey,
    DBAttributeConfig,
    DBDatatype,
)

from .api_utils import (
    get_graph_by_edge_type,
    find_class_specific_properties,
    get_property_label_from_display_name,
    get_project_manifests,
    get_manifest,
    is_node_required,
    get_node_validation_rules,
    ManifestSynapseConfig,
)

SCHEMATIC_TYPE_DATATYPES = {
    "str": DBDatatype.TEXT,
    "float": DBDatatype.FLOAT,
    "num": DBDatatype.FLOAT,
    "int": DBDatatype.INT,
    "date": DBDatatype.DATE,
}


class NoAttributesWarning(Warning):
    """
    Occurs when a database object has no attributes returned from find_class_specific_properties().
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class ManifestMissingPrimaryKeyError(Exception):
    """Raised when a manifest is missing its primary key"""

    def __init__(
        self,
        object_name: str,
        dataset_id: str,
        primary_key: str,
        manifest_columns: list[str],
    ):
        self.message = "Manifest is missing its primary key"
        self.object_name = object_name
        self.dataset_id = dataset_id
        self.primary_key = primary_key
        self.manifest_columns = manifest_columns
        super().__init__(self.message)

    def __str__(self) -> str:
        return (
            f"{self.message}; object name:{self.object_name}; "
            f"dataset_id:{self.dataset_id}; primary keys:{self.primary_key}; "
            f"manifest columns:{self.manifest_columns}"
        )


class MoreThanOneTypeRule(Exception):
    """Raised when an attribute has more than one validation type rule"""

    def __init__(
        self,
        attribute_name: str,
        type_rules: list[str],
    ):
        self.message = "Attribute has more than one validation type rule"
        self.attribute_name = attribute_name
        self.type_rules = type_rules
        super().__init__(self.message)

    def __str__(self) -> str:
        return (
            f"{self.message}; attribute name:{self.attribute_name}; "
            f"type_rules:{self.type_rules}"
        )


def get_key_attribute(object_name: str) -> str:
    """
    Standard function for getting a key's name(primary or foreign) based on the objects name.
    The Schema class uses this function to get both primary and foreign keys by default.
    Users may want to use a different function.

    Args:
        object_name (str): The name of the object in the database

    Returns:
        str: The name of the key attribute for that database
    """
    return f"{object_name}_id"


def get_manifest_ids_for_object(
    object_name: str, manifests: list[ManifestSynapseConfig]
) -> list[str]:
    """Gets the manifest ids from a list of manifests matching the object name

    Args:
        object_name (str): The name of the object to get the manifests for
        manifests (list[ManifestSynapseConfig]): A list of manifests in Synapse

    Returns:
        list[str]: A list of synapse ids for the manifests
    """
    return [
        manifest.manifest_id
        for manifest in manifests
        if manifest.component_name == object_name and manifest.manifest_id != ""
    ]


def get_dataset_ids_for_object(
    object_name: str, manifests: list[ManifestSynapseConfig]
) -> list[str]:
    """Gets the dataset ids from a list of manifests matching the object name

    Args:
        object_name (str): The name of the object to get the manifests for
        manifests (list[ManifestSynapseConfig]): A list of manifests in Synapse

    Returns:
        list[str]: A list of synapse ids for the manifest datasets
    """
    return [
        manifest.dataset_id
        for manifest in manifests
        if manifest.component_name == object_name and manifest.manifest_id != ""
    ]


@dataclass
class SchemaConfig:
    """
    A config for a Schema.
    Properties:
        schema_url (str): A url to the jsonld schema file
        synapse_project_id (str): The synapse id to the project where the manifests are stored.
        synapse_asset_view_id (str): The synapse id to the asset view that tracks the manifests.
        synapse_input_token (str): A synapse token with download permissions for both the
         synapse_project_id and synapse_asset_view_id
    """

    schema_url: str
    synapse_project_id: str
    synapse_asset_view_id: str
    synapse_input_token: str


class Schema:  # pylint: disable=too-many-instance-attributes
    """
    The Schema class interacts with the Schematic API to create a DBConfig
     object or to get a list of manifests for the schema.
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        config: SchemaConfig,
        primary_key_getter: Callable[[str], str] = lambda _: "id",
        foreign_key_getter: Callable[[str], str] = get_key_attribute,
    ) -> None:
        """Init

        The Schema class has two optional arguments primary_key_getter, and foreign_key_getter.
        These are used to determine the names of the attributes that are primary and foreign keys.
        It is assumed that all objects(tables) have one primary key that can be systematically
        determined from the objects name, and that the primary_key_getter will do that.

        By default a lambda function that returns "id" is used for primary keys. This assumes that
         all primary keys are named "id".

        By default get_key_attribute is used for foreign keys. This assumes that all foreign
        keys match the name of the the primary key they refer to. For example if the object the
        foreign key referred to was named "patient" then the foreign would be named "patient_id".

        If foreign keys do not match the primary key they refer to then the functions would need
        to be different to reflect that.

        Args:
            config(SchemaConfig): A config object
            primary_key_getter (Callable[[str], str], optional):
                Defaults to get_key_attribute.
            foreign_key_getter (Callable[[str], str], optional):
                Defaults to get_key_attribute.
        """
        self.schema_url = config.schema_url
        self.synapse_project_id = config.synapse_project_id
        self.synapse_asset_view_id = config.synapse_asset_view_id
        self.synapse_input_token = config.synapse_input_token
        self.primary_key_getter = primary_key_getter
        self.foreign_key_getter = foreign_key_getter
        self.schema_graph = self.create_schema_graph()
        self.update_manifest_configs()
        self.update_db_config()

    def create_schema_graph(self) -> networkx.DiGraph:
        """Retrieve the edges from schematic API and store in networkx.DiGraph()

        Returns:
            networkx.DiGraph: The edges of the graph
        """
        subgraph = get_graph_by_edge_type(self.schema_url, "requiresComponent")
        schema_graph = networkx.DiGraph()
        schema_graph.add_edges_from(subgraph)
        return schema_graph

    def get_db_config(self) -> DBConfig:
        "Gets the currents objects DBConfig"
        return self.db_config

    def update_db_config(self) -> None:
        """Updates the objects DBConfig object."""
        # order objects so that ones with dependencies come after they depend on
        object_names = list(
            reversed(list(networkx.topological_sort(self.schema_graph)))
        )
        object_configs: list[Optional[DBObjectConfig]] = [
            self.create_db_object_config(name) for name in object_names
        ]
        filtered_object_configs: list[DBObjectConfig] = [
            config for config in object_configs if config is not None
        ]
        self.db_config = DBConfig(filtered_object_configs)

    def create_db_object_config(self, object_name: str) -> Optional[DBObjectConfig]:
        """Creates the config for one object in the database.

        Args:
            object_name (str): The name of the object the config will be created for.
            manifests (list[dict[str:str]]): A list of manifests in dictionary form

        Returns:
            Optional[DBObjectConfig]: The config for the object if the object has attributes
              otherwise None.
        """
        # Some components will not have any attributes for various reasons
        attributes = self.create_attributes(object_name)
        if not attributes:
            return None
        primary_key = get_property_label_from_display_name(
            self.schema_url, self.primary_key_getter(object_name)
        )
        # primary keys don't always appear in the attributes endpoint
        if primary_key not in [att.name for att in attributes]:
            attributes.append(
                DBAttributeConfig(
                    name=primary_key, datatype=DBDatatype.TEXT, required=True
                )
            )
        # foreign keys don't always appear in the attributes endpoint
        foreign_keys = self.create_foreign_keys(object_name)
        for key in foreign_keys:
            name = key.name
            if name not in [att.name for att in attributes]:
                attributes.append(
                    DBAttributeConfig(
                        name=name, datatype=DBDatatype.TEXT, required=False
                    )
                )
        return DBObjectConfig(
            name=object_name,
            attributes=attributes,
            primary_key=primary_key,
            foreign_keys=foreign_keys,
        )

    def create_attributes(
        self, object_name: str
    ) -> Union[list[DBAttributeConfig], None]:
        """Create the attributes for the object

        Args:
            object_name (str): The name of the object to create the attributes for

        Returns:
            Union[list[DBAttributeConfig], None]: A list of attributes in DBAttributeConfig form
        """
        # the names of the attributes to be created, in label(not display) form
        attribute_names = find_class_specific_properties(self.schema_url, object_name)
        attributes = [self.create_attribute(name) for name in attribute_names]
        # Some components will not have any attributes for various reasons
        if not attributes:
            warnings.warn(
                NoAttributesWarning(
                    f"Object {object_name} has no attributes, and will be skipped."
                )
            )
            return None
        return attributes

    def create_attribute(self, name: str) -> DBAttributeConfig:
        """Creates an attribute

        Args:
            name (str): The name of the attribute
            datatypes (dict[str, str]): A dictionary of attributes and their types

        Returns:
            DBAttributeConfig: The DBAttributeConfig for the attribute
        """
        rules = get_node_validation_rules(self.schema_url, name)
        type_rules = [rule for rule in rules if rule in SCHEMATIC_TYPE_DATATYPES]
        if len(type_rules) > 1:
            raise MoreThanOneTypeRule(name, type_rules)
        if len(type_rules) == 1:
            datatype = SCHEMATIC_TYPE_DATATYPES[type_rules[0]]
        else:
            datatype = DBDatatype.TEXT
        return DBAttributeConfig(
            name=name,
            datatype=datatype,
            required=is_node_required(self.schema_url, name),
        )

    def create_foreign_keys(self, object_name: str) -> list[DBForeignKey]:
        """Creates a list of foreign keys for an object in the database

        Args:
            object_name (str): The name of the object the config will be created for.

        Returns:
            list[DBForeignKey]: A list of foreign keys for the object.
        """
        neighbor_object_names = list(self.schema_graph.neighbors(object_name))
        foreign_keys = [self.create_foreign_key(name) for name in neighbor_object_names]
        return foreign_keys

    def create_foreign_key(self, foreign_object_name: str) -> DBForeignKey:
        """Creates a foreign key object

        Args:
            foreign_object_name (str): The name of the object the foreign key is referring to.

        Returns:
            DBForeignKey: A foreign key object.
        """
        attribute_name = get_property_label_from_display_name(
            self.schema_url, self.foreign_key_getter(foreign_object_name)
        )
        foreign_attribute_name = get_property_label_from_display_name(
            self.schema_url, self.primary_key_getter(foreign_object_name)
        )
        return DBForeignKey(
            attribute_name,
            foreign_object_name,
            foreign_attribute_name,
        )

    def update_manifest_configs(self) -> None:
        """Updates the current objects manifest_configs."""
        self.manifest_configs = get_project_manifests(
            input_token=self.synapse_input_token,
            project_id=self.synapse_project_id,
            asset_view=self.synapse_asset_view_id,
        )

    def get_manifest_configs(self) -> list[ManifestSynapseConfig]:
        """Gets the currents objects manifest_configs"""
        return self.manifest_configs

    def get_manifests(self, config: DBObjectConfig) -> list[pd.DataFrame]:
        """Gets the manifests associated with a db object config

        Args:
            config (DBObjectConfig): The config for the database object

        Returns:
            list[pd.DataFrame]: A list manifests in dataframe form
        """
        dataset_ids = get_dataset_ids_for_object(config.name, self.manifest_configs)
        manifests = [
            self.get_manifest(dataset_id, config) for dataset_id in dataset_ids
        ]
        return manifests

    def get_manifest(self, dataset_id: str, config: DBObjectConfig) -> pd.DataFrame:
        """Gets and formats a manifest

        Args:
            dataset_id (str): The Synapse id of the dataset the manifest belongs to
            config (DBObjectConfig): The config for the db object the manifest belongs to

        Raises:
            ManifestMissingPrimaryKeyError: Raised when the manifest is missing a primary key

        Returns:
            pd.DataFrame: The manifest in dataframe form
        """
        manifest = get_manifest(
            self.synapse_input_token,
            dataset_id,
            self.synapse_asset_view_id,
        )
        # create dict with columns names as keys and attribute names as values
        attribute_names: dict[str, str] = {
            col_name: self.get_attribute_name(col_name)
            for col_name in list(manifest.columns)
        }
        # filter dict for attribute names that appear in the config
        attribute_names = {
            col_name: att_name
            for (col_name, att_name) in attribute_names.items()
            if att_name in config.get_attribute_names()
        }
        # Raise error if all primary keys do not appear
        if config.primary_key not in attribute_names.values():
            raise ManifestMissingPrimaryKeyError(
                config.name,
                dataset_id,
                config.primary_key,
                list(attribute_names.values()),
            )
        # select rename columns manifest and select those in the config
        manifest = manifest.rename(columns=attribute_names)[
            list(attribute_names.values())
        ]
        return manifest

    def get_attribute_name(self, column_name: str) -> str:
        """Gets the attribute name of a manifest column

        Args:
            column_name (str): The name of the column

        Returns:
            str: The attribute name of the column
        """
        return get_property_label_from_display_name(self.schema_url, column_name)

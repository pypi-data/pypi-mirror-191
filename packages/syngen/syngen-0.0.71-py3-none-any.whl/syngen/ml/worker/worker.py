from typing import Dict, List, Optional
from dataclasses import dataclass

from loguru import logger

from syngen.ml.data_loaders import MetadataLoader
from syngen.ml.interface import TrainInterface, InferInterface


@dataclass
class Worker:
    """
    Class for preparing training and infer settings, metadata for training and infer process
    """
    table_name: str
    metadata_path: Optional[str]
    settings: Dict
    train_interface = TrainInterface()
    infer_interface = InferInterface()
    metadata = None
    divided = []

    def __post_init__(self):
        self.metadata_loader = MetadataLoader(self.metadata_path)
        self.metadata = self.metadata_loader.load_data() if self.metadata_path else None

    def __parse_train_settings(self, config: Dict):
        """
        Parse the settings for training process
        :param config: settings for training process declared in metadata.yaml file
        """
        epochs = config.get("train_settings", {}).get("epochs", self.settings.get("epochs"))
        drop_null = config.get("train_settings", {}).get("drop_null", self.settings.get("drop_null"))
        row_limit = config.get("train_settings", {}).get("row_limit", self.settings.get("row_limit"))
        batch_size = config.get("train_settings", {}).setdefault("batch_size", self.settings.get("batch_size"))
        return {
            "table_name": self.table_name,
            "epochs": epochs,
            "drop_null": drop_null,
            "row_limit": row_limit,
            "batch_size": batch_size
        }

    def __parse_infer_settings(self, config: Dict):
        """
        Parse the settings for infer process
        :param config: settings for infer process declared in metadata.yaml file
        """
        size = config.get("infer_settings", {}).get("size", self.settings.get("size"))
        run_parallel = config.get("infer_settings", {}).get("run_parallel", self.settings.get("run_parallel"))
        random_seed = config.get("infer_settings", {}).get("random_seed", self.settings.get("random_seed"))
        print_report = config.get("infer_settings", {}).get("print_report", self.settings.get("print_report"))
        batch_size = config.get("infer_settings", {}).get("batch_size", self.settings.get("batch_size"))
        return {
            "size": size,
            "run_parallel": run_parallel,
            "random_seed": random_seed,
            "print_report": print_report,
            "batch_size": batch_size
        }

    @staticmethod
    def _get_tables(config: Dict, key_type: str):
        """
        Return the list of related tables regarding to the type of key - 'primary key', 'foreign key'
        :param config: configuration of related tables declared in metadata.yaml file
        :param key_type: type of key either 'primary key' ('PK') or 'foreign key' ('FK')
        """
        try:
            tbls = [table_name for table_name, config in config.items()
                    for key in config["keys"]
                    if config["keys"][key]["type"] == key_type]
            return list(dict.fromkeys(tbls))
        except KeyError:
            raise KeyError(
                "The structure of metadata file seems to be invalid. "
                "Please check the presence of 'configuration', 'tables', "
                "'keys', 'type' fields in metadata file"
            )

    def _prepare_metadata_for_process(self, **kwargs):
        """
        Return the list of related tables for training or infer process,
        configuration of related tables

        type_of_process can be "train", "infer" or "all" for the Enterprise version
        """
        config_of_tables = self.metadata
        table_names = list(config_of_tables.keys())
        if len(table_names) == 1 and "keys" not in config_of_tables[table_names[0]]:
            # case with one table without any keys
            chain_of_tables = table_names
        else:
            if kwargs.get("type_of_process") == ("infer" or "all"):
                config_of_tables = self._split_pk_fk_metadata(config_of_tables, list(config_of_tables.keys()))
            pk_tables = self._get_tables(config_of_tables, "PK")
            fk_tables = self._get_tables(config_of_tables, "FK")
            # chain_of_tables = [*pk_tables, *list(set(fk_tables).difference(set(pk_tables)))]
            chain_of_tables = list(dict.fromkeys([*pk_tables, *fk_tables]))

        return chain_of_tables, config_of_tables

    def _split_pk_fk_metadata(self, config, tables):
        for table in tables:
            types_of_keys = [value["type"] for key, value in config[table]["keys"].items()]
            if "PK" in types_of_keys and "FK" in types_of_keys:
                self.divided += [table+"_pk", table+"_fk"]
                pk_uq_part = {key: value for key, value in config[table]["keys"].items() if value["type"] in ["PK", "UQ"]}
                fk_part = {key: value for key, value in config[table]["keys"].items() if value["type"] == "FK"}

                # Do this to create a new object instead of a reference
                as_pk_meta = {k: v for k, v in config[table].items()}
                as_fk_meta = {k: v for k, v in config[table].items()}

                as_pk_meta["keys"] = pk_uq_part
                as_fk_meta["keys"] = fk_part

                config[table + "_pk"] = as_pk_meta
                config[table + "_fk"] = as_fk_meta
                config.pop(table)
        return config

    def __train_chain_of_tables(self, tables: List, config_of_tables: Dict):
        """
        Run training process for the list of related tables
        :param tables: the list of related tables for training process
        :param config_of_tables: configuration of related tables declared in metadata.yaml file
        """
        for table in tables:
            config_of_table = config_of_tables[table]
            source = config_of_table.get("source", None)
            if source is None:
                raise AttributeError(
                    f"The source of table - {table} is mandatory parameter. "
                    f"It seems that the information of source for training is absent. "
                    f"Please provide the information of source in metadata file."
                )
            train_settings = self.__parse_train_settings(config_of_table)
            logger.info(f"Training process of the table - {table} has started.")
            self.train_interface.run(
                metadata=self.metadata,
                source=source,
                epochs=train_settings["epochs"],
                drop_null=train_settings["drop_null"],
                row_limit=train_settings["row_limit"],
                table_name=table,
                metadata_path=self.metadata_path,
                batch_size=train_settings["batch_size"]
            )

    def __infer_chain_of_tables(self, tables: List, config_of_tables: Dict):
        """
        Run infer process for the list of related tables
        :param tables: the list of related tables for infer process
        :param config_of_tables: configuration of related tables declared in metadata.yaml file
        """
        for table in tables:
            both_keys = table in self.divided
            config_of_table = config_of_tables[table]
            infer_settings = self.__parse_infer_settings(config_of_table)
            logger.info(f"Infer process of the table - {table} has started.")
            self.infer_interface.run(
                metadata=self.metadata,
                size=infer_settings["size"],
                table_name=table,
                run_parallel=infer_settings["run_parallel"],
                batch_size=infer_settings["batch_size"],
                metadata_path=self.metadata_path,
                random_seed=infer_settings["random_seed"],
                print_report=infer_settings["print_report"],
                both_keys=both_keys,
            )

    def __train_table(self):
        """
        Run training process for a single table
        :return:
        """
        logger.info(f"Training process of the table - {self.table_name} has started.")
        self.train_interface.run(
            metadata=self.metadata,
            source=self.settings.get("source"),
            epochs=self.settings.get("epochs"),
            drop_null=self.settings.get("drop_null"),
            row_limit=self.settings.get("row_limit"),
            table_name=self.table_name,
            metadata_path=self.metadata_path,
            batch_size=self.settings.get("batch_size")
        )

    def __infer_table(self):
        """
        Run infer process for a single table
        """
        logger.info(f"Infer process of the table - {self.table_name} has started.")
        self.infer_interface.run(
            metadata=self.metadata,
            size=self.settings.get("size"),
            table_name=self.table_name,
            metadata_path=self.metadata_path,
            run_parallel=self.settings.get("run_parallel"),
            batch_size=self.settings.get("batch_size"),
            random_seed=self.settings.get("random_seed"),
            print_report=self.settings.get("print_report"),
            both_keys=False,
        )

    def launch_train(self):
        """
        Launch training process either for a single table or for related tables
        """
        if self.metadata_path is not None:
            chain_of_tables, config_of_tables = self._prepare_metadata_for_process(type_of_process="train")
            self.__train_chain_of_tables(chain_of_tables, config_of_tables)
        elif self.table_name is not None:
            self.__train_table()

    def launch_infer(self):
        """
        Launch infer process either for a single table or for related tables
        """
        if self.metadata_path is not None:
            chain_of_tables, config_of_tables = self._prepare_metadata_for_process(type_of_process="infer")
            self.__infer_chain_of_tables(chain_of_tables, config_of_tables)
        if self.table_name is not None:
            self.__infer_table()

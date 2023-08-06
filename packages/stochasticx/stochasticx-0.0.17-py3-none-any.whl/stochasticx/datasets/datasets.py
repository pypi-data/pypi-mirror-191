from stochasticx.constants.urls import (
    LocalRoutes,
    get_local_url,
    CloudRoutes,
    get_cloud_url,
)
from stochasticx.utils.auth_utils import AuthUtils
from stochasticx.utils.file_utils import DatasetUtils
from stochasticx.utils.logging import configure_logger

import requests
import json
from pathlib import Path
import os

from stochasticx.utils.stat_controller import EventLogger

logger = configure_logger(__name__)


class DatasetType:
    """Dataset type"""

    HUGGINGFACE = "hf"
    CSV = "csv"
    JSON = "json"


class Dataset:
    """Dataset class"""

    def __init__(
        self,
        name: str,
        directory_path: str,
        dataset_type: str = DatasetType.HUGGINGFACE,
    ):
        """Initializer

        Args:
            name (str): dataset name
            directory_path (str): directory in which your dataset is stored
            dataset_type (str, optional): dataset type. Defaults to DatasetType.HUGGINGFACE.
        """
        assert isinstance(name, str), "The provided name {} is not valid".format(name)
        self.name = name
        self.directory_path = directory_path
        self.dataset_type = dataset_type
        self.column_names = []
        self.dataset_id = None
        self.dataset_info = None
        self.is_uploaded = False

    def upload(self, mode):
        """Uploads the dataset to the Stochastic platform"""

        assert self.directory_path is not None
        dataset_id = DatasetUtils.upload_dataset(
            self.directory_path, self.name, self.dataset_type, mode
        )

        EventLogger.log_event(f"datasets_{mode}_upload")

        self.set_id(dataset_id)
        self.is_uploaded = True

    def set_id(self, dataset_id: str):
        """Set the ID of the dataset

        Args:
            dataset_id (str): the new ID
        """
        self.dataset_id = dataset_id

    def get_id(self):
        """Returns the ID of the dataset

        Returns:
            str: the ID
        """
        return self.dataset_id

    def sync(self):
        """Synchronize the current dataset with the cloud"""

        if self.dataset_id is not None:
            temp_ds = Datasets.get_dataset("cloud", self.dataset_id)
            self.dataset_info = temp_ds.dataset_info
            self.name = temp_ds.name

    def get_dataset_info(self):
        """Gets the dataset information

        Returns:
            dict: dataset information
        """

        self.sync()

        return self.dataset_info

    def set_dataset_info(self, dataset_info):
        """Sets the dataset information

        Args:
            dataset_info (dict): dataset information
        """
        self.dataset_info = dataset_info

    def get_column_names(self, mode):
        """Get column names of the dataset

        Returns:
            List[str]: the column names
        """
        if self.dataset_id is not None:
            temp_ds = Datasets.get_dataset(mode, self.dataset_id)
            self.column_names = temp_ds.column_names

        return self.column_names

    def set_column_names(self, column_names):
        """Set the column names of the dataset

        Args:
            column_names (List[str]): new column names
        """
        self.column_names = column_names

    def download(self, local_path: str):
        """Downloads the dataset

        Args:
            local_path (str): local path where the dataset is saved
        """
        assert self.dataset_id is not None
        DatasetUtils.download_dataset(self.dataset_id, local_path)

    def to_table(self):
        columns = ["Id", "Name", "Directory path", "Type", "Uploaded"]
        values = [
            str(self.dataset_id),
            self.name,
            self.directory_path,
            self.dataset_type,
            str(self.is_uploaded),
        ]

        return columns, values

    def __str__(self):
        """Method to convert the object to string

        Returns:
            str: string
        """
        return "ID: {} ; Dataset name: {} ; Directory path: {} ; Dataset type: {} ; Uploaded: {}".format(
            self.dataset_id,
            self.name,
            self.directory_path,
            self.dataset_type,
            self.is_uploaded,
        )


class Datasets:
    """Class to get the uploaded datasets"""

    @staticmethod
    def get_dataset(mode: str, dataset_id: str):
        """Get dataset by ID

        Args:
            dataset_id (str): ID

        Returns:
            Dataset: the dataset
        """
        if mode == "cloud":
            auth_header = AuthUtils.get_auth_headers()
            url = get_cloud_url(CloudRoutes.DATASETS_URL.formatting(dataset_id))
        else:
            auth_header = None
            url = get_local_url(LocalRoutes.DATASET_URL, "local_url") + "/{}".format(
                dataset_id
            )
        response = requests.get(url, headers=auth_header)
        dataset_data = response.json().get("data")

        EventLogger.log_event(f"datasets_{mode}_get")

        if dataset_data is not None:
            ds = Dataset(
                name=dataset_data.get("name"),
                directory_path=None if mode == "cloud" else dataset_data.get("path"),
                dataset_type=dataset_data.get("type"),
            )

            ds.set_id(dataset_data.get("id"))

            if mode == "cloud":
                ds.set_dataset_info(dataset_data.get("datasetInfo"))
                if dataset_data.get("datasetInfo") is not None:
                    ds.set_column_names(
                        dataset_data.get("datasetInfo").get("column_names")
                    )
            ds.is_uploaded = True

            return ds

        return None

    @staticmethod
    def get_datasets(mode, fmt=None):
        """Gets all the datasets

        Returns:
            List[Dataset]: all the uploaded datasets
        """
        datasets = []

        if mode == "cloud":
            auth_header = AuthUtils.get_auth_headers()
            url = get_cloud_url(CloudRoutes.DATASETS_URL)
        else:
            auth_header = None
            url = get_local_url(LocalRoutes.DATASET_URL, "local_url")
        response = requests.get(url, headers=auth_header)
        datasets_data = response.json().get("data")

        EventLogger.log_event(f"datasets_{mode}_ls")

        if datasets_data is not None:
            for dataset_data in datasets_data:
                ds = Dataset(
                    name=dataset_data.get("name"),
                    directory_path=None
                    if mode == "cloud"
                    else dataset_data.get("path"),
                    dataset_type=dataset_data.get("type"),
                )

                ds.set_id(dataset_data.get("id"))

                if mode == "cloud":
                    ds.set_dataset_info(dataset_data.get("datasetInfo"))
                    if dataset_data.get("datasetInfo") is not None:
                        ds.set_column_names(
                            dataset_data.get("datasetInfo").get("column_names")
                        )
                ds.is_uploaded = True

                datasets.append(ds)

            if fmt == "table":
                columns = []
                values = []

                if len(datasets) > 0:
                    columns, _ = datasets[0].to_table()

                for dataset in datasets:
                    _, vals = dataset.to_table()
                    values.append(vals)

                return columns, values

        return datasets

    @staticmethod
    def remove_local_dataset(dataset_id: str):
        """Removes the local dataset

        Args:
            dataset_id (str): dataset ID

        Returns:
            None
        """

        url = get_local_url(LocalRoutes.DATASET_URL, "local_url") + "/{}".format(
            dataset_id
        )

        auth_header = None
        response = requests.delete(url, headers=auth_header)
        status = response.json().get("data")

        return status

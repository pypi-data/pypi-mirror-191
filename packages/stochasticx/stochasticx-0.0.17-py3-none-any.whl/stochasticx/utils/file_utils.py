from pathlib import Path
import os
import requests
from tqdm import tqdm
import json

import stochasticx

from stochasticx.constants.urls import (
    get_local_url,
    get_cloud_url,
    LocalRoutes,
    CloudRoutes,
)

from stochasticx.utils.auth_utils import AuthUtils


class FileUtils:
    """File utils"""

    @staticmethod
    def calculate_directory_size(directory_path: str):
        """Calculates the total size of a directory

        Args:
            directory_path (str): the directory path

        Returns:
            int: size in bytes
        """
        size = 0
        directory_path = Path(directory_path)

        assert directory_path.exists()

        all_files_dirs = directory_path.glob("**/*")
        for file_or_dir in all_files_dirs:
            if file_or_dir.is_file():
                size += os.path.getsize(str(file_or_dir.resolve()))

        return size


class DownloadUploadUtils:
    """Download utils"""

    @staticmethod
    def _download(prepare_download_path: str, download_path: str, local_path: str):
        """Download request

        Args:
            prepare_download_path (str): prepare download url
            download_path (str): download url
            local_path (str): local path where the file will be saved
        """
        auth_header = AuthUtils.get_auth_headers()

        # Prepare download
        r = requests.get(url=prepare_download_path, headers=auth_header)
        r.raise_for_status()
        download_token = r.json().get("downloadToken")

        # Download model
        with requests.get(
            url=download_path + "?auth_token={}".format(download_token),
            headers=auth_header,
            stream=True,
        ) as r:
            r.raise_for_status()
            total_size_in_bytes = int(r.headers.get("content-length", 0))
            progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)
            with open(str(local_path), "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    progress_bar.update(len(chunk))
                    f.write(chunk)


class ModelUtils:
    """ModelUtils"""

    @staticmethod
    def download_model(model_id: str, local_path: str):
        """Downloads a model

        Args:
            model_id (str): model ID to be downloaded
            local_path (str): path where the model will be saved
        """
        assert model_id is not None
        prepare_download_path = (
            stochasticx.BASE_URI + "/v1/models/{}/prepareDownload".format(model_id)
        )
        download_path = stochasticx.BASE_URI + "/v1/models/{}/download/".format(
            model_id
        )

        DownloadUploadUtils._download(prepare_download_path, download_path, local_path)

    @staticmethod
    def download_optimized_model(model_id: str, local_path: str):
        """Downloads the optimized model

        Args:
            model_id (str): model ID
            local_path (str): path where the model will be saved
        """

        assert model_id is not None
        prepare_download_path = (
            stochasticx.BASE_URI
            + "/v1/processedModels/{}/prepareDownload".format(model_id)
        )
        download_path = (
            stochasticx.BASE_URI + "/v1/processedModels/{}/download/".format(model_id)
        )

        DownloadUploadUtils._download(prepare_download_path, download_path, local_path)

    @staticmethod
    def upload_model(directory_path: str, model_name: str, model_type: str, mode: str):
        """Uploads a model to the platform

        Args:
            directory_path (str): directory path where the model is located
            model_name (str): model name
            model_type (str): model type

        Returns:
            str: model ID
        """
        assert directory_path is not None
        directory_size = FileUtils.calculate_directory_size(directory_path)

        # Request upload
        if mode == "cloud":
            auth_header = AuthUtils.get_auth_headers()
            data = {
                "folderSize": directory_size,
                "resourceType": "model",
                "resourceName": model_name,
            }
            suffix = CloudRoutes.REQUEST_UPLOAD_URL
            url = get_cloud_url(suffix)

            r = requests.post(url, json=data, headers=auth_header)
            r.raise_for_status()

            url = get_cloud_url(CloudRoutes.MODEL_UPLOAD_URL)
        else:
            auth_header = None
            url = get_local_url(LocalRoutes.MODEL_UPLOAD_URL, "local_url")

        # Upload model
        base_path = Path(directory_path)
        file_list = []
        all_files_dirs = base_path.glob("**/*")

        for file_or_dir_path in all_files_dirs:
            if file_or_dir_path.is_file():
                file = open(str(file_or_dir_path), "rb")
                relative_file_path = str(file_or_dir_path.resolve()).replace(
                    str(base_path.resolve()), ""
                )[1:]

                file_list.append(
                    ("pyModel", (relative_file_path, file, "multipart/form-data"))
                )

        request_body = {
            "name": model_name,
            "type": model_type,
            "folderSize": directory_size,
        }
        r = requests.post(url, data=request_body, files=file_list, headers=auth_header)
        r.raise_for_status()

        model_id = r.json().get("data").get("id")
        return model_id

    @staticmethod
    def add_local_model(directory_path: str, model_name: str, model_type: str):
        """Uploads a model to the platform

        Args:
            directory_path (str): directory path where the model is located
            model_name (str): model name
            model_type (str): model type

        Returns:
            str: model ID
        """
        assert directory_path is not None

        # auth_header = AuthUtils.get_auth_headers()
        auth_header = None

        # Request upload
        directory_size = FileUtils.calculate_directory_size(directory_path)
        # data = {"folderSize": directory_size}
        # print("DATA SIZE: ", data)
        # r = requests.post(, json=data, headers=auth_header)
        # r.raise_for_status()

        # Upload model
        base_path = Path(directory_path)
        file_list = []
        all_files_dirs = base_path.glob("**/*")

        for file_or_dir_path in all_files_dirs:
            if file_or_dir_path.is_file():
                file = open(str(file_or_dir_path), "rb")
                relative_file_path = str(file_or_dir_path.resolve()).replace(
                    str(base_path.resolve()), ""
                )[1:]

                file_list.append(
                    ("pyModel", (relative_file_path, file, "multipart/form-data"))
                )

        request_body = {
            "name": model_name,
            "type": model_type,
            "folderSize": directory_size,
        }
        local_url = get_local_url(LocalRoutes.MODEL_UPLOAD_URL, "local_url")

        r = requests.post(
            local_url, data=request_body, files=file_list, headers=auth_header
        )
        r.raise_for_status()

        # model_id = r.json().get("data")
        model_id = r.json().get("data").get("id")
        return model_id


class DatasetUtils:
    """Dataset utils"""

    @staticmethod
    def download_dataset(dataset_id: str, local_path: str):
        """Download a dataset

        Args:
            dataset_id (str): dataset ID to be downloaded
            local_path (str): local path where the dataset will be saved
        """
        assert dataset_id is not None
        prepare_download_path = (
            stochasticx.BASE_URI + "/v1/datasets/{}/prepareDownload".format(dataset_id)
        )
        download_path = stochasticx.BASE_URI + "/v1/datasets/{}/download/".format(
            dataset_id
        )

        DownloadUploadUtils._download(prepare_download_path, download_path, local_path)

    @staticmethod
    def upload_dataset(
        directory_path: str, dataset_name: str, dataset_type: str, mode: str
    ):
        """Uploads a dataset to the Stochastic platform

        Args:
            directory_path (str): _description_
            dataset_name (str): _description_
            dataset_type (str): _description_

        Returns:
            str: dataset ID
        """
        assert directory_path is not None
        if mode == "cloud":
            auth_header = AuthUtils.get_auth_headers()
        else:
            auth_header = None

        directory_size = FileUtils.calculate_directory_size(directory_path)
        # Request upload
        if mode == "cloud":
            data = {
                "folderSize": directory_size,
                "resourceType": "dataset",
                "resourceName": dataset_name,
            }
            suffix = CloudRoutes.REQUEST_UPLOAD_URL
            url = get_cloud_url(suffix)

            r = requests.post(url, json=data, headers=auth_header)
            r.raise_for_status()

        # Upload dataset
        base_path = Path(directory_path)
        all_files_dirs = base_path.glob("**/*")
        file_list = []

        for file_or_dir_path in all_files_dirs:
            if file_or_dir_path.is_file():
                file = open(str(file_or_dir_path), "rb")
                relative_file_path = str(file_or_dir_path.resolve()).replace(
                    str(base_path.resolve()), ""
                )[1:]
                file_list.append(
                    ("pyDataset", (relative_file_path, file, "multipart/form-data"))
                )

        request_body = {
            "name": dataset_name,
            "type": dataset_type,
            "folderSize": directory_size,
        }
        if mode == "cloud":
            url = get_cloud_url(CloudRoutes.DATASET_UPLOAD_URL)
        else:
            url = get_local_url(LocalRoutes.DATASET_UPLOAD_URL, "local_url")
        r = requests.post(url, data=request_body, files=file_list, headers=auth_header)
        r.raise_for_status()

        dataset_id = r.json().get("data").get("id")
        return dataset_id


class ConversionUtils:
    @staticmethod
    def convert(
        model_path: str,
        convert_type: str,
        model_type: str,
        task_type: str,
        convert_params: dict,
    ):
        """Convert model

        Args:
            model_path (str): directory path where the model is located
            convert_type (str): model type

        Returns:
            str: model ID
        """
        assert model_path is not None

        # auth_header = AuthUtils.get_auth_headers()
        auth_header = None

        # Request upload
        # data = {"folderSize": directory_size}
        # print("DATA SIZE: ", data)
        # r = requests.post(, json=data, headers=auth_header)
        # r.raise_for_status()
        model_path = Path(model_path)
        if os.path.isdir(model_path):
            output_dir = model_path.parent
        else:
            output_dir = model_path

        # local_url = get_local_url(LocalRoutes.MODEL_UPLOAD_URL)
        if convert_type == "onnx":
            request_body = {
                "model_path": str(model_path),
                "output_dir": str(output_dir),
                "model_type": model_type,
                "task_type": task_type,
            }
            local_url = get_local_url(
                LocalRoutes.ONNX_CONVERSION_URL, "local_conversion_url"
            )
        elif convert_type == "tensorrt":
            sequence_length = convert_params.get("sequence_length", 128)
            max_batch_size = convert_params.get("max_batch_size", 1)
            request_body = {
                "model_path": str(model_path),
                "output_dir": str(output_dir),
                "sequence_length": sequence_length,
                "dynamic_batch_size": max_batch_size,
            }
            local_url = get_local_url(
                LocalRoutes.TENSORRT_CONVERSION_URL, "local_conversion_url"
            )
        elif convert_type == "onnx_int8":
            request_body = {
                "model_path": str(model_path),
                "output_dir": str(output_dir),
                "model_type": model_type,
                "task_type": task_type,
            }
            local_url = get_local_url(
                LocalRoutes.ONNX_INT8_CONVERSION_URL, "local_conversion_url"
            )
        r = requests.post(local_url, data=json.dumps(request_body), headers=auth_header)
        return r.json()

        # # model_id = r.json().get("data")
        # model_id = r.json().get("data").get("id")
        # print(model_id)
        # return model_id
        return r

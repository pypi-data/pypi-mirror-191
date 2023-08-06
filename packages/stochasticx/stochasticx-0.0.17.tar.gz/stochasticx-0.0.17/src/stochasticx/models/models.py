from stochasticx.constants.urls import (
    LocalRoutes,
    get_local_url,
    CloudRoutes,
    get_cloud_url,
)
from stochasticx.utils.auth_utils import AuthUtils
from stochasticx.utils.file_utils import ModelUtils
import requests

from stochasticx.utils.stat_controller import EventLogger


class ModelType:
    """Model type"""

    HUGGINGFACE = "hf"
    PYTORCH = "pt"
    ONNX = "onnx"
    CUSTOM = "custom"


class Model:
    """Model class"""

    def __init__(
        self, name: str, directory_path: str, model_type: str = ModelType.HUGGINGFACE
    ):
        """Initializer

        Args:
            name (str): model name
            directory_path (str): directory path where the model is located
            model_type (str, optional): model type. Defaults to ModelType.HUGGINGFACE.
        """
        assert isinstance(name, str), "The provided name {} is not valid".format(name)

        self.name = name
        self.directory_path = directory_path
        self.model_type = model_type
        self.model_id = None
        self.model_info = None
        self.is_uploaded = False

    def upload(self, mode):
        """Upload the model to the stochastic platform"""

        model_id = ModelUtils.upload_model(
            self.directory_path, self.name, self.model_type, mode
        )

        EventLogger.log_event(f"models_{mode}_upload")

        self.set_id(model_id)
        self.is_uploaded = True

    def set_id(self, model_id: str):
        """Sets the model ID

        Args:
            model_id (str): new ID
        """
        self.model_id = model_id

    def sync(self):
        """Syncs the model information with the stochastic platform"""

        if self.model_id is not None:
            temp_model = Models.get_model(self.model_id, "cloud")
            self.name = temp_model.name
            self.model_info = temp_model.model_info
            self.is_uploaded = True

    def get_id(self):
        """Gets the model ID

        Returns:
            str: the model ID
        """
        return self.model_id

    def get_model_info(self):
        """Gets the model information

        Returns:
            dict: model information
        """

        self.sync()

        return self.model_info

    def set_model_info(self, model_info):
        """Sets the model information

        Args:
            model_info (dict): model info
        """
        self.model_info = model_info

    def download(self, local_path: str):
        """Download the model for the Stochastic platform

        Args:
            local_path (str): path where the model will be saved
        """
        assert self.model_id is not None
        ModelUtils.download_model(self.model_id, local_path)

    def to_table(self):
        columns = ["Id", "Name", "Directory path", "Type", "Uploaded"]
        values = [
            str(self.model_id),
            self.name,
            self.directory_path,
            self.model_type,
            str(self.is_uploaded),
        ]

        return columns, values

    def __str__(self):
        """Convert the object to string

        Returns:
            str
        """
        return "Model ID: {} ; Name: {} ; Directory path: {} ; Model type: {} ; Uploaded: {}".format(
            self.model_id,
            self.name,
            self.directory_path,
            self.model_type,
            self.is_uploaded,
        )


class OptimizedModel:
    """Optimized model class"""

    def __init__(
        self, id: str, name: str, type: str, size: str, benchmark_results: dict
    ):
        """Initializer

        Args:
            id (str): model ID
            name (str): model name
            type (str): model type
            size (str): model size in bytes
            benchmark_results (dict): benchmark results
        """

        self.id = id
        self.name = name
        self.type = type
        self.size = size
        self.benchmark_results = benchmark_results

    def download(self, local_path: str):
        """Downloads the model from the Stochastic platform

        Args:
            local_path (str): path where the model will be saved
        """

        ModelUtils.download_optimized_model(self.id, local_path)

    def get_benchmark_results(self):
        """Get benchmark results

        Returns:
            dict: benchmark results
        """
        return self.benchmark_results

    def to_table(self):
        columns = ["Id", "Name", "Type", "Size (MB)"]
        values = [self.id, self.name, self.type, str(self.size)]

        return columns, values

    def __str__(self):
        """Converts the object to a string

        Returns:
            str
        """

        return "Optimized model ID: {} ; Name: {} ; Type: {} ; Size: {} ".format(
            self.id, self.name, self.type, self.size
        )


class Models:
    """Class to get the models uploaded in the Stochastic platform"""

    @staticmethod
    def get_model(model_id: str, mode: str):
        """Gets the model from the Stochastic platform

        Args:
            model_id (str): model ID

        Returns:
            Model: model
        """
        if mode == "cloud":
            suffix = CloudRoutes.MODELS_URL.formatting(model_id)
            url = get_cloud_url(suffix)
            auth_header = AuthUtils.get_auth_headers()
        else:
            auth_header = None
            url = get_local_url(LocalRoutes.MODEL_URL, "local_url") + "/{}".format(
                model_id
            )

        response = requests.get(url, headers=auth_header)
        model_data = response.json().get("data")

        EventLogger.log_event(f"models_{mode}_get")

        if model_data is not None:
            model = Model(
                name=model_data.get("name"),
                directory_path=None if mode == "cloud" else model_data.get("path"),
                model_type=model_data.get("type"),
            )

            model.set_id(model_data.get("id"))
            if mode == "cloud":
                model.set_model_info(model_data.get("modelInfo"))
            model.is_uploaded = True

            return model

        return None

    @staticmethod
    def get_local_model(model_id: str):
        """Gets the model from the Stochastic platform

        Args:
            model_id (str): model ID

        Returns:
            Model: model
        """

        url = get_local_url(LocalRoutes.MODEL_URL, "local_url") + "/{}".format(model_id)

        auth_header = None
        response = requests.get(url, headers=auth_header)
        model_data = response.json().get("data")

        if model_data is not None:
            model = Model(
                name=model_data.get("name"),
                directory_path=model_data.get("path"),
                model_type=model_data.get("type"),
            )

            model.set_id(model_data.get("id"))
            # model.set_model_info(model_data.get("modelInfo"))
            model.is_uploaded = True

            return model

        return None

    @staticmethod
    def get_models(mode, fmt=None):
        """Gets all the models from the stochastic platform

        Returns:
            List[Model]: list of models
        """
        models = []

        if mode == "cloud":
            auth_header = AuthUtils.get_auth_headers()
            url = get_cloud_url(CloudRoutes.MODELS_URL)
        else:
            auth_header = None
            url = get_local_url(LocalRoutes.MODEL_URL, "local_url")
            
        response = requests.get(url, headers=auth_header)
        models_data = response.json().get("data")

        if models_data is not None:
            for model_data in models_data:
                model = Model(
                    name=model_data.get("name"),
                    directory_path=None if mode == "cloud" else model_data.get("path"),
                    model_type=model_data.get("type"),
                )

                model.set_id(model_data.get("id"))
                if mode == "cloud":
                    model.set_model_info(model_data.get("modelInfo"))
                model.is_uploaded = True
                models.append(model)

            if fmt == "table":
                columns = []
                values = []

                if len(models) > 0:
                    columns, _ = models[0].to_table()

                for model in models:
                    _, vals = model.to_table()
                    values.append(vals)

                return columns, values

        return models

    @staticmethod
    def get_local_models(fmt="table"):
        """Gets all the models from the local registry

        Returns:
            List[Model]: list of models
        """
        models = []

        # auth_header = AuthUtils.get_auth_headers()
        auth_header = None
        response = requests.get(
            get_local_url(LocalRoutes.MODEL_URL, "local_url"), headers=auth_header
        )
        models_data = response.json().get("data")

        if models_data is not None:
            for model_data in models_data:

                model = Model(
                    name=model_data.get("name"),
                    directory_path=model_data.get("path"),
                    model_type=model_data.get("type"),
                )

                model.set_id(model_data.get("id"))
                # model.set_model_info(model_data.get("modelInfo"))
                model.is_uploaded = True
                models.append(model)

            if fmt == "table":
                columns = []
                values = []

                if len(models) > 0:
                    columns, _ = models[0].to_table()

                for model in models:
                    _, vals = model.to_table()
                    values.append(vals)

                return columns, values

        return models

    @staticmethod
    def get_optimized_models(fmt="table"):
        """Gets all the optimized models from the Stochastic platform

        Returns:
            List[OptimizedModel]: list of optimized models
        """

        models = []

        auth_header = AuthUtils.get_auth_headers()

        suffix = CloudRoutes.OPTIMIZED_MODELS_URL
        url = get_cloud_url(suffix)

        response = requests.get(url, headers=auth_header)
        models_data = response.json().get("data")

        if models_data is not None:
            for model_data in models_data:
                model = OptimizedModel(
                    id=model_data.get("id"),
                    name=model_data.get("userGivenName"),
                    type=model_data.get("type"),
                    size=model_data.get("size"),
                    benchmark_results=model_data.get("result").get("results"),
                )

                models.append(model)

            if fmt == "table":
                columns = []
                values = []

                if len(models) > 0:
                    columns, _ = models[0].to_table()

                for model in models:
                    _, vals = model.to_table()
                    values.append(vals)

                return columns, values

        if fmt == "table":
            return [], []

        return models

    @staticmethod
    def get_optimized_model(model_id: str):
        """Gets an optimized model from the Stochastic plarform

        Args:
            model_id (str): model ID

        Returns:
            OptimizedModel: optimized model
        """

        suffix = CloudRoutes.OPTIMIZED_MODELS_URL.formatting(model_id)
        url = get_cloud_url(suffix)

        auth_header = AuthUtils.get_auth_headers()
        response = requests.get(url, headers=auth_header)
        model_data = response.json().get("data")

        if model_data is not None and len(model_data) > 0:
            model = OptimizedModel(
                id=model_data.get("id"),
                name=model_data.get("userGivenName"),
                type=model_data.get("type"),
                size=model_data.get("size"),
                benchmark_results=model_data.get("result").get("results"),
            )

            return model

        return None

    @staticmethod
    def remove_local_model(model_id: str):
        """Removes the local model

        Args:
            model_id (str): model ID

        Returns:
            None
        """

        url = get_local_url(LocalRoutes.MODEL_URL, "local_url") + "/{}".format(model_id)

        auth_header = None
        response = requests.delete(url, headers=auth_header)
        status = response.json().get("data")

        return status

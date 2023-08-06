import os

import stochasticx
from stochasticx.utils.preferences import Preferences, AppModes

if os.name == 'nt':
  HOME = "%userprofile%"
else:
  HOME = "$HOME"

TOKEN_AUTH_PATH = os.path.expandvars(f"{HOME}/.stochastic/token.json")
PREFERENCES_PATH = os.path.expandvars(f"{HOME}/.stochastic/preferences.json")

INFERENCE_URL = stochasticx.BASE_URI + "http://infer.stochastic.ai:8000/"
FINETUNING_GET_JOBS_CLOUD_URL = stochasticx.BASE_URI + "/v1/finetuningJobs"

DEPLOYMENTS_URL = stochasticx.BASE_URI + "/v1/deploy/"
STOCHASTIC_TEMPLATES_URL = stochasticx.BASE_URI + "/v1/deploy/stochastic-template"
CUSTOM_TEMPLATES_URL = stochasticx.BASE_URI + "/v1/deploy/custom-template"
IS_INFERENCE_FILE_AVAILABLE_URL = stochasticx.BASE_URI + "/v1/deploy/is-inference-file-available"

class CloudRoutesType:
    def __init__(self, suffix):
        self.suffix = suffix

    def cloud_add(self, url):
        return url + self.suffix

    def formatting(self, id):
        self.suffix += f"/{id}"
        return self


class CloudRoutes:
    LOGIN_URL = CloudRoutesType("/v1/auth/login")
    MODELS_URL = CloudRoutesType("/v1/models")
    OPTIMIZED_MODELS_URL = CloudRoutesType("/v1/processedModels")
    REQUEST_UPLOAD_URL = CloudRoutesType("/v1/upload/requestUpload")
    MODEL_UPLOAD_URL = CloudRoutesType("/v1/upload/model")
    DATASET_UPLOAD_URL = CloudRoutesType("/v1/upload/dataset")
    DATASETS_URL = CloudRoutesType("/v1/datasets")
    ME_URL = CloudRoutesType("/v1/auth/me")
    JOBS_URL = CloudRoutesType("/v1/jobs")
    INSTANCES_URL = CloudRoutesType("/v1/instances")
    DEPLOYMENT_URL = CloudRoutesType("/v1/deploy")
    STABLE_DIFFUSION_URL = CloudRoutesType("/v1/stdDeploy")
    INFERENCE_URL = "http://infer.stochastic.ai:8000/"
    


class LocalRoutesType:
    def __init__(self, suffix):
        self.suffix = suffix

    def local_add(self, url):
        return url + self.suffix


class LocalRoutes:
    HEALTH_REGISTRY = "http://127.0.0.1:3001/"
    LOGIN_URL = LocalRoutesType("/v1/auth/login")
    MODEL_URL = LocalRoutesType("/local/model")
    MODEL_UPLOAD_URL = LocalRoutesType("/local/model/upload")
    DATASET_URL = LocalRoutesType("/local/dataset")
    DATASET_UPLOAD_URL = LocalRoutesType("/local/dataset/upload")
    BENCHMARKING_URL = LocalRoutesType("/post_benchmarking_task")
    ONNX_CONVERSION_URL = LocalRoutesType("/onnx_conversion/")
    TENSORRT_CONVERSION_URL = LocalRoutesType("/tensorrt_conversion/")
    ONNX_INT8_CONVERSION_URL = LocalRoutesType("/onnx_conversion_int8/")


class CommonRoutes:
    LOGIN_URL = "LOGIN_URL"
    MODELS_URL = "MODELS_URL"


def get_cloud_url(suffix: CloudRoutesType) -> str:
    # Read saved preferences
    preferences = Preferences.load()
    return suffix.cloud_add(preferences.cloud_url)


def get_local_url(suffix: LocalRoutesType, type: str) -> str:
    # Read saved preferences
    preferences = Preferences.load()
    return suffix.local_add(preferences.__getattribute__(type))


def get_common_url(suffix: str) -> str:
    # Read saved preferences
    print("Suffix: ", suffix)
    preferences = Preferences.load()
    current_mode = preferences.current_mode

    if current_mode == AppModes.CLOUD:
        return preferences.cloud_url + suffix
    else:
        return preferences.local_url + suffix


# def test():

#     common_url = get_common_url(CommonRoutes.LOGIN_URL)

#     print("CommonURL: ", common_url)

#     cloud_url = get_cloud_url(CommonRoutes.LOGIN_URL)

#     print("CloudURL: ", cloud_url)

#     local_url = get_local_url(CommonRoutes.LOGIN_URL)

#     print("LocalURL: ", local_url)

# test()

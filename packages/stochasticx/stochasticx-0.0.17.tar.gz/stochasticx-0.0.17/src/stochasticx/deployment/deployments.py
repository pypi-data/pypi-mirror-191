from dataclasses import dataclass, field, asdict
import requests
from datetime import datetime
import click
import sys
from typing import Dict
import uuid
from stochasticx.constants.urls import CloudRoutes, get_cloud_url
from stochasticx.utils.auth_utils import AuthUtils
from stochasticx.models.models import OptimizedModel, Models
from stochasticx.utils.logging import configure_logger
from stochasticx.utils.parse_utils import parse_date
from stochasticx.utils.stat_controller import (
    StatController,
    LocalDeploymentJobInformation,
)
from stochasticx.utils.preferences import Preferences
from stochasticx.constants.urls import (
    DEPLOYMENTS_URL, 
    STOCHASTIC_TEMPLATES_URL,
    CUSTOM_TEMPLATES_URL,
    IS_INFERENCE_FILE_AVAILABLE_URL
)

import requests
from dataclasses import dataclass

from stochasticx.models.models import Model
from stochasticx.utils.auth_utils import AuthUtils


logger = configure_logger(__name__)


class LocalDeploymentsClient:
    @staticmethod
    def get_deployments(fmt="table"):
        preferences = Preferences.load()
        response = requests.get(f"{preferences.local_deployment_url}/models")
        response.raise_for_status()

        models = response.json()
        model_results = []

        for model in models:
            model_results.append(
                LocalDeployment(
                    id=model.get("id"),
                    model_name=model.get("model_name"),
                    type=model.get("type"),
                    cuda=model.get("cuda"),
                    task_type=model.get("task_type"),
                    user_params=model.get("user_params"),
                )
            )

        if fmt == "table":
            columns = []
            values = []

            if len(model_results) > 0:
                columns, _ = model_results[0].to_table()

            for model in model_results:
                _, vals = model.to_table()
                values.append(vals)

            return columns, values
        else:
            return model_results

    @staticmethod
    def get_deployment_by_id(id):
        deployments = LocalDeploymentsClient.get_deployments(fmt=None)

        for deployment in deployments:
            if deployment.id == id:
                return deployment

        return None

    @staticmethod
    def delete_deployment(model_type, model_name):
        preferences = Preferences.load()
        response = requests.delete(
            "{}/model/{}/{}".format(
                preferences.local_deployment_url, model_type, model_name
            )
        )
        response.raise_for_status()


@dataclass
class LocalDeployment:
    model_name: str
    type: str
    cuda: bool
    task_type: str
    user_params: Dict
    id: str = None

    def to_table(self):
        columns = [
            "Model ID",
            "Model name",
            "Model type",
            "CUDA",
            "Task type",
            "User params",
        ]

        values = [
            str(self.id),
            self.model_name,
            self.type,
            str(self.cuda),
            self.task_type,
            str(self.user_params),
        ]

        return columns, values


@dataclass
class LocalSequenceClassificationDeployment(LocalDeployment):
    task_type: str = "sequence_classification"
    user_params: Dict = field(
        default_factory=lambda: {"max_batch_size": 8, "max_seq_length": 128}
    )

    def start_deployment(self):
        preferences = Preferences.load()
        response = requests.post(
            f"{preferences.local_deployment_url}/model", json=asdict(self)
        )

        response.raise_for_status()

        StatController.add_information(
            LocalDeploymentJobInformation(
                deployment_type=self.task_type,
                model_name=self.model_name,
                type=self.type,
                params=self.user_params,
                job_result=response.json(),
            )
        )


@dataclass
class LocalQuestionAnsweringDeployment(LocalDeployment):
    task_type: str = "question_answering"
    user_params: Dict = field(
        default_factory=lambda: {
            "max_batch_size": 8,
            "max_seq_length": 256,
            "stride": 30,
        }
    )

    def start_deployment(self):
        preferences = Preferences.load()
        response = requests.post(
            f"{preferences.local_deployment_url}/model", json=asdict(self)
        )

        response.raise_for_status()

        StatController.add_information(
            LocalDeploymentJobInformation(
                deployment_type=self.task_type,
                model_name=self.model_name,
                type=self.type,
                params=self.user_params,
                job_result=response.json(),
            )
        )


@dataclass
class LocalTokenClassificationDeployment(LocalDeployment):
    task_type: str = "token_classification"
    user_params: Dict = field(
        default_factory=lambda: {"max_seq_length": 256, "label_all_tokens": False}
    )

    def start_deployment(self):
        preferences = Preferences.load()
        response = requests.post(
            f"{preferences.local_deployment_url}", json=asdict(self)
        )

        response.raise_for_status()

        StatController.add_information(
            LocalDeploymentJobInformation(
                deployment_type=self.task_type,
                model_name=self.model_name,
                type=self.type,
                params=self.user_params,
                job_result=response.json(),
            )
        )


@dataclass
class LocalTranslationDeployment(LocalDeployment):
    task_type: str = "translation"
    user_params: Dict = field(
        default_factory=lambda: {
            "max_source_length": 256,
            "max_target_length": 256,
            "src_lang": "en",
            "tgt_lang": "es",
            "pad_to_max_length": False,
            "num_beams": 4,
            "ignore_pad_token_for_loss": True,
            "source_prefix": "",
            "forced_bos_token": None,
        }
    )

    def start_deployment(self):
        preferences = Preferences.load()
        response = requests.post(
            f"{preferences.local_deployment_url}/model", json=asdict(self)
        )

        response.raise_for_status()

        StatController.add_information(
            LocalDeploymentJobInformation(
                deployment_type=self.task_type,
                model_name=self.model_name,
                type=self.type,
                params=self.user_params,
                job_result=response.json(),
            )
        )


@dataclass
class LocalSummarizationDeployment(LocalDeployment):
    task_type: str = "summarization"
    user_params: Dict = field(
        default_factory=lambda: {
            "max_source_length": 256,
            "max_target_length": 64,
            "lang": "en",
            "pad_to_max_length": False,
            "num_beams": 4,
            "ignore_pad_token_for_loss": True,
            "source_prefix": "",
            "forced_bos_token": None,
        }
    )

    def start_deployment(self):
        preferences = Preferences.load()
        response = requests.post(
            f"{preferences.local_deployment_url}/model", json=asdict(self)
        )

        response.raise_for_status()

        StatController.add_information(
            LocalDeploymentJobInformation(
                deployment_type=self.task_type,
                model_name=self.model_name,
                type=self.type,
                params=self.user_params,
                job_result=response.json(),
            )
        )


@dataclass
class LocalTextGenerationDeployment(LocalDeployment):
    task_type: str = "text_generation"
    user_params: Dict = field(default_factory=lambda: {"block_size": 256})

    def start_deployment(self):
        preferences = Preferences.load()
        response = requests.post(
            f"{preferences.local_deployment_url}/model", json=asdict(self)
        )

        response.raise_for_status()

        StatController.add_information(
            LocalDeploymentJobInformation(
                deployment_type=self.task_type,
                model_name=self.model_name,
                type=self.type,
                params=self.user_params,
                job_result=response.json(),
            )
        )


class InstanceTypes:
    g4dn_xlarge = "g4dn.xlarge"
    c5_2xlarge = "c5.2xlarge"
    c5_12xlarge = "c5.12xlarge"


class Instance:
    def __init__(
        self,
        id,
        name,
        cost_per_hour,
        cost_per_month,
        spot_cost,
        storage,
        vcpus,
        memory,
        network,
    ):
        self.id = id
        self.name = name
        self.cost_per_hour = cost_per_hour
        self.cost_per_month = cost_per_month
        self.spot_cost = spot_cost
        self.storage = storage
        self.vcpus = vcpus
        self.memory = memory
        self.network = network

    def to_table(self):
        columns = [
            "Id",
            "Name",
            "Cost/hour",
            "Cost/month",
            "Spot cost",
            "Storage",
            "vCPUs",
            "Memory",
            "Network",
        ]

        values = [
            self.id,
            self.name,
            self.cost_per_hour,
            self.cost_per_month,
            self.spot_cost,
            self.storage,
            self.vcpus,
            self.memory,
            self.network,
        ]

        return columns, values

    def __str__(self):
        return "ID: {} ; Name: {} ; Cost/hour: {} ; Cost/month: {} ; Spot cost: {} ; Storage: {} ; vCPUs: {} ; Memory: {} ; Network: {}".format(
            self.id,
            self.name,
            self.cost_per_hour,
            self.cost_per_month,
            self.spot_cost,
            self.storage,
            self.vcpus,
            self.memory,
            self.network,
        )


class Instances:
    @staticmethod
    def get_instance_types(fmt=None):
        instances = []

        auth_header = AuthUtils.get_auth_headers()
        r = requests.get(get_cloud_url(CloudRoutes.INSTANCES_URL), headers=auth_header)
        r.raise_for_status()

        data = r.json()

        if data.get("ec2Instances") is not None:
            for instance_data in data["ec2Instances"]:
                instance = Instance(
                    id=instance_data["id"],
                    name=instance_data["instanceType"],
                    cost_per_hour=instance_data["hourlyCost"],
                    memory=instance_data["memory"],
                    cost_per_month=instance_data["monthlyCost"],
                    network=instance_data["network"],
                    spot_cost=instance_data["spotCost"],
                    storage=instance_data["storage"],
                    vcpus=instance_data["vcpus"],
                )

                instances.append(instance)

            if fmt == "table":
                columns = []
                values = []

                if len(instances) > 0:
                    columns, _ = instances[0].to_table()

                for instance in instances:
                    _, vals = instance.to_table()
                    values.append(vals)

                return columns, values

        return instances

    @staticmethod
    def get_instance_type_by_name(name):
        instances = Instances.get_instance_types()

        for instance in instances:
            if instance.name == name:
                return instance


class StableDiffusionDeployment:
    def __init__(self, id, status, model_name, api_key=None, client_url=None):
        self.id = id
        self.status = status
        self.model_name = model_name
        self.api_key = api_key
        self.client_url = client_url

    def __str__(self):
        return (
            "ID: {} ; Status: {} ; Model name: {} ; API key: {} ; Endpoint: {}".format(
                self.id, self.status, self.model_name, self.api_key, self.client_url
            )
        )
    
     
class StableDiffusionDeployments:
    @staticmethod
    def get_deployments():
        deployments = []

        auth_header = AuthUtils.get_auth_headers()
        r = requests.get(
            get_cloud_url(CloudRoutes.STABLE_DIFFUSION_URL), headers=auth_header
        )
        r.raise_for_status()

        data = r.json()
        deploying = False

        if data["data"] is not None:
            for deployment_data in data["data"]:

                api_key = None
                client_url = None
                if deployment_data.get("resources") is not None:
                    api_key = deployment_data.get("resources").get("apiKey")
                    client_url = deployment_data.get("clientUrl")
                else:
                    deploying = True

                deployment = StableDiffusionDeployment(
                    id=deployment_data.get("id"),
                    status=deployment_data.get("status"),
                    model_name=deployment_data.get("modelName"),
                    client_url=client_url,
                    api_key=api_key,
                )
                deployments.append(deployment)

        if deploying:
            click.secho(
                "[+] There are models that are still deploying. It can take some minutes...\n",
                bold=True,
                fg="yellow",
            )

        return deployments

    @staticmethod
    def get_deployment(id):
        url = get_cloud_url(CloudRoutes.STABLE_DIFFUSION_URL.formating(id))

        auth_header = AuthUtils.get_auth_headers()
        r = requests.get(url, headers=auth_header)

        try:
            r.raise_for_status()
        except:
            click.secho("[+] The ID is not correct\n", bold=True, fg="yellow")
            sys.exit()

        data = r.json()
        deployment_data = data["deployedModel"]
        if deployment_data is not None:
            if deployment_data.get("resources") is not None:
                api_key = deployment_data.get("resources").get("apiKey")
                client_url = deployment_data.get("clientUrl")

                deployment = StableDiffusionDeployment(
                    id=deployment_data.get("_id"),
                    status=deployment_data.get("status"),
                    model_name=deployment_data.get("modelName"),
                    client_url=client_url,
                    api_key=api_key,
                )
            else:
                deployment = StableDiffusionDeployment(
                    id=deployment_data.get("_id"),
                    status=deployment_data.get("status"),
                    model_name=deployment_data.get("modelName"),
                )

                click.secho(
                    "[+] The model is still deploying. It can take some minutes...",
                    bold=True,
                    color="yellow",
                )

            return deployment

        return None

    @staticmethod
    def deploy():
        auth_header = AuthUtils.get_auth_headers()
        r = requests.post(
            get_cloud_url(CloudRoutes.STABLE_DIFFUSION_URL),
            headers=auth_header,
            json={"name": "Stable-Diffusion-{}".format(uuid.uuid4())},
        )
        r.raise_for_status()

    @staticmethod
    def delete(id):
        url = get_cloud_url(CloudRoutes.STABLE_DIFFUSION_URL.formating(id))
        auth_header = AuthUtils.get_auth_headers()
        r = requests.delete(url, headers=auth_header)
        r.raise_for_status()


@dataclass
class Deployment:
    id: str
    name: str
    status: str
    instance_type: str
    client_url: str
    api_key: str
    model: Model
    inference_file_path: str = None
    
    def to_table(self):
        columns = [
            "Name", 
            "Status",
            "Instance",
            "Model"
        ]
        
        values = [
            self.name,
            self.status,
            self.instance_type,
            self.model.name
        ]
        
        return columns, values
    
    def __str__(self) -> str:
        return "Name {} ; Status {} ; Model {}".format(
            self.name,
            self.status,
            self.model.name
        )


class DeploymentsClient:
    @staticmethod
    def get_deployments(fmt="table"):
        deployments = []
        auth_header = AuthUtils.get_auth_headers()
        response = requests.get(
            url=DEPLOYMENTS_URL,
            headers=auth_header
        )
        
        response.raise_for_status()
        
        deployments_data_list = response.json()["data"]
                
        for deployment_data in deployments_data_list:
            try:
                deployment = Deployment(
                    id = deployment_data["id"],
                    name = deployment_data["name"],
                    client_url= deployment_data.get("clientUrl") if deployment_data.get("clientUrl") else "Not available",
                    instance_type = deployment_data["instanceType"],
                    status = deployment_data["status"],
                    api_key = deployment_data["resources"]["apiKey"] if deployment_data.get("resources") is not None else "Not available",
                    model=Model(
                        name=deployment_data["model"]["name"],
                        directory_path=None,
                        model_type=deployment_data["model"]["type"]
                    )
                )
                
                deployments.append(deployment)
            except Exception as ex:
                pass
            
        if fmt == "table":
            columns = []
            values = []
            
            if len(deployments) > 0:
                columns, _ = deployments[0].to_table()
                
            for deployment in deployments:
                _, vals = deployment.to_table()
                values.append(vals)
                
            return columns, values
        
        return deployments
        
    @staticmethod
    def get_deployment_by_id(deployment_id):
        auth_header = AuthUtils.get_auth_headers()
        response = requests.get(
            url=f"{DEPLOYMENTS_URL}/{deployment_id}",
            headers=auth_header
        )
        
        response.raise_for_status()
        
        deployment_data = response.json()["data"]
        
        deployment = Deployment(
            id = deployment_data["id"],
            name = deployment_data["name"],
            client_url= deployment_data["client_url"],
            instance_type = deployment_data["instance_type"],
            status = deployment_data["status"],
            api_key = deployment_data["resources"]["api_key"],
            model=Model(
                name=deployment_data["model"]["name"],
                directory_path=None,
                model_type=deployment_data["model"]["type"]
            )
        )
        
        return deployment
        
    @staticmethod
    def create_deployment(
        name,
        instance_type,
        model_name,
        model_type=None,
        task_type=None,
        inference_file_path=None,
        docker_image=None,
        docker_registry_username=None,
        docker_registry_password=None
    ):        
        auth_header = AuthUtils.get_auth_headers()
        
        models = Models.get_models(mode="cloud", fmt=None)
        model_id = None
        if len(models) > 0:
            
            for model in models:
                if model.name == model_name:
                    model_id = model.model_id
                    break
                
        if model_id is None:
            logger.error("The model name {} was not found".format(model_name))
            sys.exit()
        
        if model_type is not None and task_type is not None:
            response = requests.post(
                url=f"{STOCHASTIC_TEMPLATES_URL}",
                headers=auth_header,
                json={
                    "model_id": model_id,
                    "model_type": model_type,
                    "task_type": task_type
                }
            )
            
            response.raise_for_status()
        
        if inference_file_path is not None:
            response = requests.post(
                url=f"{CUSTOM_TEMPLATES_URL}",
                headers=auth_header,
                json={
                    "model_id": model_id,
                    "inference_path": inference_file_path
                }
            )
            
            response.raise_for_status()
        
        # Check inference file is available in the model
        response = requests.post(
            url=f"{IS_INFERENCE_FILE_AVAILABLE_URL}",
            headers=auth_header,
            json={
                "model_id": model_id
            }
        )
        
        response.raise_for_status()
        is_inference_file_available = response.json()["data"]
        
        if not is_inference_file_available:
            raise ValueError("There is not inference.py file in the model you have specified")
        
        response = requests.post(
            url=f"{DEPLOYMENTS_URL}",
            headers=auth_header,
            json={
                "name": name,
                "model_id": model_id,
                "instance_type": instance_type,
                #"docker_image": docker_image,
                #"docker_registry_username": docker_registry_username,
                #"docker_registry_password": docker_registry_password
            }
        )
        
        response.raise_for_status()
    
    @staticmethod
    def terminate_deployment(deployment_name):
        auth_header = AuthUtils.get_auth_headers()
        
        deployments = DeploymentsClient.get_deployments(fmt=None)
        
        deployment_id = None
        for deployment in deployments:
            if deployment.name == deployment_name:
                deployment_id = deployment.id
                break
                
        if deployment_id is None:
            logger.error("The deployment name {} was not found".format(deployment_id))
            sys.exit()
        
        response = requests.delete(
            url=f"{DEPLOYMENTS_URL}/{deployment_id}",
            headers=auth_header
        )
        
        response.raise_for_status()
    
    @staticmethod
    def stop_deployment(deployment_id):
        auth_header = AuthUtils.get_auth_headers()
        
        response = requests.put(
            url=f"{DEPLOYMENTS_URL}/{deployment_id}/stop",
            headers=auth_header
        )
        
        response.raise_for_status()
    
    @staticmethod
    def resume_deployment(deployment_id):
        auth_header = AuthUtils.get_auth_headers()
        
        response = requests.put(
            url=f"{DEPLOYMENTS_URL}/{deployment_id}/start",
            headers=auth_header
        )
        
        response.raise_for_status()      

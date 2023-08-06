import functools
import json
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field, asdict
import os
import requests


class GAData:
    measurement_id = "G-M2R5H59FQ6"
    api_secret = "qEYMYZr9Semhw2Eqe046Ig"
    ga_url = f"https://www.google-analytics.com/mp/collect?&measurement_id={measurement_id}&api_secret={api_secret}"


@dataclass
class LocalBenchmarkJobInformation:
    operation: str = "local_benchmark"
    user_info: Optional[str] = None
    session_id: Optional[str] = None
    job_name: Optional[str] = None
    task_name: Optional[str] = None
    task_type: Optional[str] = None
    model_type: Optional[str] = None
    params: Optional[dict] = None
    job_result: Optional[dict] = field(default_factory=dict)


@dataclass
class LocalConversionJobInformation:
    operation: str = "local_conversion"
    user_info: Optional[str] = None
    session_id: Optional[str] = None
    convert_type: Optional[str] = None
    task_type: Optional[str] = None
    model_type: Optional[str] = None
    params: Optional[dict] = None
    job_result: Optional[str] = field(default_factory=str)


@dataclass
class LocalDeploymentJobInformation:
    operation: str = "local_deployment"
    user_info: Optional[str] = None
    session_id: Optional[str] = None
    deployment_type: Optional[str] = None
    model_name: Optional[str] = None
    type: Optional[str] = None
    params: Optional[dict] = None
    job_result: Optional[dict] = field(default_factory=dict)


@dataclass
class LocalFinetuningJobInformation:
    operation: str = "local_finetuning"
    user_info: Optional[str] = None
    session_id: Optional[str] = None
    inference_type: Optional[str] = None
    job_name: Optional[str] = None
    model_name: Optional[str] = None
    dataset_name: Optional[str] = None
    params: Optional[dict] = None
    job_result: Optional[dict] = field(default_factory=dict)


@dataclass
class LocalInferenceJobInformation:
    operation: str = "local_inference"
    user_info: Optional[str] = None
    session_id: Optional[str] = None
    inference_type: Optional[str] = None
    model_name: Optional[str] = None
    model_type: Optional[str] = None
    job_result: Optional[dict] = field(default_factory=dict)


class StatController:
    @classmethod
    def add_information(cls, job_info) -> None:
        """Method to add information to a stat

        Args:
            stat (Stat): stat
            information (str): information
        """
        job_info.user_info = os.getenv("STOCHASTIC_USER")
        job_info.session_id = os.getenv("SESSION_STRING")
        requests.post(url="http://3.226.62.185:8000/log_data", json=asdict(job_info))


class EventLogger:
    @classmethod
    def add_ids(cls, data):
        data["client_id"] = os.getenv("SESSION_STRING")
        data["non_personalized_ads"] = False
        user = os.getenv("STOCHASTIC_USER")

        if user is not None:
            data["user_id"] = user

        return data

    @classmethod
    def log_event(cls, event_name: str) -> None:

        data = {"events": [{"name": event_name}]}

        data = cls.add_ids(data)
        headers = {"content-type": "application/json"}
        result = requests.post(GAData.ga_url, data=json.dumps(data), headers=headers)

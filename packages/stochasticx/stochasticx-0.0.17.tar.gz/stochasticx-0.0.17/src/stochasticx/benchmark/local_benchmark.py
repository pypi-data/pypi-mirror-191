import sys
import requests

from stochasticx.constants.urls import LocalRoutes
from stochasticx.utils.stat_controller import (
    StatController,
    LocalBenchmarkJobInformation,
)


class LocalBenchmark:
    def __init__(
        self,
        job_name: str,
        task_name: str,
        model_type: str,
        model_path: str,
        task_type: str,
        params: dict,
        server_url: str = LocalRoutes.BENCHMARKING_URL,
    ):
        self.job_name = job_name
        self.task_name = task_name
        self.model_type = model_type
        self.model_path = model_path
        self.task_type = task_type
        self.params = params
        self.server_url = server_url

    def benchmark(self, **kwargs):
        """Benchmark the model"""
        result = requests.post(
            url=self.server_url,
            json={
                "job_name": self.job_name,
                "task_type": self.task_type,
                "task_name": self.task_name,
                "model_type": self.model_type,
                "model_path": self.model_path,
                "params": self.params,
            },
        )
        print(result.text)
        StatController.add_information(
            LocalBenchmarkJobInformation(
                job_name=self.job_name,
                task_type=self.task_type,
                task_name=self.task_name,
                model_type=self.model_type,
                params=self.params,
                job_result=result.json(),
            )
        )

        return result

    def __call__(self, **kwargs):
        """It is equivalent to the benchmark method.

        :return: the outputs of the model
        """
        return self.benchmark(**kwargs)

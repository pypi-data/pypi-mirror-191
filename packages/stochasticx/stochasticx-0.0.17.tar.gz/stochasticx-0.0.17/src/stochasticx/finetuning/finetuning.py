from dataclasses import dataclass, asdict, field
from re import S
import requests
import click
from typing import Dict, List
from stochasticx.constants.urls import FINETUNING_GET_JOBS_CLOUD_URL
from stochasticx.utils.parse_utils import parse_date
from stochasticx.utils.auth_utils import AuthUtils
from stochasticx.utils.stat_controller import (
    StatController,
    LocalFinetuningJobInformation,
)
from stochasticx.utils.preferences import AppModes, Preferences


@dataclass
class CloudEvaluationResults:
    model_name: str
    evaluation_benchmark: field(default_factory=dict)

    def __str__(self) -> str:
        return """
\t Model name: {}
\t Evaluation benchmarks: {}        
""".format(
            self.model_name, self.evaluation_benchmark
        )


@dataclass
class CloudFinetuningJob:
    id: str
    name: str
    job_status: str = "new"
    created_at: str = ""
    results: List[CloudEvaluationResults] = field(default_factory=list)

    def __str__(self):
        string = """
ID: {}
Name: {}
Status: {}
Created at: {}
Results:
""".format(
            self.id, self.name, self.job_status, self.created_at
        )
        for result in self.results:
            string += result.__str__()

        return string

    def to_table(self):
        columns = ["ID", "Name", "Status", "Created at"]

        values = [self.id, self.name, self.job_status, parse_date(self.created_at)]

        return columns, values


@dataclass
class CloudSequenceClassificationFinetuning(CloudFinetuningJob):
    dataset_id: str = None
    model_id: str = None
    model_source: str = "s3"
    task_type: str = "sequence_classification"
    max_seq_length: int = 128
    sentence1_column: str = "sentence1"
    sentence2_column: str = "sentence2"
    label_column: str = "label"

    def start_job(self):
        data = {
            "dataset": self.dataset_id,
            "jobName": self.name,
            "model": self.model_id,
            "modelSource": self.model_source,
            "selectedColumns": {
                "sentence1_column": self.sentence1_column,
                "sentence2_column": self.sentence2_column,
                "label_column": self.label_column,
            },
            "taskArguments": {"max_seq_length": self.max_seq_length},
            "taskType": self.task_type,
        }

        auth_header = AuthUtils.get_auth_headers()
        response = requests.post(
            FINETUNING_GET_JOBS_CLOUD_URL, json=data, headers=auth_header
        )
        response.raise_for_status()
        data = response.json()

        return data.get("id")


@dataclass
class CloudQuestionAnsweringFinetuning(CloudFinetuningJob):
    dataset_id: str = None
    model_id: str = None
    model_source: str = "s3"
    task_type: str = "question_answering"
    max_seq_length: int = 128
    stride: int = 30
    question_column: str = "question"
    context_column: str = "context"
    answer_column: str = "answers"

    def start_job(self):
        data = {
            "dataset": self.dataset_id,
            "jobName": self.name,
            "model": self.model_id,
            "modelSource": self.model_source,
            "selectedColumns": {
                "question_column": self.question_column,
                "context_column": self.context_column,
                "answer_column": self.answer_column,
            },
            "taskArguments": {"max_seq_length": self.max_seq_length},
            "taskType": self.task_type,
        }

        auth_header = AuthUtils.get_auth_headers()
        response = requests.post(
            FINETUNING_GET_JOBS_CLOUD_URL, json=data, headers=auth_header
        )
        response.raise_for_status()
        data = response.json()

        return data.get("id")


@dataclass
class CloudTokenClassificationFinetuning(CloudFinetuningJob):
    dataset_id: str = None
    model_id: str = None
    model_source: str = "s3"
    task_type: str = "token_classification"
    max_seq_length: int = 128
    label_all_tokens: bool = False
    text_column: str = "tokens"
    label_column: str = "ner_tags"

    def start_job(self):
        data = {
            "dataset": self.dataset_id,
            "jobName": self.name,
            "model": self.model_id,
            "modelSource": self.model_source,
            "selectedColumns": {
                "text_column": self.text_column,
                "label_column": self.label_column,
            },
            "taskArguments": {
                "max_seq_length": self.max_seq_length,
                "label_all_tokens": self.label_all_tokens,
            },
            "taskType": self.task_type,
        }

        auth_header = AuthUtils.get_auth_headers()
        response = requests.post(
            FINETUNING_GET_JOBS_CLOUD_URL, json=data, headers=auth_header
        )
        response.raise_for_status()
        data = response.json()

        return data.get("id")


@dataclass
class CloudSummarizationFinetuning(CloudFinetuningJob):
    dataset_id: str = None
    model_id: str = None
    model_source: str = "s3"
    task_type: str = "summarization"
    max_source_length: int = 256
    max_target_length: int = 32
    lang: str = "en"
    pad_to_max_length: bool = False
    num_beams: int = 4
    ignore_pad_token_for_loss: bool = True
    source_prefix: str = ""
    forced_bos_token: str = None
    text_column: str = "review_body"
    summary_column: str = "review_title"

    def start_job(self):
        data = {
            "dataset": self.dataset_id,
            "jobName": self.name,
            "model": self.model_id,
            "modelSource": self.model_source,
            "selectedColumns": {
                "text_column": self.text_column,
                "summary_column": self.summary_column,
            },
            "taskArguments": {
                "max_source_length": self.max_source_length,
                "max_target_length": self.max_target_length,
                "lang": self.lang,
                "pad_to_max_length": self.pad_to_max_length,
                "num_beams": self.num_beams,
                "ignore_pad_token_for_loss": self.ignore_pad_token_for_loss,
                "source_prefix": self.source_prefix,
                "forced_bos_token": self.forced_bos_token,
            },
            "taskType": self.task_type,
        }

        auth_header = AuthUtils.get_auth_headers()
        response = requests.post(
            FINETUNING_GET_JOBS_CLOUD_URL, json=data, headers=auth_header
        )
        response.raise_for_status()
        data = response.json()

        return data.get("id")


@dataclass
class CloudTranslationFinetuning(CloudFinetuningJob):
    dataset_id: str = None
    model_id: str = None
    model_source: str = "s3"
    task_type: str = "translation"
    max_source_length: int = 128
    max_target_length: int = 128
    src_lang: str = "en"
    tgt_lang: str = "es"
    pad_to_max_length: bool = False
    num_beams: int = 4
    ignore_pad_token_for_loss: bool = True
    source_prefix: str = ""
    forced_bos_token: str = None
    translation_column: str = "translation"

    def start_job(self):
        data = {
            "dataset": self.dataset_id,
            "jobName": self.name,
            "model": self.model_id,
            "modelSource": self.model_source,
            "selectedColumns": {"translation_column": self.translation_column},
            "taskArguments": {
                "max_source_length": self.max_source_length,
                "max_target_length": self.max_target_length,
                "src_lang": self.src_lang,
                "tgt_lang": self.tgt_lang,
                "pad_to_max_length": self.pad_to_max_length,
                "num_beams": self.num_beams,
                "ignore_pad_token_for_loss": self.ignore_pad_token_for_loss,
                "source_prefix": self.source_prefix,
                "forced_bos_token": self.forced_bos_token,
            },
            "taskType": self.task_type,
        }

        auth_header = AuthUtils.get_auth_headers()
        response = requests.post(
            FINETUNING_GET_JOBS_CLOUD_URL, json=data, headers=auth_header
        )
        response.raise_for_status()
        data = response.json()

        return data.get("id")


@dataclass
class CloudTextGenerationFinetuning(CloudFinetuningJob):
    dataset_id: str = None
    model_id: str = None
    model_source: str = "s3"
    task_type: str = "text_generation"
    text_column: str = "review_body"

    def start_job(self):
        data = {
            "dataset": self.dataset_id,
            "jobName": self.name,
            "model": self.model_id,
            "modelSource": self.model_source,
            "selectedColumns": {"text_column": self.text_column},
            "taskArguments": {},
            "taskType": self.task_type,
        }

        auth_header = AuthUtils.get_auth_headers()
        response = requests.post(
            FINETUNING_GET_JOBS_CLOUD_URL, json=data, headers=auth_header
        )
        response.raise_for_status()
        data = response.json()

        return data.get("id")


class CloudFinetuningClient:
    @classmethod
    def get_cloud_finetuning_jobs(cls, fmt="table"):
        auth_header = AuthUtils.get_auth_headers()
        response = requests.get(FINETUNING_GET_JOBS_CLOUD_URL, headers=auth_header)
        response.raise_for_status()

        data = response.json()
        finetuning_jobs = []

        if data.get("data") is not None:
            for job in data.get("data"):
                results = job.get("results")

                evaluation_results = []
                if results is not None and len(results) > 0:
                    for result in results:
                        er = CloudEvaluationResults(
                            model_name=result.get("modelName"),
                            evaluation_benchmark=result.get("evaluationBenchmark"),
                        )

                        evaluation_results.append(er)

                finetuning_job = CloudFinetuningJob(
                    id=job.get("id"),
                    name=job.get("name"),
                    job_status=job.get("jobStatus").get("value"),
                    created_at=job.get("createdAt"),
                    results=evaluation_results,
                )

                finetuning_jobs.append(finetuning_job)

            if fmt == "table":
                columns = []
                values = []

                if len(finetuning_jobs) > 0:
                    columns, _ = finetuning_jobs[0].to_table()

                for job in finetuning_jobs:
                    _, vals = job.to_table()
                    values.append(vals)

                return columns, values

        return finetuning_jobs

    @classmethod
    def get_cloud_finetuning_by_id(cls, id):
        auth_header = AuthUtils.get_auth_headers()
        response = requests.get(
            "{}/{}".format(FINETUNING_GET_JOBS_CLOUD_URL, id), headers=auth_header
        )
        response.raise_for_status()

        data = response.json()

        if data.get("data") is not None:
            job = data.get("data")
            results = job.get("results")

            evaluation_results = []
            if results is not None and len(results) > 0:
                for result in results:
                    er = CloudEvaluationResults(
                        model_name=result.get("modelName"),
                        evaluation_benchmark=result.get("evaluationBenchmark"),
                    )

                    evaluation_results.append(er)

            finetuning_job = CloudFinetuningJob(
                id=job.get("id"),
                name=job.get("name"),
                job_status=job.get("jobStatus").get("value"),
                created_at=job.get("createdAt"),
                results=evaluation_results,
            )

            return finetuning_job

        return None


class LocalFinetuningClient:
    @classmethod
    def get_local_finetuning_jobs(cls, fmt="table"):
        preferences = Preferences.load()
        response = requests.get(f"{preferences.local_finetuning_url}/jobs")
        response.raise_for_status()

        data = response.json()

        if fmt == "table":
            if len(data) > 0:
                columns = ["Name", "status", "Created at"]

                values = []
                for entry in data:
                    values.append(
                        [entry.get("name"), entry.get("status"), entry.get("createdAt")]
                    )

                return columns, values

            else:
                return [], []

    @classmethod
    def get_logs(cls, job_name, fmt="table"):
        preferences = Preferences.load()
        response = requests.get(
            "{}/jobs/{}/logs".format(preferences.local_finetuning_url, job_name)
        )

        try:
            response.raise_for_status()
        except:
            click.secho("\n[+] This job does not exist\n", fg="red", bold=True)

        data = response.json()

        return data.get("logs")


@dataclass
class LocalFinetuning:
    job_name: str
    model_name: str
    dataset_name: str
    num_train_epochs: int = 3
    per_device_train_batch_size: int = 16
    per_device_eval_batch_size: int = 16
    learning_rate: float = 5e-5


@dataclass
class LocalSequenceClassification(LocalFinetuning):
    task_type: str = "sequence_classification"
    max_seq_length: int = 128
    sentence1_column: str = "sentence1"
    sentence2_column: str = "sentence2"
    label_column: str = "label"

    def start_finetuning(self):

        data = asdict(self)
        preferences = Preferences.load()
        response = requests.post(f"{preferences.local_finetuning_url}/jobs", json=data)
        response.raise_for_status()
        StatController.add_information(
            LocalFinetuningJobInformation(
                job_name=self.job_name,
                inference_type=self.task_type,
                model_name=self.model_name,
                dataset_name=self.dataset_name,
                job_result=response.json(),
                params={
                    "num_train_epochs": self.num_train_epochs,
                    "per_device_train_batch_size": self.per_device_train_batch_size,
                    "per_device_eval_batch_size": self.per_device_eval_batch_size,
                    "learning_rate": self.learning_rate,
                    "max_seq_length": self.max_seq_length,
                    "sentence1_column": self.sentence1_column,
                    "sentence2_column": self.sentence2_column,
                    "label_column": self.label_column,
                },
            )
        )


@dataclass
class LocalQuestionAnswering(LocalFinetuning):
    task_type: str = "question_answering"
    max_seq_length: int = 128
    stride: int = 30
    question_column: str = "question"
    context_column: str = "context"
    answer_column: str = "answers"

    def start_finetuning(self):
        data = asdict(self)
        preferences = Preferences.load()
        response = requests.post(f"{preferences.local_finetuning_url}/jobs", json=data)
        response.raise_for_status()

        StatController.add_information(
            LocalFinetuningJobInformation(
                job_name=self.job_name,
                inference_type=self.task_type,
                model_name=self.model_name,
                dataset_name=self.dataset_name,
                job_result=response.json(),
                params={
                    "num_train_epochs": self.num_train_epochs,
                    "per_device_train_batch_size": self.per_device_train_batch_size,
                    "per_device_eval_batch_size": self.per_device_eval_batch_size,
                    "learning_rate": self.learning_rate,
                    "max_seq_length": self.max_seq_length,
                    "stride": self.stride,
                    "question_column": self.question_column,
                    "context_column": self.context_column,
                    "answer_column": self.answer_column,
                },
            )
        )


@dataclass
class LocalTokenClassification(LocalFinetuning):
    task_type: str = "token_classification"
    max_seq_length: int = 128
    label_all_tokens: bool = False
    text_column: str = "tokens"
    label_column: str = "ner_tags"

    def start_finetuning(self):
        data = asdict(self)
        preferences = Preferences.load()
        response = requests.post(f"{preferences.local_finetuning_url}/jobs", json=data)
        response.raise_for_status()

        StatController.add_information(
            LocalFinetuningJobInformation(
                job_name=self.job_name,
                inference_type=self.task_type,
                model_name=self.model_name,
                dataset_name=self.dataset_name,
                job_result=response.json(),
                params={
                    "num_train_epochs": self.num_train_epochs,
                    "per_device_train_batch_size": self.per_device_train_batch_size,
                    "per_device_eval_batch_size": self.per_device_eval_batch_size,
                    "learning_rate": self.learning_rate,
                    "max_seq_length": self.max_seq_length,
                    "label_all_tokens": self.label_all_tokens,
                    "text_column": self.text_column,
                    "label_column": self.label_column,
                },
            )
        )


@dataclass
class LocalSummarization(LocalFinetuning):
    task_type: str = "summarization"
    max_source_length: int = 256
    max_target_length: int = 32
    lang: str = "en"
    pad_to_max_length: bool = False
    num_beams: int = 4
    ignore_pad_token_for_loss: bool = True
    source_prefix: str = ""
    forced_bos_token: str = None
    text_column: str = "review_body"
    summary_column: str = "review_title"

    def start_finetuning(self):
        data = asdict(self)
        preferences = Preferences.load()
        response = requests.post(f"{preferences.local_finetuning_url}/jobs", json=data)
        response.raise_for_status()

        StatController.add_information(
            LocalFinetuningJobInformation(
                job_name=self.job_name,
                inference_type=self.task_type,
                model_name=self.model_name,
                dataset_name=self.dataset_name,
                job_result=response.json(),
                params={
                    "num_train_epochs": self.num_train_epochs,
                    "per_device_train_batch_size": self.per_device_train_batch_size,
                    "per_device_eval_batch_size": self.per_device_eval_batch_size,
                    "learning_rate": self.learning_rate,
                    "max_source_length": self.max_source_length,
                    "max_target_length": self.max_target_length,
                    "lang": self.lang,
                    "pad_to_max_length": self.pad_to_max_length,
                    "num_beams": self.num_beams,
                    "ignore_pad_token_for_loss": self.ignore_pad_token_for_loss,
                    "source_prefix": self.source_prefix,
                    "forced_bos_token": self.forced_bos_token,
                    "text_column": self.text_column,
                    "summary_column": self.summary_column,
                },
            )
        )


@dataclass
class LocalTranslation(LocalFinetuning):
    task_type: str = "translation"
    max_source_length: int = 128
    max_target_length: int = 128
    src_lang: str = "en"
    tgt_lang: str = "es"
    pad_to_max_length: bool = False
    num_beams: int = 4
    ignore_pad_token_for_loss: bool = True
    source_prefix: str = ""
    forced_bos_token: str = None
    translation_column: str = "translation"

    def start_finetuning(self):
        data = asdict(self)
        preferences = Preferences.load()
        response = requests.post(f"{preferences.local_finetuning_url}/jobs", json=data)
        response.raise_for_status()

        StatController.add_information(
            LocalFinetuningJobInformation(
                job_name=self.job_name,
                inference_type=self.task_type,
                model_name=self.model_name,
                dataset_name=self.dataset_name,
                job_result=response.json(),
                params={
                    "num_train_epochs": self.num_train_epochs,
                    "per_device_train_batch_size": self.per_device_train_batch_size,
                    "per_device_eval_batch_size": self.per_device_eval_batch_size,
                    "learning_rate": self.learning_rate,
                    "max_source_length": self.max_source_length,
                    "max_target_length": self.max_target_length,
                    "src_lang": self.src_lang,
                    "tgt_lang": self.tgt_lang,
                    "pad_to_max_length": self.pad_to_max_length,
                    "num_beams": self.num_beams,
                    "ignore_pad_token_for_loss": self.ignore_pad_token_for_loss,
                    "source_prefix": self.source_prefix,
                    "forced_bos_token": self.forced_bos_token,
                    "translation_column": self.translation_column,
                },
            )
        )


@dataclass
class LocalTextGeneration(LocalFinetuning):
    text_column: str = "review_body"

    def start_finetuning(self):
        data = asdict(self)
        preferences = Preferences.load()
        response = requests.post(f"{preferences.local_finetuning_url}/jobs", json=data)
        response.raise_for_status()

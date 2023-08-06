from stochasticx.deployment.deployments import LocalDeploymentsClient, DeploymentsClient
from stochasticx.utils.logging import configure_logger
from stochasticx.utils.preferences import Preferences, AppModes
from stochasticx.utils.stat_controller import (
    StatController,
    LocalInferenceJobInformation,
)

import requests

logger = configure_logger(__name__)


class InferenceStatus:
    ALIVE = "alive"
    READY = "ready"
    DOWN = "down"


class InferenceModel:
    def __init__(self, deployment_id):
        self.deployment_id = deployment_id

        preferences = Preferences.load()

        if preferences.current_mode == AppModes.LOCAL:
            self.deployment = LocalDeploymentsClient.get_deployment_by_id(
                self.deployment_id
            )
        else:
            self.deployment = DeploymentsClient.get_deployment_by_id(
                self.deployment_id
            )

    def inference(self, *args, **kwargs):
        return """
    URL: {}
    API Key: {}
""".format(self.deployment.client_url, self.deployment.api_key)


class SequenceClassificationModel(InferenceModel):
    def __init__(self, deployment_id):
        super().__init__(deployment_id)

    def format_inputs_local(self, texts):
        return {
            "inputs": [
                {"name": "text", "datatype": "BYTES", "shape": [1], "data": texts}
            ]
        }

    def format_inputs(self, texts):
        return {
            "inputs": [
                {
                    "name": "text",
                    "datatype": "BYTES",
                    "shape": [1, len(texts)],
                    "data": texts,
                }
            ]
        }

    def format_output(self, outputs):
        outputs = outputs.get("outputs")
        if outputs is not None and isinstance(outputs, list):
            labels, scores = outputs[0], outputs[1]
            return labels.get("data"), scores.get("data")

    def local_inference(self, texts):
        model_inputs = self.format_inputs_local(texts)

        preferences = Preferences.load()
        endpoint_url = "{}/v2/models/{}_{}/versions/1/infer".format(
            preferences.local_inference_url,
            self.deployment.model_name,
            self.deployment.type,
        )

        r = requests.post(endpoint_url, json=model_inputs)
        r.raise_for_status()

        StatController.add_local_inference_job(
            LocalInferenceJobInformation(
                inference_type="sequence_classification",
                model_name=self.deployment.model_name,
                model_type=self.deployment.type,
                job_result=r.json(),
            )
        )

        outputs = r.json()
        labels, scores = self.format_output(outputs)

        return labels, scores


class QuestionAnsweringModel(InferenceModel):
    def __init__(self, deployment_id):
        super().__init__(deployment_id)

    def format_inputs_local(self, questions, contexts):
        return {
            "inputs": [
                {
                    "name": "question",
                    "datatype": "BYTES",
                    "shape": [1],
                    "data": questions,
                },
                {"name": "text", "datatype": "BYTES", "shape": [1], "data": contexts},
            ]
        }

    def format_inputs(self, questions, contexts):
        return {
            "inputs": [
                {
                    "name": "question",
                    "datatype": "BYTES",
                    "shape": [1, len(questions)],
                    "data": questions,
                },
                {
                    "name": "text",
                    "datatype": "BYTES",
                    "shape": [1, len(contexts)],
                    "data": contexts,
                },
            ]
        }

    def format_output(self, outputs):
        outputs = outputs.get("outputs")
        if outputs is not None and isinstance(outputs, list):
            answers = outputs[0]
            return answers.get("data")

    def local_inference(self, questions, contexts):
        model_inputs = self.format_inputs_local(questions, contexts)

        preferences = Preferences.load()
        endpoint_url = "{}/v2/models/{}_{}/versions/1/infer".format(
            preferences.local_inference_url,
            self.deployment.model_name,
            self.deployment.type,
        )

        r = requests.post(endpoint_url, json=model_inputs)
        r.raise_for_status()

        StatController.add_information(
            LocalInferenceJobInformation(
                inference_type="question_answering",
                model_name=self.deployment.model_name,
                model_type=self.deployment.type,
                job_result=r.json(),
            )
        )

        outputs = r.json()
        answers = self.format_output(outputs)

        return answers


class SummarizationModel(InferenceModel):
    def __init__(self, deployment_id):
        super().__init__(deployment_id)

    def format_inputs(self, texts, min_lengths, max_lengths):
        return {
            "inputs": [
                {
                    "name": "text",
                    "datatype": "BYTES",
                    "shape": [1, len(texts)],
                    "data": texts,
                },
                {
                    "name": "min_length",
                    "datatype": "INT32",
                    "shape": [1, len(min_lengths)],
                    "data": min_lengths,
                },
                {
                    "name": "max_length",
                    "datatype": "INT32",
                    "shape": [1, len(max_lengths)],
                    "data": max_lengths,
                },
            ]
        }

    def format_inputs_local(self, texts, min_lengths, max_lengths):
        return {
            "inputs": [
                {"name": "text", "datatype": "BYTES", "shape": [1], "data": texts},
                {
                    "name": "min_length",
                    "datatype": "INT32",
                    "shape": [1],
                    "data": min_lengths,
                },
                {
                    "name": "max_length",
                    "datatype": "INT32",
                    "shape": [1],
                    "data": max_lengths,
                },
            ]
        }

    def format_output(self, outputs):
        outputs = outputs.get("outputs")
        if outputs is not None and isinstance(outputs, list):
            summaries = outputs[0]
            return summaries.get("data")

    def local_inference(self, texts, min_lengths, max_lengths):
        model_inputs = self.format_inputs_local(texts, min_lengths, max_lengths)

        preferences = Preferences.load()
        endpoint_url = "{}/v2/models/{}_{}/versions/1/infer".format(
            preferences.local_inference_url,
            self.deployment.model_name,
            self.deployment.type,
        )

        r = requests.post(endpoint_url, json=model_inputs)
        r.raise_for_status()

        StatController.add_information(
            LocalInferenceJobInformation(
                inference_type="summarization",
                model_name=self.deployment.model_name,
                model_type=self.deployment.type,
                job_result=r.json(),
            )
        )

        outputs = r.json()
        summaries = self.format_output(outputs)

        return summaries


class TranslationModel(InferenceModel):
    def __init__(self, deployment_id):
        super().__init__(deployment_id)

    def format_inputs(self, texts, max_lengths):
        return {
            "inputs": [
                {
                    "name": "text",
                    "datatype": "BYTES",
                    "shape": [1, len(texts)],
                    "data": texts,
                },
                {
                    "name": "max_length",
                    "datatype": "INT32",
                    "shape": [1, len(max_lengths)],
                    "data": max_lengths,
                },
            ]
        }

    def format_inputs_local(self, texts, max_lengths):
        return {
            "inputs": [
                {"name": "text", "datatype": "BYTES", "shape": [1], "data": texts},
                {
                    "name": "max_length",
                    "datatype": "INT32",
                    "shape": [1],
                    "data": max_lengths,
                },
            ]
        }

    def format_output(self, outputs):
        outputs = outputs.get("outputs")
        if outputs is not None and isinstance(outputs, list):
            translations = outputs[0]
            return translations.get("data")

    def local_inference(self, texts, max_lengths):
        model_inputs = self.format_inputs_local(texts, max_lengths)

        preferences = Preferences.load()
        endpoint_url = "{}/v2/models/{}_{}/versions/1/infer".format(
            preferences.local_inference_url,
            self.deployment.model_name,
            self.deployment.type,
        )

        r = requests.post(endpoint_url, json=model_inputs)
        r.raise_for_status()

        StatController.add_information(
            LocalInferenceJobInformation(
                inference_type="translation",
                model_name=self.deployment.model_name,
                model_type=self.deployment.type,
                job_result=r.json(),
            )
        )

        outputs = r.json()
        translations = self.format_output(outputs)

        return translations


class TokenClassificationModel(InferenceModel):
    def __init__(self, deployment_id):
        super().__init__(deployment_id)

    def format_inputs(self, texts):
        return {
            "inputs": [
                {
                    "name": "text",
                    "datatype": "BYTES",
                    "shape": [1, len(texts)],
                    "data": texts,
                }
            ]
        }

    def format_inputs_local(self, texts):
        return {
            "inputs": [
                {"name": "text", "datatype": "BYTES", "shape": [1], "data": texts}
            ]
        }

    def format_output(self, outputs):
        outputs = outputs.get("outputs")
        if outputs is not None and isinstance(outputs, list):
            tokens, tags, scores = outputs[0], outputs[1], outputs[2]
            return tokens.get("data"), tags.get("data"), scores.get("data")

    def local_inference(self, texts):
        model_inputs = self.format_inputs_local(texts)

        preferences = Preferences.load()
        endpoint_url = "{}/v2/models/{}_{}/versions/1/infer".format(
            preferences.local_inference_url,
            self.deployment.model_name,
            self.deployment.type,
        )

        r = requests.post(endpoint_url, json=model_inputs)
        r.raise_for_status()

        StatController.add_information(
            LocalInferenceJobInformation(
                inference_type="token_classification",
                model_name=self.deployment.model_name,
                model_type=self.deployment.type,
                job_result=r.json(),
            )
        )

        outputs = r.json()

        return self.format_output(outputs)

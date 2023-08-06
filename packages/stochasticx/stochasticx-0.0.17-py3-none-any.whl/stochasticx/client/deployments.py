from pathlib import Path
import time
import click

from stochasticx.deployment.deployments import (
    Deployment,
    DeploymentsClient,
    Instances
)

from stochasticx.models.models import Models
from stochasticx.utils.parse_utils import print_table
from stochasticx.utils.preferences import Preferences, AppModes
from stochasticx.utils.docker import (
    start_container,
    exists_running_container,
    stop_and_remove_container,
    get_logs_container,
    get_open_ports_container,
    exists_container,
    auto_port_selection,
    wait_container_is_up,
)
from stochasticx.utils.gpu_utils import is_nvidia_gpu_available
from stochasticx.deployment.deployments import (
    LocalDeploymentsClient,
    LocalSequenceClassificationDeployment,
    LocalQuestionAnsweringDeployment,
    LocalTokenClassificationDeployment,
    LocalTranslationDeployment,
    LocalSummarizationDeployment,
    LocalTextGenerationDeployment,
)
from stochasticx.constants.docker_images import DockerImages, ContainerNames
from stochasticx.utils.auth_utils import AuthUtils
import sys

from stochasticx.utils.stat_controller import EventLogger


@click.group(name="deployments")
@click.option(
    "--port",
    default=9000,
    help="Port which Stochastic local inference container will run on",
)
def deployments(port):
    try:
        AuthUtils.get_auth_headers()
    except:
        sys.exit()

    preferences = Preferences.load()

    if (
        preferences.current_mode == AppModes.LOCAL and
        not exists_running_container(ContainerNames.INFERENCE)
    ):
        click.secho(
            "\n[+] We are configuring the environment for inference. If it is the first time, it will take some minutes\n",
            fg="yellow",
            bold=True,
        )

        original_port = port
        port, is_replace = auto_port_selection(port, ContainerNames.INFERENCE)
        if is_replace:
            click.secho(
                f"[+] Port {original_port} is using on another service, port {port} will be selected to run stochasticx model inference",
                fg="blue",
                bold=True,
            )

        port2, _ = auto_port_selection(
            5051, ContainerNames.INFERENCE, selected_ports=[port]
        )
        port3, _ = auto_port_selection(
            9001, ContainerNames.INFERENCE, selected_ports=[port, port2]
        )
        port4, _ = auto_port_selection(
            9002, ContainerNames.INFERENCE, selected_ports=[port, port2, port3]
        )

        start_container(
            docker_image=DockerImages.INFERENCE,
            ports={"5000": port2, "8000": port, "8001": port3, "8002": port4},
            container_name=ContainerNames.INFERENCE,
            detach=True,
            gpu=is_nvidia_gpu_available(),
            network_links={"x-local": "x-local"},
            volumes_from=["x-local"],
        )

        click.echo("[+] Setting up preferences...")
        preferences = Preferences.load()
        preferences.current_mode = AppModes.LOCAL
        preferences.local_inference_url = f"http://127.0.0.1:{port}"
        preferences.local_deployment_url = f"http://127.0.0.1:{port2}"
        Preferences.save(preferences)

        local_url = f"{preferences.local_deployment_url}/model"

        wait_container_is_up(local_url)

        click.secho(
            f"[+] x-local-inference server running in the port {port}",
            fg="green",
            bold=True,
        )
        EventLogger.log_event("deployments_local")


@click.command(name="ls")
def ls_deployments():
    preferences = Preferences.load()

    click.secho("\n[+] Collecting all deployments\n", fg="blue", bold=True)
    if preferences.current_mode == AppModes.LOCAL:
        columns, values = LocalDeploymentsClient.get_deployments()
        EventLogger.log_event("deployments_local_ls")
    else:
        columns, values = DeploymentsClient.get_deployments(fmt="table")
        EventLogger.log_event("deployments_cloud_ls")
    print_table(columns, values)
    
    click.secho("\n[+] Client URL or API key will be available once the deployment is running. Execute the following command to get them: stochasticx inference inspect --deployment_name deployment_name\n", fg="yellow", bold=True)


@click.group(name="deploy")
def deploy():
    pass


@click.command(name="launch") 
@click.option('--name', required=True, help='Deployment name')
@click.option('--instance_type', required=True, help='Instance type')
@click.option('--model_name', required=True, default="hf", show_default=True, help='Model ID')
@click.option('--model_type', required=False, help='Model type')
@click.option('--sub_type', required=False, help='Task or submodel type')
@click.option('--inference_file_path', required=False, help='Inference file path')
@click.option('--docker_image', required=False, help='Custom Docker image')
@click.option('--docker_registry_username', required=False, help='Docker registry username to download the Docker image')
@click.option('--docker_registry_password', required=False, help='Docker registry password to download the Docker image')
def launch_deployment(name, instance_type, model_name, model_type, sub_type, inference_file_path, docker_image, docker_registry_username, docker_registry_password):
    preferences = Preferences.load()
    click.secho("\n[+] Creating deployment...", fg='blue', bold=True)
    
    if preferences.current_mode == AppModes.LOCAL:
        click.secho("\n[+] Command not available in the local version", fg='red', bold=True)
        EventLogger.log_event("deployments_local_launch")
    else:
        DeploymentsClient.create_deployment(
            name=name,
            instance_type=instance_type,
            model_name=model_name,
            model_type=model_type,
            task_type=sub_type,
            inference_file_path=inference_file_path,
            docker_image=docker_image,
            docker_registry_username=docker_registry_username,
            docker_registry_password=docker_registry_password
        )
        EventLogger.log_event("deployments_cloud_launch")

    click.secho("\n[+] Deployed", fg='green', bold=True)

@click.command(name="delete") 
@click.option('--name', required=True, help='Deployment ID')
@click.option('--model_name_or_id', required=False, help='Model ID')
@click.option('--model_type', required=False, default="hf", show_default=True, help='Model ID')
def delete_deployment(name, model_name_or_id, model_type):
    preferences = Preferences.load()

    click.secho("\n[+] Deleting deployment...", fg="blue", bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        LocalDeploymentsClient.delete_deployment(
            model_type=model_type, model_name=model_name_or_id
        )
        EventLogger.log_event("deployments_local_delete")
    else:
        DeploymentsClient.terminate_deployment(name)
        EventLogger.log_event("deployments_cloud_delete")

    click.secho("[+] Deleted\n", fg="green", bold=True)


@click.command(name="sequence_classification")
@click.option("--model_name_or_id", required=True, help="Model ID")
@click.option(
    "--model_type", required=False, default="hf", show_default=True, help="Model ID"
)
@click.option("--instance_type", required=False, default=None, help="Instance type")
@click.option(
    "--max_batch_size",
    required=False,
    default=8,
    show_default=True,
    help="Maximum batch size",
)
@click.option(
    "--max_seq_length",
    required=False,
    default=128,
    show_default=True,
    help="Maximum source length",
)
def sequence_classification(
    model_name_or_id, model_type, instance_type, max_batch_size, max_seq_length
):
    preferences = Preferences.load()

    click.secho("\n[+] Starting deployment...", fg="blue", bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        LocalSequenceClassificationDeployment(
            model_name=model_name_or_id,
            type=model_type,
            cuda=is_nvidia_gpu_available(),
            user_params={
                "max_batch_size": max_batch_size,
                "max_seq_length": max_seq_length,
            },
        ).start_deployment()
        EventLogger.log_event("deployments_local_sequence_classification")
    else:
        click.secho("\n[+] Command not available in the cloud version", fg='red', bold=True)
        EventLogger.log_event("deployments_cloud_sequence_classification")

    click.secho("[+] Model deployed\n", fg="green", bold=True)


@click.command(name="question_answering")
@click.option("--model_name_or_id", required=True, help="Model ID")
@click.option(
    "--model_type", required=False, default="hf", show_default=True, help="Model ID"
)
@click.option("--instance_type", required=False, default=None, help="Instance type")
@click.option(
    "--max_batch_size", default=8, show_default=True, help="Maximum batch size"
)
@click.option(
    "--max_seq_length", default=128, show_default=True, help="Maximum sequence length"
)
def question_answering(
    model_name_or_id, model_type, instance_type, max_batch_size, max_seq_length
):
    preferences = Preferences.load()

    click.secho("\n[+] Starting deployment...", fg="blue", bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        LocalQuestionAnsweringDeployment(
            model_name=model_name_or_id,
            type=model_type,
            cuda=is_nvidia_gpu_available(),
            user_params={
                "max_batch_size": max_batch_size,
                "max_seq_length": max_seq_length,
            },
        ).start_deployment()
        EventLogger.log_event("deployments_local_question_answering")
    else:
        click.secho("\n[+] Command not available in the cloud version", fg='red', bold=True)
        EventLogger.log_event("deployments_cloud_question_answering")

    click.secho("[+] Model deployed\n", fg="green", bold=True)


@click.command(name="summarization")
@click.option("--model_name_or_id", required=True, help="Model ID")
@click.option(
    "--model_type", required=False, default="hf", show_default=True, help="Model ID"
)
@click.option("--instance_type", required=False, default=None, help="Instance type")
@click.option(
    "--max_batch_size", default=8, show_default=True, help="Maximum batch size"
)
@click.option(
    "--max_source_length", default=128, show_default=True, help="Maximum source length"
)
@click.option("--source_prefix", default="", show_default=True, help="Source prefix")
@click.option("--lang", default="en", show_default=True, help="Language")
def summarization(
    model_name_or_id,
    model_type,
    instance_type,
    max_batch_size,
    max_source_length,
    source_prefix,
    lang,
):
    preferences = Preferences.load()

    click.secho("\n[+] Starting deployment...", fg="blue", bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        LocalSummarizationDeployment(
            model_name=model_name_or_id,
            type=model_type,
            cuda=is_nvidia_gpu_available(),
            user_params={
                "max_batch_size": max_batch_size,
                "max_source_length": max_source_length,
                "lang": lang,
                "source_prefix": source_prefix,
            },
        ).start_deployment()
        EventLogger.log_event("deployments_local_summarization")
    else:
        click.secho("\n[+] Command not available in the cloud version", fg='red', bold=True)
        EventLogger.log_event("deployments_cloud_summarization")

    click.secho("[+] Model deployed\n", fg="green", bold=True)


@click.command(name="translation")
@click.option("--model_name_or_id", required=True, help="Model ID")
@click.option(
    "--model_type", required=False, default="hf", show_default=True, help="Model ID"
)
@click.option("--instance_type", required=False, default=None, help="Instance type")
@click.option(
    "--max_batch_size", default=8, show_default=True, help="Maximum batch size"
)
@click.option(
    "--max_source_length", default=128, show_default=True, help="Maximum source length"
)
@click.option("--source_prefix", default="", show_default=True, help="Source prefix")
@click.option("--src_lang", default="en", show_default=True, help="Source language")
@click.option("--tgt_lang", default="de", show_default=True, help="Target language")
def translation(
    model_name_or_id,
    model_type,
    instance_type,
    max_batch_size,
    max_source_length,
    source_prefix,
    src_lang,
    tgt_lang,
):
    preferences = Preferences.load()

    click.secho("\n[+] Starting deployment...", fg="blue", bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        LocalTranslationDeployment(
            model_name=model_name_or_id,
            type=model_type,
            cuda=is_nvidia_gpu_available(),
            user_params={
                "max_batch_size": max_batch_size,
                "max_source_length": max_source_length,
                "src_lang": src_lang,
                "tgt_lang": tgt_lang,
                "source_prefix": source_prefix,
            },
        ).start_deployment()
        EventLogger.log_event("deployments_local_translation")
    else:
        click.secho("\n[+] Command not available in the cloud version", fg='red', bold=True)
        EventLogger.log_event("deployments_cloud_translation")

    click.secho("[+] Model deployed\n", fg="green", bold=True)


@click.command(name="token_classification")
@click.option("--model_name_or_id", required=True, help="Model ID")
@click.option(
    "--model_type", required=False, default="hf", show_default=True, help="Model ID"
)
@click.option("--instance_type", required=False, default=None, help="Instance type")
@click.option(
    "--max_batch_size", default=8, show_default=True, help="Maximum batch size"
)
@click.option(
    "--max_seq_length", default=128, show_default=True, help="Maximum source length"
)
def token_classification(
    model_name_or_id, model_type, instance_type, max_batch_size, max_seq_length
):
    preferences = Preferences.load()

    click.secho("\n[+] Starting deployment...", fg="blue", bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        LocalTokenClassificationDeployment(
            model_name=model_name_or_id,
            type=model_type,
            cuda=is_nvidia_gpu_available(),
            user_params={
                "max_batch_size": max_batch_size,
                "max_seq_length": max_seq_length,
            },
        ).start_deployment()
        EventLogger.log_event("deployments_local_token_classification")
    else: 
        click.secho("\n[+] Command not available in the cloud version", fg='red', bold=True)
        EventLogger.log_event("deployments_cloud_token_classification")

    click.secho("[+] Model deployed\n", fg="green", bold=True)


@click.group(name="instances")
def instances():
    pass


@click.command(name="ls")
def ls_instances():
    click.secho("\n[+] Collecting all instances\n", fg="blue", bold=True)
    columns, values = Instances.get_instance_types(fmt="table")
    print_table(columns, values)
    EventLogger.log_event("deployments_ls_instances")


deploy.add_command(sequence_classification)
deploy.add_command(question_answering)
deploy.add_command(token_classification)
deploy.add_command(summarization)
deploy.add_command(translation)

deployments.add_command(ls_deployments)
deployments.add_command(launch_deployment)
deployments.add_command(delete_deployment)

instances.add_command(ls_instances)

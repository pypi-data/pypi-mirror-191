import time
import click

from stochasticx.finetuning.finetuning import (
    LocalFinetuningClient,
    CloudFinetuningClient,
    LocalQuestionAnswering,
    LocalSequenceClassification,
    CloudSequenceClassificationFinetuning,
    LocalSummarization,
    LocalTextGeneration,
    LocalTokenClassification,
    LocalTranslation,
    LocalQuestionAnswering,
    LocalSummarization,
    LocalTranslation,
    LocalTextGeneration,
)
from stochasticx.utils.parse_utils import print_table
from stochasticx.utils.docker import (
    start_container,
    stop_and_remove_container,
    get_logs_container,
    get_open_ports_container,
    exists_container,
    exists_running_container,
    auto_port_selection,
    wait_container_is_up,
)
from stochasticx.utils.gpu_utils import is_nvidia_gpu_available
from stochasticx.utils.preferences import Preferences, AppModes
from stochasticx.constants.docker_images import DockerImages, ContainerNames
from stochasticx.utils.auth_utils import AuthUtils
import sys
import requests

from stochasticx.utils.stat_controller import EventLogger


@click.group(name="finetuning")
@click.option(
    "--port",
    default=5050,
    help="Port which Stochastic local finetuning container will run on",
)
def finetuning_jobs(port):
    try:
        AuthUtils.get_auth_headers()
    except:
        sys.exit()

    preferences = Preferences.load()

    if (
        not exists_running_container("x-finetuning")
        and preferences.current_mode == AppModes.LOCAL
    ):
        click.secho(
            "\n[+] We are configuring the environment for finetuning. If it is the first time, it will take some minutes\n",
            fg="yellow",
            bold=True,
        )

        original_port = port
        port, is_replace = auto_port_selection(port, ContainerNames.FINETUNE)
        if is_replace:
            click.secho(
                f"[+] Port {original_port} is using on another service, port {port} will be selected to run stochasticx model finetuning",
                fg="blue",
                bold=True,
            )

        start_container(
            docker_image=DockerImages.FINETUNE,
            ports={"5000": str(port)},
            container_name=ContainerNames.FINETUNE,
            detach=True,
            gpu=is_nvidia_gpu_available(),
            volumes=["stochasticx:/vol"],
            network_links={"x-local": "x-local"},
        )

        click.secho("[+] Environment already configured\n", fg="green", bold=True)
        click.echo("[+] Setting up preferences...")
        preferences = Preferences.load()
        preferences.current_mode = AppModes.LOCAL
        preferences.local_finetuning_url = f"http://127.0.0.1:{port}"
        Preferences.save(preferences)

        wait_container_is_up(f"{preferences.local_finetuning_url}/jobs")

        click.secho(
            f"[+] x-local-finetuning server running in the port {port}",
            fg="green",
            bold=True,
        )
        EventLogger.log_event("finetuning_local")


@click.command(name="ls")
def ls_finetuning_jobs():
    preferences = Preferences.load()

    click.secho("\n[+] Collecting all jobs\n", fg="blue", bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        columns, values = LocalFinetuningClient.get_local_finetuning_jobs(fmt="table")
        EventLogger.log_event("finetuning_local_ls")
    else:
        columns, values = CloudFinetuningClient.get_cloud_finetuning_jobs(fmt="table")
        EventLogger.log_event("finetuning_cloud_ls")

    print_table(columns, values)


@click.command(name="inspect")
@click.option("--id", required=True, help="Finetuning job ID or job name")
def inspect_finetuning_jobs(id):
    preferences = Preferences.load()

    click.secho("\n[+] Inspecting the specified job\n", fg="blue", bold=True)

    if preferences.current_mode == AppModes.LOCAL:
        # click.secho("\n[+] This command is not support for local mode\n", fg='red', bold=True)
        preferences = Preferences.load()
        response = requests.get(f"{preferences.local_finetuning_url}/jobs/{id}").json()
        if response["status"] == "running":
            click.secho("\n[+] Job is still running\n", fg="green", bold=True)
        elif response["status"] == "successful":
            logs = LocalFinetuningClient.get_logs(id)
            click.secho(
                f"\n[+] Job is successful, here is the logs:\n{logs}",
                fg="green",
                bold=True,
            )
        elif response["status"] == "failed":
            logs = LocalFinetuningClient.get_logs(id)
            click.secho(f"\n[-] Job is failed\n", fg="red", bold=True)
        EventLogger.log_event("finetuning_local_inspect")
    else:
        job = CloudFinetuningClient.get_cloud_finetuning_by_id(id)
        click.secho(str(job), fg="white", bold=True)
        EventLogger.log_event("finetuning_cloud_inspect")


@click.command(name="logs")
@click.option("--name", required=True, help="Job name")
def logs_finetuning_job(name):
    click.secho("\n[+] Collecting logs\n", fg="blue", bold=True)
    logs = LocalFinetuningClient.get_logs(name)
    click.secho(logs, fg="white", bold=True)
    EventLogger.log_event("finetuning_logs")


@click.group(name="launch")
def job_launch():
    pass


@click.command(name="sequence_classification")
@click.option("--name", required=True, help="Job name")
@click.option("--model_name_or_id", required=True, help="Model ID")
@click.option("--dataset_name_or_id", required=True, help="Dataset ID")
@click.option("--sentence1_column", required=True, help="Sentence 1")
@click.option("--sentence2_column", required=True, help="Sentence 2")
@click.option("--label_column", required=True, help="Label")
@click.option(
    "--max_seq_length", required=False, default=128, help="Maximum sequence length"
)
@click.option(
    "--num_train_epochs",
    required=False,
    default=3,
    show_default=True,
    help="Number of training epochs",
)
@click.option(
    "--per_device_train_batch_size",
    required=False,
    default=16,
    show_default=True,
    help="Train batch size",
)
@click.option(
    "--learning_rate",
    required=False,
    default=5e-5,
    show_default=True,
    help="Learning rate",
)
def job_launch_sequence_classification(
    name,
    model_name_or_id,
    dataset_name_or_id,
    sentence1_column,
    sentence2_column,
    label_column,
    max_seq_length,
    num_train_epochs,
    per_device_train_batch_size,
    learning_rate,
):
    preferences = Preferences.load()

    if preferences.current_mode == AppModes.LOCAL:
        local_finetuning = LocalSequenceClassification(
            job_name=name,
            model_name=model_name_or_id,
            dataset_name=dataset_name_or_id,
            sentence1_column=sentence1_column,
            sentence2_column=sentence2_column,
            label_column=label_column,
            max_seq_length=max_seq_length,
            num_train_epochs=num_train_epochs,
            per_device_eval_batch_size=per_device_train_batch_size,
            learning_rate=learning_rate,
        )

        click.secho("\n[+] Launching finetuning job\n", fg="blue", bold=True)
        local_finetuning.start_finetuning()
        EventLogger.log_event("finetuning_local_sequence_classification")
    else:
        cloud_finetuning = CloudSequenceClassificationFinetuning(
            id=None,
            name=name,
            dataset_id=dataset_name_or_id,
            model_id=model_name_or_id,
            sentence1_column=sentence1_column,
            sentence2_column=sentence2_column,
            label_column=label_column,
            max_seq_length=max_seq_length,
        )

        click.secho("\n[+] Launching finetuning job\n", fg="blue", bold=True)
        cloud_finetuning.start_job()
        EventLogger.log_event("finetuning_cloud_sequence_classification")


@click.command(name="question_answering")
@click.option("--name", required=True, help="Job name")
@click.option("--model_name_or_id", required=True, help="Model ID")
@click.option("--dataset_name_or_id", required=True, help="Dataset ID")
@click.option("--question_column", required=True, help="Question column")
@click.option("--context_column", required=True, help="Context column")
@click.option("--answer_column", required=True, help="Answer column")
@click.option(
    "--max_seq_length", required=False, default=128, help="Maximum sequence length"
)
@click.option("--stride", required=False, default=30, help="Stride")
@click.option(
    "--num_train_epochs",
    required=False,
    default=3,
    show_default=True,
    help="Number of training epochs",
)
@click.option(
    "--per_device_train_batch_size",
    required=False,
    default=16,
    show_default=True,
    help="Train batch size",
)
@click.option(
    "--learning_rate",
    required=False,
    default=5e-5,
    show_default=True,
    help="Learning rate",
)
def job_launch_question_answering(
    name,
    model_name_or_id,
    dataset_name_or_id,
    question_column,
    context_column,
    answer_column,
    max_seq_length,
    stride,
    num_train_epochs,
    per_device_train_batch_size,
    learning_rate,
):
    preferences = Preferences.load()

    if preferences.current_mode == AppModes.LOCAL:
        local_finetuning = LocalQuestionAnswering(
            job_name=name,
            model_name=model_name_or_id,
            dataset_name=dataset_name_or_id,
            question_column=question_column,
            context_column=context_column,
            answer_column=answer_column,
            max_seq_length=max_seq_length,
            stride=stride,
            num_train_epochs=num_train_epochs,
            per_device_eval_batch_size=per_device_train_batch_size,
            learning_rate=learning_rate,
        )

        click.secho("\n[+] Launching finetuning job\n", fg="blue", bold=True)
        local_finetuning.start_finetuning()
        EventLogger.log_event("finetuning_local_question_answering")


@click.command(name="token_classification")
@click.option("--name", required=True, help="Job name")
@click.option("--model_name_or_id", required=True, help="Model ID")
@click.option("--dataset_name_or_id", required=True, help="Dataset ID")
@click.option("--text_column", required=True, help="Text column")
@click.option("--label_column", required=True, help="Label column")
@click.option(
    "--max_seq_length", required=False, default=128, help="Maximum sequence length"
)
@click.option(
    "--label_all_tokens", required=False, default=False, help="Label all tokens"
)
@click.option(
    "--num_train_epochs",
    required=False,
    default=3,
    show_default=True,
    help="Number of training epochs",
)
@click.option(
    "--per_device_train_batch_size",
    required=False,
    default=16,
    show_default=True,
    help="Train batch size",
)
@click.option(
    "--learning_rate",
    required=False,
    default=5e-5,
    show_default=True,
    help="Learning rate",
)
def job_launch_token_classification(
    name,
    model_name_or_id,
    dataset_name_or_id,
    text_column,
    label_column,
    max_seq_length,
    label_all_tokens,
    num_train_epochs,
    per_device_train_batch_size,
    learning_rate,
):
    preferences = Preferences.load()

    if preferences.current_mode == AppModes.LOCAL:
        local_finetuning = LocalTokenClassification(
            job_name=name,
            model_name=model_name_or_id,
            dataset_name=dataset_name_or_id,
            text_column=text_column,
            label_column=label_column,
            max_seq_length=max_seq_length,
            label_all_tokens=label_all_tokens,
            num_train_epochs=num_train_epochs,
            per_device_eval_batch_size=per_device_train_batch_size,
            learning_rate=learning_rate,
        )

        click.secho("\n[+] Launching finetuning job\n", fg="blue", bold=True)
        local_finetuning.start_finetuning()
        EventLogger.log_event("finetuning_local_token_classification")


@click.command(name="summarization")
@click.option("--name", required=True, help="Job name")
@click.option("--model_name_or_id", required=True, help="Model ID")
@click.option("--dataset_name_or_id", required=True, help="Dataset ID")
@click.option("--text_column", required=True, help="Text column")
@click.option("--summary_column", required=True, help="Summary column")
@click.option(
    "--max_source_length",
    required=False,
    default=256,
    help="Maximum source sequence length",
)
@click.option(
    "--max_target_length",
    required=False,
    default=32,
    help="Maximum target sequence length",
)
@click.option("--lang", required=False, default="en", help="Language")
@click.option(
    "--pad_to_max_length", required=False, default=False, help="Pad to max length"
)
@click.option("--num_beams", required=False, default=4, help="Number of beams")
@click.option(
    "--ignore_pad_token_for_loss",
    required=False,
    default=True,
    help="Ignore pad token for loss",
)
@click.option("--source_prefix", required=False, default="", help="Source prefix")
@click.option(
    "--forced_bos_token", required=False, default=None, help="Forced BOS token"
)
@click.option(
    "--num_train_epochs",
    required=False,
    default=3,
    show_default=True,
    help="Number of training epochs",
)
@click.option(
    "--per_device_train_batch_size",
    required=False,
    default=16,
    show_default=True,
    help="Train batch size",
)
@click.option(
    "--learning_rate",
    required=False,
    default=5e-5,
    show_default=True,
    help="Learning rate",
)
def job_launch_summarization(
    name,
    model_name_or_id,
    dataset_name_or_id,
    text_column,
    summary_column,
    max_source_length,
    max_target_length,
    lang,
    pad_to_max_length,
    num_beams,
    ignore_pad_token_for_loss,
    source_prefix,
    forced_bos_token,
    num_train_epochs,
    per_device_train_batch_size,
    learning_rate,
):
    preferences = Preferences.load()

    if preferences.current_mode == AppModes.LOCAL:
        local_finetuning = LocalSummarization(
            job_name=name,
            model_name=model_name_or_id,
            dataset_name=dataset_name_or_id,
            text_column=text_column,
            max_source_length=max_source_length,
            max_target_length=max_target_length,
            lang=lang,
            pad_to_max_length=pad_to_max_length,
            num_beams=num_beams,
            ignore_pad_token_for_loss=ignore_pad_token_for_loss,
            source_prefix=source_prefix,
            forced_bos_token=forced_bos_token,
            num_train_epochs=num_train_epochs,
            per_device_eval_batch_size=per_device_train_batch_size,
            learning_rate=learning_rate,
        )

        click.secho("\n[+] Launching finetuning job\n", fg="blue", bold=True)
        local_finetuning.start_finetuning()
        EventLogger.log_event("finetuning_local_token_summarization")


@click.command(name="translation")
@click.option("--name", required=True, help="Job name")
@click.option("--model_name_or_id", required=True, help="Model ID")
@click.option("--dataset_name_or_id", required=True, help="Dataset ID")
@click.option("--translation_column", required=True, help="Translation column")
@click.option(
    "--max_source_length",
    required=False,
    default=128,
    help="Maximum source sequence length",
)
@click.option(
    "--max_target_length",
    required=False,
    default=128,
    help="Maximum target sequence length",
)
@click.option("--src_lang", required=False, default="en", help="Source language")
@click.option("--tgt_lang", required=False, default="es", help="Target language")
@click.option(
    "--pad_to_max_length", required=False, default=False, help="Pad to max length"
)
@click.option("--num_beams", required=False, default=4, help="Number of beams")
@click.option(
    "--ignore_pad_token_for_loss",
    required=False,
    default=True,
    help="Ignore pad token for loss",
)
@click.option("--source_prefix", required=False, default="", help="Source prefix")
@click.option(
    "--forced_bos_token", required=False, default=None, help="Forced BOS token"
)
@click.option(
    "--num_train_epochs",
    required=False,
    default=3,
    show_default=True,
    help="Number of training epochs",
)
@click.option(
    "--per_device_train_batch_size",
    required=False,
    default=16,
    show_default=True,
    help="Train batch size",
)
@click.option(
    "--learning_rate",
    required=False,
    default=5e-5,
    show_default=True,
    help="Learning rate",
)
def job_launch_translation(
    name,
    model_name_or_id,
    dataset_name_or_id,
    translation_column,
    max_source_length,
    max_target_length,
    src_lang,
    tgt_lang,
    pad_to_max_length,
    num_beams,
    ignore_pad_token_for_loss,
    source_prefix,
    forced_bos_token,
    num_train_epochs,
    per_device_train_batch_size,
    learning_rate,
):
    preferences = Preferences.load()

    if preferences.current_mode == AppModes.LOCAL:
        local_finetuning = LocalTranslation(
            job_name=name,
            model_name=model_name_or_id,
            dataset_name=dataset_name_or_id,
            text_column=translation_column,
            max_source_length=max_source_length,
            max_target_length=max_target_length,
            src_lang=src_lang,
            tgt_lang=tgt_lang,
            pad_to_max_length=pad_to_max_length,
            num_beams=num_beams,
            ignore_pad_token_for_loss=ignore_pad_token_for_loss,
            source_prefix=source_prefix,
            forced_bos_token=forced_bos_token,
            num_train_epochs=num_train_epochs,
            per_device_eval_batch_size=per_device_train_batch_size,
            learning_rate=learning_rate,
        )

        click.secho("\n[+] Launching finetuning job\n", fg="blue", bold=True)
        local_finetuning.start_finetuning()
        EventLogger.log_event("finetuning_local_translation")


@click.command(name="text_generation")
@click.option("--name", required=True, help="Job name")
@click.option("--model_name_or_id", required=True, help="Model ID")
@click.option("--dataset_name_or_id", required=True, help="Dataset ID")
@click.option("--text_column", required=True, help="Text column")
@click.option(
    "--num_train_epochs",
    required=False,
    default=3,
    show_default=True,
    help="Number of training epochs",
)
@click.option(
    "--per_device_train_batch_size",
    required=False,
    default=16,
    show_default=True,
    help="Train batch size",
)
@click.option(
    "--learning_rate",
    required=False,
    default=5e-5,
    show_default=True,
    help="Learning rate",
)
def job_launch_text_generation(
    name,
    model_name_or_id,
    dataset_name_or_id,
    text_column,
    num_train_epochs,
    per_device_train_batch_size,
    learning_rate,
):
    preferences = Preferences.load()

    if preferences.current_mode == AppModes.LOCAL:
        local_finetuning = LocalTextGeneration(
            job_name=name,
            model_name=model_name_or_id,
            dataset_name=dataset_name_or_id,
            text_column=text_column,
            num_train_epochs=num_train_epochs,
            per_device_eval_batch_size=per_device_train_batch_size,
            learning_rate=learning_rate,
        )

        click.secho("\n[+] Launching finetuning job\n", fg="blue", bold=True)
        local_finetuning.start_finetuning()
        EventLogger.log_event("finetuning_local_text_generation")


job_launch.add_command(job_launch_sequence_classification)
job_launch.add_command(job_launch_question_answering)
job_launch.add_command(job_launch_summarization)
job_launch.add_command(job_launch_translation)
job_launch.add_command(job_launch_token_classification)
job_launch.add_command(job_launch_text_generation)
finetuning_jobs.add_command(ls_finetuning_jobs)
finetuning_jobs.add_command(logs_finetuning_job)
finetuning_jobs.add_command(job_launch)
finetuning_jobs.add_command(inspect_finetuning_jobs)


"""

stochasticx finetuning launch sequence_classification \
    --name test2 \
    --model_id bert-base-uncased \
    --dataset_id "/home/azureuser/datasets/mrpc" \
    --sentence1_column "sentence1" \
    --sentence2_column "sentence2" \
    --label_column "label"

"""

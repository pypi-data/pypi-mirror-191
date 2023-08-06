import click
from stochasticx.utils.docker import (
    start_container, 
    stop_and_remove_container,
    get_logs_container,
    get_open_ports_container
)
from stochasticx.utils.gpu_utils import is_nvidia_gpu_available, get_gpu_info
from stochasticx.stable_diffusion.stable_diffusion import (
    inference,
    init,
    generate_images
)
import sys
from PIL import Image
import numpy as np
from pathlib import Path
import uuid
from stochasticx.datasets.datasets import Datasets
from stochasticx.stable_diffusion.download_models import download_model_from_s3
from stochasticx.utils.logging import configure_logger
from stochasticx.deployment.deployments import (
    StableDiffusionDeployments,
    StableDiffusionDeployment
)
from stochasticx.utils.auth_utils import AuthUtils
import sys
import requests
import time

from stochasticx.utils.stat_controller import EventLogger

logger = configure_logger(__name__)

@click.group(name="stable-diffusion")
def stable_diffusion():
    try:
        AuthUtils.get_auth_headers()
    except:
        click.secho("\n[+] Execute ---> stochasticx login", fg='red', bold=True) 
        click.secho("[+] Or sign up in the following URL https://app.stochastic.ai/signup \n", fg='red', bold=True)
        sys.exit()
    EventLogger.log_event("stable_diffusion")


@click.command(name="download")
@click.option(
    '--type', 
    default="pytorch", 
    show_default=True, 
    help='Model type', 
    type=click.Choice([
        'pytorch', 
        'onnx',
        'tensorrt',
        'nvfuser',
        'flash_attention'
    ])
)
@click.option(
    '--local_dir_path', 
    default="downloaded_models", 
    show_default=True, 
    help='Path where the model will be downloaded'
)
def download(type, local_dir_path):
    click.secho("\n[+] Downloading model\n", fg='blue', bold=True) 
    download_model_from_s3(
        "https://stochasticai.s3.amazonaws.com/stable-diffusion/{}_model.zip".format(type),
        local_dir_path
    )
    click.secho("[+] Model downloaded\n", fg='blue', bold=True)
    EventLogger.log_event("stable_diffusion_download")
    

@click.command(name="deploy")
@click.option(
    '--type', 
    default="auto", 
    show_default=True, 
    help='Model type', 
    type=click.Choice([
        'auto',
        'cloud',
        'pytorch', 
        'aitemplate', 
        'tensorrt'
    ], case_sensitive=False)
)
@click.option(
    '--port', 
    default="5000", 
    show_default=True, 
    help='Port'
)
def deploy(type, port):    
    if not AuthUtils.is_logged_in():
        click.secho("\n[+] Execute ---> stochasticx login", fg='red', bold=True) 
        click.secho("[+] Or sign up in the following URL https://app.stochastic.ai/signup \n", fg='red', bold=True)
        sys.exit()
        
    if type == "cloud":
        click.secho("\n[+] Deploying the Stable-Diffusion model. It might take some minutes", fg='blue', bold=True)
        click.secho("[+] List your deployments with the following command: stochasticx stable-diffusion ls\n", fg='blue', bold=True)
        StableDiffusionDeployments.deploy()
        EventLogger.log_event("stable_diffusion_cloud_deploy")
    else: # local
        gpu2type = {
            "a100":"aitemplate",
            "t4":"tensorrt",
            "rtx_30":"aitemplate",
            "rtx_40":"aitemplate",
            "a30":"aitemplate",
        }
        
        gpu_info = None
        try:
            gpu_info = get_gpu_info()[0]
        except:
            pass
        
        # If there is no GPU
        if gpu_info is None or len(gpu_info) == 0:
            logger.warning("Please install gpu driver or use the machine which has gpu")
            return

        # Support only for T4 and A100 GPUs
        if gpu_info["name"] not in gpu2type:
            logger.warning("Currently we only support gpus which have compute capability >=7,5. We might support other gpus in the future")
            return
        
        # If there is GPU
        if type == "auto":
            # aitemplate or tensorrt
            type = gpu2type[gpu_info["name"]]
            click.secho("[+] Your gpu is {}, the best option is {}".format(gpu_info["name"],type), fg='blue', bold=True)

        if type == "tensorrt":
            if gpu_info["name"].lower() not in ["a100","t4"]:
                logger.warning("TensorRT is only supported on A100 and T4.")
                return
            docker_image = "public.ecr.aws/t8g5g2q5/stable-diffusion:{}_{}".format(
                type, 
                gpu_info["name"].lower()
            )
        else:
            docker_image = "public.ecr.aws/t8g5g2q5/stable-diffusion:{}".format(type)

        click.secho("[+] Deploying Stable Diffusion model", fg='blue', bold=True)
        click.secho("[+] If it is the first time you deploy the model, it might take some minutes to deploy it", fg='blue', bold=True)

        start_container(
            docker_image=docker_image,
            ports={"5000": port},
            container_name="stochasticx_stable_diffusion",
            detach=True,
            gpu=is_nvidia_gpu_available()
        )
        
        if type == "aitemplate":
            click.secho("[+] Start compiling models, it will take about 15 minutes", fg='blue', bold=True)
            time.sleep(20)
            url = "http://127.0.0.1:{}/load".format(port)
            response = requests.post(url)
            if response.json()["status"] == 'failed':
                click.secho("[-] Compiling AITemplate models failed", fg='red', bold=True)
                return
        
        click.secho("[+] Stable Diffusion running in the port {}".format(port), fg='blue', bold=True)
        click.secho("[+] Using GPU: {}".format(is_nvidia_gpu_available()), fg='blue', bold=True)
        click.secho("[+] Run the following command to start generating:", fg='blue', bold=True)
        click.secho("\tstochasticx stable-diffusion infer --prompt 'an astronaut riding a horse'", fg='blue', bold=True)
        EventLogger.log_event("stable_diffusion_local_deploy")
        
        
@click.command(name="ls")
@click.option(
    '--id', 
    help='The ID of the deployment'
)
def list_command(id):
    click.secho("\n[+] Deployments\n", fg='blue', bold=True)
    
    if id is not None:
        deployment = StableDiffusionDeployments.get_deployment(id)
        print(deployment)
    else:
        deployments = StableDiffusionDeployments.get_deployments()
        
        for deployment in deployments:
            print(deployment)
    EventLogger.log_event("stable_diffusion_ls")


@click.command(name="logs")
def logs():
    click.secho("\n[+] Logs\n", fg='blue', bold=True)
    logs = get_logs_container("stochasticx_stable_diffusion")
    print(logs)
    EventLogger.log_event("stable_diffusion_logs")


@click.command(name="stop")
@click.option(
    '--cloud_id', 
    help='The ID of the deployment from the cloud'
)
def stop(cloud_id):
    click.secho("[+] Stopping and removing stable-diffusion model", fg='blue', bold=True)
    if cloud_id is not None:
        StableDiffusionDeployments.delete(cloud_id)
    else:
        stop_and_remove_container("stochasticx_stable_diffusion")
    
    click.secho("[+] Removed", fg='green', bold=True)
    EventLogger.log_event("stable_diffusion_stop")
    
    
@click.command(name="inference")
@click.option(
    '--prompt', 
    required=True, 
    type=str,
    help='Prompt to generate images'
)
@click.option(
    '--cloud_id', 
    default=None,
    type=str, 
    show_default=True,
    help='Cloud ID deployment'
)
@click.option(
    '--img_height', 
    default=512, 
    type=int,
    show_default=True, 
    help='The height in pixels of the generated image.'
)
@click.option(
    '--img_width', 
    default=512, 
    type=int,
    show_default=True, 
    help='The width in pixels of the generated image.'
)
@click.option(
    '--num_inference_steps', 
    default=50, 
    type=int,
    show_default=True, 
    help='The number of denoising steps. More denoising steps usually lead to a higher quality image at the expense of slower inference'
)
@click.option(
    '--num_images_per_prompt', 
    default=1, 
    type=int,
    show_default=True, 
    help='The number of images to generate per prompt.'
)
@click.option(
    '--seed', 
    default=None, 
    type=int,
    show_default=True, 
    help='Seed to make generation deterministic'
)
@click.option(
    '--saving_path', 
    default="generated_images", 
    type=str,
    show_default=True, 
    help='Directory where the generated images will be saved'
)
def infer(
    prompt, 
    cloud_id,
    img_height, 
    img_width, 
    num_inference_steps,
    num_images_per_prompt,
    seed,
    saving_path
):
    # Create directory to save images if it does not exist
    saving_path = Path(saving_path)
    if not saving_path.exists():
        saving_path.mkdir(exist_ok=True, parents=True)   
 
    if cloud_id is not None:
        deployment = StableDiffusionDeployments.get_deployment(cloud_id)
        url = deployment.client_url
        headers = {
            "apiKey": deployment.api_key
        }
    else:                   
        ports = get_open_ports_container("stochasticx_stable_diffusion")
        if len(ports) == 0:
            click.secho("[+] Before doing the inference you have to run: stochasticx stable-diffusion deploy", fg='yellow', bold=True)
            sys.exit()
            
        url = "http://127.0.0.1:{}/predict".format(
            list(ports.values())[0]
        )
        headers = {}
        
    click.secho("[+] Generating images...", fg='blue', bold=True)
    try:
        images, time = inference(
            url=url,
            headers=headers,
            prompt=prompt, 
            img_height=img_height, 
            img_width=img_width, 
            num_inference_steps=num_inference_steps,
            num_images_per_prompt=num_images_per_prompt,
            seed=seed
        )
        
        click.secho("[+] Time needed to generate the images: {} seconds".format(time), fg='blue', bold=True)
        
        pil_images = []
        for img in images:
            pil_images.append(
                Image.fromarray(np.uint8(img))
            )
                
        # Save PIL images with a random name
        for img in pil_images:
            img.save('{}/{}.png'.format(
                saving_path.as_posix(),
                uuid.uuid4()
            ))

        click.secho("[+] Images saved in the following path: {}".format(saving_path.as_posix()), fg='green', bold=True)
        EventLogger.log_event("stable_diffusion_inference")
    except:
        click.secho("[+] Fail to generate images...", fg='red', bold=True)


stable_diffusion.add_command(download)
stable_diffusion.add_command(deploy)
stable_diffusion.add_command(logs)
stable_diffusion.add_command(stop)
stable_diffusion.add_command(list_command)
stable_diffusion.add_command(infer)
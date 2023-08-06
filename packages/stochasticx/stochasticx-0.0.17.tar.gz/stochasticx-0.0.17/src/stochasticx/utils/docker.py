import sys
from unicodedata import name
import docker
import time
from typing import Dict, List
from stochasticx.utils.logging import configure_logger
from stochasticx.utils.spinner_slash import Spinner
import sys
from collections import OrderedDict
import requests

logger = configure_logger(__name__)


def get_docker_client_safely(return_status=False):
    """Get docker client safely"""
    try:
        client = docker.from_env()
        return client
    except:
        if return_status:
            return None
        else:
            logger.error(
                "Cannot connect to the Docker daemon. Make sure Docker is correctly installed and running."
            )
            sys.exit()


def wait_container_is_up(local_url):
    error = True
    while error:
        try:
            response = requests.post(url=local_url, json={})
            if response.status_code != 404:
                error = False
            else:
                time.sleep(10)
                logger.debug(str(response.text))
        except Exception as e:
            logger.debug(str(e))
            time.sleep(10)


def exists_container(container_name: str) -> bool:
    """Check if container already exists

    :param container_name: container name
    :return: if the container exists or not
    """

    client = get_docker_client_safely()
    all_containers = client.containers.list(all=True)

    for container in all_containers:
        if container_name == container.name:
            return True

    return False


def exists_running_container(container_name: str) -> bool:
    client = get_docker_client_safely()

    try:
        container = client.containers.get(container_name)
    except:
        return False

    if container is None:
        return False
    else:
        return container.status == "running"


def start_container(
    docker_image: str,
    ports: Dict[str, str],
    container_name: str,
    detach: bool = True,
    gpu: bool = False,
    volumes: List[str] = [],
    volumes_from: List[str] = [],
    network_links: Dict[str, str] = None,
    shm_size="1G",
):
    """Starts a Docker container locally

    :param docker_image: the Docker image
    :param ports: a dictionary speciying the ports
    :param detach: detach it or not, defaults to True
    :param gpu: use GPUs or not, defaults to False
    :param volumes: list of volumes to use with container
    """

    with Spinner():
        client = get_docker_client_safely()

        if exists_container(container_name):
            # logger.warning("Container {} already running. Stopping and removing it...")
            stop_and_remove_container(container_name)

        device_requests = []
        if gpu:
            device_requests = [
                docker.types.DeviceRequest(device_ids=["all"], capabilities=[["gpu"]])
            ]

        try:
            container = client.containers.run(
                docker_image,
                detach=detach,
                ports=ports,
                device_requests=device_requests,
                name=container_name,
                volumes_from=volumes_from,
                volumes=volumes,
                links=network_links,
                shm_size=shm_size,
            )
        except docker.errors.DockerException as ex:
            logger.error(str(ex))

        return container.id


def stop_and_remove_container(container_name):
    """Stops and removes the container

    :param container_name: container name
    """

    client = get_docker_client_safely()

    try:
        client = get_docker_client_safely()
        container = client.containers.get(container_name)
        container.stop(timeout=50)
        container.remove()
    except docker.errors.DockerException as ex:
        logger.error(str(ex))


def get_logs_container(container_name):
    """Get the logs of a Docker container

    :param container_name: container name
    :return: the logs
    """
    client = get_docker_client_safely()

    if exists_container(container_name):
        return client.containers.get(container_name).logs().decode("utf-8")
    else:
        return "No logs\n"


def get_open_ports_container(container_name):
    """Get open ports of a Docker container

    :param container_name: container name
    :return: container ports
    """
    client = get_docker_client_safely()
    postprocess_ports = {}

    if exists_container(container_name):
        ports = client.containers.get(container_name).ports

        for container_port, host_port in ports.items():
            postprocess_ports[container_port] = host_port[0].get("HostPort")

        return postprocess_ports
    else:
        return {}


def auto_port_selection(port, container_name, selected_ports=[]):
    check = False
    client = get_docker_client_safely()
    port_maps = {}
    for container in client.containers.list(all=True):
        name = container.name
        ports = container.ports
        for host_port in ports.values():
            if host_port is None:
                continue
            host_port = int(host_port[0].get("HostPort"))
            port_maps[host_port] = name

    port_maps = OrderedDict(sorted(port_maps.items()))
    for host_port, name in port_maps.items():
        if port == host_port and name != container_name:
            check = True
            port += 1
    for s_p in selected_ports:
        if s_p == port:
            port += 1

    return port, check

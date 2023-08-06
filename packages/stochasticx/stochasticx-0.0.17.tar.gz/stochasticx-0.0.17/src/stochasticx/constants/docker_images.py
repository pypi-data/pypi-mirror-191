class DockerImages:
    BENCHMARK = "public.ecr.aws/t8g5g2q5/x-benchmarking:latest"
    CONVERSION = "public.ecr.aws/t8g5g2q5/x-conversion:latest"
    FINETUNE = "public.ecr.aws/t8g5g2q5/x-finetuning:latest"
    INFERENCE = "public.ecr.aws/t8g5g2q5/x-inference:latest"
    LOCAL = "public.ecr.aws/t8g5g2q5/x-local:latest"


class ContainerNames:
    BENCHMARK = "x-benchmarking"
    CONVERSION = "x-conversion"
    FINETUNE = "x-finetuning"
    INFERENCE = "x-inference"
    LOCAL = "x-local"

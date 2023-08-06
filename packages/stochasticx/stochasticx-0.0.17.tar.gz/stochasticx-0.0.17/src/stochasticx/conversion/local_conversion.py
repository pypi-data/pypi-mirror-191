from stochasticx.utils.file_utils import ConversionUtils
from stochasticx.models.models import ModelType
from stochasticx.utils.stat_controller import (
    StatController,
    LocalConversionJobInformation,
)


class ConversionType:
    """Conversion type"""

    ONNX = "onnx"
    TRT = "tensorrt"


class LocalConversion:
    """Model class"""

    def __init__(
        self,
        model_path: str,
        convert_type: str = ConversionType.ONNX,
        model_type: str = ModelType.HUGGINGFACE,
        task_type: str = "",
        convert_params: dict = {},
    ):
        """Initializer

        Args:
            model_path (str): directory path where the model is located
            convert_type (str, optional): conversion type. Defaults to ModelConversion.ONNX.
            model_type (str, optional): model type. Defaults to ModelType.HUGGINGFACE.
            task_type (str, optional): task type.
        """

        self.model_path = model_path
        self.convert_type = convert_type
        self.model_type = model_type
        self.task_type = task_type
        self.convert_params = convert_params
        self.model_id = None
        self.model_info = None
        self.is_uploaded = False

    def convert(self):
        """Convert model to onnx/trt/nvfuser"""

        result = ConversionUtils.convert(
            self.model_path,
            self.convert_type,
            self.model_type,
            self.task_type,
            self.convert_params,
        )
        StatController.add_information(
            LocalConversionJobInformation(
                convert_type=self.convert_type,
                model_type=self.model_type,
                task_type=self.task_type,
                params=self.convert_params,
                job_result=result,
            )
        )
        return result

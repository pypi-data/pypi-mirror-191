import logging
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Dict, List, Optional

from baseten.common import settings
from baseten.common.api import (
    cancel_training_run,
    deploy_from_training_run,
    finetune_zoo_model,
    get_all_training_runs,
    get_blueprint_projects,
)
from baseten.common.api import get_training_run as get_training_run_api
from baseten.common.core import ApiError
from baseten.common.files import DatasetTrainingType
from baseten.models.stable_diffusion import StableDiffusionPipeline
from baseten.training.datasets import DatasetIdentifier
from baseten.training.logs import TrainingLogsConsumer
from baseten.training.utils import encode_base64_json

logger = logging.getLogger(__name__)


class FinetuningConfig(ABC):
    """
    Base abstract class for defining fine tuning configs. Each new fine-tuning
    algorithm that we support must support a subclass of this.

    Each fine-tuning algorithm will have a different set of variables that
    need to be provided.
    """

    @property
    @abstractmethod
    def dataset_training_type(self) -> DatasetTrainingType:
        """
        The dataset training type associated with this config type.
        """

    @property
    @abstractmethod
    def training_truss_name(self) -> str:
        """
        The name of the truss associated with this config.
        """

    @abstractmethod
    def resolve_fine_tuning_variables(self) -> Dict:
        """
        Method that must be implemented that returns a variables dictionary
        for this type of FineTuning configuration.
        """


@dataclass
class DreamboothConfig(FinetuningConfig):
    """
    Fine-tuning config for Dreambooth fine-tuning with Stable Diffusion.

    **Examples:**

    ```python
    from baseten.training import Dataset, DreamboothConfig

    config = DreamboothConfig(
        instance_prompt="photo of sks dog",
        input_dataset=Dataset("DATASET_ID"),
        class_prompt="photo of dog",
        train_text_encoder=False,
        max_train_steps=1000
    )
    ```

    Args:
        instance_prompt:
            The prompt with an identifier specifying the instance
            that you're teaching Stable Diffusion
        input_dataset:
            An identifier, either an ID or a public URL, for the Dataset that Dreambooth should use
        wandb_api_key:
            [API key](https://docs.wandb.ai/quickstart) for Weights & Biases
            to monitor your model training
        pretrained_model_name_or_path:
            Path to pretrained model or model identifier from huggingface.co/models.
        revision:
            Revision of pretrained model identifier from huggingface.co/models.
        tokenizer_name:
            Pretrained tokenizer name or path if not the same as model_name
        class_prompt:
            The prompt to specify images in the same class as
            your instance images. This helps regularize the model
            (e.g. so that not all prompts with "dog" look
            like your dog but only "sks dog" does)
        with_prior_preservation:
            Flag to use prior preservation loss
        prior_loss_weight:
            The weight of the prior preservation loss
        num_class_images:
            The number of class images to use for fine-tuning,
            only relevant if using prior preservation. If greater
            than the number of class images in your dataset, it
            will generate the remainder using the base model.
        seed:
            The random seed to use for fine-tuning
        resolution:
            The resolution of your input images. Images will be resized to this value.
        center_crop:
            Whether to center crop the images to the resolution
        train_text_encoder:
            Whether to train the text encoder alongside the UNet
        train_batch_size:
            The batch size to use for training. This value can cause OOMs if
            too large. We reccomend using between 1-4 based on the
            resolution of your images.
        sample_batch_size:
            The batch size to use for sampling images.
        num_train_epochs:
            The number of epochs to train for. If you set max_train_steps, this will be ignored.
        max_train_steps:
            The number of training steps to train for.
            If you set this, num_train_epochs will be ignored.
        learning_rate:
            Initial learning rate (after the potential warmup period) to use.
        lr_scheduler:
            The scheduler type to use. Choose between ["linear",
            "cosine", "cosine_with_restarts", "polynomial",
            "constant", "constant_with_warmup"].
        lr_warmup_steps:
            The number of steps to warmup for the learning rate schedule.
        adam_beta1:
            The beta1 parameter for the Adam optimizer.
        adam_beta2:
            The beta2 parameter for the Adam optimizer.
        adam_weight_decay:
            The weight decay value for the Adam optimizer.
        adam_epsilon:
            The epsilon value for the Adam optimizer.
        max_grad_norm:
            The max gradient normalizatino to clip gradients to.
            Helps prevent exploding gradients.
        mixed_precision:
            Whether to use mixed precision. Choose between
            fp16 and bf16 (bfloat16) or None for no mixed
            precision. This value can cause OOMs in some
            cases with batch size. We reccomend using fp16.
        image_log_steps:
            The number of steps to log sample images to Weights
            and Biases. This allows you to visually assess your
            model during training. Only relevant if wandb_api_key is set.
    """

    instance_prompt: str
    input_dataset: DatasetIdentifier
    wandb_api_key: Optional[str] = None
    hf_access_token: Optional[str] = None

    pretrained_model_name_or_path: str = "CompVis/stable-diffusion-v1-4"
    revision: Optional[str] = None
    tokenizer_name: Optional[str] = None

    class_prompt: Optional[str] = None
    with_prior_preservation: bool = False
    gradient_checkpointing: bool = True
    gradient_accumulation_steps: int = 1
    prior_loss_weight: float = 1.0
    num_class_images: int = 100
    seed: Optional[int] = None
    resolution: int = 512
    center_crop: bool = False
    train_text_encoder: bool = False
    train_batch_size: int = 1
    sample_batch_size: int = 1
    num_train_epochs: int = 1
    max_train_steps: Optional[int] = None
    learning_rate: float = 5e-6
    lr_scheduler: str = "constant"
    lr_warmup_steps: int = 500
    adam_beta1: float = 0.9
    adam_beta2: float = 0.999
    adam_weight_decay: float = 1e-2
    adam_epsilon: float = 1e-08
    max_grad_norm: float = 1.0
    mixed_precision: str = "fp16"
    image_log_steps: int = 20

    def _resolve_dataset(self) -> str:
        return self.input_dataset.resolve_dataset_url(training_type=self.dataset_training_type)

    def resolve_fine_tuning_variables(self) -> Dict:
        """
        Returns fine-tuning variables dict to send when triggering the fine-tuning
        job. The dataset URLs here are resolved to S3 URLs.
        """
        resolved_variables = asdict(self)

        resolved_variables.update({"dataset_zip_url": self._resolve_dataset()})

        del resolved_variables["input_dataset"]

        return {key: value for key, value in resolved_variables.items() if value is not None}

    @property
    def training_truss_name(self) -> str:
        return "dreambooth"

    @property
    def dataset_training_type(self) -> DatasetTrainingType:
        return DatasetTrainingType.DREAMBOOTH


@dataclass
class FullStableDiffusionConfig(FinetuningConfig):
    """
    Fine-tuning config for full fine-tuning with Stable Diffusion.

    **Examples:**

    ```python
    from baseten.training import Dataset, FullStableDiffusionConfig

    config = FullStableDiffusionConfig(
        input_dataset=Dataset("DATASET_ID"),
        train_text_encoder=False,
        num_train_epochs=10
    )
    ```

    Args:
        input_dataset:
            An identifier, either an ID or a public URL, for the Dataset that Dreambooth should use
        wandb_api_key:
            [API key](https://docs.wandb.ai/quickstart) for Weights & Biases to monitor your model training
        pretrained_model_name_or_path:
            Path to pretrained model or model identifier from huggingface.co/models.
        revision:
            Revision of pretrained model identifier from huggingface.co/models.
        seed:
            The random seed to use for fine-tuning
        resolution:
            The resolution of your input images. Images will be resized to this value.
        num_train_epochs:
            The number of epochs to train for. If you set max_train_steps, this will be ignored.
        train_text_encoder:
            Whether to train the text encoder alongside the UNet
        center_crop:
            Whether to center crop the images to the resolution
        random_flip:
            Whether to randomly flip the images horizontally
        train_batch_size:
            The batch size to use for training. This value can cause OOMs if too large.
            We reccomend using between 1-4 based on the resolution of your images.
        max_train_steps:
            The number of training steps to train for. If you set this, num_train_epochs will be ignored.
        learning_rate:
            Initial learning rate (after the potential warmup period) to use.
        lr_scheduler:
            The scheduler type to use. Choose between ["linear", "cosine",
            "cosine_with_restarts", "polynomial", "constant", "constant_with_warmup"].
        lr_warmup_steps:
            The number of steps to warmup for the learning rate schedule.
        use_ema:
            Whether to use exponential moving average for the model weights.
        non_ema_revision:
            Revision of pretrained non-ema model identifier. Must be remote
            repository specified with --pretrained_model_name_or_path.
        adam_beta1:
            The beta1 parameter for the Adam optimizer.
        adam_beta2:
            The beta2 parameter for the Adam optimizer.
        adam_weight_decay:
            The weight decay value for the Adam optimizer.
        adam_epsilon:
            The epsilon value for the Adam optimizer.
        max_grad_norm:
            The max gradient normalizatino to clip gradients to. Prevents exploding gradients.
        image_log_steps:
            The number of steps to log sample images to Weights and Biases. This allows you to visually assess your
            model during training. Only relevant if wandb_api_key is set.
    """

    input_dataset: DatasetIdentifier
    wandb_api_key: Optional[str] = None
    hf_access_token: Optional[str] = None

    pretrained_model_name_or_path: str = "CompVis/stable-diffusion-v1-4"
    revision: Optional[str] = None
    max_train_samples: Optional[int] = None
    seed: Optional[int] = None
    resolution: int = 512
    num_train_epochs: int = 10
    train_text_encoder: bool = False
    center_crop: bool = False
    random_flip: bool = False
    train_batch_size: int = 1
    max_train_steps: Optional[int] = None
    gradient_checkpointing: bool = True
    gradient_accumulation_steps: int = 1
    learning_rate: float = 1e-4
    lr_scheduler: str = "cosine"
    lr_warmup_steps: int = 500
    use_ema: bool = False
    non_ema_revision: Optional[str] = None
    adam_beta1: float = 0.9
    adam_beta2: float = 0.999
    adam_weight_decay: float = 1e-2
    adam_epsilon: float = 1e-08
    max_grad_norm: float = 1.0
    image_log_steps: int = 50

    def _resolve_dataset(self) -> str:
        return self.input_dataset.resolve_dataset_url(training_type=self.dataset_training_type)

    def resolve_fine_tuning_variables(self) -> Dict:
        """
        Returns fine-tuning variables dict to send when triggering the fine-tuning
        job. The dataset URLs here are resolved to S3 URLs.
        """
        resolved_variables = asdict(self)

        resolved_variables.update({"dataset_zip_url": self._resolve_dataset()})

        del resolved_variables["input_dataset"]

        return {key: value for key, value in resolved_variables.items() if value is not None}

    @property
    def training_truss_name(self) -> str:
        return "full_stable_diffusion"

    @property
    def dataset_training_type(self) -> DatasetTrainingType:
        return DatasetTrainingType.CLASSIC_STABLE_DIFFUSION


class FinetuningRun:
    """
    Class to represent a single finetuning run.

    **Examples:**

    Instantiate a new fine-tuning run and stream logs

    ```python
    from baseten.training import FinetuningRun

    my_run = FinetuningRun.create(
        trained_model_name="My Model",
        fine_tuning_config=config
    )
    my_run.stream_logs()
    ```

    Access an existing fine-tuning run

    ```python
    from baseten.training import FinetuningRun

    my_run = FinetuningRun("RUN_ID")
    ```

    Args:
        trained_model_name: The name you want your fine-tuned model to have
        fine_tuning_config: The configuration for the fine-tuning process

    Returns:
        FinetuningRun (str): A string with the id of the newly created FinetuningRun on Blueprint
    """

    @staticmethod
    def create(
        trained_model_name: str, fine_tuning_config: FinetuningConfig
    ) -> Optional["FinetuningRun"]:
        """
        Fine-tune a model by creating a FinetuningRun

        **Example:**

        ```python
        from baseten.training import FinetuningRun

        my_run = FinetuningRun.create(
            trained_model_name="My Model",
            fine_tuning_config=config
        )
        ```

        Args:
            trained_model_name: The name you want your fine-tuned model to have
            fine_tuning_config: The configuration for the fine-tuning process

        Returns:
            FinetuningRun (str): A string with the id of the newly created FinetuningRun on Blueprint
        """
        variables_dict = fine_tuning_config.resolve_fine_tuning_variables()
        encoded_variables = encode_base64_json(variables_dict)

        logger.info("Starting fine-tuning of %s", fine_tuning_config.training_truss_name)
        try:
            run_id = finetune_zoo_model(
                trained_model_name, fine_tuning_config.training_truss_name, encoded_variables
            )
            return FinetuningRun(run_id)
        except ApiError as err:

            def log_error(msg: str):
                logger.error(f"Failed to create TrainingRun. {msg}")

            log_error(str(err))
            return None

    @staticmethod
    def list() -> List["FinetuningRun"]:
        """
        List all finetuning runs for user.

        **Example**

        ```python
        from baseten.training import FinetuningRun

        FinetuningRun.list()
        ```

        """
        resolved_runs = get_all_training_runs()
        return list([FinetuningRun(r["id"], r["trained_model_name"]) for r in resolved_runs])

    class Status(Enum):
        """Status of FinetuningRun on Baseten."""

        PENDING = "PENDING"
        RUNNING = "RUNNING"
        SUCCEEDED = "SUCCEEDED"
        FAILED = "FAILED"
        CANCELLED = "CANCELLED"

    def __init__(
        self,
        id: str,
        trained_model_name: Optional[str] = None,
    ):
        """Initialize the object with the given id.

        Args:
            id (str): The ID of the FinetuningRun on Blueprint
        """
        self.id = id
        self.trained_model_name = trained_model_name
        self.refresh()

    def __repr__(self) -> str:
        trained_name = ""
        if self.trained_model_name:
            trained_name = f", name: {self.trained_model_name}"
        return f"""<FinetuningRun id: {self.id}{trained_name}>"""

    @property
    def status(self) -> str:
        """
        Get the status of your FinetuningRun.
        Statuses are:

        1. PENDING: The run has not yet started
        2. RUNNING: The run is actively fine-tuning the model
        3. SUCCEEDED: The run is finished and fine-tuned the model
        4. FAILED: The run hit an error and did not fine-tune the model
        5. CANCELLED: The run was cancelled by a user

        **Example**

        ```python
        my_run = FinetuningRun("RUN_ID")
        my_run.status
        ```
        """
        return self._status

    @property
    def is_pending(self) -> bool:
        """Is the run pending (waiting to start)"""
        return self._status == FinetuningRun.Status.PENDING.value

    @property
    def is_running(self) -> bool:
        """Is the run running (actively fine-tuning the model)"""
        return self._status == FinetuningRun.Status.RUNNING.value

    @property
    def is_succeeded(self) -> bool:
        """Has the run succeeded (finished fine-tuning the model)"""
        return self._status == FinetuningRun.Status.SUCCEEDED.value

    @property
    def is_failed(self) -> bool:
        """Has the run failed (errored and stopped running)"""
        return self._status == FinetuningRun.Status.FAILED.value

    @property
    def is_cancelled(self) -> bool:
        """Was the run cancelled (terminated by the user)"""
        return self._status == FinetuningRun.Status.CANCELLED.value

    def refresh(self):
        """Re-fetch training data from the server."""
        training_run_data = get_training_run_api(self.id)

        # TODO (Sid): Handle case of training run not found

        self._status = training_run_data["status"]
        self.created = training_run_data["created"]
        self.started = training_run_data["started"]
        self.stopped = training_run_data["stopped"]
        self.trained_model_name = training_run_data["trained_model_name"]

        self.variables = {
            variable["key"]: variable["value"] for variable in training_run_data["variables"]
        }

    # Mutations
    def deploy(self, idle_time_minutes: int = 30) -> StableDiffusionPipeline:
        """
        Deploy the fine-tuned model created during the FinetuningRun

        **Example**

        ```python
        from baseten.training import FinetuningRun

        my_run = FinetuningRun("RUN_ID")
        # After the run is finished
        my_run.deploy()
        ```

        Args:
            idle_time_minutes: How long the deployed model should wait between invocations
                before scaling resources to zero

        Returns:
            StableDiffusionPipeline: A model object using the finetuning run results
        """
        model_id, _ = deploy_from_training_run(
            training_run_id=self.id,
            name=self.trained_model_name,
            idle_time_minutes=idle_time_minutes,
        )
        # TODO: determine which model to return based on finetuning type
        return StableDiffusionPipeline(model_id=model_id)

    def cancel(self) -> bool:
        """
        Cancels this FinetuningRun.

        **Example**

        ```python
        from baseten.training import FinetuningRun

        my_run = FinetuningRun("RUN_ID")
        # While the run is still going
        my_run.cancel()
        ```

        Returns:
            bool: True if the run was successfully canceled
        """
        return cancel_training_run(training_run_id=id)

    def stream_logs(self):
        """Stream logs from the FinetuningRun."""
        TrainingLogsConsumer(self).stream_logs()

    @property
    def blueprint_url(self) -> str:
        """
        Link to view this FinetuningRun in the Blueprint UI

        **Example:**

        ```python
        from baseten.training import FinetuningRun

        my_run = FinetuningRun("RUN_ID")
        my_run.blueprint_url
        ```
        """
        try:
            blueprint_project_id = get_blueprint_projects()[0]["id"]
            return (
                f"{settings.get_server_url()}/blueprint/projects/"
                f"{blueprint_project_id}?est=trained-model--{self.id}"
            )
        except IndexError:
            raise ValueError("User does not have any blueprint projects.")

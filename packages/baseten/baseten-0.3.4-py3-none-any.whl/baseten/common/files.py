import logging
import os
import pathlib
import tempfile
import zipfile
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import IO, Optional
from uuid import uuid4

from PIL import Image

from baseten.common.api import (
    create_training_dataset,
    upload_user_dataset_file,
    upload_user_file,
)

logger = logging.getLogger(__name__)


class DatasetTrainingType(Enum):
    DREAMBOOTH = "DREAMBOOTH"
    CLASSIC_STABLE_DIFFUSION = "CLASSIC_STABLE_DIFFUSION"


DEFAULT_FILE_PATH = "png"


def upload_to_s3(io_stream: IO, file_name: str) -> str:
    """
    Uploads any stream to S3.

    Args:
        io_stream (IO): Any IO byte stream. This could be a bytes buffer, or
        an open binary file.
        file_name (str): The file_name to use when saving the file to S3

    Returns:
        str: A URL to fetch the uploaded S3 object.
    """
    upload_user_file(io_stream, file_name)
    return upload_user_file(io_stream, file_name)


def upload_pil_to_s3(image: Image.Image, file_name: Optional[str] = None) -> str:
    """
    Uploads a PIL image object to S3.

    Args:
        image (PIL.Image): A PIL image object.
        file_name (Optional[str]): The file_name to use when saving the file to S3.
            Must have an image file extension (.jpg, .png, etc.). Can be None.

    Returns:
        str: A URL to fetch the uploaded S3 object.
    """

    # If no file_name is passed, generate a random file path
    if file_name is None:
        file_name = f"{str(uuid4())}.{DEFAULT_FILE_PATH}"

    # Get the file extension from the passed in file name.
    image_format = pathlib.Path(file_name).suffix.strip(".")

    byte_buffer = BytesIO()
    image.save(byte_buffer, format=image_format)

    return upload_to_s3(byte_buffer, file_name)


def _validate_dreambooth_dataset(dir: Path) -> None:
    if not dir.exists():
        raise ValueError("The dataset directory does not exist.")
    if not (dir / "object").exists():
        raise ValueError("The dataset must contain a subdirectory called 'object'")
    if (dir / "prior_preservation").exists():
        logger.info(
            "🛎️ Please make sure to update your finetuning config to use prior_preservation loss! 🛎️"
        )
    logger.info("🛎️ Your Dreambooth dataset is valid! 🛎️")


def _validate_full_stable_diffusion_dataset(dir: Path) -> None:
    if not dir.exists():
        raise ValueError("The dataset directory does not exist.")

    image_files = [
        file
        for file in dir.glob("**/*")
        if file.suffix in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
    ]
    text_files = [file for file in dir.glob("**/*") if file.suffix == ".txt"]
    image_file_names = [file.stem for file in image_files]
    text_file_names = [file.stem for file in text_files]

    if set(image_file_names) != set(text_file_names):
        # Find the image files that don't have a corresponding text file
        # and vice versa
        missing_text_files = set(image_file_names) - set(text_file_names)
        missing_image_files = set(text_file_names) - set(image_file_names)
        if missing_text_files:
            logger.info(
                f"🛑 Missing text files for the following image files: {missing_text_files} 🛑"
            )
        if missing_image_files:
            logger.info(
                f"🛑 Missing image files for the following text files: {missing_image_files} 🛑"
            )
        raise ValueError(
            "The dataset must contain a corresponding text file for each image file and vice versa."
        )

    logger.info("🛎️ Your Stable Diffusion dataset is valid! 🛎️")


def upload_dataset(name: str, dir: Path, training_type: DatasetTrainingType) -> str:
    if training_type == DatasetTrainingType.DREAMBOOTH:
        _validate_dreambooth_dataset(dir)
    elif training_type == DatasetTrainingType.CLASSIC_STABLE_DIFFUSION:
        _validate_full_stable_diffusion_dataset(dir)

    zipfile_name = f"{name}.zip"
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_file = zipfile.ZipFile(os.path.join(tmpdir, zipfile_name), "w")
        for file in dir.glob("**/*"):
            # We want to ignore .DS_STORE files on Mac
            if file.name.lower() == ".ds_store":
                continue
            zip_file.write(file, arcname=f"{dir.name}/{file.relative_to(dir)}")

        zip_file.close()
        upload_params = upload_user_dataset_file(os.path.join(tmpdir, zipfile_name), zipfile_name)

        s3_key = upload_params["form_fields"]["key"]
        return create_training_dataset(name, s3_key, training_type.value)

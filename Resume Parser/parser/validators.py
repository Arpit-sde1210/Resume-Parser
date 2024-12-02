import os

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

VALID_EXTENSIONS = [".pdf", ".docx", ".doc"]


def validate_file_extension(file_object: UploadedFile) -> str:
    """
    Validates the file extension of the uploaded file.
    Only PDF, DOCX, or DOC files are allowed.
    """
    # Extract file extension
    ext = os.path.splitext(file_object.name)[1].lower()

    if ext not in VALID_EXTENSIONS:
        raise ValidationError(f"Unsupported file format: {
                              ext}. Only PDF, DOCX, or DOC files are allowed.")

    return ext


def validate_file_size(file_object: UploadedFile):
    """
    Validates the file size of the uploaded file.
    The maximum allowed file size is 2MB.
    """
    MAX_UPLOAD_SIZE = 2_096_152  # 2MB in bytes

    # Check if the uploaded file exceeds the max size
    if file_object.size > MAX_UPLOAD_SIZE:
        size_in_mb = file_object.size / 1_048_576  # Convert bytes to MB
        raise ValidationError(f"Max file size is 2MB. You uploaded {
                              size_in_mb:.2f}MB.")

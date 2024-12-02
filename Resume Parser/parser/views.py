import logging
from typing import Any

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .utils import extract_resume_info, read_uploaded_file
from .validators import validate_file_extension, validate_file_size

# Set up logging
logger = logging.getLogger(__name__)


def home(request: HttpRequest):
    return render(request, "index.html")


@csrf_exempt
def upload_resume(request: HttpRequest) -> JsonResponse:
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)

    if "file" not in request.FILES:
        return JsonResponse({"error": "No file uploaded"}, status=400)

    file: UploadedFile = request.FILES["file"]

    try:
        # Log the uploaded file's name and extension for debugging
        logger.info(f"Uploaded file: {file.name}")

        # Validate the file's extension and log the result
        ext: str = validate_file_extension(file)
        logger.info(f"File extension: {ext}")

        # Validate the file size
        validate_file_size(file)

        # Read the file content
        file_content = read_uploaded_file(file, ext)

        # Extract the resume info
        data: Any = extract_resume_info(file_content)

        # Return the extracted info as a JSON response
        return JsonResponse(data, status=200)

    except ValidationError as err:
        logger.error(f"Validation error: {err.message}")
        return JsonResponse({"error": err.message}, status=400)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

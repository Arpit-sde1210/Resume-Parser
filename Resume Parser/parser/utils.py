import json
import logging

import boto3
import fitz  # Alias for pymupdf
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from docx import Document

# Configure logger
logger = logging.getLogger(__name__)


def read_uploaded_file(file_object: UploadedFile, file_extension: str) -> str:
    """
    Reads the uploaded file and extracts its text content based on the file format.
    Supports PDF, DOC, and DOCX formats.
    """
    try:
        if file_extension.lower() in ["doc", "docx"]:
            logger.info("Reading DOC/DOCX file.")
            document = Document(file_object)
            text = "\n".join([para.text for para in document.paragraphs])
        elif file_extension.lower() == "pdf":
            logger.info("Reading PDF file.")
            document = fitz.open(stream=file_object.read(),
                                 filetype=file_extension)
            text = "".join([page.get_text() for page in document])
        else:
            logger.error("Unsupported file format.")
            raise ValidationError(
                "Unsupported file format. Please upload PDF, DOC, or DOCX files.", 400)
        return text
    except Exception as e:
        logger.error(f"Error reading uploaded file: {e}")
        raise ValidationError(f"Error processing file: {e}", 500)


# AI credentials and configuration
ai_credentials_options = {
    "region_name": settings.GEN_AI_REGION,
    "aws_access_key_id": settings.GEN_AI_ACCESS_KEY,
    "aws_secret_access_key": settings.GEN_AI_SECRET_KEY,
}

prompt_data = """
You are an AI bot designed to act as a professional for parsing resumes. You are given a resume and your job is to
extract the following information from the resume:

1. applicant_name: ""
2. highest_level_of_education: ""
3. area_of_study: ""
4. institution: ""
5. introduction: ""
6. skills: string []
7. english_proficiency_level: ""
8. experiences: [{"employer_name":"", "role":"", "duration":""}]

Give the extracted info in JSON format only.
Note: if the info is not present, leave the field blank.
"""


def extract_resume_info(text: str):
    """
    Sends the extracted text to AWS Bedrock for parsing and returns the extracted resume information in JSON format.
    """
    try:
        logger.info("Initializing Bedrock client.")
        bedrock = boto3.client("bedrock-runtime", **ai_credentials_options)

        payload = {
            "prompt": f"[INST]{prompt_data}Resume Content::{text}[INST]",
            "max_gen_len": 1024,
            "temperature": 0.5,
            "top_p": 0.9,
        }
        logger.debug(f"Payload: {payload}")

        response = bedrock.invoke_model(
            body=json.dumps(payload),
            modelId="meta.llama2-70b-chat-v1",
            accept="application/json",
            contentType="application/json",
        )
        logger.info("Model invocation successful.")

        response_body = json.loads(response.get("body").read())
        response_text = response_body.get("generation", "")
        if not response_text:
            logger.error("Model returned an empty response.")
            raise ValueError("Empty generation response from the AI model.")

        # Extract JSON from the response
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        json_str = response_text[start:end]
        data = json.loads(json_str)
        logger.info("Resume parsed successfully.")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        raise ValidationError(f"Failed to parse response JSON: {e}", 500)
    except Exception as err:
        logger.error(f"Error during AI invocation: {err}")
        raise ValidationError(f"Something went wrong: {err}", 500)

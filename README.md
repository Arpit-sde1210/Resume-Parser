
# Resume Parser

This project is a Resume Parser built using Python and Django. The goal of the project is to extract structured data from resumes in various formats such as PDF, DOC, and DOCX. The extracted information includes applicant details such as name, education, skills, and work experience, which are then displayed in a structured JSON format.

## Features

- **File Upload**: Users can upload their resumes in PDF, DOC, or DOCX format.
- **Resume Parsing**: The parser extracts key information such as:
  - Applicant's name
  - Highest level of education
  - Area of study
  - Institution
  - Introduction
  - Skills
  - English proficiency level
  - Work experiences (employer name, role, and duration)
- **Error Handling**: The application handles file format errors, size limitations, and unexpected issues during parsing.
- **Editable Form**: An editable form populated with the extracted data for further modification.
  
## Tech Stack

- **Backend**: Python with Django framework
- **File Handling**: `PyMuPDF` (for PDF parsing), `python-docx` (for DOCX parsing)
- **Frontend**: HTML, CSS (Bootstrap or custom styling)
- **File Validation**: Validation for supported file types (PDF, DOC, DOCX) and file size (max 2MB)
- **AI Integration**: AWS Bedrock (or an alternative) to extract structured data from the resumes

## Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.8+ 
- Django 4.0+
- Required Python libraries:
  - `boto3` (for AWS services)
  - `python-docx` (for DOCX parsing)
  - `pymupdf` (for PDF parsing)
  - `django` (for Django framework)
  

## Setup

1. Clone this repository:

    ```bash
    git clone https://github.com/Arpit-sde1210/resume-parser.git
    cd resume-parser
    ```

2. Set up your AWS credentials (for AI-based parsing). Add the following to your Django settings (`settings.py`):

    ```python
    GEN_AI_REGION = 'your-aws-region'
    GEN_AI_ACCESS_KEY = 'your-aws-access-key'
    GEN_AI_SECRET_KEY = 'your-aws-secret-key'
    ```

3. Run database migrations (if using a database):

    ```bash
    python manage.py migrate
    ```

4. Start the Django development server:

    ```bash
    python manage.py runserver
    ```

5. Open your browser and go to `http://localhost:8000` to see the application in action.

## File Formats

- **PDF**: Supported for parsing via `PyMuPDF`.
- **DOCX**: Supported for parsing via `python-docx`.
- **DOC**: Supported as an alternate file type (requires parsing via a compatible library).

## File Upload Validation

- Supported file formats: PDF, DOC, DOCX
- Max file size: 2MB (for efficient processing)

## Error Handling

- **Unsupported file format**: If the user uploads a file that is not PDF, DOC, or DOCX, the system will return an error message.
- **File too large**: If the file size exceeds 2MB, an error message is shown.
- **Parsing errors**: In case of any unexpected errors during the parsing process, an appropriate error message is returned.

## Screenshots / Demo

<img width="959" alt="Resume Parse" src="https://github.com/user-attachments/assets/f6662c8e-1d87-4bd0-8c7a-0cc929c5311e">


## Future Improvements

- Improve accuracy of data extraction (such as detecting education and work experience more precisely).
- Add support for additional file formats (like RTF, TXT).
- Implement user authentication for saving parsed resumes and extracted data.

## Contributing

Contributions are welcome! Feel free to fork this repository, submit issues, or create pull requests.

To contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and commit them with clear messages.
4. Push your branch and open a pull request.

## License

This project is open-source and available under the [MIT License](LICENSE).


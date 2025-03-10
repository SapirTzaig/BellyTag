# Dochumation

Dochumation is a medical information management system designed to help pregnant women upload and process their test results using advanced AI-driven extraction techniques. The system enables doctors to access patient data securely and temporarily, ensuring privacy and control over medical information.

## Features

### For Pregnant Women:
- **Upload Test Results**: Select a test name and upload the corresponding file.
- **Automated Data Extraction**: Uses LLM and prompt engineering to extract relevant medical information from uploaded documents.
- **Secure Data Control**: Patients generate a temporary 5-minute barcode to allow doctors to access their information.
- **Unique Login Barcode**: Upon registration, each patient receives a unique barcode used for authentication.

### For Doctors:
- **Access Patient Data with Consent**: Doctors can view a patient's medical information only if the patient consents by generating a temporary access barcode.
- **View Test Results**: Extracted test information is displayed in an easy-to-read format.

## Technology Stack
Dochumation is built using modern technologies to ensure security, efficiency, and scalability:

- **Frontend**: Vue.js, JavaScript  
- **Backend**: AWS (DynamoDB)  
- **AI Processing**: Gemini AI (for LLM-based data extraction)  
- **Authentication**: Unique barcode-based login system  

## How It Works
1. **User Registration**: Both doctors and patients register and receive a unique barcode.  
2. **Patient File Upload**: Patients select the test type and upload their test result files.  
3. **Data Processing**: The system extracts relevant medical information using LLM and displays it.  
4. **Doctor Access**: A patient can generate a temporary 5-minute barcode to allow a doctor to access their medical data.  
5. **Secure Login**: Users log in using their barcode and password.  

## Security & Privacy
- Data access is controlled by the patient.  
- Temporary access tokens ensure no unauthorized access.  
- All data is securely stored in AWS DynamoDB and processed using AWS services.  

## Installation & Setup

### Prerequisites
- Node.js & npm installed  
- AWS DynamoDB setup  
- AWS credentials configured  

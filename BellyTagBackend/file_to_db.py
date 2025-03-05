import PyPDF2
import pdfplumber
from pdfminer.high_level import extract_text
from google import genai
import os
import pytesseract
from PIL import Image


def pdf_to_text(pdf_path):
    text = ""

    # Try extracting text using PyPDF2
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"PyPDF2 failed: {e}")

    # If PyPDF2 fails, try using pdfplumber
    if not text.strip():
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text.strip():
                print("Text extracted successfully using pdfplumber.")
        except Exception as e:
            print(f"pdfplumber failed: {e}")

    # If pdfplumber fails, try pdfminer.six
    if not text.strip():
        try:
            text = extract_text(pdf_path)
            if text.strip():
                print("Text extracted successfully using pdfminer.six.")
        except Exception as e:
            print(f"pdfminer failed: {e}")

    return text.strip()  # Remove any leading/trailing whitespace


if __name__ == "__main__":
    # pdf_path = r"C:\Users\galev\OneDrive\Desktop\לימודים\יזמות וחדשנות\pdf\first-trimester-ultrasound-report-to-lmc-sample.pdf"
    pdf_path = r"C:\Users\galev\OneDrive\Desktop\לימודים\יזמות וחדשנות\images\estaridol_test_high-1.png"
    if pdf_path[-3:] == "pdf":
        pdf_text = pdf_to_text(pdf_path)
    elif pdf_path[-3:] == "png" or pdf_path[-3:] == "jpg" or pdf_path[-4:] == "jpeg":

        image = Image.open(pdf_path)
        pdf_text = pytesseract.image_to_string(image)

    else:
        raise ValueError("Invalid file format. Only PDF, PNG, and JPG files are supported.")

    

    if not pdf_text:
        print("❌ Failed to extract text from file.")
    else:
        print("✅ Successfully extracted text:")
        # print(pdf_text[:500])  # Print the first 500 characters for debugging

    prenatal_tests = {
        "Ultrasound for Fetal Nuchal Translucency": [
            ("Nuchal Translucency", "float"),
            ("Crown Rump Length", "float"),
            ("Fetal Heart Rate", "float"),
            ("Biparietal diameter", "float"),
        ],
        "Ultrasound for Fetal Nasal Bone Determination": [
            ("Nasal Bone Visible", "boolean")
        ],
        "Maternal Serum (Blood) Tests": [
            ("Pregnancy Associated Plasma Protein A", "float"),
            ("Human Chorionic Gonadotropin", "float")
        ],
        "Genetic Screening Recommendation": [
            ("Genetic Counseling Recommended", "boolean"),
            ("Additional Testing Needed", "boolean"),
            ("Additional Tests", "list")
        ],
        "Multiple Marker Blood Tests (Second Trimester)": [
            ("AFP Screening", "float"),
            ("Estriol", "float"),
            ("Inhibin", "float"),
            ("Human Chorionic Gonadotropin", "float")
        ],
        "Possible Abnormal Indications": [
            ("Abnormal AFP", "boolean"),
            ("Miscalculated Due Date", "boolean"),
            ("Fetal Abdominal Wall Defects", "boolean"),
            ("Chromosomal Abnormalities", "boolean"),
            ("Open Neural Tube Defects", "boolean"),
            ("Multiple Fetuses Detected", "boolean")
        ],
        "Follow-up Testing": [
            ("Ultrasound Recommended", "boolean"),
            ("Amniocentesis Needed", "boolean")
        ],
        "Screening Accuracy": [
            ("False Positive Risk", "float"),
            ("False Negative Risk", "float")
        ],
        "Group B Streptococcus Presence": [
            ("Result", "boolean")
        ]
    }

    kvp = prenatal_tests["Ultrasound for Fetal Nuchal Translucency"]


    # Extract text
    # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    

    pdf_text = pdf_text.replace("\n", " ")
    pdf_text += "\n\nI want you to get from the text the following parameters and their values " \
                "(the desired type is provided) and the metric (mm/cm/bpm etc...). " \
                "If something doesn't exist, put None instead:\n"

    for key, value in kvp:
        pdf_text += f"{key} : {value}\n"

    pdf_text += "I want only the parameters, values of the parameters, and the metric, " \
                "no * or bullet points or the opening line\n"

    client = genai.Client(api_key="AIzaSyBpT6qJ1A28dh2XQDnmSiNL4hIl-P94jFU")
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=pdf_text,
    )
    print(response.text)

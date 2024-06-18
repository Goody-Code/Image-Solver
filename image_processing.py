import re
from io import BytesIO
from PIL import Image
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
from config import AZURE_SUBSCRIPTION_KEY, AZURE_ENDPOINT
from nlp_model import generate_response

computervision_client = ComputerVisionClient(AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_SUBSCRIPTION_KEY))

def clean_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^A-Za-z0-9ء-ي\s]', '', text)
    return text.strip()

def process_image(photo_file):
    photo_bytes = BytesIO(photo_file.download_as_bytearray())
    image = Image.open(photo_bytes)
    
    image_bytes = BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes = image_bytes.getvalue()

    ocr_results = computervision_client.read_in_stream(BytesIO(image_bytes), raw=True)
    operation_location = ocr_results.headers["Operation-Location"]
    operation_id = operation_location.split("/")[-1]

    while True:
        result = computervision_client.get_read_result(operation_id)
        if result.status not in ['notStarted', 'running']:
            break

    if result.status == OperationStatusCodes.succeeded:
        extracted_text = ""
        for text_result in result.analyze_result.read_results:
            for line in text_result.lines:
                extracted_text += line.text + " "
        cleaned_text = clean_text(extracted_text)
        return generate_response(cleaned_text)
    else:
        return 'حدث خطأ أثناء قراءة النص من الصورة.'

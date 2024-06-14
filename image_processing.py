from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from config import AZURE_COMPUTER_VISION_ENDPOINT, AZURE_COMPUTER_VISION_SUBSCRIPTION_KEY

def extract_text_from_image(image_path):
    client = ComputerVisionClient(
        AZURE_COMPUTER_VISION_ENDPOINT, 
        CognitiveServicesCredentials(AZURE_COMPUTER_VISION_SUBSCRIPTION_KEY)
    )
    
    with open(image_path, "rb") as image_stream:
        ocr_result = client.recognize_printed_text_in_stream(image_stream)
    
    text = ""
    for region in ocr_result.regions:
        for line in region.lines:
            for word in line.words:
                text += word.text + " "
            text += "\n"
    
    return text

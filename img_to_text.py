import pyscreenshot as ImageGrab
import cStringIO
import base64
import os
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials

DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

#Captures a file image, saves it to a buffer, and converts it to a base64 representation, and returns
#Defines image as the entire desktop
def grabScreen():
    im = ImageGrab.grab()
    pngBuffer = cStringIO.StringIO()
    im.save(pngBuffer, format="PNG")
    imgStr = base64.b64encode(pngBuffer.getvalue())
    return imgStr

#Captures a file image, saves it to the temporary location/file name
#Defines two opposing cornes of a rectangle to capture
def grabBox(topLeftX, topLeftY, bottomRightX, bottomRightY):
    im = ImageGrab.grab(bbox=(topLeftX, topLeftY, bottomRightX, bottomRightY))
    pngBuffer = cStringIO.StringIO()
    im.save(pngBuffer, format="PNG")
    imgStr = base64.b64encode(pngBuffer.getvalue())
    return imgStr

#Takes a base 64 string representation of an image, and exchanges it for OCR based text from googles cloud vision API
def getTextFromImage(base64ImageString):
    #Get a hold of the api key, this has a hard blow up on purpose
    apiKey = os.environ['GOOGLE_TRANSLATE_API_KEY']

    requests = [{
        'image': {
            'content': base64ImageString.decode('utf-8')
        },
        'features': [{
            'type': 'TEXT_DETECTION'
        }]
    }]

    credentials = GoogleCredentials.get_application_default()
    service = build('vision', 'v1', credentials=credentials, discoveryServiceUrl=DISCOVERY_URL)

    result = service.images().annotate(body={
            'requests': requests
        }).execute()

    return result;

if __name__ == "__main__":
    #Example usage
    print grabScreen()

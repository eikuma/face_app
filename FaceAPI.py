from PIL import ImageDraw, ImageFont
import requests

from PIL import Image
import io

subscription_key = '76959f7e27984da9b6ca36f0544f1b4a'

assert subscription_key

face_api_url = 'https://2020ikuma.cognitiveservices.azure.com/face/v1.0/detect'

img = Image.open('ikuma.jpg')

# with open('ikuma.jpg', 'rb') as f:
#     binary_img = f.read()

with io.BytesIO() as output:
    img.save(output, format="JPEG")
    binary_img = output.getvalue()

headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key
}

params = {
    'returnFaceId': 'true',
    'returnFaceAttributes': 'age, gender, headPose, smile, facialHair, glasses, emotion'
}

res = requests.post(face_api_url, params=params,
                    headers=headers, data=binary_img)
results = res.json()
for result in results:
    rect = result['faceRectangle']
    gender = result['faceAttributes']['gender']
    age = result['faceAttributes']['age']
    text = f'{gender} {round(age)}'
    fontsize = max(16, int(rect['width'] / len(text)))
    font = ImageFont.truetype("/System/Library/Fonts/Courier.dfont", fontsize)
    text_width, text_height = font.getsize(text)
    draw = ImageDraw.Draw(img)
    draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'],
                                                  rect['top']+rect['height'])], fill=None, outline='green', width=5)

    draw.text((rect['left'] + rect['width'] / 2 - text_width / 2, rect['top'] - text_height - 1),
              text=text, align='center', fill='red', font=font)
img.show()

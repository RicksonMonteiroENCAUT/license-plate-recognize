from google.cloud import vision
import io
import os
import segmentation as sg

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="Credenciais/ApiVision-6ad15f873f95.json"
TEXTS=[]

# Instantiates a client
def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
   # print('Texts:')

    for text in texts:
        #print('\n"{}"'.format(text.description))
        dict={'description': text.description, 'Locale':text.locale, 'Vertices':text.bounding_poly.vertices}
        TEXTS.append(dict)
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        #print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


crop_path=sg.preprocessing('imagens/000.jpg')

if crop_path is not None:
    detect_text(crop_path)
    for t in TEXTS[1:]:
        if not t['description'].isalpha():
            print("Placa: {}".format(t['description']))
else:
    print('Tente outra imagem!')

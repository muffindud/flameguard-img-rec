from requests import get

from torch import load, device, argmax
from torchvision.transforms.transforms import Compose, Resize, ToTensor, Normalize
from PIL import Image

Image.LOAD_TRUNCATED_IMAGES = True

model_path = 'trained-models/model_final.pth'
img_dir_path = 'images/'

class_names = ['Fire', 'Neutral', 'Smoke']


def scan_image(img_path: str) -> tuple:
    model = load(model_path, map_location=device('cpu'))
    img_data = get(img_path).content
    img_name = img_path.split('/')[-1]
    with open(img_dir_path + img_name, 'wb') as handler:
        handler.write(img_data)

    ptrediction_transform = Compose([
        Resize(size=(224, 224)),
        ToTensor(), 
        Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    img = Image.open(img_dir_path + img_name)
    img = ptrediction_transform(img)[:3,:,:].unsqueeze(0)
    img = img.cpu()

    pred = model(img)
    idx = argmax(pred)
    prob = pred[0][idx].item()*100

    return class_names[idx], round(prob, 2)

from flask import Flask, request, jsonify
import requests
from PIL import Image
import io
import torch
from torchvision import models, transforms

app = Flask(__name__)

# Pre-trained model for image classification (ResNet50)
model = models.resnet50(pretrained=True)
model.eval()

# Image transformation for ResNet50
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Nutritionix API for calorie estimation based on food name
NUTRITIONIX_API_URL = 'https://api.nutritionix.com/v1_1/search/'
NUTRITIONIX_API_KEY = 'YOUR_API_KEY'
NUTRITIONIX_APP_ID = 'YOUR_APP_ID'

def get_calories_from_food_name(food_name):
    params = {
        'query': food_name,
        'fields': 'item_name,nf_calories',
        'appId': NUTRITIONIX_APP_ID,
        'appKey': NUTRITIONIX_API_KEY
    }
    response = requests.get(NUTRITIONIX_API_URL, params=params)
    data = response.json()

    if 'hits' in data and len(data['hits']) > 0:
        return data['hits'][0]['fields']['nf_calories']
    return None

@app.route('/estimate-calories', methods=['GET'])
def estimate_calories():
    food_name = request.args.get('food_name')
    if not food_name:
        return jsonify({'error': 'Food name is required'}), 400
    
    calories = get_calories_from_food_name(food_name)
    if calories:
        return jsonify({'calories': calories})
    else:
        return jsonify({'error': 'Food not found'}), 404

@app.route('/estimate-calories-from-image', methods=['POST'])
def estimate_calories_from_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image = request.files['image']
    img = Image.open(io.BytesIO(image.read()))
    img = transform(img).unsqueeze(0)

    with torch.no_grad():
        outputs = model(img)
    
    _, predicted_class = torch.max(outputs, 1)
    class_id = predicted_class.item()

    mock_calories = {
        130: 250,  # Example for pizza
        227: 300   # Example for burger
    }

    calories = mock_calories.get(class_id, 100)  # Default calories
    return jsonify({'calories': calories})

if __name__ == '__main__':
    app.run(debug=True)

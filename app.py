from flask import Flask, render_template, request, jsonify
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.densenet import preprocess_input
from tensorflow.keras.models import model_from_json
import numpy as np
import pickle
from PIL import Image

app = Flask(__name__)

# # Load models for different pet types
models = {}
for pet_type in ['hen', 'cat', 'cow', 'dog']:
    with open(f'{pet_type}_model.pkl', 'rb') as f:
        model_dict = pickle.load(f)
        model = model_from_json(model_dict['architecture'])
        model.set_weights(model_dict['weights'])
        models[pet_type] = model

# Load the pre-trained model
# with open('Hen_model.pkl', 'rb') as f:
#     model_dict = pickle.load(f)
#     model = model_from_json(model_dict['architecture'])
#     model.set_weights(model_dict['weights'])

['AvianPox', 'FowlCholera', 'MarekDisease', 'Normal']
# ['Feline_Dermatophytosis', 'Mange', 'NormalCat', 'feline_acne']
dict_cat={
    0:"Feline Dermatophytosis",
    1:"Mange",
    2:"Healthy Cat",
    3:"Feline Acne"
}
dict_hen={
    0:"AvianPox",
    1:"FowlCholera",
    2:"MarekDisease",
    3:"Normal"
}
dict_cow={
    
0:'Actinomycosis Lumpy Jaw ',
1: 'Bovine Papillomatosis', 
2:'foot and mouth disease', 
3:'healthy', 
4:'lumpy skin dsease'
}
dict_dog={
    0:'Conjunctivitis1',1: 'Mange',2: 'Ringworm',3: 'Ticks',4: 'healthy'
}
dict_cat_treatment = {
    0: {
        'medicines': ['Griseofulvin', 'Ketoconazole'],
        'treatment': 'Administer Griseofulvin or Ketoconazole as prescribed. Treat affected areas with antifungal cream and ensure the cat’s environment is cleaned thoroughly.'
    },
    1: {
        'medicines': ['Ivermectin', 'Selamectin'],
        'treatment': 'Apply Ivermectin or Selamectin topically or orally. Bathe the cat with a medicated shampoo and keep its environment clean.'
    },
    2: {
        'medicines': [],
        'treatment': 'Maintain a balanced diet and regular checkups. Ensure a clean and stress-free environment for overall health.'
    },
    3: {
        'medicines': ['Benzoyl Peroxide shampoo', 'Antibiotic ointment (e.g., Neomycin)'],
        'treatment': 'Wash affected areas with Benzoyl Peroxide shampoo. Apply antibiotic ointment to reduce inflammation and prevent infection.'
    }
}

dict_hen_treatment = {
    0: {
        'medicines': ['Vaccination (Avian Pox vaccine)', 'Antibiotics (e.g., Tetracycline)'],
        'treatment': 'Administer Avian Pox vaccine as per schedule. Treat secondary bacterial infections with antibiotics.'
    },
    1: {
        'medicines': ['Vaccination (Fowl Cholera vaccine)', 'Antibiotics (e.g., Oxytetracycline)'],
        'treatment': 'Vaccinate against Fowl Cholera. Treat with antibiotics and provide supportive care to manage symptoms.'
    },
    2: {
        'medicines': ['Vaccination (Marek’s disease vaccine)', 'None'],
        'treatment': 'Vaccinate chicks against Marek’s disease at an early age. No specific treatment once symptoms appear; supportive care is crucial.'
    },
    3: {
        'medicines': [],
        'treatment': 'Ensure a balanced diet and clean environment. Regular health checkups and proper management practices are key to maintaining health.'
    }
}

dict_cow_treatment = {
    0: {
        'medicines': ['Penicillin', 'Oxytetracycline'],
        'treatment': 'Administer Penicillin or Oxytetracycline intramuscularly. Clean the affected area and provide supportive care.'
    },
    1: {
        'medicines': ['Vaccination (Papillomavirus vaccine)', 'Antiviral drugs'],
        'treatment': 'Apply topical antiviral treatments to warts. Ensure proper vaccination to prevent further outbreaks.'
    },
    2: {
        'medicines': ['Vaccination (FMD vaccine)', 'Antibiotics (e.g., Oxytetracycline)'],
        'treatment': 'Administer FMD vaccine as per schedule. Treat secondary infections with antibiotics and provide supportive care.'
    },
    3: {
        'medicines': [],
        'treatment': 'Ensure a balanced diet and regular health checkups. Maintain good hygiene and provide adequate shelter.'
    },
    4: {
        'medicines': ['Vaccination (Lumpy Skin Disease vaccine)', 'Antibiotics (e.g., Oxytetracycline)'],
        'treatment': 'Administer the Lumpy Skin Disease vaccine. Treat secondary bacterial infections with antibiotics and provide supportive care.'
    }
}

dict_dog_treatment = {
    0: {
        'medicines': ['Neomycin eye drops', 'Tobramycin eye drops'],
        'treatment': 'Clean the dog’s eyes with saline solution. Apply eye drops 2-3 times daily for 7-10 days.'
    },
    1: {
        'medicines': ['Ivermectin', 'Selamectin'],
        'treatment': 'Administer Ivermectin or Selamectin orally according to the instructions. Bathe the dog with medicated shampoo twice a week.'
    },
    2: {
        'medicines': ['Griseofulvin', 'Ketoconazole'],
        'treatment': 'Apply antifungal cream to affected areas. Give oral antifungal medication daily for 2-4 weeks.'
    },
    3: {
        'medicines': ['Bravecto (Fluralaner)', 'Nexgard (Afoxolaner)'],
        'treatment': 'Administer Bravecto or Nexgard according to the dog’s weight. Check and remove ticks daily with a tick removal tool.'
    },
    4: {
        'medicines': [],
        'treatment': 'Maintain a healthy diet and regular checkups. Ensure regular grooming and use preventive measures against parasites.'
    }
}


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pet-image' not in request.files:
        return jsonify({'result': 'No image uploaded'}), 400

    if 'pet-type' not in request.form:
        return jsonify({'result': 'No pet type selected'}), 400

    pet_type = request.form['pet-type']
    file = request.files['pet-image']

    if pet_type not in models:
        return jsonify({'result': 'Invalid pet type selected'}), 400

    model = models[pet_type]

    if file:
        # Convert file to an image
        image = Image.open(file.stream)
        
        # Resize and preprocess the image
        image = image.resize((224, 224))
        image_array = img_to_array(image)
        image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension
        image_array = preprocess_input(image_array)

        # Make prediction
        prediction = model.predict(image_array)
        predicted_class = np.argmax(prediction[0])
        ans=""
        print(pet_type)
        if pet_type=="cat":
            return jsonify({'result': f'Disease: {dict_cat[predicted_class]}','treatment':dict_cat_treatment[predicted_class]})
        if pet_type=="hen":
            return jsonify({'result': f'Disease: {dict_hen[predicted_class]}','treatment':dict_hen_treatment[predicted_class]})
        if pet_type=="dog":
            return jsonify({'result': f'Disease: {dict_dog[predicted_class]}','treatment':dict_dog_treatment[predicted_class]})
        if pet_type=="cow":
            return jsonify({'result': f'Disease: {dict_cow[predicted_class]}','treatment':dict_cow_treatment[predicted_class]})
        
        return jsonify({'result': f'Predicted class: {predicted_class}'})

    return jsonify({'result': 'No image file provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)

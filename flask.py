from flask import Flask, jsonify
app = Flask(__name__)
# Sample NGO data with coordinates
ngos_list = [
    {'NGO_Name': 'CRY (Child Rights and You)', 'Latitude': 19.0760, 'Longitude': 72.8777},
    {'NGO_Name': 'Goonj', 'Latitude': 28.6139, 'Longitude': 77.2090},
    {'NGO_Name': 'Akshaya Patra Foundation', 'Latitude': 12.9716, 'Longitude': 77.5946},
    {'NGO_Name': 'Teach For India', 'Latitude': 19.0760, 'Longitude': 72.8777},
    {'NGO_Name': 'Smile Foundation', 'Latitude': 28.6139, 'Longitude': 77.2090},
    {'NGO_Name': 'Oxfam India', 'Latitude': 28.6139, 'Longitude': 77.2090},
    {'NGO_Name': 'HelpAge India', 'Latitude': 28.6139, 'Longitude': 77.2090},
    {'NGO_Name': 'SankalpTaru Foundation', 'Latitude': 26.9124, 'Longitude': 75.7873},
    {'NGO_Name': 'Pratham', 'Latitude': 19.0760, 'Longitude': 72.8777},
    {'NGO_Name': 'The V Foundation for Cancer Research', 'Latitude': 28.6139, 'Longitude': 77.2090},
]
@app.route('/api/ngos', methods=['GET'])
def get_ngos():
    return jsonify(ngos_list)
if __name__ == '__main__':
    app.run(debug=True)

import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Load student marks from the JSON file
with open("q-vercel-python.json", "r") as file:
    students = json.load(file)

# Convert list to a dictionary for faster lookups
student_dict = {student["name"]: student["marks"] for student in students}

@app.route('/api', methods=['GET'])
def get_marks():
    names = request.args.getlist('name')
    marks = [student_dict.get(name, None) for name in names]
    return jsonify({"marks": marks})

if __name__ == "__main__":
    app.run(debug=True)

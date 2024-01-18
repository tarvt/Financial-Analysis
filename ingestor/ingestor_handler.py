from flask import Flask, request, jsonify 
import json 

app = Flask(__name__) 

@app.route('/ingest', methods=['POST']) 
def ingest_data(): 
    try: 
        data = request.json 
        # Validate and process data 
        # Forward to stream processing service 
        return jsonify({"status": "success", "message": "Data received"}), 200 
    except Exception as e: 
        return jsonify({"status": "error", "message": str(e)}), 500 

if name == '__main__': 
    app.run(debug=True, host='0.0.0.0', port=5000)

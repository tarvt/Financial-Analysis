from flask import Flask, request 
 
app = Flask(__name__) 
 
@app.route('/', methods=['POST']) 
def receive_data(): 
    data = request.get_json() 
    print("Received data:", data) 
    return "Data Received", 200 
 
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5004)

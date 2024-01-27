import socket 
from flask import Flask, request 
import threading 
 
app = Flask(__name__) 
 
def forward_to_spark(data, spark_host, spark_port): 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        s.connect((spark_host, spark_port)) 
        s.sendall(data.encode('utf-8')) 
 
@app.route('/ingest', methods=['POST']) 
def ingest_data(): 
    try: 
        data = request.data.decode('utf-8') 
        # Forward data to Spark Streaming Service 
        threading.Thread(target=forward_to_spark, args=(data, "localhost", 9999)).start() 
        return {"status": "success", "message": "Data received and forwarded"}, 200 
    except Exception as e: 
        return {"status": "error", "message": str(e)}, 500 
 
if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0', port=6000)
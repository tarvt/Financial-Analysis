from flask import Flask, request, jsonify 
 
app = Flask(__name__) 
 
@app.route("/signal", methods=['GET', 'POST']) 
def generate_signal(): 
    if request.method == 'POST': 
        data = request.get_json()  # Ensures JSON parsing 
        print(f"Received data: {data}") 
 
        data_type = data.get('data_type') 
        signal = "hold"  # Default signal 
 


        if data.get('MA') and data.get('EMA'): 
            if data['MA'] > data['EMA']: 
                signal = "sell" 
            elif data['MA'] < data['EMA']: 
                signal = "buy" 
 
        # Add more conditions for other data types as needed 
 
        print("*******************************") 
        print(f"Signal for {data_type}: {signal}") 
        print("*******************************") 
        return jsonify({"signal": signal}) 
    else: 
        # Handle GET request: display a message or form 
        return 'This endpoint expects a POST request with data.' 
 
if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=5005)
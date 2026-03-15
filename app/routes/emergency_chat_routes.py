from flask import Blueprint, request, jsonify #imports Blueprint (to organize routes), request (to access incoming request data), and jsonify (to return JSON responses) from Flask

try: #This starts a try block.
    from app.controllers.emergency_chat_controller import handle_emergency_chat #his imports the controller function.
    CONTROLLER_LOADED = True #creates a variable CONTROLLER_LOADED and sets it to True, usually to indicate that the controller file has been successfully loaded
except Exception as e: #If something goes wrong (for example): file missing, syntax error, dependency error  Python jumps here.
    print(f"Could not load emergency chat controller: {e}") #Prints an error message in the server console. This helps debug the issue.
    CONTROLLER_LOADED = False #Your API will later handle this safely.

emergency_chat_bp = Blueprint("emergency_chat", __name__) #Creates a Blueprint module for emergency chat routes.


@emergency_chat_bp.route("/api/emergency/chat", methods=["POST"]) #uses a route decorator to define a POST API endpoint /api/emergency/chat in a Flask Blueprint called emergency_chat_bp
def emergency_chat(): #This function runs when the endpoint is called.
    print("--- Request received at /api/emergency/chat ---") #Prints a log message in the server console.

    if not CONTROLLER_LOADED: #Checks if the controller failed to import earlier.
        #Return Emergency Message
        return jsonify({ #Creates a JSON response.
            "msg": "Emergency chat service unavailable. Call 112.", #Message telling the user to call emergency services directly.
            "emergency_numbers": {"ambulance": "102", "general": "112"} #Returns emergency numbers.
        }), 503 #503= Service Unavailable.

    data = request.get_json(silent=True) or {} #Reads JSON data from the request body. silent=True: If the JSON is invalid Flask doesn't throw an error, instead it returns none.

    response_body, status_code = handle_emergency_chat(data) #Calls the controller function. The controller processes it and reeturns two values response_body & status_code.

    return jsonify(response_body), status_code #Converts the response into JSON and sends it back to the client.
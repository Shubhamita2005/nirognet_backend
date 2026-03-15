from flask import Blueprint, request, jsonify #imports Blueprint to organize routes, request to access incoming request data, and jsonify to return JSON responses from Flask

# ---- Try loading controller ----
try: #starts a try block. This means Python will attempt to run the code, and if an error occurs it will move to the except block. This is used to prevent the server from crashing if the controller fails to load.
    from app.controllers.symptom_controller import handle_symptom_analysis #Imports the controller function responsible for analyzing symptoms.
    CONTROLLER_LOADED = True #If the import succeeds, the system marks that: The system controller is available.
except Exception as e: #If something goes wrong (for example): file missing, syntax error, dependency issue Python jumps here.
    print(f"Could not load symptom controller: {e}") #Prints an error message in the server console. This helps developers debug the issue.
    CONTROLLER_LOADED = False #Marks that the controller failed to load. Later the API will handle this safely instead of crashing.

symptom_bp = Blueprint("symptom", __name__) #creates a Blueprint named "symptom" to group symptom-related routes in the application using Flask


@symptom_bp.route("/api/symptoms/analyze", methods=["POST"]) #Defines an API endpoint.
def analyze_symptoms_route(): #his function runs whenever someone calls: POST /api/symptoms/analyze
    print("--- Request received at /api/symptoms/analyze ---") #Prints a log message in the server console.

    if not CONTROLLER_LOADED: #Checks if the controller failed to import earlier.If CONTROLLER_LOADED is False, then the symptom analysis service cannot run.
        return jsonify({"msg": "Symptom service not available"}), 503 #Returns a JSON error message. 503= Service Anvailable.

    data = request.get_json(silent=True) or {} #Reads the JSON body sent by the client.

    response_body, status_code = handle_symptom_analysis(data) #Calls the controller function that handles the actual analysis.

    return jsonify(response_body), status_code #Sends the response back to the client.
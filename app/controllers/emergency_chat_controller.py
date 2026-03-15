from app.services.emergency_gemini_service import emergency_ai_response # imports the function emergency_ai_response from the emergency_gemini_service module located in the app.services package.
from app.models import Hospital #Imports the Hospital database model.


def handle_emergency_chat(data: dict) -> tuple: #defines the main function that processes emergency chat requests
    #This docstring explains that the function handles emergency chat requests, takes parsed JSON data as input, and returns a response dictionary with an HTTP status code.
    """
    Controller logic for emergency chat.

    Args:
        data: parsed JSON body from the request

    Returns:
        tuple: (response_dict, status_code)
    """

    # ---- Input Validation ----
    if not data: #Checks if request body is empty.
        return {"msg": "Request body is required"}, 400 #message explaining issue, 400 HTTP status (Bad Request)

    message = data.get("message") #Gets "message" field from JSON.

    #Check if Message Exists
    if not message:
        return {"msg": "Message is required"}, 400

    #Validate Message Type
    if not isinstance(message, str): #Checks if message is a string.
        return {"msg": "Message must be a string"}, 400 #Rejects invalid data types.

    #Remove Extra Spaces
    message = message.strip()

    #Minimum Length Check
    if len(message) < 3: #If message is too short.
        return {"msg": "Please describe your emergency in more detail"}, 400 #Encourages the user to explain the problem.

    #Maximum Length Check
    if len(message) > 2000: #Limits message size to 2000 characters, to prevent abuse & very large AI requests.
        return {"msg": "Message is too long (max 2000 characters)"}, 400

    # ---- Call AI Service ----
    try: #Starts error handling block, If AI service fails, program won't crash.
        print(f"Emergency message received: {message}") #Logs message in server console.
        print("--- Calling Gemini for emergency response... ---") #Shows AI processing started.

        ai_reply = emergency_ai_response(message) #Calls AI service.

        #Check AI Response
        if not ai_reply: #If AI returns empty response.
            return {"msg": "Empty response from AI service"}, 502 #502 = Bad Gateway, Meaning external service failed.

        print("--- Emergency AI response generated ---") #Log showing AI response finished.

    #AI Error Handling
    except Exception as e: #If any error occurs during AI call eg: API error, internet failure, timeout.
        print(f"Emergency AI exception: {e}") #Prints error in server logs.
        #Fallback message telling user to call emergency services, Provides Indian emergency numbers.
        return {
            "msg": "AI error. Please call emergency services immediately.",
            "emergency_numbers": {"ambulance": "102", "general": "112"}
        }, 500 #500 = Internal Server Error

    # ---- Fetch Nearby Hospitals ----
    try: #Start database query block.
        hospitals = Hospital.query.all() #Fetch all hospitals from database.
        #Convert Hospital Objects to JSON
        hospital_data = [ #Creates list of hospital dictionaries.
            #For each hospital object h, extract fields.
            {
                "name": h.name,
                "distance": h.distance,
                "doctors": h.doctors,
                "beds": h.beds,
                "ventilators": h.ventilators,
                "blood": h.blood
            }
            for h in hospitals #Loop through all hospital records.
        ]
        print(f"Found {len(hospital_data)} hospitals") #Log Hospital Count

    #Handle Hospital Query Failure
    except Exception as e: #If database query fails.
        print(f"Hospital fetch failed: {e}") #Log error.
        hospital_data = [] #Return empty hospital list instead of crashing.

    # ---- Return Response ----
    return { #Returning JSON response.
        "text": ai_reply, #First aid advice from AI.
        "hospitals": hospital_data, #List of hospitals.
        "disclaimer": "This is AI-generated first-aid guidance, NOT medical advice. Call emergency services immediately.", #Important legal warning.
        #Provides quick emergency contacts.
        "emergency_numbers": {
            "ambulance": "102",
            "general": "112"
        }
    }, 200 #200 = Success
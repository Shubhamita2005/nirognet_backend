from app.services.symptom_checker_service import analyze_symptoms_with_gemini #imports the function analyze_symptoms_with_gemini from the symptom_checker_service module inside the app.services package so it can be used in the current file.


def handle_symptom_analysis(data: dict) -> tuple: #efines a function that handles symptom analysis requests
    #the function handles the controller logic for symptom analysis, takes data (parsed JSON from the request) as input, and returns a tuple containing the response dictionary and HTTP status code
    """
    Controller logic for symptom analysis.

    Args:
        data: parsed JSON body from the request

    Returns:
        tuple: (response_dict, status_code)
    """

    # ---- Input Validation ----
    if not data: # Checks if the request body is empty.
        return {"msg": "Request body is required"}, 400 #Returns an error response.

    symptom_text = data.get("symptoms") #extracts the "symptoms" field from the JSON request

    if not symptom_text: # Checks if the "symptoms" field is missing.
        return {"msg": "Symptom text is required"}, 400

    if not isinstance(symptom_text, str): #Checks if the symptoms are a string.
        return {"msg": "Symptom text must be a string"}, 400 #Rejects invalid data type.

    symptom_text = symptom_text.strip() #Removes spaces from beginning and end.

    if len(symptom_text) < 3: #Checks if the text is too short.
        return {"msg": "Please describe your symptoms in more detail"}, 400 #Encourages the user to give more details.

    if len(symptom_text) > 2000: #Limits input to 2000 characters, to prevent abuse, prevent very large AI requests, protect server resources.
        return {"msg": "Symptom text is too long (max 2000 characters)"}, 400 #Returns error if too long.

    # ---- Call Service Layer ----
    try: #Starts a try block, This ensures that if the AI API fails, the application does not crash.
        print(f"Symptom received: {symptom_text}") #Logs the symptoms in the server console.
        print("--- Calling Gemini API... ---") #Log indicating that the AI API call is starting.

        ai_response = analyze_symptoms_with_gemini(symptom_text) #This calls the service function.

        if not ai_response: #Checks if the AI service returned empty output.
            return {"msg": "Empty response from AI service"}, 502 #an external service failed

        print("--- Gemini API call successful! ---") #Printed in the console if AI response is received successfully.

        return { #Now the API prepares the final JSON response.
            "reply": ai_response, #the AI-generated symptom analysis
            "symptom_input": symptom_text, #Returns the original symptoms sent by user.
            "disclaimer": "This is AI-generated guidance, not a medical diagnosis." #Medical Disclaimer
        }, 200 #200 means Success.

    except Exception as e: #If any error occurs in the try block.
        print(f"Gemini exception: {e}") #Prints the error in the server console.
        #Returns error response.
        return {
            "msg": "An internal error occurred while analyzing symptoms"
        }, 500 #500 = Internal Server Error
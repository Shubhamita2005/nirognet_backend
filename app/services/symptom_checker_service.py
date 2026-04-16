import google.generativeai as genai
from flask import current_app
from app.config.settings import GEMINI_API_KEY

# -------------------------------
# Configure Gemini API
# -------------------------------

api_key = GEMINI_API_KEY

FORCE_MOCK_MODE = False

if not api_key:
    FORCE_MOCK_MODE = True
    print("No API key found → using mock mode")
else:
    genai.configure(api_key=api_key)
    print("Gemini API configured successfully")


# -------------------------------
# Main Function
# -------------------------------

def analyze_symptoms_with_gemini(symptom_text: str) -> str:
    
    # Get model from Flask app
    model = getattr(current_app, "gemini_model", None)

    if not model:
        print("No Gemini model found → using mock")
        return generate_smart_response(symptom_text)

    # Try real Gemini API
    if not FORCE_MOCK_MODE:
        try:
            print("Using real Gemini API")

            prompt = f"""
You are an empathetic and cautious AI health assistant for NirogNet.

User's symptoms: "{symptom_text}"

Respond naturally with:
- empathy
- clarifying questions
- OTC medicine suggestions
- doctor recommendations
- urgency level
- disclaimer
"""

            response = model.generate_content(prompt)

            return response.text

        except Exception as e:
            print(f"API failed: {str(e)} → Falling back to mock")

    # Fallback mock response
    print("Using intelligent mock response")
    return generate_smart_response(symptom_text)


# -------------------------------
# Smart Mock Responses
# -------------------------------

def generate_smart_response(symptom_text: str) -> str:
    symptom_lower = symptom_text.lower()

    # Headache
    if 'head' in symptom_lower or 'migraine' in symptom_lower:
        return """I understand you're experiencing a headache. That can be really uncomfortable.

To help you better:
• How severe is the pain (1–10)?
• How long has it lasted?
• Any nausea or light sensitivity?

You may take Paracetamol (Dolo 650) if not allergic. Rest in a quiet place and stay hydrated.

Consult a doctor if it persists more than 2–3 days or worsens.

⚠️ This is not medical advice. Please consult a doctor if needed."""

    # Fever
    elif 'fever' in symptom_lower:
        return """I'm sorry to hear you have a fever.

• What is your temperature?
• How many days?
• Any cough or body pain?

Take Paracetamol, stay hydrated, and rest.

Consult a doctor if fever exceeds 103°F or lasts more than 3 days.

⚠️ Not a medical diagnosis."""

    # Chest pain (urgent)
    elif 'chest' in symptom_lower and 'pain' in symptom_lower:
        return """⚠️ Chest pain can be serious.

If you have:
• breathing difficulty
• sweating
• pain spreading to arm/jaw

👉 Seek immediate medical help or call emergency services.

Do NOT ignore chest pain.

⚠️ This is urgent guidance only."""

    # Default
    else:
        return f"""Thanks for sharing: "{symptom_text}"

Please provide:
• duration
• severity
• other symptoms

I recommend consulting a doctor for proper diagnosis.

⚠️ This is AI guidance, not medical advice."""
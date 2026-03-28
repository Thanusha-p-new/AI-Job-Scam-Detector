import pickle
from django.shortcuts import render

model = pickle.load(open('predictor/model.pkl', 'rb'))
vectorizer = pickle.load(open('predictor/vectorizer.pkl', 'rb'))

# def home(request):
#     result = None
#     risk = None
#     reasons = []

#     if request.method == 'POST':
#         text = request.POST.get('job_text', '')

#         # ✅ ONLY for empty input (basic requirement)
#         if text.strip() == "":
#             return render(request, 'index.html', {
#                 'result': "⚠️ Please enter job description",
#                 'risk': None,
#                 'reasons': []
#             })

#         # 🔍 ML Prediction
#         vector = vectorizer.transform([text])
#         prediction = model.predict(vector)[0]
#         proba = model.predict_proba(vector)[0][1]
#         risk = round(proba * 100, 2)

#         text_lower = text.lower()

#         # 🚨 Negative indicators (scam signals)
#         scam_words = ['fee', 'registration', 'whatsapp', 'earn money fast', 'urgent', 'no experience']

#         # ✅ Positive indicators (genuine signals)
#         good_words = ['company', 'experience', 'salary', 'role', 'responsibilities', 'qualification']

#         scam_count = 0
#         good_count = 0

#         # Check scam words
#         for word in scam_words:
#             if word in text_lower:
#                 reasons.append(f"Contains suspicious word: '{word}'")
#                 scam_count += 1

#         # Check good words
#         for word in good_words:
#             if word in text_lower:
#                 good_count += 1

#         # 🔥 FINAL DECISION LOGIC

#         if scam_count > 0:
#             prediction = 1
#             risk = max(risk, 80)
#             result = "❌ Fake Job"
#             reasons.append("Multiple scam indicators detected")

#         elif good_count >= 2:
#             result = "✅ Genuine Job"
#             reasons.append("Contains structured job details (role, experience, etc.)")
#             reasons.append("No strong scam signals detected")

#         else:
#             result = "⚠️ Suspicious / Unclear Job"
#             reasons.append("Not enough information to confirm legitimacy")
#             reasons.append("Lacks strong professional indicators")

#     return render(request, 'index.html', {
#         'result': result,
#         'risk': risk,
#         'reasons': reasons
#     })

def home(request):
    result = None
    risk = None
    reasons = []

    if request.method == 'POST':
        text = request.POST.get('job_text', '')

        if text.strip() != "":
            # ML Prediction
            vector = vectorizer.transform([text])
            prediction = model.predict(vector)[0]
            proba = model.predict_proba(vector)[0][1]
            risk = round(proba * 100, 2)

            # ⭐ Suspicious words (JUSTIFICATION)
            scam_words = ['fee', 'registration', 'whatsapp', 'earn money fast', 'urgent']

            for word in scam_words:
                if word in text.lower():
                    reasons.append("Found suspicious word: " + word)
                    prediction = 1
                    risk = max(risk, 80)

            # If genuine
            if prediction == 0:
                reasons.append("No suspicious words found")
                reasons.append("Looks like a professional job description")

            # Final result
            if prediction == 1:
                result = "❌ Fake Job"
            else:
                result = "✅ Genuine Job"

        else:
            result = "⚠️ Please enter job description"
            risk = 0

    return render(request, 'index.html', {
        'result': result,
        'risk': risk,
        'reasons': reasons
    })

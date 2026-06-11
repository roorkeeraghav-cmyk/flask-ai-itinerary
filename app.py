from flask import Flask, render_template, request
import google.genai as genai

print("App is starting...")

app = Flask(__name__)


API_KEY = ""

print("Using API key starting with:", API_KEY[:10])

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():

    source = request.form["source"]
    destination = request.form["destination"]
    budget = request.form["budget"]
    days = request.form["days"]
    interests = request.form["interests"]
    trip_type = request.form["trip_type"]

    client = genai.Client(api_key=API_KEY)

    prompt = f"""
Create a detailed travel itinerary in HTML format.

Use these sections:

<h2>Trip Summary</h2>
<h2>Tourist Attractions</h2>
<h2>Recommended Hotels</h2>
<h2>Day-wise Itinerary</h2>
<h2>Budget Breakdown</h2>
<h2>Food Suggestions</h2>
<h2>Packing List</h2>
<h2>Travel Tips</h2>

Source: {source}
Destination: {destination}
Budget Category: {budget}
Days: {days}
Interests: {interests}
Trip Type: {trip_type}

Requirements:

1. Give 5-10 tourist attractions with short descriptions.
2. Suggest 5 hotels according to the budget category.
3. Suggest famous local foods.
4. Create a packing list.
5. Give 5 travel tips.
6. Generate a realistic day-wise itinerary.
7. Include estimated expenses.
8. Make output attractive HTML.
"""

    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-flash-lite-latest",
        "gemini-3.5-flash"
    ]

    response = None

    for model in models:
        try:
            print(f"Trying model: {model}")

            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            print(f"Success with model: {model}")
            break

        except Exception as e:
            print(f"{model} failed: {e}")

    if response:
        plan = response.text

        plan = plan.replace("```html", "")
        plan = plan.replace("```", "")
        

        with open("trip_history.txt", "a", encoding="utf-8") as f:
            f.write("\n\n")
            f.write(f"Destination: {destination}\n")
            f.write(plan)

    else:
        plan = "All Gemini models are currently unavailable. Please try again in a few minutes."

    return render_template("result.html", plan=plan)


if __name__ == "__main__":
    app.run(debug=True)
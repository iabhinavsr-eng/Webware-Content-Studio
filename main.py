import logging
import os

from flask import Flask, render_template, request
from openai import OpenAI

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")


def get_openai_client():
    """Get OpenAI client, raising error if API key not configured."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)


def call_openai(system_prompt, user_prompt, model="gpt-4.1-mini"):
    """Call OpenAI API and return the model's text response."""
    client = get_openai_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content


@app.route("/", methods=["GET", "POST"])
def index():
    model_output = None
    error = None
    icp = ""
    uvp = ""
    prompt_instructions = ""
    model = "gpt-4.1-mini"

    if request.method == "POST":
        icp = request.form.get("icp", "").strip()
        uvp = request.form.get("uvp", "").strip()
        prompt_instructions = request.form.get("prompt_instructions", "").strip()
        model = request.form.get("model", "").strip() or "gpt-4.1-mini"

        if not prompt_instructions:
            error = "Please provide prompt instructions (system message)."
        else:
            try:
                user_message = f"Here is the current data:\n\nICP:\n{icp}\n\nUVP:\n{uvp}"
                model_output = call_openai(prompt_instructions, user_message, model)
            except Exception as e:
                error = str(e)
                logging.error(f"Error: {e}")

    return render_template(
        "index.html",
        model_output=model_output,
        error=error,
        icp=icp,
        uvp=uvp,
        prompt_instructions=prompt_instructions,
        model=model,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

import json
import logging
import os

from flask import Flask, render_template, request
from openai import OpenAI

from prompts import TOOL_BUILDERS, TOOL_NAMES

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

def get_openai_client():
    """Get OpenAI client, raising error if API key not configured."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set. Please configure it in your environment.")
    return OpenAI(api_key=api_key)


def call_openai(system_prompt, user_prompt, model="gpt-4.1-mini"):
    """Call OpenAI API and return the model's text response."""
    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        raise


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    is_json = False
    error = None
    selected_tool = "icp_uvp"
    form_data = {}

    if request.method == "POST":
        selected_tool = request.form.get("tool", "icp_uvp")
        
        form_data = {
            "business_name": request.form.get("business_name", "").strip(),
            "business_type": request.form.get("business_type", "").strip(),
            "target_audience": request.form.get("target_audience", "").strip(),
            "products_services_offered": request.form.get("products_services_offered", "").strip(),
            "service_areas": request.form.get("service_areas", "").strip(),
            "icp": request.form.get("icp", "").strip(),
            "uvp": request.form.get("uvp", "").strip(),
            "previous_pages": request.form.get("previous_pages", "").strip(),
            "requested_page_name": request.form.get("requested_page_name", "").strip(),
            "requested_page_type": request.form.get("requested_page_type", "").strip(),
            "other_pages_json": request.form.get("other_pages_json", "").strip(),
            "batch_pages": request.form.get("batch_pages", "").strip(),
            "new_gbp_category": request.form.get("new_gbp_category", "").strip(),
        }

        builder_func = TOOL_BUILDERS.get(selected_tool)
        if builder_func:
            try:
                prompts = builder_func(form_data)
                raw_result = call_openai(prompts["system"], prompts["user"])
                
                try:
                    parsed = json.loads(raw_result)
                    result = json.dumps(parsed, indent=2)
                    is_json = True
                except json.JSONDecodeError:
                    result = raw_result
                    is_json = False
                    
            except Exception as e:
                error = str(e)
                logging.error(f"Error processing request: {e}")
        else:
            error = f"Unknown tool: {selected_tool}"

    return render_template(
        "index.html",
        tool_names=TOOL_NAMES,
        selected_tool=selected_tool,
        result=result,
        is_json=is_json,
        error=error,
        form_data=form_data,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

import json
import logging
import os

from flask import Flask, render_template, request
from openai import OpenAI

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

DEFAULT_HOMEPAGE_PROMPT = """SYSTEM PROMPT (Homepage Content Builder)

Role:
You are an expert website copywriter specialising in SEO-optimised homepage content, using structured inputs (ICP, UVP, and page SEO data) to produce clear, persuasive, conversion-focused content.

Rules (MUST follow all):
Language & Formatting

Use British English.

Output standard ASCII only (no curly quotes, no emojis).

Normalise whitespace (no double spaces, no trailing spaces).

Do not mention phone numbers, emails, URLs, or the business address.

Do not write the business name more than once in the entire content unless the input instructs otherwise.

No hype language (e.g., "world-class", "best ever").

Tone: professional, direct, trustworthy.

SEO & Content Requirements

Use the provided H1, keywords, ICP, UVP, and any SEO page structure.

Do not invent new services, locations, or claims.

Do not include geographic references unless they appear in the service areas list.

Naturally weave relevant keywords into the content without over-optimising.

DO NOT include keywords as a list; integrate them in context.

Homepage Structure (MUST output all sections):

Your output must be valid JSON with these exact keys:

{
  "hero_section": {
    "h1": "Main headline",
    "paragraph": "2-3 sentences explaining what the business does and who it helps. End with a CTA."
  },
  "blog_guide_section": {
    "headline": "Question-style headline about property maintenance",
    "paragraph": "4-6 sentences about how the guide helps customers."
  },
  "value_prop_1": {
    "headline": "Short benefit headline (2-4 words)",
    "paragraph": "2-3 sentences about this benefit.",
    "testimonial_quote": "1 sentence testimonial",
    "testimonial_name": "First name + last initial"
  },
  "value_prop_2": {
    "headline": "Short benefit headline",
    "paragraph": "2-3 sentences about this benefit.",
    "testimonial_quote": "1 sentence testimonial",
    "testimonial_name": "First name + last initial"
  },
  "value_prop_3": {
    "headline": "Short benefit headline",
    "paragraph": "2-3 sentences about this benefit.",
    "testimonial_quote": "1 sentence testimonial",
    "testimonial_name": "First name + last initial"
  },
  "final_cta_section": {
    "headline": "Question encouraging action",
    "paragraph": "2-3 sentences about getting started.",
    "button_text": "CTA button text"
  }
}"""

DEFAULT_SERVICE_PAGE_PROMPT = """Role:
You are an expert SEO website copywriter.
Your job is to generate full service page content using the ICP, UVP, and SEO page structure provided.
Your output must be strictly formatted JSON, use British English, and follow all constraints.

RULES (MUST FOLLOW ALL):
Language & Style

British English only.

Standard ASCII only (no curly quotes, emojis, special characters).

Professional, informative, calm tone - no exaggerated claims.

Do not repeat the business name more than once unless provided in the structure.

Do not include: phone numbers, emails, URLs, pricing, owner names, awards, claims of superiority.

No location mentions unless explicitly present in the service_areas input.

SEO Constraints

Use the provided H1 and naturally integrate relevant keywords.

Do not keyword-stuff.

Do not produce a list of keywords - integrate them into prose.

Only use services/products explicitly provided.

Do not invent new service offerings.

Structural Requirements (MUST output ALL sections):

Your JSON output must include the following keys:

{
  "hero_section": {
    "h1": "Main headline from page_structure",
    "intro": "2-3 sentence intro summarising the service and its value.",
    "cta": "Short CTA sentence (e.g., Get started today)"
  },
  "service_overview_section": {
    "paragraphs": ["Paragraph 1", "Paragraph 2", "Paragraph 3"]
  },
  "key_benefits_section": [
    "Benefit 1: 1-2 sentences",
    "Benefit 2: 1-2 sentences",
    "Benefit 3: 1-2 sentences"
  ],
  "process_section": [
    {"title": "Step 1 title", "description": "1-2 sentence explanation"},
    {"title": "Step 2 title", "description": "1-2 sentence explanation"},
    {"title": "Step 3 title", "description": "1-2 sentence explanation"}
  ],
  "use_cases_section": [
    "Use case 1: 1-2 sentences",
    "Use case 2: 1-2 sentences",
    "Use case 3: 1-2 sentences"
  ],
  "faq_section": [
    {"question": "FAQ question 1", "answer": "2-3 sentence answer"},
    {"question": "FAQ question 2", "answer": "2-3 sentence answer"},
    {"question": "FAQ question 3", "answer": "2-3 sentence answer"}
  ],
  "final_cta_section": {
    "paragraph": "2-3 sentence closing encouraging the user to take the next step."
  }
}"""

DEFAULT_SERVICE_AREA_PROMPT = """SYSTEM PROMPT - Location Page Content Builder (2025 Google-Compliant)

You are an expert SEO website copywriter specialising in local service pages.
Your job is to generate high-quality, location-specific content that follows Google's 2025 Helpful Content, Local SEO, and E-E-A-T guidelines.

Your output MUST be strict JSON, British English, standard ASCII, and follow ALL rules below.

GLOBAL RULES (MUST FOLLOW ALL)
Language & Writing Style

British English only.

Standard ASCII only (no curly quotes, emojis, special characters).

Tone: professional, trustworthy, concise, clearly helpful.

No hype (e.g., "best", "world-class", "#1").

Mention the business name no more than once.

Do NOT include:

phone numbers, emails, URLs, pricing, awards or guarantees, unverifiable claims, owner names

Google Helpful Content (2025) Requirements

Your writing MUST:

Be user-first, not keyword-first.

Address real customer needs and problems specific to this location.

Provide unique, non-duplicated insights - NO template repetition.

Demonstrate local expertise:

local conditions, common issues unique to the area, realistic examples, environmental, regulatory, or property-specific context

Include helpful, educational information that informs users.

Local SEO Rules (2025)

Use the location name ONLY where natural, 1-3 times in the entire page.

Do NOT city-stuff.

Use real local context - NOT fluffy "we proudly serve the community" lines.

Do NOT invent new neighbourhoods or service areas.

NEVER list multiple cities inside paragraphs.

E-E-A-T Requirements

Show experience, expertise, and understanding, such as:

Professional process explanation, safety or quality considerations, realistic local use cases, customer scenarios, common local issues related to the service

OUTPUT FORMAT (JSON):

{
  "hero_section": {
    "h1": "Location-specific headline",
    "intro": "2-3 sentences about the service in this specific location.",
    "cta": "Short CTA sentence"
  },
  "local_context_section": {
    "headline": "Why [Location] Properties Need This Service",
    "paragraphs": ["Paragraph about local conditions", "Paragraph about common local issues"]
  },
  "service_overview_section": {
    "paragraphs": ["What the service includes for this area", "Who benefits from it locally"]
  },
  "key_benefits_section": [
    "Location-specific benefit 1",
    "Location-specific benefit 2",
    "Location-specific benefit 3"
  ],
  "process_section": [
    {"title": "Step 1", "description": "Explanation"},
    {"title": "Step 2", "description": "Explanation"},
    {"title": "Step 3", "description": "Explanation"}
  ],
  "faq_section": [
    {"question": "Location-relevant FAQ 1", "answer": "2-3 sentence answer"},
    {"question": "Location-relevant FAQ 2", "answer": "2-3 sentence answer"},
    {"question": "Location-relevant FAQ 3", "answer": "2-3 sentence answer"}
  ],
  "final_cta_section": {
    "paragraph": "2-3 sentences encouraging local customers to take action."
  }
}"""


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


def get_default_prompt(page_type):
    """Get default prompt based on page type."""
    if page_type == "service_page":
        return DEFAULT_SERVICE_PAGE_PROMPT
    elif page_type == "service_area":
        return DEFAULT_SERVICE_AREA_PROMPT
    return DEFAULT_HOMEPAGE_PROMPT


@app.route("/", methods=["GET", "POST"])
def index():
    model_output = None
    parsed_output = None
    error = None
    icp = ""
    uvp = ""
    prompt_instructions = ""
    page_type = "homepage"
    model = "gpt-4.1-mini"

    if request.method == "POST":
        icp = request.form.get("icp", "").strip()
        uvp = request.form.get("uvp", "").strip()
        prompt_instructions = request.form.get("prompt_instructions", "").strip()
        page_type = request.form.get("page_type", "homepage").strip()
        model = request.form.get("model", "").strip() or "gpt-4.1-mini"

        if not prompt_instructions:
            prompt_instructions = get_default_prompt(page_type)

        try:
            user_message = f"Here is the current data:\n\nICP:\n{icp}\n\nUVP:\n{uvp}"
            model_output = call_openai(prompt_instructions, user_message, model)
            
            # Try to parse as JSON for visual display
            try:
                # Clean up potential markdown code blocks
                clean_output = model_output.strip()
                if clean_output.startswith("```json"):
                    clean_output = clean_output[7:]
                if clean_output.startswith("```"):
                    clean_output = clean_output[3:]
                if clean_output.endswith("```"):
                    clean_output = clean_output[:-3]
                clean_output = clean_output.strip()
                
                parsed_output = json.loads(clean_output)
            except json.JSONDecodeError:
                # If not valid JSON, just show raw output
                parsed_output = None
                
        except Exception as e:
            error = str(e)
            logging.error(f"Error: {e}")

    return render_template(
        "index.html",
        model_output=model_output,
        parsed_output=parsed_output,
        error=error,
        icp=icp,
        uvp=uvp,
        prompt_instructions=prompt_instructions,
        page_type=page_type,
        default_prompt=get_default_prompt(page_type),
        model=model,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

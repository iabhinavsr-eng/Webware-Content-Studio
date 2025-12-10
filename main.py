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
    "intro_paragraph": "4-6 sentence intro explaining the service, who it helps, and the value provided. This should be comprehensive."
  },
  "service_overview_section": {
    "paragraph_1": "3-4 sentences about the service approach and methodology.",
    "paragraph_2": "3-4 sentences about professionalism, communication, and what to expect.",
    "cta_button_text": "Short CTA text (e.g., Request a no-obligation quote now)"
  },
  "benefits_section": [
    {"headline": "Short benefit headline (2-4 words)", "description": "2-3 sentences explaining this benefit."},
    {"headline": "Short benefit headline (2-4 words)", "description": "2-3 sentences explaining this benefit."},
    {"headline": "Short benefit headline (2-4 words)", "description": "2-3 sentences explaining this benefit."},
    {"headline": "Short benefit headline (2-4 words)", "description": "2-3 sentences explaining this benefit."}
  ],
  "service_details": [
    {
      "title": "Service detail title",
      "paragraph_1": "2-3 sentences about this specific service aspect.",
      "paragraph_2": "2-3 sentences with more details.",
      "bullets": ["Bullet point 1", "Bullet point 2", "Bullet point 3", "Bullet point 4", "Bullet point 5"]
    },
    {
      "title": "Service detail title",
      "paragraph_1": "2-3 sentences about this specific service aspect.",
      "paragraph_2": "2-3 sentences with more details.",
      "bullets": ["Bullet point 1", "Bullet point 2", "Bullet point 3", "Bullet point 4", "Bullet point 5"]
    },
    {
      "title": "Service detail title",
      "paragraph_1": "2-3 sentences about this specific service aspect.",
      "paragraph_2": "2-3 sentences with more details.",
      "bullets": ["Bullet point 1", "Bullet point 2", "Bullet point 3", "Bullet point 4", "Bullet point 5"]
    },
    {
      "title": "Service detail title",
      "paragraph_1": "2-3 sentences about this specific service aspect.",
      "paragraph_2": "2-3 sentences with more details.",
      "bullets": ["Bullet point 1", "Bullet point 2", "Bullet point 3", "Bullet point 4", "Bullet point 5"]
    },
    {
      "title": "Service detail title",
      "paragraph_1": "2-3 sentences about this specific service aspect.",
      "paragraph_2": "2-3 sentences with more details.",
      "bullets": ["Bullet point 1", "Bullet point 2", "Bullet point 3", "Bullet point 4", "Bullet point 5"]
    }
  ],
  "faq_section": [
    {"question": "FAQ question 1", "answer": "2-3 sentence answer"},
    {"question": "FAQ question 2", "answer": "2-3 sentence answer"},
    {"question": "FAQ question 3", "answer": "2-3 sentence answer"},
    {"question": "FAQ question 4", "answer": "2-3 sentence answer"}
  ],
  "final_cta_section": {
    "headline": "Compelling headline encouraging action",
    "paragraph": "2-3 sentence closing about getting started.",
    "button_text": "CTA button text"
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
    "h1": "Location-specific headline including business name and location",
    "intro_paragraph": "3-4 sentences about the service in this specific location and how it helps local customers."
  },
  "overview_section": {
    "headline": "Compelling headline about the service in this location",
    "paragraph": "4-5 sentences about how the service helps local customers, what they can expect, and the value provided.",
    "cta_link_text": "Short CTA text (e.g., Contact us to begin)"
  },
  "main_content_section": {
    "headline": "Headline about the approach or methodology",
    "paragraph": "5-6 sentences explaining the detailed approach, what makes the service valuable, and how it addresses local customer needs."
  },
  "services_list_section": [
    {"title": "Service 1 Name", "description": "2-3 sentences describing this specific service and its benefits."},
    {"title": "Service 2 Name", "description": "2-3 sentences describing this specific service and its benefits."},
    {"title": "Service 3 Name", "description": "2-3 sentences describing this specific service and its benefits."}
  ],
  "benefits_section": {
    "headline": "Headline about support or expertise",
    "paragraph": "2-3 sentences introducing the benefits.",
    "bullets": [
      "Benefit bullet 1",
      "Benefit bullet 2",
      "Benefit bullet 3",
      "Benefit bullet 4",
      "Benefit bullet 5",
      "Benefit bullet 6",
      "Benefit bullet 7"
    ]
  },
  "newsletter_cta_section": {
    "headline": "Headline encouraging subscription or ongoing engagement",
    "paragraph": "2-3 sentences about staying informed or getting updates.",
    "button_text": "CTA button text (e.g., Subscribe Now)"
  }
}"""

DEFAULT_SERVICES_OVERVIEW_PROMPT = """SYSTEM PROMPT - Services Overview Page Builder

Role:
You are an expert SEO website copywriter specialising in services overview pages.
Your job is to generate a comprehensive services landing page that showcases multiple service offerings.

RULES (MUST FOLLOW ALL):
Language & Style

British English only.

Standard ASCII only (no curly quotes, emojis, special characters).

Professional, informative, trustworthy tone.

Mention the business name no more than once.

Do NOT include: phone numbers, emails, URLs, pricing, awards, unverifiable claims.

SEO & Content Requirements

Use the provided ICP and UVP to inform the content.

Naturally integrate the location into headlines and content.

Each service description should be unique and compelling.

Focus on benefits and value to the customer.

OUTPUT FORMAT (JSON):

{
  "hero_section": {
    "h1": "[Service Category] Services in [City], Delivered with Skill and Transparency",
    "intro_paragraph": "3-4 sentences describing what services the business provides, the location served, and the key value proposition."
  },
  "services_section": {
    "headline": "Our [Service Category] Services in [City]",
    "services": [
      {"title": "Service 1 Name", "description": "4-6 sentences describing this service, what it includes, the process, and benefits to customers."},
      {"title": "Service 2 Name", "description": "4-6 sentences describing this service, what it includes, the process, and benefits to customers."},
      {"title": "Service 3 Name", "description": "4-6 sentences describing this service, what it includes, the process, and benefits to customers."},
      {"title": "Service 4 Name", "description": "4-6 sentences describing this service, what it includes, the process, and benefits to customers."},
      {"title": "Service 5 Name", "description": "4-6 sentences describing this service, what it includes, the process, and benefits to customers."}
    ]
  },
  "cta_banner": {
    "headline": "Ready to [action verb] your [benefit/outcome] with expertise?",
    "paragraph": "2-3 sentences about staying informed, getting updates on services, or encouraging consultation.",
    "button_text": "Request a private consultation"
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
        temperature=0.2,
        max_tokens=16000
    )
    return response.choices[0].message.content


def get_default_prompt(page_type):
    """Get default prompt based on page type."""
    if page_type == "service_page":
        return DEFAULT_SERVICE_PAGE_PROMPT
    elif page_type == "service_area":
        return DEFAULT_SERVICE_AREA_PROMPT
    elif page_type == "services_overview":
        return DEFAULT_SERVICES_OVERVIEW_PROMPT
    return DEFAULT_HOMEPAGE_PROMPT


@app.route("/", methods=["GET", "POST"])
def index():
    model_output = None
    parsed_output = None
    error = None
    icp = ""
    uvp = ""
    city = ""
    service_name = ""
    prompt_instructions = ""
    page_type = "homepage"
    model = "gpt-4.1-mini"

    if request.method == "POST":
        icp = request.form.get("icp", "").strip()
        uvp = request.form.get("uvp", "").strip()
        city = request.form.get("city", "").strip()
        service_name = request.form.get("service_name", "").strip()
        prompt_instructions = request.form.get("prompt_instructions", "").strip()
        page_type = request.form.get("page_type", "homepage").strip()
        model = request.form.get("model", "").strip() or "gpt-4.1-mini"

        if not prompt_instructions:
            prompt_instructions = get_default_prompt(page_type)

        try:
            # Build user message based on page type
            if page_type == "service_area" and city:
                user_message = f"""Here is the current data:

TARGET LOCATION: {city}

Important: Generate content specifically for {city}. Include real local context such as:
- Local climate and weather patterns that affect property maintenance
- Common property types and issues in the area
- Regional considerations (bylaws, seasonal challenges, typical property sizes)
- Neighbourhood characteristics if relevant

ICP:
{icp}

UVP:
{uvp}"""
            elif page_type == "service_page" and service_name:
                user_message = f"""Here is the current data:

TARGET SERVICE: {service_name}

Important: Generate content specifically for the {service_name} service. Focus on:
- What this specific service entails
- Benefits specific to this service
- Common customer questions about this service
- Process and methodology for this service

ICP:
{icp}

UVP:
{uvp}"""
            elif page_type == "services_overview" and city:
                user_message = f"""Here is the current data:

TARGET LOCATION: {city}

Important: Generate a services overview page for {city}. Create compelling descriptions for 5 different services that this business offers. Each service should:
- Have a clear, specific title
- Include a detailed 4-6 sentence description
- Focus on customer benefits and outcomes
- Be unique and not repeat content from other services

ICP:
{icp}

UVP:
{uvp}"""
            else:
                user_message = f"Here is the current data:\n\nICP:\n{icp}\n\nUVP:\n{uvp}"
            
            model_output = call_openai(prompt_instructions, user_message, model)
            
            # Try to parse as JSON for visual display
            try:
                # Clean up potential markdown code blocks
                clean_output = (model_output or "").strip()
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

    # Extract prose portion (before OUTPUT FORMAT or Homepage Structure)
    prompt_instructions_prose = prompt_instructions
    for marker in ["OUTPUT FORMAT (JSON):", "Homepage Structure (MUST output all sections):", "Structural Requirements (MUST output ALL sections):"]:
        if marker in prompt_instructions:
            prompt_instructions_prose = prompt_instructions.split(marker)[0].strip()
            break
    
    return render_template(
        "index.html",
        model_output=model_output,
        parsed_output=parsed_output,
        error=error,
        icp=icp,
        uvp=uvp,
        city=city,
        service_name=service_name,
        prompt_instructions=prompt_instructions,
        prompt_instructions_prose=prompt_instructions_prose,
        page_type=page_type,
        default_prompt=get_default_prompt(page_type),
        model=model,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

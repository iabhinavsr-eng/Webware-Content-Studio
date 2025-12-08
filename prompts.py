"""
SEO Prompt Library - Prompt Builder Functions

Each function takes a data dict and returns a dict with 'system' and 'user' keys
for OpenAI chat completion.
"""


def build_icp_uvp_prompt(data):
    """Build prompt for ICP & UVP Generator tool."""
    system = """You are an expert marketing strategist specializing in local SEO and business positioning.
Your task is to analyze a business and generate:
1. Ideal Customer Profile (ICP) - detailed persona of the target customer
2. Unique Value Proposition (UVP) - what makes this business stand out

Respond in valid JSON format with the following structure:
{
    "icp": {
        "demographics": {...},
        "psychographics": {...},
        "pain_points": [...],
        "goals": [...],
        "buying_behavior": {...}
    },
    "uvp": {
        "headline": "...",
        "subheadline": "...",
        "key_differentiators": [...],
        "proof_points": [...]
    }
}"""

    user = f"""Analyze this business and generate their Ideal Customer Profile (ICP) and Unique Value Proposition (UVP):

Business Name: {data.get('business_name', 'N/A')}
Business Type: {data.get('business_type', 'N/A')}
Target Audience: {data.get('target_audience', 'N/A')}
Products/Services Offered: {data.get('products_services_offered', 'N/A')}
Service Areas: {data.get('service_areas', 'N/A')}

Generate a comprehensive ICP and compelling UVP based on this information."""

    return {"system": system, "user": user}


def build_gbp_builder_prompt(data):
    """Build prompt for GBP Categories & Description Builder tool."""
    system = """You are a Google Business Profile optimization expert.
Your task is to recommend the best GBP categories and write an optimized business description.

Respond in valid JSON format with the following structure:
{
    "primary_category": "...",
    "secondary_categories": [...],
    "business_description": "...",
    "seo_keywords_used": [...],
    "optimization_tips": [...]
}

The description should be 750 characters max, keyword-rich, and compelling."""

    user = f"""Create optimized Google Business Profile categories and description for:

Business Name: {data.get('business_name', 'N/A')}
Business Type: {data.get('business_type', 'N/A')}
Target Audience: {data.get('target_audience', 'N/A')}
Products/Services Offered: {data.get('products_services_offered', 'N/A')}
Service Areas: {data.get('service_areas', 'N/A')}

ICP Data (if available): {data.get('icp', 'Not provided')}
UVP Data (if available): {data.get('uvp', 'Not provided')}

Recommend the best primary and secondary GBP categories, and write an SEO-optimized business description."""

    return {"system": system, "user": user}


def build_gbp_keywords_prompt(data):
    """Build prompt for New GBP Category Keywords tool."""
    system = """You are an SEO keyword research expert specializing in local search and Google Business Profile optimization.
Your task is to generate comprehensive keyword lists for a specific GBP category.

Respond in valid JSON format with the following structure:
{
    "category": "...",
    "primary_keywords": [...],
    "long_tail_keywords": [...],
    "local_keywords": [...],
    "question_keywords": [...],
    "service_keywords": [...],
    "keyword_clusters": {...}
}"""

    user = f"""Generate comprehensive SEO keywords for this GBP category:

New GBP Category: {data.get('new_gbp_category', 'N/A')}
Business Name: {data.get('business_name', 'N/A')}
Business Type: {data.get('business_type', 'N/A')}
Service Areas: {data.get('service_areas', 'N/A')}
Products/Services Offered: {data.get('products_services_offered', 'N/A')}

Generate a comprehensive list of keywords optimized for this category, including local variations for the service areas."""

    return {"system": system, "user": user}


def build_site_structure_prompt(data):
    """Build prompt for Full Site Structure SEO Builder tool."""
    system = """You are a senior SEO architect and website strategist.
Your task is to design a complete website structure optimized for SEO and user experience.

Respond in valid JSON format with the following structure:
{
    "site_structure": {
        "homepage": {...},
        "main_pages": [...],
        "service_pages": [...],
        "location_pages": [...],
        "blog_categories": [...]
    },
    "page_details": [
        {
            "page_name": "...",
            "page_type": "...",
            "url_slug": "...",
            "h1": "...",
            "meta_title": "...",
            "meta_description": "...",
            "target_keywords": [...],
            "content_outline": [...]
        }
    ],
    "internal_linking_strategy": {...},
    "priority_order": [...]
}"""

    user = f"""Design a complete SEO-optimized website structure for:

Business Name: {data.get('business_name', 'N/A')}
Business Type: {data.get('business_type', 'N/A')}
Target Audience: {data.get('target_audience', 'N/A')}
Products/Services Offered: {data.get('products_services_offered', 'N/A')}
Service Areas: {data.get('service_areas', 'N/A')}

ICP Data (if available): {data.get('icp', 'Not provided')}
UVP Data (if available): {data.get('uvp', 'Not provided')}

Create a comprehensive site structure with all necessary pages, proper hierarchy, and SEO metadata for each page."""

    return {"system": system, "user": user}


def build_single_page_prompt(data):
    """Build prompt for Single Page SEO Regenerator tool."""
    system = """You are an SEO content strategist specializing in on-page optimization.
Your task is to generate or regenerate complete SEO elements for a single page.

Respond in valid JSON format with the following structure:
{
    "page_name": "...",
    "page_type": "...",
    "url_slug": "...",
    "h1": "...",
    "h2_suggestions": [...],
    "meta_title": "...",
    "meta_description": "...",
    "target_keywords": {
        "primary": "...",
        "secondary": [...],
        "lsi_keywords": [...]
    },
    "content_outline": [...],
    "internal_linking_suggestions": [...],
    "schema_markup_type": "...",
    "call_to_action": "..."
}"""

    user = f"""Generate complete SEO elements for this page:

Requested Page Name: {data.get('requested_page_name', 'N/A')}
Requested Page Type: {data.get('requested_page_type', 'N/A')}

Business Context:
- Business Name: {data.get('business_name', 'N/A')}
- Business Type: {data.get('business_type', 'N/A')}
- Target Audience: {data.get('target_audience', 'N/A')}
- Products/Services: {data.get('products_services_offered', 'N/A')}
- Service Areas: {data.get('service_areas', 'N/A')}

Other Pages on Site (for internal linking): {data.get('other_pages_json', 'Not provided')}

ICP Data: {data.get('icp', 'Not provided')}
UVP Data: {data.get('uvp', 'Not provided')}

Generate comprehensive SEO elements for this page that align with the site structure and business goals."""

    return {"system": system, "user": user}


def build_batch_regenerator_prompt(data):
    """Build prompt for SEO Keyword Recheck / Batch Regenerator tool."""
    system = """You are an SEO audit and optimization specialist.
Your task is to review and regenerate SEO elements for multiple pages to ensure consistency and optimization.

Respond in valid JSON format with the following structure:
{
    "audit_summary": {
        "pages_reviewed": 0,
        "issues_found": [...],
        "recommendations": [...]
    },
    "regenerated_pages": [
        {
            "page_name": "...",
            "original_issues": [...],
            "h1": "...",
            "meta_title": "...",
            "meta_description": "...",
            "target_keywords": [...],
            "improvements_made": [...]
        }
    ],
    "keyword_overlap_analysis": {...},
    "cannibalization_warnings": [...],
    "priority_fixes": [...]
}"""

    user = f"""Review and regenerate SEO elements for these pages:

Pages to Review/Regenerate:
{data.get('batch_pages', 'No pages provided')}

Previous Pages Context:
{data.get('previous_pages', 'Not provided')}

Business Context:
- Business Name: {data.get('business_name', 'N/A')}
- Business Type: {data.get('business_type', 'N/A')}
- Target Audience: {data.get('target_audience', 'N/A')}
- Products/Services: {data.get('products_services_offered', 'N/A')}
- Service Areas: {data.get('service_areas', 'N/A')}

ICP Data: {data.get('icp', 'Not provided')}
UVP Data: {data.get('uvp', 'Not provided')}

Audit these pages for SEO issues, check for keyword cannibalization, and regenerate optimized elements for each page."""

    return {"system": system, "user": user}


TOOL_BUILDERS = {
    "icp_uvp": build_icp_uvp_prompt,
    "gbp_builder": build_gbp_builder_prompt,
    "gbp_keywords": build_gbp_keywords_prompt,
    "site_structure": build_site_structure_prompt,
    "single_page": build_single_page_prompt,
    "batch_regenerator": build_batch_regenerator_prompt,
}

TOOL_NAMES = {
    "icp_uvp": "ICP & UVP Generator",
    "gbp_builder": "GBP Categories & Description Builder",
    "gbp_keywords": "New GBP Category Keywords",
    "site_structure": "Full Site Structure SEO Builder",
    "single_page": "Single Page SEO Regenerator",
    "batch_regenerator": "SEO Keyword Recheck / Batch Regenerator",
}

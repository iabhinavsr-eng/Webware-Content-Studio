# SEO Prompt Library

A Flask-based web application that helps generate SEO-optimized content using AI-powered tools.

## Overview

This application provides a library of 6 specialized SEO tools powered by OpenAI's GPT-4.1-mini model:

1. **ICP & UVP Generator** - Creates Ideal Customer Profiles and Unique Value Propositions
2. **GBP Categories & Description Builder** - Optimizes Google Business Profile content
3. **New GBP Category Keywords** - Generates keyword lists for GBP categories
4. **Full Site Structure SEO Builder** - Designs complete website architecture
5. **Single Page SEO Regenerator** - Creates SEO elements for individual pages
6. **SEO Keyword Recheck / Batch Regenerator** - Audits and regenerates multiple pages

## Features

- **Tool-specific field visibility** - Shows only relevant form fields for each tool
- **Preset templates** - Quick-start templates for 8 common business types (plumber, dentist, restaurant, lawyer, realtor, HVAC, salon, fitness)
- **JSON validation** - Real-time validation with error highlighting for JSON input fields
- **Export functionality** - Copy to clipboard or download outputs as JSON files
- **Response history** - Database-backed storage of all generations with view/download capabilities

## Project Structure

```
├── main.py              # Flask routes and OpenAI integration
├── app.py               # Flask app configuration and database setup
├── models.py            # SQLAlchemy models (GenerationHistory)
├── prompts.py           # Prompt builder functions for each SEO tool
├── templates/
│   └── index.html       # Main UI template with form and outputs
└── design_guidelines.md # Frontend design specifications
```

## Environment Variables

- `OPENAI_API_KEY` - Required for OpenAI API access
- `SESSION_SECRET` - Flask session secret
- `DATABASE_URL` - PostgreSQL database connection

## Technical Stack

- **Backend**: Python 3.11, Flask, Flask-SQLAlchemy
- **Database**: PostgreSQL (for response history)
- **AI**: OpenAI GPT-4.1-mini with temperature=0.2 for consistent outputs
- **Frontend**: HTML/CSS with vanilla JavaScript, Inter font, JetBrains Mono for code

## Running the Application

The application runs on port 5000 using Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

## Recent Changes

- **2024-12-08**: Initial implementation with all 6 SEO tools
- **2024-12-08**: Added tool-specific field visibility, presets, JSON validation
- **2024-12-08**: Implemented response history with PostgreSQL persistence
- **2024-12-08**: Added export/download functionality for outputs

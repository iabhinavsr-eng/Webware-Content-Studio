# Prompt Tester

A minimal Flask web application for testing prompts with OpenAI's API.

## Overview

This is a simple prompt tester where you can:
1. Paste your ICP (Ideal Customer Profile)
2. Paste your UVP (Unique Value Proposition)
3. Enter your prompt/instructions (system message)
4. Optionally select a model (defaults to gpt-4.1-mini)
5. Click "Run Prompt" to see the model's response

## Project Structure

```
├── main.py              # Flask app with OpenAI integration
├── templates/
│   └── index.html       # Main UI template
└── design_guidelines.md # Frontend design specifications
```

## Environment Variables

- `OPENAI_API_KEY` - Required for OpenAI API access
- `SESSION_SECRET` - Flask session secret

## Running the Application

The application runs on port 5000 using Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 --reload main:app
```

## How It Works

1. The system message is your `prompt_instructions`
2. The user message is built as:
   ```
   Here is the current data:
   
   ICP:
   {your icp}
   
   UVP:
   {your uvp}
   ```
3. The response is displayed below the form
4. Your inputs are preserved so you can tweak and run again

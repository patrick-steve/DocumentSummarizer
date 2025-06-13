import gradio as gr
import requests
import pymupdf

GAIANET_API_KEY = "gaia-MTczYWY3MTYtMjgyMy00ZGQ4LTg0NTUtY2M3OTQ3MDFkNTI4-oUcV1uFeoib0iNLY"

url = "https://llama.gaia.domains/v1/chat/completions"

headers = {
    "Authorization": "Bearer " + GAIANET_API_KEY,
    "Content-Type": "application/json"
}

SYSTEM_PROMPT = """You are an expert document summarizer. Your role is to create clear, accurate, and useful summaries of documents while maintaining the original meaning and key information.

## Core Principles:
- **Accuracy**: Never add information not present in the original document
- **Clarity**: Use clear, concise language accessible to the intended audience
- **Completeness**: Capture all essential points while eliminating redundancy
- **Structure**: Organize information logically and coherently

## Summary Guidelines:
1. **Length**: Aim for 15-25% of the original document length unless specified otherwise
2. **Key Elements**: Always include:
   - Main thesis or purpose
   - Key arguments, findings, or conclusions
   - Important supporting evidence or data
   - Actionable items or recommendations (if present)
3. **Structure**: Use clear paragraphs or bullet points as appropriate
4. **Tone**: Match the formality level of the original document

## Process:
1. Read the entire document first
2. Identify the document type (report, article, memo, etc.) and adjust approach accordingly
3. Extract main themes and supporting details
4. Organize information by importance and logical flow
5. Write in your own words while preserving technical terms when necessary

## What to Exclude:
- Excessive examples (keep 1-2 of the most illustrative)
- Repetitive information
- Minor details that don't support main points
- Filler content or transitional phrases

## Output Format:
Provide a well-structured summary in the form of a paragraph."""

def summarize_from_file(file):
    text = ""
    with pymupdf.open(file.name) as doc:
        for page in doc:
            pg_text = page.get_text()
            print(pg_text)
            text += pg_text

    return summarize_text_from_gaianet(text)

def summarize_text_from_gaianet(text):
    data = {
        "messages": [{"role":"system", "content": SYSTEM_PROMPT}, {"role":"user", "content": "Summarize this text: " + text}],
    }

    print(data)

    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

with gr.Blocks() as app:
    gr.Markdown("# 📄 AI Document Summarizer\nUpload a PDF or paste text below to get a summary.")
    
    with gr.Tab("Summarize PDF"):
        input_file = gr.File(label="Upload PDF", file_types=[".pdf"])
        output_text = gr.Textbox(label="Summary", lines=10)
        summarize_button = gr.Button("Summarize PDF")
        summarize_button.click(fn=summarize_from_file, inputs=[input_file], outputs=[output_text])

app.launch()
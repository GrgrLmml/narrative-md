GEN_QUESTIONNAIRE_PROMPT = """
"You are tasked with transforming a series of questionnaire questions into a structured JSON format, adhering closely to a specified schema. Each question needs to be categorized by its type (e.g., open, boolean, number, list, multiple choice) and encapsulated within a JSON object as shown in the example structure below:

{"questions": [
      {"question": "What is your reason for coming today?", "kind": "open"},
      {"question": "Are you exercising often?", "kind": "boolean"},
      {"question": "How often did you exercise last week?", "kind": "number", "condition": "previous answer was 'yes'"},
      {"question": "How did your performance change last month?", "kind": "multiple choice", "options": ["stable", "lost weight", "gained weight"]},
      {"question": "What kind of dietary supplement are taking regularly", "kind": "list"}
    ]
}

Please follow these guidelines:

Identify and classify: Determine the type of each question as open, boolean, number, list, or multiple choice.
Options for multiple choice: Where applicable, list all potential answers under an 'options' key.
Ensure completeness and correctness: Make sure that every question is represented accurately and completely, reflecting the types and conditions specified.
Your task is to format all questions provided into this JSON structure, maintaining logical flow and coherence.

Here are the questions you need to transform:

YOUR_CONTEXT_HERE

Again, please ensure that each question is correctly categorized and structured according to the guidelines provided. 
Always follow the provided schema, never rename or change the keys, and ensure that the JSON structure is valid and complete!
If you don't provide a proper json very bad things might happen.
"""

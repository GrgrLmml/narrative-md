GEN_QUESTIONNAIRE_PROMPT = """
You are tasked with transforming a series of questionnaire questions into a structured JSON format, adhering closely to a specified schema. Each question needs to be categorized by its type (e.g., open, boolean, number, list, multiple choice) and encapsulated within a JSON object as shown in the example structure below:

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

FILL_IN_QUESTIONNAIRE_PROMPT = """
You are a medical doctor and you are reading a transcript of a patient interview. Your task is to fill in the questionnaire based on the patient's responses.

Each question has a specific format and type, such as open, boolean, number, list, or multiple choice. 

Your goal is to provide a valid answer for each question, ensuring that the response aligns with the question type 
and any specified conditions.

Some of the questions are dependent on previous answers, so make sure to consider the context and provide accurate responses.

Here you see a (partially) filled questionnaire:

{ "questions":QUESTIONNAIRE_HERE }

You are only focusing on rows with the 'answer' field as 'n/a'. Don't change the other rows. Also don't make changes to the structure of the JSON.

Ok here is the partial transcript of the ongoing interview:

TRANSCRIPT_HERE

Read the transcript carefully and provide the appropriate answers for each question in the questionnaire.



Respond in a proper JSON format, adhering to the structure of the provided questionnaire. Be extra careful with the ID and the 'answer' field.

If you don't provide a proper json very bad things might happen.
"""
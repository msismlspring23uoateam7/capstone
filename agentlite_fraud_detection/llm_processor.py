import openai
from agentlite_fraud_detection.promptgen import PromptGenerator

class LLMProcessor:
    def __init__(self, api_key, custom_templates=None):
        # Set the API key for OpenAI
        openai.api_key = api_key

        # Initialize the PromptGenerator with custom templates if provided
        self.prompt_generator = PromptGenerator(custom_templates=custom_templates)

    def generate_insights(self, data, task="general_analysis"):
        # Generate the prompt using the prompt generator
        prompt = self.prompt_generator.generate_prompt(data, task=task)

        # Use the newer OpenAI ChatCompletion API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the GPT-4 model
            messages=[
                {"role": "system", "content": "You are an expert in financial data analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,  # Set appropriate max tokens
            temperature=0.7  # Set the temperature as needed
        )

        # Return the content of the response
        return response['choices'][0]['message']['content']

    def perform_nlp_task(self, data, task):
        # Perform an NLP task by generating a prompt and using the LLM for insights
        prompt = self.prompt_generator.generate_prompt(data, task=task)
        result = self.generate_insights(data, task=task)
        return result
   
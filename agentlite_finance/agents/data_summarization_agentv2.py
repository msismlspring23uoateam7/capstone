from openai import OpenAI

# from agentlite_fraud_detection.promptgen import PromptGenerator
from agentlite.agents.BaseAgent import BaseAgent

client = OpenAI(api_key="DUMMY_KEY")

class DataSummarizationAgent(BaseAgent):
    def __init__(self, api_key, llm, actions, shared_mem, custom_templates=None):
        agent_name="DataSummarization"
        agent_role="""You are a finance data summarization agent who is familiar
                        with finance books, thoughts and techniques. Use your
                        knowledge to summarize the given data.
                    """
        super().__init__(
            name=agent_name,
            role=agent_role,
            llm=llm,
            actions=actions
        )
        self.shared_mem = shared_mem
        # Set the API key for OpenAI
        client.api_key = api_key
        # Initialize the PromptGenerator with custom templates if provided
        # self.prompt_generator = PromptGenerator(custom_templates=custom_templates)

    def generate_insights(self, data, task="general_analysis"):
        # Generate the prompt using the prompt generator
        # prompt = self.prompt_generator.generate_prompt(data, task=task)
        prompt = data
        # Use the newer OpenAI ChatCompletion API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use the GPT-4 model
            messages=[
                {"role": "system", "content": "You are an expert in financial data analysis."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,  # Set appropriate max tokens
            temperature=0.7  # Set the temperature as needed
        )

        # Return the content of the response
        return response.choices[0].message.content

    def perform_nlp_task(self, data, task):
        # Perform an NLP task by generating a prompt and using the LLM for insights
        # prompt = self.prompt_generator.generate_prompt(data, task=task)
        result = self.generate_insights(data, task=task)
        return result

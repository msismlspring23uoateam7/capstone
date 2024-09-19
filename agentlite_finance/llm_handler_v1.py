import openai

class LLMHandlerV1:
    def __init__(self, shared_mem, api_key='sk-Vo7jCT5lrwMyJ1YeqpzmYvDaS9sYF4Xt_BPLSaiOywT3BlbkFJVP2JXFoP36HSMWqWluMD88AkB7t0KHJ8j-FM0BUngA'):
        self.shared_mem = shared_mem
        openai.api_key = api_key

    def handle_prompt(self, prompt):
        dataframe = self.shared_mem.get('dataframe', None)
        if dataframe is None:
            return "No data available. Please upload a CSV file first."

        # Generate the response based on the user prompt and the dataframe
        response_text = self.query_llm(prompt, dataframe)
        return response_text

    def query_llm(self, prompt, dataframe):
        # Summarize the dataframe for better context
        data_summary = self.summarize_data(dataframe)
        #print(data_summary)
        # Combine the prompt with data summary for better context
        llm_prompt = f"Data Summary:\n{data_summary}\nUser Prompt: {prompt}"

        # Interact with OpenAI's Chat API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can also use "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a data analysis assistant."},
                {"role": "user", "content": llm_prompt}
            ],
            max_tokens=1000,
            temperature=0.5
        )

        # Return the generated response as plain text
        return response['choices'][0]['message']['content']

    def summarize_data(self, dataframe):
        # Simple summary of the dataframe for LLM context
        summary = dataframe.describe(include='all').to_string()
        #summary = dataframe.to_string(index=False)
        return summary
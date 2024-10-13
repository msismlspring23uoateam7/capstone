import os
from llama_index.core.query_pipeline import (
    QueryPipeline as QP,
    Link,
    InputComponent,
)
from agentlite.actions.BaseAction import BaseAction
from llama_index.experimental.query_engine.pandas import (
    PandasInstructionParser,
)
from agentlite_finance.memory.memory_keys import DATA_FRAME
from llama_index.llms.openai import OpenAI
from llama_index.core import PromptTemplate

class GenericInsightsAction(BaseAction):

    def __init__(
        self,
        shared_mem : dict = None
    ):
        action_name = "GenericInsightsAction"
        action_desc = f"""This is a {action_name} action. 
                            It will provide text based information about the data."""
        params_doc = {"query": "Let any generic query be handled by this action."}
        super().__init__(
            action_name=action_name,
            action_desc=action_desc,
            params_doc=params_doc
        )
        self.shared_mem = shared_mem

    def __call__(self, query):
        result = self.dataframe_query(query)
        # st.write(result)
        return result

    def dataframe_query(self, query):
        df = self.shared_mem.get(DATA_FRAME)
        command = (
            "1. Convert the query to executable Python code using Pandas.\n"
            "2. The final line of code should be a Python expression that can be called with the `eval()` function.\n"
            "3. The code should represent a solution to the query.\n"
            "4. PRINT ONLY THE EXPRESSION.\n"
            "5. Do not quote the expression.\n"
        )

        dataframe_filter_prompt = (
            "You are working with a pandas dataframe in Python.\n"
            "The name of the dataframe is `df`.\n"
            "This is the result of `print(df.head())`:\n"
            "{stock_df_str}\n\n"
            "Follow these instructions:\n"
            "{command}\n"
            "Query: {user_prompt}\n\n"
            "Expression:"
        )

        synthesis_template = (
            "Given an input question, synthesize a response from the query results.\n"
            "Query: {user_prompt}\n\n"
            "Pandas Instructions (optional):\n{pandas_instructions}\n\n"
            "Pandas Output: {filtered_dataframe}\n\n"
            "Response: "
        )

        pandas_prompt = PromptTemplate(dataframe_filter_prompt).partial_format(
            command=command, stock_df_str=df.head(5)
        )
        pandas_output_parser = PandasInstructionParser(df)
        response_synthesis_prompt = PromptTemplate(synthesis_template)
        llm = OpenAI(
                model="gpt-3.5-turbo",
                api_key=os.getenv('OPENAI_API_KEY')
            )
        qp = QP(
            modules={
                "input": InputComponent(),
                "pandas_prompt": pandas_prompt,
                "llm1": llm,
                "pandas_output_parser": pandas_output_parser,
                "response_synthesis_prompt": response_synthesis_prompt,
                "llm2": llm,
            },
            verbose=True,
        )
        qp.add_chain(["input", "pandas_prompt", "llm1", "pandas_output_parser"])
        qp.add_links(
            [
                Link("input", "response_synthesis_prompt", dest_key="user_prompt"),
                Link(
                    "llm1", "response_synthesis_prompt", dest_key="pandas_instructions"
                ),
                Link(
                    "pandas_output_parser",
                    "response_synthesis_prompt",
                    dest_key="filtered_dataframe",
                ),
            ]
        )
        qp.add_link("response_synthesis_prompt", "llm2")
        response = qp.run(
            user_prompt=query,
        )
        return response.message.content
import pandas as pd
from ...agentlite.agentlite.agent_prompts.prompt_utils import (
    DEFAULT_PROMPT,
    PROMPT_TOKENS,
    action_chain_format,
    format_act_params_example,
    format_agent_call_example,
    task_chain_format,
)
from ...agentlite.agentlite.agent_prompts.BasePrompt import ManagerPromptGen

class FinancePrompt(ManagerPromptGen):

    def __init__(
        self,
        agent_role: str = None,
        constraint: str = DEFAULT_PROMPT["constraint"],
        instruction: str = DEFAULT_PROMPT["agent_instruction"],
        default_task: str = "general_analysis",
        custom_templates: dict = None
    ):
        """Prompt Generator for Base Agent
        :param agent_role: the role of this agent, defaults to None
        :type agent_role: str, optional
        :param constraint: the constraint of this agent, defaults to None
        :type constraint: str, optional
        """
        super().__init__(agent_role=agent_role, constraint=constraint, instruction=instruction)
        self.prompt_type = "FinancePrompt"
        self.agent_role = None
        self.default_task = default_task
        self.custom_templates = custom_templates if custom_templates else {}
        

    def generate_prompt(self, data, task=None, custom_templates=None):
        # Ensure the data is a pandas DataFrame
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data should be a pandas DataFrame")

        # Default task handling if none is provided
        task = task or self.default_task

        # Use custom templates if available for the given task
        if custom_templates and task in custom_templates:
            template = custom_templates[task]
            return template.format(data=self._format_data_for_prompt(data))

        # Use class-level custom templates if available for the given task
        elif task in self.custom_templates:
            template = self.custom_templates[task]
            return template.format(data=self._format_data_for_prompt(data))
        
        # Check for specific column names and generate relevant prompts
        if 'Amount' in data.columns:
            return f"Analyze the following credit card transaction data and identify potential fraud:\n\n{self._format_data_for_prompt(data)}."
        elif 'Revenue' in data.columns:
            return f"Analyze the following financial data and provide insights on company performance:\n\n{self._format_data_for_prompt(data)}."
        else:
            return f"Perform {task} on the following data:\n\n{self._format_data_for_prompt(data)}."

    def _format_data_for_prompt(self, data, max_rows=5, max_columns=10):
        """
        Helper function to format the data for use in the prompt.
        Limits the number of rows and columns sent to the LLM.
        """
        # Limit the number of rows and columns
        limited_data = data.iloc[:max_rows, :max_columns]
        return limited_data.to_string()
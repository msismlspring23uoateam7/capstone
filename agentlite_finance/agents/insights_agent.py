# from agentlite_fraud_detection.promptgen import PromptGenerator
from agentlite.agents.BaseAgent import BaseAgent

class DataInsightsAgent(BaseAgent):
    def __init__(self, llm, actions, shared_mem, custom_templates=None):
        agent_name="DataInsights"
        agent_role="""You are an expert data Insights agent. Use your
                        knowledge to generate elabulated insights of the data
                        and visualise it based on the task.
                    """
        super().__init__(
            name=agent_name,
            role=agent_role,
            llm=llm,
            actions=actions
        )
        self.shared_mem = shared_mem
        # Initialize the PromptGenerator with custom templates if provided
        # self.prompt_generator = PromptGenerator(custom_templates=custom_templates)
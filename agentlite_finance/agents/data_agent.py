from agentlite.agents.BaseAgent import BaseAgent

class DataAgent(BaseAgent):
    def __init__(self, llm, actions, shared_mem, custom_templates=None):
        agent_name="DataAgent"
        agent_role="""You are an expert in data preprocessing and data insights. Use your
                        knowledge to preprocess the data and generate expert insights from it 
                        based on the task. Think step by step.
                    """
        super().__init__(
            name=agent_name,
            role=agent_role,
            llm=llm,
            actions=actions
        )
        self.shared_mem = shared_mem

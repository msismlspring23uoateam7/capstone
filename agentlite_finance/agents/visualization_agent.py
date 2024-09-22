from agentlite.agents.BaseAgent import BaseAgent

class VisualizationAgent(BaseAgent):
    def __init__(self, llm, actions, shared_mem, custom_templates=None):
        agent_name="VisualizationAgent"
        agent_role="""You are an expert data visualization agent.
                      Think step by step in case of complex charts. 
                    """
        super().__init__(
            name=agent_name,
            role=agent_role,
            llm=llm,
            actions=actions
        )
        self.shared_mem = shared_mem

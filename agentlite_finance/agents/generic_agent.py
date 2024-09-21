from agentlite.agents.BaseAgent import BaseAgent

class DataInsightsAgent(BaseAgent):
    def __init__(self, llm, actions, shared_mem, custom_templates=None):
        agent_name="GenericAgent"
        agent_role="""You are an expert in handling questions which are not related to charts
                    """
        super().__init__(
            name=agent_name,
            role=agent_role,
            llm=llm,
            actions=actions
        )
        self.shared_mem = shared_mem
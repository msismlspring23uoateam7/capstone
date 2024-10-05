from agentlite.agents.BaseAgent import BaseAgent

class GenericAgent(BaseAgent):
    def __init__(
            self, 
            llm=None, 
            actions=[],
            shared_mem=None,
            logger=None,
            custom_templates=None
        ):
        agent_name="GenericAgent"
        agent_role="""You are an expert in handling questions related to data analysis.
                    """
        super().__init__(
            name=agent_name,
            role=agent_role,
            llm=llm,
            actions=actions,
            logger=logger
        )
        self.shared_mem = shared_mem
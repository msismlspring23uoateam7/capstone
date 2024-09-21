from agentlite.agents.BaseAgent import BaseAgent

class VisualizationAgent(BaseAgent):
    def __init__(self, llm, actions, shared_mem, custom_templates=None):
        agent_name="VisualizationAgent"
        agent_role="""You are an expert visualization agent.Use your
                        knowledge to generate accurate code of the charts 
                        and visualise it based on the task. You can also any question based on the charts.
                    """
        super().__init__(
            name=agent_name,
            role=agent_role,
            llm=llm,
            actions=actions
        )
        self.shared_mem = shared_mem

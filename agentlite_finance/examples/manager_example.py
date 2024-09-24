from agentlite.actions.InnerActions import INNER_ACT_KEY
from agentlite.agents.agent_utils import AGENT_CALL_ARG_KEY
from agentlite.commons import AgentAct
from agentlite.commons import TaskPackage
from agentlite.actions import ThinkAct
from agentlite.actions import FinishAct
import pandas as pd

#TODO needed later
class ManagerExample:
    def build_manager_example(self):
        """
        constructing the examples for agent working.
        Each example is a successful action-obs chain of an agent.
        those examples should cover all those api calls
        """
        # An example of Financial Data Manager Agent 
        # task
        task = "Generate a bar chart showing the total trading volume over the last five years for AAL stock."

        # 1. think action and obs
        thought = "I should first use DataAgent and then use VisualizationAgent. Do not use DataAgent again if already used before."
        act_1 = AgentAct(name=ThinkAct.action_name, params={INNER_ACT_KEY: thought})
        obs_1 = "OK"

        act_2 = AgentAct(
            name='DataAgent',
            params={AGENT_CALL_ARG_KEY: "Use FileHandler to load the data and then Preprocess it." }
        )
        obs_2 = "I have loaded the data and pre-processed it."

        act_3 = AgentAct(
            name=ThinkAct.action_name,
            params={
                INNER_ACT_KEY: f"""I have loaded the data and pre-processed the data. I now should ask VisualizationAgent to generate plotly code and draw the chart."""
            },
        )
        obs_3 = "OK"
        act_4 = AgentAct(
            name='VisualizationAgent',
            params={AGENT_CALL_ARG_KEY: task}
        )
        obs_4 = """Done!"""      

        act_5 = AgentAct(name=FinishAct.action_name, params={INNER_ACT_KEY: "I have successfully completed the task."})
        obs_5 = "Task Completed."
        return TaskPackage(instruction=task),[(act_1, obs_1), (act_2, obs_2), (act_3, obs_3), (act_4, obs_4), (act_5, obs_5)]
    
    def build_manager_example_for_data_summary(self):
        """
        constructing the examples for agent working.
        Each example is a successful action-obs chain of an agent.
        those examples should cover all those api calls
        """
        # An example of Financial Data Manager Agent task
        task = "summarise the AAL stock."

        thought = "I should first use DataAgent and then GenericAgent to summarise and share insights."
        act_1 = AgentAct(name=ThinkAct.action_name, params={INNER_ACT_KEY: thought})
        obs_1 = "OK"

        act_2 = AgentAct(
            name='DataAgent',
            params={AGENT_CALL_ARG_KEY: "Use FileHandler to load the data and then Preprocess it." }
        )
        obs_2 = "I have loaded the data and pre-processed it."

        act_3 = AgentAct(
            name='GenericAgent',
            params={AGENT_CALL_ARG_KEY: task }
        )
        obs_3 = "I have summarised the query."    

        act_4 = AgentAct(name=FinishAct.action_name, params={INNER_ACT_KEY: "I have successfully completed the task."})
        obs_4 = "Task Completed."
        return TaskPackage(instruction=task),[(act_1, obs_1), (act_2, obs_2), (act_3, obs_3), (act_4, obs_4)]    
    
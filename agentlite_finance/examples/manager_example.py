import os
from agentlite.actions.InnerActions import INNER_ACT_KEY
from agentlite.agents.agent_utils import AGENT_CALL_ARG_KEY
from agentlite.commons import AgentAct
from agentlite.actions import FinishAct
from agentlite.commons import TaskPackage

from agentlite_finance.agents.data_agent import DataAgent
from agentlite_finance.agents.generic_agent import GenericAgent
from agentlite_finance.agents.visualization_agent import VisualizationAgent

class ManagerExample:
    def build_manager_example(self):
        """
        constructing the examples for manager working.
        Each example is a successful action-obs chain of a manager agent.
        those examples should cover all those api calls
        """
        # An example of Financial Data Manager Agent task
        task = """Generate a bar chart showing the total trading volume over the last five years for AAL stock.
                  Show a bar chart of the total trading volume over the last five years for AAL stock.
                  Display a bar chart of the total trading volume over the last five years for AAL stock.
                  Plot a bar chart of the total trading volume over the last five years for AAL stock.
                """

        act_1 = AgentAct(
            name=DataAgent().name,
            params={ AGENT_CALL_ARG_KEY: "Use FileHandler to load the data and then Preprocess it." }
        )
        obs_1 = "I have loaded the data and pre-processed it."

        
        cur_dir = os.getcwd()
        examples_dir = "/agentlite_finance/examples/"
        vis_code = open(
                            cur_dir +
                            examples_dir +
                            "data/example_vis_code.txt"
                        ).read()

        act_2 = AgentAct(
            name=VisualizationAgent().name,
            params={ AGENT_CALL_ARG_KEY: task}
        )
        obs_2 = "Plotting of the chart is complete."

        act_3 = AgentAct(
            name=FinishAct.action_name,
            params={ INNER_ACT_KEY: """showing the bar chart for the total trading volume over 
                                       the last five years for AAL stock. Here is the code
                                       used for visualization: \n""" + vis_code}
        )
        obs_3 = "Task Complete."

        return TaskPackage(instruction=task),[ (act_1, obs_1), (act_2, obs_2), (act_3, obs_3)]
    
    def build_manager_example_for_data_summary(self):
        """
        constructing the examples for agent working.
        Each example is a successful action-obs chain of an agent.
        those examples should cover all those api calls
        """
        # An example of Financial Data Manager Agent task
        task = "share insights for AAL stock. summarize the AAL stock. analyse AAL stock"

        act_1 = AgentAct(
            name=DataAgent().name,
            params={ AGENT_CALL_ARG_KEY: "Use FileHandler to load the data and then Preprocess it." }
        )
        obs_1 = "I have loaded the data and pre-processed it."

        act_2 = AgentAct(
            name=GenericAgent().name,
            params={ AGENT_CALL_ARG_KEY: task }
        )
        cur_dir = os.getcwd()
        examples_dir = "/agentlite_finance/examples/"
        insights_text = open(
                                cur_dir
                                + examples_dir
                                + "data/stock_data_insights.txt"
                            ).read()
        obs_2 = "summarization of AAL stock is complete."

        act_3 = AgentAct(
            name=FinishAct.action_name,
            params={ INNER_ACT_KEY: insights_text}
        )
        obs_3 = "Task Complete."

        return TaskPackage(instruction=task),[(act_1, obs_1), (act_2, obs_2), (act_3, obs_3)]    
    
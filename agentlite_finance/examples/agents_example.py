import os
from agentlite.actions.InnerActions import INNER_ACT_KEY
from agentlite.commons import AgentAct
from agentlite.commons import TaskPackage
from agentlite.actions import ThinkAct
from agentlite.actions import FinishAct
from agentlite_finance.actions.file_handler_action import FileHandlerAction
from agentlite_finance.actions.code_generation_action import CodeGenerationAction
from agentlite_finance.actions.generic_insights_action import GenericInsightsAction
from agentlite_finance.actions.plotting_action import PlottingAction
from agentlite_finance.actions.preprocessing_action import PreprocessingAction
import pandas as pd

class AgentsExample:
    def build_data_agent_example(self):
        """
        constructing the examples for agent working.
        Each example is a successful action-obs chain of an agent.
        those examples should cover all those api calls
        """
        # An example of Data Agent task
        task = "Use FileHandler to load the data and then Preprocess it."

        # 1. FileHandler action and obs
        act_params = {"query": "loading the data"}
        act_1 = AgentAct(name=FileHandlerAction().action_name, params=act_params)
        obs_1 = "Data is loaded."
    
         # 2. Preprocessing action and obs
        act_2 = AgentAct(name=PreprocessingAction().action_name, params={"query": "Preprocessing the data."})
        obs_2 = 'Preprocessing Completed.'

        return TaskPackage(instruction=task),[(act_1, obs_1), (act_2, obs_2),]
    
    def build_visualisation_example(self):
        """
        constructing the examples for agent working.
        Each example is a successful action-obs chain of an agent.
        those examples should cover all those api calls
        """
        # An example of visualisation Agent task
        task = """Generate a bar chart showing the total trading volume over the last five years for AAL stock.
                  Show a bar chart of the total trading volume over the last five years for AAL stock.
                  Display a bar chart of the total trading volume over the last five years for AAL stock.
                  Plot a bar chart of the total trading volume over the last five years for AAL stock.
                """

        act_params = {"query": task}
        act_1 = AgentAct(name=CodeGenerationAction().action_name, params=act_params)
        obs_1 = 'Code generated for the chart.'
        
        cur_dir = os.getcwd()
        examples_dir = "/agentlite_finance/examples/"
        code_gen_resp = open(
                            cur_dir +
                            examples_dir +
                            "data/example_vis_code.txt"
                        ).read()
        obs_1 = code_gen_resp

        # 2. Visualisation action
        act_2 = AgentAct(
            name=PlottingAction().action_name,
            params={"input": "Here is the code received from CodeGen to plot visualization: \n" + code_gen_resp})
        obs_2 = "Plotting of the visualisation is complete."

        # 3. Finish action
        act_3 = AgentAct(
            name=FinishAct.action_name,
            params={INNER_ACT_KEY: "Here is the code received from CodeGen: \n" + code_gen_resp})
        obs_3 = "Code used to plot visualisation is returned successfully."

        return TaskPackage(instruction=task),[(act_1, obs_1), (act_2, obs_2), (act_3, obs_3)]
    

    def build_summary_example(self):
        """
        constructing the examples for agent working.
        Each example is a successful action-obs chain of an agent.
        those examples should cover all those api calls
        """
        # An example of visualisation Agent task
        task = "share insights for AAL stock. analyse AAL stock. summarize AAL stock"

        # 1. GenericInsights action
        act_1 = AgentAct(name=GenericInsightsAction().action_name, params={"query": task})
        cur_dir = os.getcwd()
        examples_dir = "/agentlite_finance/examples/"
        insights_resp = open(
                            cur_dir +
                            examples_dir +
                            "data/stock_data_insights.txt"
                        ).read()
        obs_1 = "Insights received from Generic Action."

        # 2. Finish action
        act_2 = AgentAct(
            name=FinishAct.action_name,
            params={INNER_ACT_KEY: insights_resp})
        obs_2 = "Task Complete."
   
        return TaskPackage(instruction=task),[(act_1, obs_1), (act_2, obs_2)]
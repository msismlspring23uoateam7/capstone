from agentlite.actions.InnerActions import INNER_ACT_KEY
from agentlite.commons import AgentAct
from agentlite.commons import TaskPackage
from agentlite.actions import ThinkAct
from agentlite.actions import FinishAct
from agentlite_finance.actions.file_handler_action import FileHandlerAction
from agentlite_finance.actions.visualization_action import VisualizationAction
from agentlite_finance.actions.codegeneration_action import CodegenerationAction
from agentlite_finance.actions.generic_insights_action import GenericInsightsAction
from agentlite_finance.actions.plotting_action import PlottingAction
from agentlite_finance.actions.preprocessing_action import PreprocessingAction
import pandas as pd

class InsightsExample:
    def build_dataagent_example(self):
        """
        constructing the examples for agent working.
        Each example is a successful action-obs chain of an agent.
        those examples should cover all those api calls
        """
        # An example of Insights Agent 
        # task
        task = "Generate a bar chart showing the total trading volume over the last five years for AAL stock."

        # 1. think action and obs
        thought = "I should first use FileHandler to load the data. Do not use FileHandler again if already used before"
        act_1 = AgentAct(name=ThinkAct.action_name, params={INNER_ACT_KEY: thought})
        obs_1 = ""

        # 2. FileHandler action and obs
        act_params = {"query": "loading the data"}
        act_2 = AgentAct(name=FileHandlerAction().action_name, params=act_params)
        import os
        cur_dir = os.getcwd()
        examples_dir = "/agentlite_finance/examples/"
        df_string = pd.read_csv(
                                    cur_dir
                                    + examples_dir
                                    + "data/stock_data.csv"
                                ).to_string(index=False)
        obs_2 = df_string
        # print(obs_2)
        # 3. think action and obs
        insights_text = open(
                                cur_dir
                                + examples_dir
                                + "data/stock_data_insights.txt"
                            ).read()
        thought = insights_text

        # 3. finish action
        act_3 = AgentAct(name=FinishAct.action_name, params={INNER_ACT_KEY: thought})
        # obs_3 = "Task Completed."
        obs_3 = thought
        return TaskPackage(instruction=task),[(act_1, obs_1), (act_2, obs_2), (act_3, obs_3)]
    
    def build_visualisation_example(self):
        """
        constructing the examples for agent working.
        Each example is a successful action-obs chain of an agent.
        those examples should cover all those api calls
        """
        # An example of Insights Agent 
        # task
        task = "show visualisation for the data"

        # 1. think action and obs
        thought = "I should first use FileHandler to load the data. and then use Visualization action to plot and visualise."
        act_1 = AgentAct(name=ThinkAct.action_name, params={INNER_ACT_KEY: thought})
        obs_1 = ""

        # 1. FileHandler action and obs
        act_params = {"query": "loading the data"}
        act_2 = AgentAct(name=FileHandlerAction().action_name, params=act_params)
        import os
        cur_dir = os.getcwd()
        examples_dir = "/agentlite_finance/examples/"
        df_string = pd.read_csv(
                                    cur_dir
                                    + examples_dir
                                    + "data/stock_data.csv"
                                ).to_string(index=False)
        obs_2 = df_string

        # 3. Python action
        act_3 = AgentAct(name=PythonAction().action_name, params={"query": "Fetching code for visualisation."})
        obs_3 = "Task Completed."

        # 4. Visualisation action
        act_4 = AgentAct(name=VisualizationAction().action_name, params={"query": "Creating visualisation"})
        obs_4 = "Done."

        thought = "Check if Visualization action is executed else use Visualization action to plot and visualise."
        act_5 = AgentAct(name=ThinkAct.action_name, params={INNER_ACT_KEY: thought})
        obs_5 = ""

        # 5. finish action
        act_6 = AgentAct(name=FinishAct.action_name, params={INNER_ACT_KEY: "Finish if visualization is complete."})
        obs_6 = "Ok."
        return TaskPackage(instruction=task),[(act_1, obs_1), (act_2, obs_2), (act_3, obs_3),
                                                (act_4, obs_4), (act_5, obs_5), (act_6, obs_6)]
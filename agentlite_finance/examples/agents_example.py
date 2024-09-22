from agentlite.actions.InnerActions import INNER_ACT_KEY
from agentlite.commons import AgentAct
from agentlite.commons import TaskPackage
from agentlite.actions import ThinkAct
from agentlite.actions import FinishAct
from agentlite_finance.actions.file_handler_action import FileHandlerAction
from agentlite_finance.actions.codegeneration_action import CodegenerationAction
from agentlite_finance.actions.generic_insights_action import GenericInsightsAction
from agentlite_finance.actions.plotting_action import PlottingAction
from agentlite_finance.actions.preprocessing_action import PreprocessingAction
import pandas as pd

class AgentsExample:
    def build_dataagent_example(self):
        """
        constructing the examples for agent working.
        Each example is a successful action-obs chain of an agent.
        those examples should cover all those api calls
        """
        # An example of Data Agent 
        # task
        task = "Use FileHandler to load the data and then Preprocess it."

        # 1. think action and obs
        thought = "I should first use FileHandler to load the data. Then use Preprocessing to process the data."
        act_1 = AgentAct(name=ThinkAct.action_name, params={INNER_ACT_KEY: thought})
        obs_1 = "Data loading is completed."

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
        insights_text = open(
                                cur_dir
                                + examples_dir
                                + "data/stock_data_insights.txt"
                            ).read()
        thought = insights_text


        act_3 = AgentAct(name=PreprocessingAction().action_name, params={"query": thought})
        obs_3= 'Preprocessing Completed.'

        # 3. finish action
        act_4 = AgentAct(name=FinishAct.action_name, params={INNER_ACT_KEY: thought})
        # obs_3 = "Task Completed."
        obs_4= thought
        return TaskPackage(instruction=task),[(act_1, obs_1), (act_2, obs_2), (act_3, obs_3), (act_4, obs_4)]
    
    def build_visualisation_example(self):
        """
        constructing the examples for agent working.
        Each example is a successful action-obs chain of an agent.
        those examples should cover all those api calls
        """
        # An example of visualisation Agent 
        # task
        task = "Generate a bar chart showing the total trading volume over the last five years for AAL stock."

        # 1. think action and obs
        thought = "I should first use Codegenerator to generate the code and then I should use Plotting action to plot and visualise."
        act_1 = AgentAct(name=ThinkAct.action_name, params={INNER_ACT_KEY: thought})
        obs_1 = "OK"

        act_params = {"query": task}
        act_2 = AgentAct(name=CodegenerationAction().action_name, params=act_params)
        obs_2 = 'Code generated for the chart.'

        # 4. Visualisation action
        act_3 = AgentAct(name=PlottingAction().action_name, params={"query": task})
        obs_3 = "Chart is plotted."

        # 5. finish action
        act_4 = AgentAct(name=FinishAct.action_name, params={INNER_ACT_KEY: "Finish if Plotting is complete."})
        obs_4 = "Ok."
        return TaskPackage(instruction=task),[(act_1, obs_1), (act_2, obs_2), (act_3, obs_3), (act_4, obs_4)]
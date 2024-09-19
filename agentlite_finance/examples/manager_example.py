from agentlite.actions.InnerActions import INNER_ACT_KEY
from agentlite.commons import AgentAct
from agentlite.commons import TaskPackage
from agentlite.actions import ThinkAct
from agentlite.actions import FinishAct
from agentlite_finance.actions.file_handler_action import FileHandlerAction
import pandas as pd

#TODO needed later
class ManagerExample:
    def build_manager_example(self):
        """
        constructing the examples for agent working.
        Each example is a successful action-obs chain of an agent.
        those examples should cover all those api calls
        """
        # An example of Insights Agent 
        # task
        task = "generate insights for the shared data"

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
                                    + "data/test_data.csv"
                                ).to_string(index=False)
        obs_2 = df_string
        # print(obs_2)
        # 3. think action and obs
        insights_text = open(
                                cur_dir
                                + examples_dir
                                + "data/test_data_insights.txt"
                            ).read()
        thought = insights_text

        # 4. finish action
        act_3 = AgentAct(name=FinishAct.action_name, params={INNER_ACT_KEY: thought})
        obs_3 = "Task Completed."
        return TaskPackage(instruction=task),[(act_1, obs_1), (act_2, obs_2), (act_3, obs_3)]
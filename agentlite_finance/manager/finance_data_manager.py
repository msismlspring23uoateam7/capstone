import streamlit as st
# from prompts.finance_prompt import FinancePrompt
from agentlite.agents import ManagerAgent
from agentlite.logging.streamlit_logger import UILogger

class FinanceDataManagerAgent(ManagerAgent):

    def __init__(self, llm, team, logger):
        super().__init__(
            name="DataManager",
            role="Manage and Execute the pre-processing, insights, and visualization of data based on given task",
            llm=llm,
            TeamAgents=team,
            logger=logger
        )

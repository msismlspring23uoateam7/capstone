import streamlit as st
from prompts.finance_prompt import FinancePrompt
from ...agentlite.agentlite.agents import ManagerAgent
from ...agentlite.agentlite.logging.streamlit_logger import UILogger

class FinanceDataManagerAgent(ManagerAgent):

    def __init__(self, llm, team, logger):
        super().__init__(
            name="FinanceDataManager",
            role="Manage the data pre-processing, LLM insights, and visualization for finance data",
            llm=llm,
            TeamAgents=team,
            logger=logger
        )
        self.prompt_gen = FinancePrompt()
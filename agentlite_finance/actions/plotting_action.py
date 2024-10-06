import streamlit as st
from sklearn.preprocessing import StandardScaler
from agentlite.actions.BaseAction import BaseAction
from agentlite.logging.streamlit_logger import UILogger
from agentlite_finance.memory.memory_keys import CODE
from agentlite_finance.memory.memory_keys import DATA_FRAME
import sys
import os
import re
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

class PlottingAction(BaseAction):

    def __init__(
        self,
        shared_mem : dict = None
    ):
        action_name = "PlottingAction"
        action_desc = f"""This is a {action_name} action. 
                            This will plot the chart using response generated from codegenerator"""
        params_doc = {"input": "Let the plotting be done by this action using input code"}
        super().__init__(
            action_name=action_name,
            action_desc=action_desc,
            params_doc=params_doc
        )
        self.shared_mem = shared_mem

    def __call__(self, input):
        if self.shared_mem.get(CODE) is None:
            return "Could not find dataframe. Load dataframe using FileHandler action first."
        code_response = self.shared_mem.get(CODE)
        self.execute_pure_code(code_response)
        return input

    def execute_pure_code(self, response):
        data = self.shared_mem.get(DATA_FRAME)
        exec(response)
        exec("plot_chart_for_stock_data(data)")
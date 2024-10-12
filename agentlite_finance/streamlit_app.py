import os
import streamlit as st
import logging

from agentlite.logging.terminal_logger import AgentLogger
from agentlite.llm.agent_llms import get_llm_backend
from agentlite.commons import TaskPackage
from agentlite.logging.streamlit_logger import UILogger

from agentlite_finance.actions.code_generation_action import CodeGenerationAction
from agentlite_finance.actions.file_handler_action import FileHandlerAction
from agentlite_finance.actions.generic_insights_action import GenericInsightsAction
from agentlite_finance.actions.plotting_action import PlottingAction
from agentlite_finance.actions.preprocessing_action import PreprocessingAction
from agentlite.llm.LLMConfig import LLMConfig
from agentlite_finance.examples.agents_example import AgentsExample
from agentlite_finance.examples.manager_example import ManagerExample
from agentlite_finance.memory.shared_memory import SharedMemory
from agentlite_finance.agents.data_agent import DataAgent
from agentlite_finance.agents.generic_agent import GenericAgent
from agentlite_finance.agents.visualization_agent import VisualizationAgent
from agentlite_finance.manager.finance_data_manager import FinanceDataManagerAgent
from agentlite_finance.memory.memory_keys import FILE
logging.basicConfig(level=logging.DEBUG)


def main():
    st.title("AgentLite Framework: Enhanced Data Visualization")
    uploaded_file = st.file_uploader("Upload a ZIP or CSV file", type=["zip", "csv"])
    if uploaded_file:
        # Initialize LLM and logger
        llm_config_dict = {
                            "llm_name": "gpt-3.5-turbo",
                            "temperature": 0.7,
                            "max_tokens": 2000,
                            "api_key": "sk-Vo7jCT5lrwMyJ1YeqpzmYvDaS9sYF4Xt_BPLSaiOywT3BlbkFJVP2JXFoP36HSMWqWluMD88AkB7t0KHJ8j-FM0BUngA"
                            }
        llm_config = LLMConfig(llm_config_dict)
        llm = get_llm_backend(llm_config)
        logger = UILogger()
        # define the logger. You can set the PROMPT_DEBUG_FLAG=True to show the actual prompt and generation for LLM
        agent_logger = AgentLogger(PROMPT_DEBUG_FLAG=True) 

        # Initialize agents
        shared_mem = SharedMemory()
        shared_mem.add(FILE, uploaded_file)

        file_handler_action = FileHandlerAction(shared_mem)
        preprocessing_action = PreprocessingAction(shared_mem)

        
        data_agent = DataAgent(
            llm=llm,
            actions=[file_handler_action, preprocessing_action],
            shared_mem=shared_mem,
            logger=agent_logger
            )
        
        codegeneration_action = CodeGenerationAction(shared_mem)
        plotting_action = PlottingAction(shared_mem)
        
        visualization_agent = VisualizationAgent(
            llm=llm,
            actions=[codegeneration_action, plotting_action],
            shared_mem=shared_mem,
            logger=agent_logger
            )
        
        generic_insights_action = GenericInsightsAction(shared_mem)
        generic_agent = GenericAgent(
            llm=llm,
            actions=[generic_insights_action],
            shared_mem=shared_mem,
            logger=agent_logger
            ) 

        example_task1, act_chain1 = AgentsExample().build_data_agent_example()
        data_agent.add_example(task=example_task1, action_chain=act_chain1)
        example_task2, act_chain2 = AgentsExample().build_visualisation_example()
        visualization_agent.add_example(task=example_task2, action_chain=act_chain2)
        example_task3, act_chain3 = AgentsExample().build_summary_example()
        generic_agent.add_example(task=example_task3, action_chain=act_chain3)

        # Manager agent
        finance_data_manager = FinanceDataManagerAgent(
            llm=llm,
            team=[
                    data_agent ,visualization_agent, generic_agent                    
                ],
            logger=agent_logger
        )
        manager_task, manager_chain = ManagerExample().build_manager_example()
        finance_data_manager.add_example(task=manager_task, action_chain=manager_chain)

        summary_task, summary_chain = ManagerExample().build_manager_example_for_data_summary()
        finance_data_manager.add_example(task=summary_task, action_chain=summary_chain)

        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask for specific analysis, EDA, insights, or request a specific chart (e.g., 'Show me a 50-day and 200-day moving average for AAL')"):
            task_pack = TaskPackage(instruction=prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
                
            response = finance_data_manager(task_pack)
            with st.chat_message("assistant"):
                 st.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()

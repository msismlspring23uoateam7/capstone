import os
import streamlit as st

from agentlite.llm.agent_llms import get_llm_backend
from agentlite.commons import TaskPackage
from agentlite.logging.streamlit_logger import UILogger

from agentlite_finance.actions.codegeneration_action import CodegenerationAction
from agentlite_finance.actions.file_handler_action import FileHandlerAction
from agentlite_finance.actions.generic_insights_action import GenericInsightsAction
from agentlite_finance.actions.plotting_action import PlottingAction
from agentlite_finance.actions.preprocessing_action import PreprocessingAction
from agentlite_finance.actions.visualization_action import VisualizationAction
from agentlite.llm.LLMConfig import LLMConfig
from agentlite_finance.memory.shared_memory import SharedMemory
from agentlite_finance.memory.memory_keys import FILE
from agentlite_finance.memory.memory_keys import DATA_FRAME
from agentlite_finance.examples.insights_example import InsightsExample


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

        # Initialize agents
        shared_mem = SharedMemory()
        shared_mem.add(FILE, uploaded_file)

        file_handler_action = FileHandlerAction(shared_mem)
        preprocessing_action = PreprocessingAction(shared_mem)

        from agentlite_finance.agents.data_agent import DataAgent
        data_agent = DataAgent(
            llm=llm,
            actions=[file_handler_action, preprocessing_action],
            shared_mem=shared_mem
            )
        
        codegeneration_action = CodegenerationAction(shared_mem)
        plotting_action = PlottingAction(shared_mem)
        from agentlite_finance.agents.visualization_agent import VisualizationAgent
        visualization_agent = VisualizationAgent(
            llm=llm,
            actions=[codegeneration_action, plotting_action],
            shared_mem=shared_mem
            )
        
        generic_insights_action = GenericInsightsAction(shared_mem)
        from agentlite_finance.agents.generic_agent import GenericAgent
        generic_agent = GenericAgent(
            llm=llm,
            actions=[codegeneration_action, plotting_action],
            shared_mem=shared_mem
            ) 
   #TODO provide examples
   #     example_task, act_chain = InsightsExample().build_insights_example()
   #     example_visual_task, visual_act_chain = InsightsExample().build_visualisation_example()
   #     insights_agent.add_example(task=example_task, action_chain=act_chain)
   #     insights_agent.add_example(task=example_visual_task, action_chain=visual_act_chain)


        # Manager agent
        from agentlite_finance.manager.finance_data_manager import FinanceDataManagerAgent
        finance_data_manager = FinanceDataManagerAgent(
            llm=llm,
            team=[
                    data_agent,visualization_agent,generic_agent                    
                ],
            logger=logger
        )
        # finance_data_manager.add_example(task=example_task, action_chain=act_chain)

        if "messages" not in st.session_state:
            st.session_state.messages = []

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

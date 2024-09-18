import streamlit as st

from agentlite.llm.agent_llms import get_llm_backend
from agentlite.commons import TaskPackage
from agentlite.logging.streamlit_logger import UILogger

from agentlite_finance.actions.file_handler_action import FileHandlerAction
from agentlite_finance.actions.data_preprocessing_action import PreProcessingAction
from agentlite_finance.actions.visualization_action import VisualizationAction
from agentlite.llm.LLMConfig import LLMConfig
from agentlite_finance.memory.shared_memory import SharedMemory
from agentlite_finance.memory.memory_keys import FILE
from agentlite_finance.memory.memory_keys import DATA_FRAME
from agentlite_finance.examples.insights_example import InsightsExample


# def execute_workflow(self):
#     # Generate LLM insights
#     insights = self.llm_processor.generate_insights(processed_data, task="general_analysis")
#     st.write("LLM Insights:")
#     st.write(insights)

def main():
    st.title("AgentLite Framework: Enhanced Data Analysis")
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
        preprocessing_action = PreProcessingAction(shared_mem)
        visualization_action = VisualizationAction(shared_mem)
        from agentlite_finance.agents.data_summarization_agent import DataSummarizationAgent
        summarization_agent = DataSummarizationAgent(
            api_key="DUMMY_KEY",
            llm=llm,
            actions=[file_handler_action, preprocessing_action, visualization_action, ],
            shared_mem=shared_mem
            )
        example_task, act_chain = InsightsExample().build_insights_example()
        summarization_agent.add_example(task=example_task, action_chain=act_chain)

        from agentlite_finance.agents.insights_agent import DataInsightsAgent
        insights_agent = DataInsightsAgent(
            api_key="DUMMY_KEY",
            llm=llm,
            actions=[file_handler_action, preprocessing_action, visualization_action, ],
            shared_mem=shared_mem
            )
        insights_agent.add_example(task=example_task, action_chain=act_chain)

        # Manager agent
        from agentlite_finance.manager.finance_data_manager import FinanceDataManagerAgent
        finance_data_manager = FinanceDataManagerAgent(
            llm=llm,
            team=[
                    # summarization_agent,
                    insights_agent
                ],
            logger=logger
        )
        # finance_data_manager.add_example(task=example_task, action_chain=act_chain)

        if "messages" not in st.session_state:
            st.session_state.messages = []

        if prompt := st.chat_input("Ask any question related to the shared data."):
            # task_pack = TaskPackage(instruction="Start a finance data analysis pipeline")
            task_pack = TaskPackage(instruction=prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            # response = summarization_agent(task_pack)
            response = finance_data_manager(task_pack)
            st.write(response)
            # with st.chat_message("assistant"):
            #     st.markdown(response)

            st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()

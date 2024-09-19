class ManagerAgent:
    def __init__(self, shared_mem, llm_handler, file_handler_action, visualization_actions):
        self.shared_mem = shared_mem
        self.llm_handler = llm_handler
        self.file_handler_action = file_handler_action
        self.visualization_actions = visualization_actions

    def handle_user_input(self, user_input):
        """
        This method handles the user input and coordinates which agent to activate.
        """
        if "upload" in user_input:
            # Trigger the file handler
            self.file_handler_action.handle_uploaded_file(user_input["file"])

        elif "analyze" in user_input:
            # Pass to LLM for analysis
            response = self.llm_handler.handle_prompt(user_input["prompt"])
            return response

        elif "visualize" in user_input:
            # Trigger the relevant visualization
            chart_type = user_input.get("chart_type", "line chart")
            if chart_type == "line chart":
                self.visualization_actions.plot_line_chart(self.shared_mem.get("dataframe"))
            elif chart_type == "bar chart":
                self.visualization_actions.plot_bar_chart(self.shared_mem.get("dataframe"))
            # You can add other chart types here

        return "Task completed"
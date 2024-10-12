from agentlite_print.commons import TaskPackage
from agentlite_finance.manager.finance_data_manager import FinanceDataManagerAgent

evaluation_prompts = dict()

prompt_visual_list = []
with open('tests/dataset/visual_ques.txt', 'r') as file:
    for num, line in enumerate(file):
        # if num < 5:
        prompt_type = "Visualization"
        prompt = line.split(":")[0]
        expected_response = ""
        while True:
            try:
                expected_response = FinanceDataManagerAgent(TaskPackage(instruction=line))
                break
            except UnboundLocalError:
                print("Retring again. UnboundLocalError")
            except Exception:
                print("Retring again. Exception")
        # new_data_dict = {'prompt_type': prompt_type, 'prompt': prompt, 'expected_response': expected_response}
        # new_data_df = pd.DataFrame([new_data_dict])
        # evaluation_dataframe = pd.concat([evaluation_dataframe, new_data_df], ignore_index=True)
        new_dict = dict()
        new_dict['prompt'] = prompt
        new_dict['response'] = expected_response
        prompt_visual_list.append(new_dict)
evaluation_prompts['Visualization'] = prompt_visual_list
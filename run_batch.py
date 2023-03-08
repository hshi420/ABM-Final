from infection_model.model_q import Infection
from mesa.batchrunner import FixedBatchRunner
import pandas as pd

fixed_parameters = {
  'height': 50,
  'width': 50,
}


parameters_list = [{"self_q_threshold": 0.125},
                   {"self_q_threshold": 0.25},
                   {"self_q_threshold": 0.375},
                   {"self_q_threshold": 0.5},
                   {"self_q_threshold": 0.625}, 
                   {"self_q_threshold": 0.75},
                   {"self_q_threshold": 0.875}, 
                   {"self_q_threshold": 1}]
  

batch_run = FixedBatchRunner(Infection, parameters_list, fixed_parameters, iterations=5, max_steps = 150)

batch_run.run_all()

ordered_dict = batch_run.get_collector_model()

step_dict = {'threshold':[],  'infected_agents':[]}
for key, value in ordered_dict.items():
    for i in value['Infection_Num']:
        step_dict['threshold'].append(key[0])
        step_dict['infected_agents'].append(i)

step_df = pd.DataFrame(step_dict)
step_df.to_csv('Infection_model_step_batch_run_data.csv')

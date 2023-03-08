from infection_model.model_q import Infection

# Set your parameter values for one run
# Reminder that the model takes on these parameter values:
# width, height, num_agents, minority_pc, intolerance
model = Infection(50, 50)
for t in range(150):
    model.step()

# extract data as a pandas Data Frame
model_df = model.datacollector.get_model_vars_dataframe()

## NOTE: to do data collection, you need to be sure your pathway is correct to save this!
# export the data to a csv file for graphing/analysis
model_df.to_csv("Infection_model_single_run_data.csv")

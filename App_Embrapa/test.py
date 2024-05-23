from plots import plotsData
from data_ingest import json_list


data_list = []

for data in json_list[:3]:
    data_list.append(plotsData.melt_df(data))

for data in json_list[3:]:
    data_list.append(plotsData.combine_df(data))

print(data_list[3])



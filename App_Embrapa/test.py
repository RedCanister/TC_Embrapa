from pathlib import Path

data_list = []

#for data in json_list[:3]:
#    data_list.append(plotsData.melt_df(data))

#for data in json_list[3:]:
#    data_list.append(plotsData.combine_df(data))

#print(data_list[3])

project_root = Path(__file__).parent.parent.resolve()
print("project_root", project_root)

new_path = project_root / 'Data_Embrapa' / 'Dados_Embrapa' / 'JSON'
print("new_path", new_path)
#print(type(new_path))

"""
import pandas as pd
from pathlib import Path

json_path = Path(__file__).parent.parent.resolve()
json_ImpExp_type = ["Espumantes", "Suco", "Vinho", "Uva",]

# Comercialização e produção
json_com = pd.read_json(json_path / "/Comercio.json")
json_prd = pd.read_json(json_path / "/Producao.json")

# Exportação
json_exp = pd.DataFrame()
for type in json_ImpExp_type:
    json_temp = pd.read_json(
        json_path / "/" / "Exp" / type / ".json"
    )
    json_exp = pd.concat([json_exp, json_temp])

# Importação
json_imp = pd.DataFrame()
for type in json_ImpExp_type[:2]:
    json_temp = pd.read_json(
        json_path / "/" / "Imp" / type / ".json"
    )
    json_imp = pd.concat([json_imp, json_temp])

json_imp = pd.concat([
    json_imp, 
    pd.read_json(json_path / "/" / "Imp" / "Frescas" / ".json"),
    pd.read_json(json_path / "/" / "Imp" / "Passas" / ".json"),
])

# Processamento
json_proc_type = ["Americanas", "Mesa", "Semclass", "Viniferas"]

json_proc = pd.DataFrame()
for type in json_proc_type:
    json_temp = pd.read_json(
        json_path / "/" / "Processa" / type / ".json"
    )
    json_proc = pd.concat([json_proc, json_temp])

# Lista de acesso
json_list = [json_prd, json_proc, json_com, json_imp, json_exp,]

#print(json_list[0])
"""
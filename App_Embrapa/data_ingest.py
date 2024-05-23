import pandas as pd

json_path = "C:/Users/andma/OneDrive/Documentos/FIAP/Projeto/Dados_Embrapa/JSON"
json_ImpExp_type = ["Espumantes", "Suco", "Vinho", "Uva",]

# Comercialização e produção
json_cm = pd.read_json(json_path + "/Comercio.json")
json_pd = pd.read_json(json_path + "/Producao.json")

# Exportação
json_exp = pd.DataFrame()
for type in json_ImpExp_type:
    json_temp = pd.read_json(
        json_path + "/" + "Exp" + type + ".json"
    )
    json_exp = pd.concat([json_exp, json_temp])

# Importação
json_imp = pd.DataFrame()
for type in json_ImpExp_type[:2]:
    json_temp = pd.read_json(
        json_path + "/" + "Imp" + type + ".json"
    )
    json_imp = pd.concat([json_imp, json_temp])

json_imp = pd.concat([
    json_imp, 
    pd.read_json(json_path + "/" + "Imp" + "Frescas" + ".json"),
    pd.read_json(json_path + "/" + "Imp" + "Passas" + ".json"),
])

# Processamento
json_proc_type = ["Americanas", "Mesa", "Semclass", "Viniferas"]

json_proc = pd.DataFrame()
for type in json_proc_type:
    json_temp = pd.read_json(
        json_path + "/" + "Processa" + type + ".json"
    )
    json_proc = pd.concat([json_proc, json_temp])

# Lista de acesso
json_list = [json_cm, json_pd, json_proc, json_exp, json_imp,]
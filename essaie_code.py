import requests

url = "https://rest.uniprot.org/idmapping/run"
data = {
    "from": "UniProtKB_AC-ID",
    "to": "UniRef50",
    "ids": "Q2TYW1",
    "types": "application",
    "format": "json"
}

response = requests.post(url, data=data)

if response.status_code == 200:
    with open("results.xlsx", "wb") as f:
        f.write(response.content)
    print("Results saved to results.xlsx")
else:
    print(f"Error {response.status_code}: {response.text}")


import requests
import pandas as pd
#
# url = "https://www.uniprot.org/uploadlists/"
# params = {
#     "from": "UniProtKB_AC-ID",
#     "to": "UniRef50",
#     "ids": "Q2TYW1",
#     "format": "json",
# }
#
# response = requests.get(url, params=params)
#
# if response.status_code == 200:
#     data = response.json()
#
#     # convertir les données en un DataFrame pandas
#     df = pd.DataFrame(data)
#
#     # écrire le DataFrame dans un fichier Excel
#     writer = pd.ExcelWriter("output.xlsx")
#     df.to_excel(writer, index=False)
#     writer.save()
# else:
#     print(f"Error {response.status_code}: {response.text}")
# #url = "https://rest.uniprot.org/idmapping/run"
# import requests
#
# url = "https://rest.uniprot.org/idmapping/run"
# data = {
#     "from": "UniProtKB_AC-ID",
#     "to": "UniRef50",
#     "ids": "Q2TYW1",
#     "format": "xlsx"
# }
#
# response = requests.post(url, data=data)
#
# if response.status_code == 200:
#     with open("results.xlsx", "wb") as f:
#         f.write(response.content)
#     print("Results saved to results.xlsx")
# else:
#     print(f"Error {response.status_code}: {response.text}")
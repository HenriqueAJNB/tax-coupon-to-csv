# Import libraries
from tika import parser
import regex as re
import pandas as pd
import os
from pprint import pprint


# Path to PDF file
folder_path = r"C:\Users\Henrique\Google Drive\CFe\\"

[(_, _, filenames)] = os.walk(folder_path)

data = []
# Get raw content from PDF file
for index, file in enumerate(filenames, 1):
    raw_content = parser.from_file(folder_path + file)["content"]

    market_name = re.findall(r"\n\n\w+\s", raw_content)[0][2:-1]

    date = re.findall(r"\d{2}[/]\d{2}[/]\d{4}", raw_content)[0]

    lines_from_raw_file = re.findall(r"\n\d{1,2} \d+[ | \w | .,()]+", raw_content)

    pprint(lines_from_raw_file)

    pattern = r"\n(\d{1,2}) (\d{3,}) ?([A-Z .\d]+) ?(\d[,]\d{4}) ?(UN|KG) (\d+[,]\d{2}) ?\((\d+[,]\d{2})\)"
    for line in lines_from_raw_file:
        row = list(re.search(pattern, line, re.IGNORECASE).groups())
        row.append(market_name)
        row.append(date)
        row.append(index)
        data.append(row)

columns = [
    "Id_cupom_fiscal",
    "Código",
    "Item",
    "Quantidade",
    "Unidade",
    "Valor unitário (R$)",
    "Valor_tributo (R$)",
    "Mercado",
    "Data",
    "Id_compra",
]
df = pd.DataFrame(data, columns=columns)


def replace_comma_for_dot(cols):
    for col in cols:
        df[col] = [x.replace(",", ".") for x in df[col]]


replace_comma_for_dot(["Quantidade", "Valor unitário (R$)", "Valor_tributo (R$)"])

numeric_cols = [
    "Id_cupom_fiscal",
    "Código",
    "Quantidade",
    "Valor unitário (R$)",
    "Valor_tributo (R$)",
    "Id_compra",
]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)

df["Unidade"] = [un.upper() for un in df["Unidade"]]

df.to_csv("items.csv")
df
raw_content

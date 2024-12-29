"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel

from zipfile import ZipFile
import pandas as pd
import os

def clean_campaign_data():

    if not os.path.exists("files/output"):
        os.makedirs("files/output")
    
    #Creación de nombres de urls para acceder a los zip
    list_nums = [ "{:1d}".format(number) for number in range(10)]
    url_zips = "files/input/bank-marketing-campaing-{}.csv.zip"

    df = pd.DataFrame()

    #Concatenación de los archivos dentro de los zip en un Dataframe
    for num in list_nums:
        with ZipFile(url_zips.format(num), 'r') as zip:
            for file in zip.namelist():
                with zip.open(file) as f:
                    df_1 = pd.read_csv(f, header=0)
                    df = pd.concat(objs=[df,df_1],ignore_index=True)

    #Creación de los Dataframes solicitados
    client = df[["client_id","age","job","marital","education","credit_default","mortgage"]]
    campaign = df[["client_id","number_contacts","contact_duration","previous_campaign_contacts","previous_outcome","campaign_outcome"]]
    economics = df[["client_id","cons_price_idx","euribor_three_months"]]

    client = client.set_index("client_id")
    campaign = campaign.set_index("client_id")
    economics = economics.set_index("client_id")

    #Limpieza del Dataframe client
    client.job = client.job.str.replace(".","")
    client.job = client.job.str.replace("-","_")
    client.education = client.education.str.replace(".","_")
    client.education = client.education.map(lambda x: pd.NA if x == "unknown" else x)
    client.credit_default = client.credit_default.map(lambda x: 1 if x == "yes" else 0)
    client.mortgage = client.mortgage.map(lambda x: 1 if x == "yes" else 0)

    #Limpieza del Dataframe campaign
    campaign.previous_outcome = campaign.previous_outcome.map(lambda x: 1 if x == "success" else 0)
    campaign.campaign_outcome = campaign.campaign_outcome.map(lambda x: 1 if x == "yes" else 0)
    month_mapping = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
    df.month = df.month.map(month_mapping)
    campaign["last_contact_date"] = pd.to_datetime(dict(year="2022", month=df.month, day=df.day),errors="ignore")

    #Guardar los DataFrames en la carpeta files/output
    client.to_csv("files/output/client.csv", encoding="utf-8")
    campaign.to_csv("files/output/campaign.csv", encoding="utf-8")
    economics.to_csv("files/output/economics.csv", encoding="utf-8")
    
    return client,campaign,economics

    # """
    # En esta tarea se le pide que limpie los datos de una campaña de
    # marketing realizada por un banco, la cual tiene como fin la
    # recolección de datos de clientes para ofrecerls un préstamo.

    # La información recolectada se encuentra en la carpeta
    # files/input/ en varios archivos csv.zip comprimidos para ahorrar
    # espacio en disco.

    # Usted debe procesar directamente los archivos comprimidos (sin
    # descomprimirlos). Se desea partir la data en tres archivos csv
    # (sin comprimir): client.csv, campaign.csv y economics.csv.
    # Cada archivo debe tener las columnas indicadas.

    # Los tres archivos generados se almacenarán en la carpeta files/output/.

    # client.csv:
    # - client_id
    # - age
    # - job: se debe cambiar el "." por "" y el "-" por "_"
    # - marital
    # - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    # - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    # - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    # campaign.csv:
    # - client_id
    # - number_contacts
    # - contact_duration
    # - previous_campaing_contacts
    # - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    # - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    # - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
    #     combinando los campos "day" y "month" con el año 2022.

    # economics.csv:
    # - client_id
    # - const_price_idx
    # - eurobor_three_months



    # """

if __name__ == "__main__":
    clean_campaign_data()

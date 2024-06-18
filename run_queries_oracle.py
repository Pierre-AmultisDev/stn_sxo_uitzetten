import os
import csv
import json
import datetime

import oracledb

import pandas as pd
from remove_rtf_formatting import remove_rtf_formatting

# Added in run_queries_oracle.spec under hiddenimports=[]
# =========================================================
# https://stackoverflow.com/questions/75599583/python-no-module-named-secrets-oracledb-module

# =====================================
# SETUP SECTION
# =====================================
this_version = "v007"
print("[INFO   ] Retrieve data from oracle db to pandas df " + this_version + " gestart ...")
print("[INFO   ] Gestart om:", datetime.datetime.now())

with open("qry_parameters.json", 'r') as parametersfile:
    parameters = json.load(parametersfile)

database_interface = parameters["database"]["type"]
print("[INFO   ] Run for   :", database_interface)

with open("qry_connections.json", 'r') as connectionsfile:
    connections = json.load(connectionsfile)

# get the connection info
db_cnxn_info = parameters["database"]["name"][database_interface]

un = connections[db_cnxn_info]["un"]
cs = connections[db_cnxn_info]["cs"]
pw = connections[db_cnxn_info]["pw"]

con = None
cur = None

# return ./ when not found in parameters.json
sql_input_path = parameters.get("retrievedata", {}).get("sqlplus", {}).get("sql_folder", "./")

# return empty list [] when not found in parameters.json
qry_list = parameters.get("retrievedata", {}).get("sqlplus", {}).get("query_list", [])

# return ./out when not found in parameters.json
sql_output_path = parameters.get("filepaths", {}).get("dataoutputfolder", "./out/")

# if no value given assume output to excel is also required
output_to_excel = parameters.get("output", {}).get("output_to_excel", "true")

# if no value is given assumes Excel 97-2003 workbook size
max_excel_lines = int(parameters.get("output", {}).get("max_excel_lines", 65535))

dbg_lvl_df = int(parameters.get("retrievedata", {}).get("debug", {}).get("list_df", 1))
dbg_lvl_sql = int(parameters.get("retrievedata", {}).get("debug", {}).get("list_sql", 1))

if not os.path.exists(sql_output_path):
    os.makedirs(sql_output_path)

try:  # create connection with database
    con = oracledb.connect(user=un, password=pw, dsn=cs)

except oracledb.DatabaseError as er:
    print('[ERROR] There is an error in the Oracle database:', er)

else:
    print("[INFO   ] Oracle Database version:", con.version)
    if os.path.exists(sql_input_path) and len(qry_list) > 0:
        for qry in qry_list:
            df_all = pd.DataFrame()

            with open(sql_input_path + qry + '.sql', 'r') as file:
                sql_qry = file.read()
            if dbg_lvl_sql > 0:
                print("[INFO   ] Query     :")
                print("== START ===========================")
                print(sql_qry)
                print("==  END  ===========================")

            try:
                cur = con.cursor()

                # fetchall() is used to fetch all records from result set
                cur.execute(sql_qry)
                rows = cur.fetchall()
                if dbg_lvl_sql > 0:
                    print("== fetchall  START ===========================")
                    print(rows)
                    print("== fetchall   END   ==========================")
                # https://stackoverflow.com/questions/49949764/python-list-to-dataframe-with-column-headers-and-removing-data-types
                df_all = pd.DataFrame.from_records(rows, columns=[x[0] for x in cur.description])

            except oracledb.DatabaseError as er:
                print('There is an error in the Oracle database:', er)

            except Exception as er:
                print('Error:'+str(er))

            finally:
                if cur:
                    cur.close()

            if len(df_all) > 0:
                if dbg_lvl_df > 0:
                    print(df_all.columns.tolist())
                    print(df_all.dtypes)

                # remove rtf formatting
                if 'NOTITIE_TEKST' in df_all.columns.tolist():
                    # Apply the function to the column
                    df_all['NOTITIE_TEKST'+'_CLEAN'] = df_all['NOTITIE_TEKST'].apply(remove_rtf_formatting)
                    df_all.drop(columns=['NOTITIE_TEKST'], inplace=True)

                # set data format for all columns to string
                for column_name in df_all.columns.tolist():
                    df_all[column_name] = df_all[column_name].astype(str)
                    
                    # Cleanup
                    if column_name not in ['SQUITXO_ZAAKNUMMER'. 'OMSCHRIJVING', 'GLOBALE_LOCATIE',]:
                        df_all[column_name] = df_all[column_name].str.replace('NaT','')
                        df_all[column_name] = df_all[column_name].str.replace('None','')
                        df_all[column_name] = df_all[column_name].str.replace('nan','')
                    
                if dbg_lvl_df > 0:
                    print(df_all.dtypes)
                
                # save dataframe contents
                df_all.to_csv(sql_output_path+qry+".csv", index=False, sep=';', quotechar='"', quoting=csv.QUOTE_ALL)

                if len(df_all) < max_excel_lines and output_to_excel.lower() == "true":
                    df_all.to_excel(sql_output_path+qry+".xlsx", index=False, )

                if dbg_lvl_df > 0:
                    print(df_all.head())
                    print(df_all.tail())

finally:
    if con:
        con.close()

print()
print("[INFO   ] Gestopt om:", datetime.datetime.now())

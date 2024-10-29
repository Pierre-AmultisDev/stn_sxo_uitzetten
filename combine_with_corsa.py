import json
import datetime
import os

import pandas as pd

# =====================================
# SE TUP SECTION
# =====================================
this_version = "v002"
print("[INFO   ] Combineren van data uit squit oracle db met corsa dossierid" + this_version + " gestart ...")
print("[INFO   ] Gestart om:", datetime.datetime.now())

with open("corsa_parameters.json", 'r') as parametersfile:
    parameters = json.load(parametersfile)

input_folder = parameters["filepaths"]["input_folder"]
input_files_list = parameters["filepaths"]["input_files_list"]

corsa_folder = parameters["filepaths"]["corsa_folder"]
corsa_files_list = parameters["filepaths"]["corsa_files_list"]
dataoutputfolder = parameters["filepaths"]["dataoutputfolder"]

if not os.path.exists(dataoutputfolder):
   os.makedirs(dataoutputfolder)

# ===================================
for input_file in input_files_list:
    print("======================================================")
    print(input_file)
    input_df = pd.read_csv(input_folder+input_file, sep=";", quotechar='"', quoting=1, dtype=str)
    output_fields_list = input_df.columns.to_list()
    #print(input_df.columns)
    input_df['DOSSIERCODE'] = ""
    
    for corsa_file in corsa_files_list:
        print(corsa_file)
        corsa_df = pd.read_excel(corsa_folder+corsa_file, dtype=str)
        corsa_df.columns = corsa_df.columns.str.replace(' ', '_')
        corsa_df.drop_duplicates(inplace=True, ignore_index=True) 
        
        for index, row in input_df.iterrows():
            for check_column in ['SQTXO_EZ', 'SQUITXO_ZAAKNUMMER_AANGEPAST_B',
                                 'SQUITXO_ZAAKNUMMER_AANGEPAST_B_PUNT', 'SQUITXO_ZAAKNUMMER_AANGEPAST_S']:

                # check if value in check column is in the corsa file
                # print("-----------------------------------------")
                # print(check_column)
                # print(row[[check_column, 'SQUITXO_HOOFDZAAKNUMMER']])
                corsa_index = corsa_df.loc[corsa_df['KING_Zaakidentificatie'] == row[check_column]].index.tolist()
                # print(type(corsa_index))
                # print(corsa_index)
                if len(corsa_index) > 0: # some value found. As there are no duplicates in corsa_df, we can use the first 
                    # print(corsa_index[0])
                    dossierid = corsa_df.loc[corsa_index[0], 'Dossiercode']
                    # print(corsa_df.loc[corsa_index[0], 'Dossiercode'])                      
                    input_df.at[index, 'DOSSIERCODE'] = dossierid 
                    break # a value is found, no more need to test other columns    

    output_fields_list = ['DOSSIERCODE'] + output_fields_list
    input_df.drop_duplicates(inplace=True, ignore_index=True)
    
    met_corsadossiercode_df = input_df[input_df['DOSSIERCODE'] != ""]
    zonder_corsadossiercode_df = input_df[input_df['DOSSIERCODE'] == ""]
    
    met_corsadossiercode_df[output_fields_list].to_csv(dataoutputfolder+input_file+"_met_corsa_id.csv", sep=";", quotechar='"', quoting=1, index=False)
    met_corsadossiercode_df[output_fields_list].to_excel(dataoutputfolder+input_file+"_met_corsa_id.xlsx", index=False)
    
    zonder_corsadossiercode_df[output_fields_list].to_csv(dataoutputfolder+input_file+"_zonder_corsa_id.csv", sep=";", quotechar='"', quoting=1, index=False)
    zonder_corsadossiercode_df[output_fields_list].to_excel(dataoutputfolder+input_file+"_zonder_corsa_id.xlsx", index=False)
        
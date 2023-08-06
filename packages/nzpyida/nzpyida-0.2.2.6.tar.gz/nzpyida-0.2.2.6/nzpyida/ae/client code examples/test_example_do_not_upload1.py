from nzpyida import IdaDataBase, IdaDataFrame
from nzpyida.ae import NZFunGroupedApply, NZFunTApply
import pandas as pd
nzpy_cfg = {
"host":'nz-920b3fbb-6e57-4127-8d87-befeac080494.eastus2.data-warehouse.cloud.ibm.com',
"port":5480, "database":"telco", "logLevel":0}

nzpy_cfg = {"user":"admin", "password":"password", "host":'9.30.57.160', "port":5480, "database":"telco", "logLevel":0}

nzpy_dsn ={
        "database":"STOCKS",
        "port" :5480,
        "host" : "9.30.250.118",

        "logLevel":0
        }
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
#idadb = IdaDataBase(nzpy_cfg, uid="marcin",pwd="Netezza4Ever4Ever!", verbose=True)
idadb = IdaDataBase(nzpy_dsn, verbose=True)
print(idadb)
idadf = IdaDataFrame(idadb, 'stocks_date')
#print(idadf.head())
print(idadf.head(15))



code_str_host_spus = """def decision_tree_ml(self, df):

    #from sklearn.tree import DecisionTreeClassifier
    #features = df.columns[1:-1]
    #dt = DecisionTreeClassifier(min_samples_split=20, random_state=99)
    #dt.fit(df[features], df['IS_FRAUD'])
    self.output(['hello', 1 ] )

    

"""

output_signature = {'msg' :'str', 'RET': 'int'}



nz_fun_tapply = NZFunTApply(df=idadf, parallel=False, code_str=code_str_host_spus, fun_name="decision_tree_ml",
                                             output_signature=output_signature, merge_output_with_df=False, id='IMSI'  )

result = nz_fun_tapply.get_result()


import json
import pandas as pd
from etl_factory.factory.transform.abs_transform import AbsTransform

class JsonLivePositionTransform(AbsTransform):

    def execute(self, data_content):
        result = {}
        try:
            data_content = [json.loads(line) for line in data_content if line.strip()]

            event_list = ["create", "register", "update", "deregister"]
            df_data = {}
            df_dataframe = pd.DataFrame()

            for item in event_list:
                data = [period for period in data_content if period['event'] == item]
                if data:
                    list_periods = [pd.DataFrame.from_dict([row]) for row in data]
                    df_dataframe = pd.concat(list_periods, ignore_index=True)
                    data_column = pd.json_normalize(df_dataframe["data"])
                    df_dataframe = pd.concat([df_dataframe.drop("data", axis=1), data_column], axis=1)
                    df_dataframe = df_dataframe.reset_index()
                    print(df_dataframe)
                    df_data[item] = df_dataframe

            print("File Successfully Transformed")
            result['Validation'] = "SUCCESS"
            return result, df_data
        except:
            result['Validation'] = "FAILURE"
            result['Reason'] = "Error while transforming Json file in the source bucket"
            print('Error while transforming Json file')
            return result, None
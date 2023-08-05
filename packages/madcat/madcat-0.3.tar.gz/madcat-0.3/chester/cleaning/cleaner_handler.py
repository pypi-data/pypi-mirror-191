from chester.cleaning import cleaning_func as cln

from chester.zero_break.problem_specification import DataInfo


class CleanerHandler:
    def __init__(self, data_info: DataInfo, text_cleaner: cln.TextCleaner = None):
        self.data_info = data_info
        self.text_cleaner = text_cleaner
        if text_cleaner is not None:
            self.text_cleaner.df = self.data_info.data
        self.target = data_info.target
        self.problem_type_val = data_info.problem_type_val
        self.feature_types_val = data_info.feature_types_val
        self.loss_detector_val = data_info.loss_detector_val
        self.metrics_detector_val = data_info.metrics_detector_val
        self.model_selection_val = data_info.model_selection_val
        self.label_transformation_val = data_info.label_transformation_val

    def transform(self):
        text_columns = self.feature_types_val.get("text")
        for col in text_columns:
            if self.text_cleaner is not None:
                curr_text_cleaner = self.text_cleaner
                curr_text_cleaner.text_column = col
                text_cleaner = curr_text_cleaner
            else:
                text_cleaner = cln.TextCleaner(self.data_info.data, text_column=col)
            print(f"{col} text cleaning")
            text_cleaner.generate_report()
            self.data_info.data = cln.clean_text_df(text_cleaner)

#
# import numpy as np
#
# df1 = load_data_pirates().assign(target='chat_logs')
# df2 = load_data_king_arthur().assign(target='pirates')
# df = pd.concat([df1, df2])
#
# # Add numerical column
# df["number"] = np.random.uniform(0, 1, df.shape[0])
#
# # Add categorical column
# df["categ"] = 'aaa'
#
# # Add boolean column
# df["booly"] = True
#
# # df.drop(columns='text', inplace=True)
#
# # calc data into
# data_info = DataInfo(data=df, target='target')
# data_info.calculate()
# print(data_info)
# # extract features
# print(data_info.data[0:10])
#
# cleaner = CleanerHandler(data_info)
# cleaner.transform()
# print(cleaner.data_info.data[0:10])

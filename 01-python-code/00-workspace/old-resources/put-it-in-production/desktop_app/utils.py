from sklearn.externals import joblib
import pandas as pd


class SavedPipeline():
    def __init__(self, pipeline_fname, columns_data):
        self.pipeline = joblib.load(pipeline_fname)
        self.columns_data = columns_data

    def predict(self, observation):
        obs_df = self.dict_to_df(observation)
        prediction = self.pipeline.predict(obs_df)[0]
        return prediction

    def dict_to_df(self, obs):
        obs_df = pd.DataFrame([obs])
        for col, data in self.columns_data.items():
            if col in obs_df.columns and obs[col]:
                obs_df[col] = obs_df[col].astype(data["dtype"])
            else:
                obs_df[col] = None
        return obs_df


def load_dtypes(dtypes_fname):
    return joblib.load(dtypes_fname)

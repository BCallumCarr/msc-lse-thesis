"""data loading utilities"""
import time

from sklearn.externals import joblib
import pandas as pd


def load_dataset(dataset_fname, dtypes_fname, target_variable):
    """ Dataset loading function"""
    print(f"LOADING DATA FROM FILE {dataset_fname}")
    data = pd.read_csv(dataset_fname)
    dtypes = load_pickle(dtypes_fname)
    categorical_cols = []
    numerical_cols = []
    for col in data.columns:
        if col in dtypes:
            data[col] = data[col].astype(dtypes[col]["dtype"])
            # we only allow numerical or categorical for this pipeline
            if str(dtypes[col]["dtype"]) == "object":
                categorical_cols.append(col)
            else:
                numerical_cols.append(col)
    y = data[target_variable]
    X = data[list(dtypes.keys())]
    return X, y, categorical_cols, numerical_cols

def load_pickle(pickle_file):
    return joblib.load(pickle_file)

def save_pipeline(pipeline):
    """exports a pipeline with a timestamp appended"""
    print("SAVING TRAINED PIPELINE")
    joblib.dump(pipeline, "pipeline.pkl")

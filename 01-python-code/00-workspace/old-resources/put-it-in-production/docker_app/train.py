"""
Retrains a predictive model pipeline to predict house pricing.

Inputs:
    - a CSV formatted file named `training_listings.csv` located in this folder, containing listing properties and sale price.
    This dataset needs to follow the (pandas) data types contained in `dtypes.pkl` (that needs to be in this folder too).
    Additionally, the prices must be in a column named `sale_price` and must be decimals.
Outputs:
    - a file named `pipeline.pkl` that contains a scikit-learn model that can be used by the file `predict.py` to create
    new predictions
To run:
    $ python train.py
"""
from category_encoders import OneHotEncoder
from mlxtend.feature_selection import ColumnSelector
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline, make_union
from sklearn.preprocessing import StandardScaler

from utils import load_dataset, save_pipeline

PRICE_DATASET_FNAME = "training_listings.csv"
DTYPES_FNAME = "dtypes.pkl"
TARGET_VARIABLE = "sale_price"


def train_pipeline(X, y, categorical_cols, numerical_cols):
    """
    Builds and trains a scikit-learn pipeline
    """
    processing_pipeline = make_union(
        make_pipeline(
            ColumnSelector(cols=categorical_cols),
            OneHotEncoder()
        ),
        make_pipeline(
            ColumnSelector(cols=numerical_cols),
            SimpleImputer(),
            StandardScaler()
        )
    )
    predictive_pipeline = make_pipeline(
        processing_pipeline,
        RandomForestRegressor(
             bootstrap=True,
             max_features=10,
             min_impurity_decrease=0.9102981779915218,
             min_samples_leaf=5,
             min_samples_split=7,
             n_estimators=890,
        )
    )
    predictive_pipeline.fit(X, y)
    return predictive_pipeline


def main():
    """
    Main function.
    1 .Loads the listings price data
    2. trains a machine learning pipeline
    3. exports the pipeline to a file
    """
    X, y, categorical_cols, numerical_cols = load_dataset(PRICE_DATASET_FNAME, DTYPES_FNAME, TARGET_VARIABLE)
    trained_pipeline = train_pipeline(X, y, categorical_cols, numerical_cols)
    save_pipeline(trained_pipeline)


if __name__ == "__main__":
    main()

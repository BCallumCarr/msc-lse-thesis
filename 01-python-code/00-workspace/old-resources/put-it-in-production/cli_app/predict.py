"""
Provide price predictions for new listings

Inputs:
    - a CSV formatted file named `input_listings.csv` located in this folder, containing listing properties.
    This dataset needs to follow the (pandas) data types contained in `dtypes.pkl` (that needs to be in this folder too).
Outputs:
    - a file named `output_listings.csv` that contains the same input file plus a new column (sale_price) with the predicted sale price
To run:
    $python predict.py
"""
import pandas as pd
from utils import load_pickle

INPUT_DATASET = "input_listings.csv"
TARGET_VARIABLE = "sale_price"
OUTPUT_DATASET = "output_listings.csv"


def main():
    """
    Main function.
    1 .Loads the input listings price data
    2. loads a trained machine learning pipeline
    3. adds predictions to the file and saves it
    """
    print("LOAD LISTINGS DATA")
    input_listings = pd.read_csv(INPUT_DATASET)
    pipeline = load_pickle("pipeline.pkl")
    print("PREDICTING PRICES")
    # we dont care about cents in the prices of houses
    input_listings[TARGET_VARIABLE] = pipeline.predict(input_listings).astype(int)
    print("SAVING OUTPUT")
    input_listings.to_csv(OUTPUT_DATASET, index=False)


if __name__ == "__main__":
    main()

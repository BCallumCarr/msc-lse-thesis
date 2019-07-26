"""
Provide price predictions for new listings

Inputs:
    a dictionary for an observation
Outputs:
    prints a sale price prediction
To run:
    $python predict.py

Example Observation

obs = {
    'building_class': 60,
    'lot_area': 8450,
    'overall_quality': 7,
    'overall_condition': 5,
    'year_build': 2003,
    'first_floor_area': 856,
    'second_floor_area': 854,
    'n_bedrooms': 3,
    'n_kitchens': 1,
    'n_full_baths': 2,
    'n_half_baths': 1,
    'pool_area': 0,
    'garage_area': 548,
    'n_fireplaces': 0,
    'sale_price': 208500,
    'house_style': '2Story',
    'foundation': 'PConc'
}

"""
import sys
import json
from pprint import pprint

from utils import load_pickle, dict_to_df


def main(obs):
    """
    Main function.
    1 .Loads the input listings price data
    2. loads a trained machine learning pipeline
    3. adds predictions to the file and saves it
    """
    pipeline = load_pickle("pipeline.pkl")
    dtypes = load_pickle("dtypes.pkl")
    obs_df = dict_to_df(obs, dtypes)
    # we dont care about cents in the prices of houses
    prediction = pipeline.predict(obs_df).astype(int)
    print(prediction[0])


if __name__ == "__main__":
    obs = json.loads(''.join(sys.argv[1:]))
    main(obs)

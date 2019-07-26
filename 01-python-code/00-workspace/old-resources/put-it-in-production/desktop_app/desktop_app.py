#! /usr/bin/env python
"""
Example of desktop application that loads a scikit-learn pipeline to predict house prices
The desktop UI is built with Gooey, which can be installed with:

    'pip install Gooey '
"""
import warnings
warnings.simplefilter("ignore")
import time

from gooey import Gooey, GooeyParser
from utils import SavedPipeline, load_dtypes
from mlxtend.feature_selection import ColumnSelector


def load_pipeline(pipeline_fname, dtypes_fname):
    pipeline = SavedPipeline(pipeline_fname, dtypes_fname)
    return pipeline


@Gooey(dump_build_config=True, program_name="Real State price prediction tool")
def main():
    """
    observation = {
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

    pipeline = SavedPipeline("pipeline_ames.pkl", column_data)

    prediction = pipeline.predict(observation)
    print("observation: {}".format(observation))
    print("Predicted Price: {:.2f}€".format(prediction))
    """
    settings_msg = "Please submit property characteristics"
    column_data = load_dtypes("dtypes.pkl")

    parser = GooeyParser(description=settings_msg)
    parser.add_argument('--verbose', help='be verbose', dest='verbose',
                      action='store_true', default=False)
    subs = parser.add_subparsers(dest="property_info")

    property_parser = subs.add_parser('property_info')
    property_parser.add_argument('--model_path',
                           type=str, widget='FileChooser')

    for column_name, data in column_data.items():
        if data["dtype"] == object:
            property_parser.add_argument("--{}".format(column_name),
                                    widget='Dropdown',
                                    choices=data["options"])
        else:
            property_parser.add_argument("--{}".format(column_name))
    args = parser.parse_args()
    pipeline = load_pipeline(args.model_path, column_data)
    observation = vars(args)
    prediction = pipeline.predict(observation)

    def display_message(observation, prediction):
        message = ["\n***********\nOutput for property:"]
        for key, value in observation.items():
            if value:
                message.append("{}:{}".format(key, value))
        message.append("Predicted house value: {:.2f}$".format(prediction))
        delay = 1.8 / len(message)

        for line in message:
            print(line)
            time.sleep(delay)
    display_message(observation, prediction)


if __name__ == "__main__":
    main()

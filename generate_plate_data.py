import pandas as pd
from utils.converter_utils import ConverterUtils
from utils.constants import Constants
import json


def generate_plate_data(hts_dataframe: pd.DataFrame):
    print("Processing HTS data...")

    # Data paths
    schedule_b_reference_path = 'data/schedule_b_reference.xlsx'
    hts_data = hts_dataframe

    # Cleans HTS code to n figures, removes apostrophe at start of code (ex. clean('010287, 4) => 0102)
    def clean_hts_value(hts_value, figures=4):
        return int(hts_value[1:figures + 1])

    hts_data["HTS"] = hts_data["HTS"].apply(clean_hts_value)

    utils = ConverterUtils(schedule_b_reference_path)
    code_to_category = utils.schedule_b_to_category()

    nutrient_distribution_yearly = {}

    min_year, max_year = hts_data["year"].min(), hts_data["year"].max()
    for year in range(min_year, max_year + 1):
        print("Processing year {}".format(year))
        plate_distribution = {cat: 0 for cat in Constants.get_food_categories()}
        data_current_year = hts_data[hts_data["year"] == year]
        for index, row in data_current_year.iterrows():
            if row["HTS"] in code_to_category:
                plate_distribution[code_to_category[row['HTS']]] += 1

        # BANDAID: MOVE ICECREAM COUNT TO OTHER
        plate_distribution["other"] += plate_distribution["ice_cream"]
        plate_distribution.pop("ice_cream")

        nutrient_distribution_yearly[year] = plate_distribution

    # Add latest month for newest data
    latest_month = hts_data[hts_data["year"] == max_year]["month"].max()
    nutrient_distribution_yearly["latest_year_extra"] = {
        "latest_month": int(latest_month)
    }

    plate_data_out = 'data/plate/nutrient_distribution_yearly.json'
    with open(plate_data_out, 'w') as f:
        json.dump(nutrient_distribution_yearly, f, indent=4)

    print(f'Done, extracted data is available in {plate_data_out}')


if __name__ == '__main__':
    pass

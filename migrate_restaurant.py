import pandas as pd
from dotenv import load_dotenv

from constants import DATA_DIR_NAME
from gmap import *

load_dotenv(verbose=True)


class RestaurantMigrator:
    """Add necessary restaurant info to dataset.
    - Add lat and lng to restaurant.csv
    - Add restaurant id to reviews.csv
    Note: This is a very slow operation.
    """

    def __init__(self, review_path):
        self.review_df = pd.read_csv(review_path)

    def migrate(self):
        review_df = self.review_df.copy()
        review_df.columns = map(str.lower, review_df.columns)
        df = review_df[["name", "location"]]
        df = df.drop_duplicates().reset_index(drop=True)
        df["id"] = df.index

        for index, row in df.iterrows():
            loc = get_lat_lng(row["location"])
            df.at[index, "lat"] = loc["lat"]
            df.at[index, "lng"] = loc["lng"]

        # lowercase columns name
        df.columns = map(str.lower, df.columns)
        df.to_csv("./{}/restaurants.csv".format(DATA_DIR_NAME), index=False)

        # add/update id columns in reviews.csv
        review_df['res_id'] = review_df.apply(
            lambda x: df[(df['name'] == x['name']) & (df['location'] == x['location'])]['id'].iloc[0],
            axis=1
        )
        # Change id column to the beginning
        review_df = review_df.reindex(columns=['res_id'] + review_df.columns[:-1].tolist())
        review_df.to_csv("./{}/reviews.csv".format(DATA_DIR_NAME), index=False)


if __name__ == '__main__':
    RestaurantMigrator("./{}/reviews_origin.csv".format(DATA_DIR_NAME)).migrate()

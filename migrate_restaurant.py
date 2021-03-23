import pandas as pd
from dotenv import load_dotenv
from tinydb import TinyDB

from constants import DATA_DIR_NAME, RESTAURANT_DB_PATH
from gmap import *

load_dotenv(verbose=True)


class RestaurantMigrator:
    """Add necessary restaurant info to dataset.
    - Add lat and lng to restaurant db
    - Add restaurant id to reviews.csv
    Note: This is a very slow operation.
    """
    reviews_output_path = "./{}/reviews.csv".format(DATA_DIR_NAME)

    def __init__(self, review_path):
        self.review_df = pd.read_csv(review_path)
        self.restaurant_db = TinyDB(RESTAURANT_DB_PATH)

    def migrate(self):
        review_df = self.review_df.copy()
        review_df.columns = map(str.lower, review_df.columns)
        df = review_df[["name", "location"]]
        df = df.drop_duplicates().reset_index(drop=True)
        df["id"] = df.index
        # Change id column to the beginning
        df = df.reindex(columns=['id'] + df.columns[:-1].tolist())

        for index, row in df.iterrows():
            loc = get_lat_lng(row["location"])
            df.at[index, "lat"] = loc["lat"]
            df.at[index, "lng"] = loc["lng"]

        # lowercase columns name
        df.columns = map(str.lower, df.columns)
        # Remove all restaurants1 and write to db
        self.restaurant_db.truncate()
        self.restaurant_db.insert_multiple(df.to_dict('records'))

        # add/update id columns in reviews.csv
        review_df['res_id'] = review_df.apply(
            lambda x: df[(df['name'] == x['name']) & (df['location'] == x['location'])]['id'].iloc[0],
            axis=1
        )
        # Change id column to the beginning
        review_df = review_df.reindex(columns=['res_id'] + review_df.columns[:-1].tolist())
        review_df.to_csv(self.reviews_output_path, index=False)


if __name__ == '__main__':
    RestaurantMigrator("./{}/reviews_origin.csv".format(DATA_DIR_NAME)).migrate()

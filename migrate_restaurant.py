from dotenv import load_dotenv
import pandas as pd

load_dotenv(verbose=True)


def migrate_restaurant():
    review_df = pd.read_csv("./data/reviews.csv")


if __name__ == '__main__':
    migrate_restaurant()

# Script to run an additional transformation on the input data
import os
import random
import argparse
import pandas as pd


def get_file_list(pathway):
    """Script to get all image file paths"""
    file_paths = []
    for root, _, filenames in os.walk(pathway):
        for filename in filenames:
            if ".csv" in filename:
                file_paths.append(os.path.join(root, filename))
    return file_paths


def main(source=None, output_path=None):

    file_list = get_file_list(source)
    df = pd.read_csv(file_list[0])  # + '/' + filename)
    print(df.head())

    # Get list of place, and filter for a random sample
    place_list = list(df['place_name'].unique())
    random_sample = random.sample(place_list, 5)
    df = df[df['place_name'].isin(random_sample)]

    # Re-format to get places in columns
    dfx = df.pivot_table(index=['yr', 'period'], values='index_nsa', columns='place_name').reset_index()
    print(dfx.head())
    print(f" Random sample length is {len(dfx)}")
    df.to_csv(output_path + "/" + 'random_cities.csv', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="filepaths")
    parser.add_argument("--input_data", help='Input file path')
    parser.add_argument("--output_data", help='Output file path')
    args = parser.parse_args()
    main(source=args.input_data, output_path=args.output_data)

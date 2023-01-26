# Script to run a few data filtering and transformation operations
import os
import argparse
import pandas as pd


def get_file_list(pathway):
    """Script to get all image file paths"""
    file_paths = []
    for root, _, filenames in os.walk(pathway):
        for filename in filenames:
            if "random_cities.csv" in filename:
                file_paths.append(os.path.join(root, filename))
    return file_paths


def main(source=None, output_path=None):
    file_list = get_file_list(source)
    print(file_list)
    df = pd.read_csv(file_list[0])
    mth_qtr_mapping = {1: 3, 2: 6, 3: 9, 4: 12}

    # Filtering conditions
    df = df[(df['frequency'] == 'quarterly') &
            (df['level'] == 'MSA') &
            (df['hpi_type'] == 'traditional') &
            (df['hpi_flavor'] == 'all-transactions')]
    '''
    As this passes to the OutputDatasetFileConfig, string specifics like commas
    in the name of the place can cause errors like pandas.errors.ParserError: Error tokenizing data. C error:
    Calling read(nbytes) on source failed. Try engine='python'. To avoid that, do
    some string formatting here to make this a tighter process.
    '''
    # String formatting
    df['place_name'] = df['place_name'].str.replace(',', '|')
    df['place_name'] = df['place_name'].str.replace(' ', '')
    # Added columns, for date changes
    df['month'] = df['period'].map(mth_qtr_mapping).astype(str)
    df = df.rename(columns={'yr': 'year'})
    df['year'] = df['year'].astype(str)
    df['day'] = '1'
    df['Date'] = pd.to_datetime(df[['year', 'month', 'day']])

    # Given data gaps between MSAs, starting from Q4, 2000
    df = df.loc[df['Date'] >= '2000-11-01']
    print(df.head())

    # Drop unneeded columns
    df = df.drop(['frequency', 'level', 'hpi_type',
                  'hpi_flavor', 'year', 'period', 'day', 'month',
                  'index_sa', 'place_id'], axis=1)
    df.to_csv(output_path + '/' + 'data_prep.csv', index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="filepaths")
    parser.add_argument("--input_data", help='Input file path')
    parser.add_argument("--output_data", help='Output file path')
    args = parser.parse_args()
    main(source=args.input_data, output_path=args.output_data)

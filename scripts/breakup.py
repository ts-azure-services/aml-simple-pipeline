# Script to run an additional transformation on the input data
import datetime, random, argparse
import pandas as pd
import datetime as dt

def getArgs(argv=None):
    parser = argparse.ArgumentParser(description="filepaths")
    parser.add_argument("--input_file_path", help='Input file path')
    parser.add_argument("--output_file_path", help='Output file path')
    parser.add_argument("--filename", help='Filename')
    return parser.parse_args(argv)

def breakup(source=None, filename=None):
    df = pd.read_csv(source + '/' + filename)
    print(df.head())

    # Get list of place, and filter for a random sample
    place_list = list(df['place_name'].unique())
    random_sample = random.sample(place_list, 5)
    df = df [ df['place_name'].isin(random_sample) ]

    # Re-format to get places in columns
    dfx = df.pivot_table(index='Date',values='index_nsa', columns='place_name')
    print(dfx.head())
    print(f" Random sample length is {len(dfx)}")
    return dfx
    
if __name__ == "__main__":
    args = getArgs()
    print(f'Input args: {args.input_file_path}')
    print(f'Output args: {args.output_file_path}')
    output_filename = '/finalresults.csv'
    df = breakup(source=args.input_file_path, filename=args.filename)
    df.to_csv(args.output_file_path + output_filename, index=False)

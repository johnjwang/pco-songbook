import argparse

import generator

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('out_file')
    parser.add_argument('--csv', help='CSV file, required for CSV mode.')
    parser.add_argument('--band', help='Executes band mode (no CSV required, pulls all songs from API.', action='store_true')
    args = parser.parse_args()

    if args.band:
        generator.generate_from_api(args.out_file)
    else:
        generator.generate_from_csv(args.csv, args.out_file)

if __name__ == '__main__':
    main()

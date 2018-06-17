import sys

import generator


def main():
    if len(sys.argv) != 3:
        print('Usage: pco-songbook input.csv output.pdf')
        return

    generator.generate_pdf(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()

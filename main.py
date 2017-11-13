from itertools import islice

def main():
    filename = ""
    rate = 6
    with open(filename, 'r') as infile:
        lines_gen = islice(infile, rate)

    infile.close()

if __name__ == "__main__":
    main()
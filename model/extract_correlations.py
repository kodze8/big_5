from tabula import read_pdf
import pandas as pd

PATH = "/Users/saikodze/Desktop/Supplemental_material.pdf"


def read_table():
    global PATH
    tb = []
    for x in range(13, 15):
        pages_to_extract = [12, x]

        data = read_pdf(PATH, pages=pages_to_extract, multiple_tables=True)
        tb.append(data[0])

    column_names = tb[0].iloc[0]
    tb[0] = tb[0][1:]
    tb[0].columns = column_names
    tb[1].loc[tb[1].shape[0]] = tb[1].columns
    tb[1].columns = column_names

    concatenated = pd.concat([tb[0], tb[1]], axis=0)
    concatenated.set_index("Genres", drop=True, inplace=True)
    return concatenated


def write_table():
    with open("correlation.csv", "w") as file:
        read_table().to_csv(file)


if __name__ == '__main__':
    write_table()

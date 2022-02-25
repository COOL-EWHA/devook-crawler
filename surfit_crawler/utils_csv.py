import csv


def save_to_csv(
        file_name, column, data
):  # file_name: string, columns: list, data: [(), (), ..] list(tuple)
    with open(file_name, mode="w", newline="", encoding="utf-8") as out:
        csv_out = csv.writer(out)
        csv_out.writerow(column)
        for row in data:
            csv_out.writerow(row)

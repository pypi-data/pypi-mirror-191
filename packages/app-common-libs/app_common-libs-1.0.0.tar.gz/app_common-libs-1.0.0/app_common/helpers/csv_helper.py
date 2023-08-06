import csv
from io import StringIO


def write_into_csv(data):
    csv_file = StringIO()
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(data)
    return csv_file

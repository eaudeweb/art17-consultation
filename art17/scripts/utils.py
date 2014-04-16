import csv
from StringIO import StringIO

def generate_csv(header, rows, delimiter=','):

    output = StringIO()
    csv_writer = csv.writer(output, delimiter=delimiter)

    csv_writer.writerow(header)
    for item in rows:
        csv_writer.writerow([value.encode('utf-8') for value in item])

    return output.getvalue()

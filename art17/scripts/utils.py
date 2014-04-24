import csv
from StringIO import StringIO


def generate_csv(header, rows, delimiter=','):
    output = StringIO()
    csv_writer = csv.writer(output, delimiter=delimiter)

    csv_writer.writerow(header)
    for item in rows:
        csv_writer.writerow([value.encode('utf-8') for value in item])

    return output.getvalue()


def dump_to_file(filename, data):
    with open(filename, 'w') as file_out:
        file_out.write(data)


def do_csv_export(header, rows, filename):
    ret = generate_csv(header, rows)
    if filename:
        dump_to_file(filename, ret)
    else:
        print ret

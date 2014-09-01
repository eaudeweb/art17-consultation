import codecs
import csv
from StringIO import StringIO


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        data = self.encoder.encode(data)
        self.stream.write(data)
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def generate_csv(header, rows, delimiter=','):
    output = StringIO()
    csv_writer = UnicodeWriter(output, delimiter=delimiter)

    csv_writer.writerow(header)
    for item in rows:
        csv_writer.writerow([value for value in item])

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

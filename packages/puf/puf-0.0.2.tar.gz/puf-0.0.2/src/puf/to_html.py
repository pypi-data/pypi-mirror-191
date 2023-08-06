#!/usr/bin/env python
import sys
import json
import logging
from collections.abc import Mapping, Sequence


logging.basicConfig(level=logging.INFO)


class App:
    def main(self, files):
        for infile in files:
            outfile = f"{infile}.html"
            logging.info("handling %s", infile)
            self.handle(infile, outfile)

    def handle(self, infile, outfile):
        with open(infile) as fin:
            txt = fin.read()
        obj = json.loads(txt)
        rows = self.extract_rows(obj)
        if not rows:
            return
        with open(outfile, "wt") as fout:
            self.to_html(fout, rows)

    def extract_rows(self, obj):
        if isinstance(obj, Sequence):
            return obj

        data = obj.get("data", None)
        if isinstance(data, str):  # DMS
            data = json.loads(data)
            return data["data"]
        elif instance(data, Mapping):  # RDS
            return data["data"]

        raise RuntimeError("unsupported format")

    def to_html(self, fout, rows):
        if isinstance(rows[0], Mapping):
            keys = tuple(rows[0].keys())
        else:
            keys = range(len(rows[0]))
        fout.write("<table>\n")
        for row in rows:
            fout.write("<tr>")
            for k in keys:
                it = str(row[k]).replace("<", "&lt;").replace(">", "&gt;")
                it = it.replace("\n", "<br/>")
                fout.write(f"<td>{it}</td>")
            fout.write("</tr>\n")
        fout.write("</table>")


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} input.json")
        sys.exit(1)

    App().main(sys.argv[1:])


if __name__ == "__main__":
    main()

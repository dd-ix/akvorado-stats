import argparse
import os
import datetime
import matplotlib.pyplot as plt
import numpy as np
import yaml
import sys


def latin_prefix(scale):
    if scale >= 10**9:
        return "G"
    elif scale >= 10**6:
        return "M"
    elif scale >= 10**3:
        return "k"
    else:
        return ""


def check_yaml_filename(fn):
    """
    Checks if the given path is a file
    """
    print(fn)
    for path in fn:
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError(f"{path} does not exist")
        if not os.path.isfile(path):
            raise argparse.ArgumentTypeError(f"{path} is not a file")

    return fn


def check_time_stamp(ts):
    return datetime.datetime.fromisoformat(ts)


# Instantiate the parser
parser = argparse.ArgumentParser(description="DD-IX Traffic Analysis Tooling")
parser.add_argument("-d", "--data", nargs="+", help="Paths to the yaml file containing the stats")
parser.add_argument("--scale", type=int, default=10**9)
parser.add_argument("--ignore", nargs="+", default=[])

args = parser.parse_args()
yaml_file = None

if args.data == []:
    print("no data file specified!")
    sys.exit(1)

data = {}


for path in args.data:
    with open(path) as stream:
        try:
            yaml_file = yaml.safe_load(stream)

            for as_number, numbers in yaml_file["top_peers"].items():
                if str(as_number) not in args.ignore:
                    if as_number not in data:
                        data[as_number] = {
                            "org": numbers["org"],
                            "in_p95": numbers["in_p95"],
                            "out_p95": numbers["out_p95"],
                            "in_avg": numbers["in_avg"],
                            "out_avg": numbers["out_avg"],
                        }
                    else:
                        data[as_number]["in_p95"] += numbers["in_p95"]
                        data[as_number]["out_p95"] += numbers["out_p95"]
                        data[as_number]["in_avg"] += numbers["in_avg"]
                        data[as_number]["out_avg"] += numbers["out_avg"]

        except yaml.YAMLError as exc:
            print("cannot parse yaml file", exc)
            sys.exit(1)

as_numbers = data.keys()
names = []
in_p95 = []
out_p95 = []
in_avg = []
out_avg = []

for as_number, values in data.items():
    names.append(values["org"])
    in_p95.append(values["in_p95"])
    out_p95.append(values["out_p95"])
    in_avg.append(values["in_avg"])
    out_avg.append(values["out_avg"])

zipped = sorted(zip(in_p95, out_p95, in_avg, out_avg, names, as_numbers), reverse=True)

p95_in, p95_out, avg_in, avg_out, names, as_numbers = zip(*zipped)

data = {"in_p95": p95_in, "out_p95": p95_out, "in_avg": avg_in, "out_avg": avg_out}

x = np.arange(len(names))
width = 0.25
multiplier = 0

fig, ax = plt.subplots()

for attribute, measurement in data.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    multiplier += 1

ax.set_ylabel("traffic with network in " + latin_prefix(args.scale) + "bit/s")
ax.set_title("AS numbers of different networks")
ax.set_xticks(x + width, names, rotation=40, ha="right")
ax.legend(loc="upper left", ncols=4)
plt.title("Traffic-Statistics recorded from " + yaml_file["from"] + " until " + yaml_file["to"], loc="center")
plt.show()

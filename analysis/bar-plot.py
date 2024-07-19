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
    if not os.path.exists(fn):
        raise argparse.ArgumentTypeError(f"{fn} does not exist")
    if not os.path.isfile(fn):
        raise argparse.ArgumentTypeError(f"{fn} is not a file")

    return fn


def check_time_stamp(ts):
    return datetime.datetime.fromisoformat(ts)


# Instantiate the parser
parser = argparse.ArgumentParser(description="DD-IX Traffic Analysis Tooling")
parser.add_argument("-d", "--data", type=check_yaml_filename, help="Path to the yaml file containing the stats")

parser.add_argument("--scale", type=int, default=10**9)
parser.add_argument("--ignore", nargs="+", default=[])

args = parser.parse_args()
yaml_file = None

if args.data is None:
    print("no data file specified!")
    sys.exit(1)

with open(args.data) as stream:
    try:
        yaml_file = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print("cannot parse yaml file", exc)
        sys.exit(1)

as_numbers = []
names = []
p95_in = []
p95_out = []
avg_in = []
avg_out = []

for as_number, numbers in yaml_file["top_peers"].items():
    if str(as_number) not in args.ignore:
        as_numbers.append(as_number)
        names.append(numbers["org"])
        p95_in.append(numbers["in_p95"] / args.scale)
        p95_out.append(numbers["out_p95"] / args.scale)
        avg_in.append(numbers["in_avg"] / args.scale)
        avg_out.append(numbers["out_avg"] / args.scale)


zipped = sorted(zip(p95_in, p95_out, avg_in, avg_out, names, as_numbers), reverse=True)

p95_in, p95_out, avg_in, avg_out, names, as_numbers = zip(*zipped)

data = {"in_p95": p95_in, "out_p95": p95_out, "in_avg": avg_in, "out_avg": avg_out}

x = np.arange(len(names))
width = 0.25
multiplier = 0

fig, ax = plt.subplots()

for attribute, measurement in data.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    # ax.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel("traffic with network in " + latin_prefix(args.scale) + "bit/s")
ax.set_title("AS numbers of different networks")
ax.set_xticks(x + width, names, rotation=40, ha='right')
ax.legend(loc="upper left", ncols=4)
plt.title("Traffic-Statistics recorded from " + yaml_file["from"] + " until " + yaml_file["to"], loc='center')
plt.show()

#!/usr/bin/env python3


import clickhouse_connect
from collections import namedtuple
import math
import numpy as np
import argparse
import os
import datetime
import configparser

def is_ini_file(string):
    if os.path.exists(string):
        return string
    else:
        raise NotADirectoryError(string)


# Instantiate the parser
parser = argparse.ArgumentParser(description='DD-IX Akvorado Stat Collector')
parser.add_argument('--config', type=is_ini_file)

parser.add_argument(
        '--starttime',
        type=lambda s: datetime.datetime.fromisoformat(s),
)

parser.add_argument(
        '--endtime',
        type=lambda s: datetime.datetime.fromisoformat(s),
)


args = parser.parse_args()
config = configparser.ConfigParser()
config.read(args.config)

time_range = [args.starttime, args.endtime]
si_prefixes = ['', 'K', 'M', 'G']


def format_bps(n):
    idx = max(0,
              min(
                  len(si_prefixes) - 1,
                  int(math.floor(0 if n == 0 else math.log10(abs(n))/3))
              )
              )

    return '{:.0f}{}bps'.format(n / 10**(3 * idx), si_prefixes[idx])


# client = clickhouse_connect.get_client(host='akvorado.ibh.net', secure=True, port=443, username='default', password='password')
client = clickhouse_connect.get_client(host='localhost')
result = client.query(f"""
 WITH
 source AS (SELECT * FROM flows_5m0s SETTINGS asterisk_include_alias_columns = 1),
 rows AS (SELECT SrcAS FROM source WHERE TimeReceived BETWEEN toDateTime('{time_range[0]}', 'UTC') AND toDateTime('{time_range[1]}', 'UTC') AND (InIfBoundary = 'external') GROUP BY SrcAS ORDER BY SUM(Bytes) DESC LIMIT 50)
SELECT 1 AS axis, * FROM (
SELECT
 toStartOfInterval(TimeReceived + INTERVAL 900 second, INTERVAL 900 second) - INTERVAL 900 second AS time,
 SUM(Bytes*SamplingRate*8)/900 AS xps,
 if((SrcAS) IN rows, [concat(toString(SrcAS), ': ', dictGetOrDefault('asns', 'name', SrcAS, '???'))], ['Other']) AS dimensions
FROM source
WHERE TimeReceived BETWEEN toDateTime('{time_range[0]}', 'UTC') AND toDateTime('{time_range[1]}', 'UTC') AND (InIfBoundary = 'external')
GROUP BY time, dimensions
ORDER BY time WITH FILL
 FROM toDateTime('{time_range[0]}', 'UTC')
 TO toDateTime('{time_range[1]}', 'UTC') + INTERVAL 1 second
 STEP 900
 INTERPOLATE (dimensions AS ['Other']))
""")

# build list of bandwidths per ASN
asn_xps = {}
for axis, ts, xps, asn in result.result_rows:
    if asn[0] in asn_xps:
        asn_xps[asn[0]].append(xps)
    else:
        asn_xps[asn[0]] = [xps]

# build stats for each ASN
asn_stats = {}
for asn, xps in asn_xps.items():
    arr = np.array(xps)

    stats = {
      'avr': np.mean(arr),
      'p95': np.percentile(arr, 95),
    }

    asn_stats[asn] = namedtuple('ASNStats', stats.keys())(**stats)

# sort & print ASN stats
for asn, stats in sorted(asn_stats.items(), key=lambda i: i[1].p95):
    print("{asn: <42} {avr: >8} {p95: >8}".format(asn=asn, avr=format_bps(stats.avr), p95=format_bps(stats.p95)))

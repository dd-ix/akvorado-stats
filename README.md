# Akvorado top ASN stats

This repository contains some scripts to fetch the top ASN traffic from a clickhouse instance containing [Akvorado](https://github.com/akvorado/akvorado) flow data.

## Configuration

Inside the file ./akvo-top-asn/akvo-top-asn.conf.ex there is an example config on how to use the collection script.

## Automatic Collection Campaign

Both the Systemd-Timer and the CronJob are configured to collect data every sunday at 00:00. In those examples the script is located inside the 
`/var/lib` folder please update the locations based on your deployment.

### Systemd

**Systemd One-Shot Unit**

`/etc/systemd/system/dd-ix-export.service`
```
[Unit]
Description=DD-IX Traffic Statistics Collection

[Service]
Type=oneshot
ExecStart=/var/lib/akvorado-stats/akvo-top-asn/akvo-top-asn --week 1 --config=/var/lib/akvorado-stats/akvorado-top-asn/akvo-top-asn.conf
RemainAfterExit=yes
```

**Systemd Timer**

`/etc/systemd/system/dd-ix-export.timer`
```
[Unit]
Description=Run DD-IX Traffic Collection weekly

[Timer]
OnCalendar=weekly
Persistent=true

[Install]
WantedBy=timers.target
```

### CronJob

```
0 0 * * 0 /var/lib/akvorado-stats/akvo-top-asn/akvo-top-asn --week 1 --config=/var/lib/akvorado-stats/akvorado-top-asn/akvo-top-asn.conf
```

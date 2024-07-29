# Akvorado top ASN stats

This repository contains some scripts to fetch the top ASN traffic from a clickhouse instance containing [Akvorado](https://github.com/akvorado/akvorado) flow data.

## Configuration

Inside the file ./akvo-top-asn/akvo-top-asn.conf.ex there is an example config on how to use the collection script.

## Automatic Collection Campaign

Both the Systemd-Timer and the CronJob are configured to collect data every sunday at 00:00. In those examples the script is located inside the 
`/usr/src/` folder please update the locations based on your deployment. The script needs to some python dependencies to be installed in the 
system which can be found inside the `requirements.txt` using the following command `pip install -r ./requirements.txt`.

### Systemd

**Systemd One-Shot Unit**

`/etc/systemd/system/akvorado-top-asn-export.service`
```
[Unit]
Description=Akvorado Top ASN Collection Timer

[Service]
Type=oneshot
User=akvorad-stats
ExecStart=/usr/src/akvorado-stats/akvo-top-asn/akvo-top-asn --config=/usr/src/akvorado-stats/akvorado-top-asn/akvo-top-asn.conf --upload
RemainAfterExit=yes
```

**Systemd Timer**

`/etc/systemd/system/akvorado-top-asn-export.timer`
```
[Unit]
Description=Akvorado Top ASN Collection Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

### CronJob

```
0 0 * * * /usr/src/akvorado-stats/akvo-top-asn/akvo-top-asn --config=/usr/src/akvorado-stats/akvorado-top-asn/akvo-top-asn.conf --upload
```

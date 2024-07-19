[clickhouse]
## Connect to a remote clickhouse via https in a akvorado setup:
# host = akvorado.ibh.net/clickhouse
# secure = 1
# port = 443

## Use localhost:8123 via http (default):
# host = localhost

[query]
## How to query clickhouse

## how many rows per query
# query_limit = 100

## how many rows will be extracted in total
# value_limit = 1000

## the maximum number of queries against clickhouse is value_limit / query_limit

[upload]
## upload server & auth (i.e. Nextcloud public share)
# url = https://cloud.dd-ix.net/public.php/webdav
# username = nc-share-id
# password = nc-share-secret

## filename pattern (strftime), we be appended to the
## upload url and used for saving to local files
# filename = export-%Y-W%W.yml

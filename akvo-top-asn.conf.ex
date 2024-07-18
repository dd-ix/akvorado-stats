[clickhouse]
## Connect to a remote clickhouse via https in a akvorado setup:
# host = akvorado.ibh.net/clickhouse
# secure = 1
# port = 443

## Use localhost:8123 via http (default):
# host = localhost

[upload]
## upload server & auth (i.e. Nextcloud public share)
# url = https://cloud.dd-ix.net/public.php/webdav/
# username = nc-share-id
# password = nc-share-secret

## filename pattern (strftime), we be appended to the
## upload url and used for saving to local files
# filename = export-%Y-W%W.yml

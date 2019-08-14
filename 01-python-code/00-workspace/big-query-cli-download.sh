bq show stack-exchange-project:stackoverflow_stackexchange.trim_betw_date

bq query "SELECT count(*) FROM stackoverflow_stackexchange.trim_betw_date"

bq extract stackoverflow_stackexchange.trim_betw_date 'gs://bucket-brad-project/initial-data/stackoverflow.stackexchange.com/file-*.json'

## copy first file to local machine
gsutil cp -r gs://bucket-brad-project/initial-data/stackoverflow.stackexchange.com/ .

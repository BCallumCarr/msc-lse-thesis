bq show stack-exchange-project:stackoverflow_stackexchange.date_included

bq query "SELECT count(*) FROM stackoverflow_stackexchange.date_included"

bq extract stackoverflow_stackexchange.date_included 'gs://bucket-brad-project/final-datasets/stackoverflow.stackexchange.com_date/file-*.json'

## copy first file to local machine
gsutil cp gs://bucket-brad-project/final-datasets/stackoverflow.stackexchange.com/file-000000000000.json .

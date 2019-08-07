bq show stack-exchange-project:stackoverflow_stackexchange.trimmed_date

bq query "SELECT count(*) FROM stackoverflow_stackexchange.trimmed_date"

bq extract stackoverflow_stackexchange.trimmed_date 'gs://bucket-brad-project/final-datasets/stackoverflow.stackexchange.com_trimdate/file-*.json'

## copy first file to local machine
gsutil cp gs://bucket-brad-project/final-datasets/stackoverflow.stackexchange.com_trimdate/file-000000000000.json .

bq show stack-exchange-project:stackoverflow_stackexchange.stackoverflow_final

bq query "SELECT count(*) FROM stackoverflow_stackexchange.stackoverflow_final"

bq extract stackoverflow_stackexchange.stackoverflow_final 'gs://bucket-brad-project/final-datasets/file-*.json'

## copy first file to local machine
gsutil cp gs:/bucket-brad-project/final-datasets/stackoverflow.stackexchange.com/file-000000000000.json .

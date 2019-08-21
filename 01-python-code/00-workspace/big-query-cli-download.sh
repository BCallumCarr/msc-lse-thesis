## checking tables exist
bq show stack-exchange-project:stackoverflow_stackexchange.betw_date_Mar_09
bq query "SELECT count(*) FROM stackoverflow_stackexchange.betw_date_Mar_09"

## looping through to download data to GCP
# declare table identifiers
declare -a arr=(
   'Mar_09'
   'Apr_09'
   'May_09'
   'Jun_09'
   'Jul_09'
   'Aug_09'
   'Sep_09'
   'Oct_09'
   'Nov_09'
   'Dec_09'
)

# loop through in bash
for i in "${arr[@]}"
do
  a='gs://bucket-brad-project/initial-data/stackoverflow_'
  b='.stackexchange.com/file-*.json'
  c="$a$i$b"
  bq extract stackoverflow_stackexchange.betw_date_$i $c
done

## copy files to local machine, in FOLDER
for i in "${arr[@]}"
do
  gsutil cp -r gs://bucket-brad-project/initial-data/stackoverflow_$i.stackexchange.com/ .
done

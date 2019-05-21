## install unzipper
sudo apt-get install --yes p7zip-full

## create folder and datasets array
mkdir datasets && cd datasets

declare -a arr=(
"expatriates.stackexchange.com"
"elementaryos.stackexchange.com"
"lifehacks.stackexchange.com"
"literature.stackexchange.com"
"opendata.stackexchange.com"
"tor.stackexchange.com"
"patents.stackexchange.com"
"ham.stackexchange.com"
"hsm.stackexchange.com"
"latin.stackexchange.com"
"martialarts.stackexchange.com"
"opensource.stackexchange.com"
"woodworking.stackexchange.com"
)

## loop downloading, unzipping and extracting all XML data
for i in "${arr[@]}"
do
   mkdir "$i" && cd "$i"
   wget https://archive.org/download/stackexchange/"$i".7z
   p7zip -d "$i".7z
   mv PostLinks.xml Postlinks.xml
   mv PostHistory.xml Posthistory.xml
   cd ..
done

cd

## DON'T FORGET TO copy datasets folder over to bucket!!
#gsutil cp -r datasets gs://bucket-brad/datasets

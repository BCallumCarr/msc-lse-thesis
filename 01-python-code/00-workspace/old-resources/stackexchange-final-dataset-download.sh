## install unzipper
sudo apt-get install --yes p7zip-full

## create folder and datasets array (SO must be done separately)
mkdir datasets && cd datasets

declare -a arr=(
"askubuntu.com"
"codereview.stackexchange.com"
"math.stackexchange.com"
"physics.stackexchange.com"
"ru.stackoverflow.com"
#"serverfault.com"
"stackoverflow.com-Posts"
"superuser.com"
#"tex.stackexchange.com"
"unix.stackexchange.com"

"es.stackoverflow.com"
"codegolf.stackexchange.com"
)

## loop downloading, unzipping and extracting all XML data
for i in "${arr[@]}"
do
   mkdir "$i" && cd "$i"
   wget https://archive.org/download/stackexchange/"$i".7z
   p7zip -d "$i".7z
   find . -type f ! -name 'Posts.xml' -delete # dlt everything except Posts.xml
   #mv PostLinks.xml Postlinks.xml # messes up import later
   cd ..
   echo "On to next dataset!"
done

## rename folders for ease of import later
mv stackoverflow.com-Posts stackoverflow.stackexchange.com
mv superuser.com superuser.stackexchange.com
mv askubuntu.com askubuntu.stackexchange.com
#mv serverfault.com serverfault.stackexchange.com
mv ru.stackoverflow.com rus_stackoverflow.stackexchange.com
mv es.stackoverflow.com es_stackoverflow.stackexchange.com

cd

## DON'T FORGET TO copy datasets folder over to bucket!!
gsutil cp -r datasets gs://bucket-brad-project/

## install unzipper using homebrew
brew update
brew install p7zip

## move to folder and create datasets array (SO must be done separately)
cd initial-data

declare -a arr=(
   'buddhism.stackexchange.com'
   'economics.stackexchange.com'
   'fitness.stackexchange.com'
   'health.stackexchange.com'
   'interpersonal.stackexchange.com'
#"english.stackoverflow.com"
#"ru.stackoverflow.com"
#"superuser.com"
#"stackoverflow.com-Posts"
#"math.stackexchange.com"
)

## loop downloading, unzipping and extracting all XML data
for i in "${arr[@]}"
do
   mkdir "$i" && cd "$i"
   wget --no-check-certificate https://archive.org/download/stackexchange/"$i".7z
   7z x "$i".7z
   find . -type f ! -name 'Posts.xml' -delete # dlt everything except Posts.xml
   #mv PostLinks.xml Postlinks.xml # messes up import later
   cd ..
   echo "On to next dataset!"
done

## rename folders for ease of import later
#mv stackoverflow.com-Posts stackoverflow.stackexchange.com
#mv superuser.com superuser.stackexchange.com
#mv askubuntu.com askubuntu.stackexchange.com
#mv serverfault.com serverfault.stackexchange.com
#mv ru.stackoverflow.com rus_stackoverflow.stackexchange.com
#mv es.stackoverflow.com es_stackoverflow.stackexchange.com
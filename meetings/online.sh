#! /bin/bash -e

JSON_DIR="/var/popong/data/meetings"

echo
date
echo "update assembly minutes"

# crawl assembly minutes
cd "/var/popong/crawlers/meetings/"
./crawl.py

# commit to [data-meetings.git](https://bitbucket.org/teampopong/data-meetings)
cd $JSON_DIR
git add .
git commit -m "Auto update: `date`"
git push

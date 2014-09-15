#! /bin/bash -e

JSON_DIR="." # change me

echo
date
echo "update assembly minutes"

# crawl assembly minutes
cd "~/crawlers/meetings/" # change me to meetings crawler directory
./crawl.py

# commit to [data-meetings.git](https://github.com/teampopong/data-meetings)
cd $JSON_DIR
git add .
git commit -m "Auto update: `date`"
git push

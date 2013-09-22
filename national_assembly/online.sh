#!/bin/bash -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DATA_DIR="/var/popong/data/assembly"


date
echo "update assembly members"

# crawl assembly members
cd $SCRIPT_DIR
./crawl.py
cp assembly.csv $DATA_DIR

# commit to [data-assembly.git](https://github.com/teampopong/data-assembly)
cd $DATA_DIR
git add .
git commit -m "`date`"
git push

# TODO: insert bills to DB (`$ python /var/apps/polidic/server.py insert_people`)
# TODO: post diff to twitter

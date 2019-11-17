#!/bin/bash

stats_dir=$1
merged_dir=$2

files=`find $stats_dir -name '*.json' -o -name '*.1st' -o -name '*.log'`

echo "Copying data ..."

cp $files $merged_dir

echo "Getting stats ..."

./get_stats.py $merged_dir/*.1st

mv *stats.csv $merged_dir

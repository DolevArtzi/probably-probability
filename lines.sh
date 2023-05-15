c=0
for f in *.py; do
    l=$(< $f wc -l | xargs);
    c=$(($c+$l));

done
echo "Total Lines = ${c}"
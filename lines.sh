c=0
for file in $(find ./ -name '*.py' -type f -not -path './/venv/*'); do
    l=$(< $file wc -l | xargs);
    c=$(($c+$l));
done
echo "Total Lines = ${c}"

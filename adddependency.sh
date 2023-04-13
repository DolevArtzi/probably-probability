add() {
  v=$1
  echo "\nfrom ${v%???} import ${v%???}" >> ./allRVs.py; }

add $1

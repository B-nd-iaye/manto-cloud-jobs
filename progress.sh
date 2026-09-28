#!/bin/sh
# Progress of the cloud jobs. Locally: git pull && sh progress.sh
cd "$(dirname "$0")"
bar() { printf '%*s' $(($1*40/$2)) '' | tr ' ' '#'; }
vn=$(ls vr_shards/*.txt | wc -l); vd=0
for s in vr_shards/*.txt; do b=$(basename $s .txt); n=$(grep -c '^\[' $s); [ -f out/vr/$b.jsonl ] && [ $(wc -l < out/vr/$b.jsonl) -ge $n ] && vd=$((vd+1)); done
rn=$(ls rx_batches/*.txt | wc -l); rd=$(ls out/rx/*.jsonl 2>/dev/null | wc -l)
printf "verify+reclass  %3d/%d  [%-40s]\n" $vd $vn "$(bar $vd $vn)"
printf "re-extraction   %3d/%d  [%-40s]\n" $rd $rn "$(bar $rd $rn)"

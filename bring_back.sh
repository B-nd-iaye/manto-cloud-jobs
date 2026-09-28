#!/bin/sh
# Run LOCALLY after the cloud work: pull results and copy them into the project.
set -e; cd "$(dirname "$0")"; git pull
P="/Users/bokarndiaye/Documents/Claude/Projects/Myth Classifier (the right one)"
mkdir -p "$P/manto_pass5/verification/vr_verdicts" "$P/taxonomy_audit/reextract/drafts_h"
cp out/vr/*.jsonl "$P/manto_pass5/verification/vr_verdicts/"
cp out/rx/*.jsonl "$P/taxonomy_audit/reextract/drafts_h/"
sh progress.sh

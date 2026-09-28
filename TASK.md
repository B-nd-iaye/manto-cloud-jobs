# MANTO cloud jobs — instructions for the cloud session

You are running two batch LLM jobs over files already in this repository. You do not need any other source files.
Do the phases in order. **After every wave, commit and push `out/`** (`git add out && git commit -m "wave N" && git push`), so nothing is lost if the VM is reclaimed. Never re-run an input whose output is already complete. Report tokens honestly.

## Jobs
| job | inputs | prompt | outputs |
|---|---|---|---|
| VR: semantic verification + v2 predicate | `vr_shards/*.txt` (73 shards, ≈150 records each, records start with `[ID]`) | `prompts/verify_reclass_v1.md` | `out/vr/<shard>.jsonl`, one JSON line per record |
| RX: targeted re-extraction | `rx_batches/*.txt` (170 batches of passages) | `prompts/extract_fam_v1h.md` | `out/rx/<batch>.jsonl`, 0–n JSON lines per passage |

`out/vr/B_S001.jsonl` and `out/rx/P5B_X001.jsonl` are already done (the local test). `ref/` holds reference verdicts for B_S001.

## Phase 0 — check the headless path (≈10 min)
1. `claude --version` and `claude auth status`.
2. If signed in, run ONE shard at low effort into a scratch folder:
   `python3 headless.py prompts/verify_reclass_v1.md out_test/vr vr_shards/B_S002.txt --ids --model sonnet --effort low`
   Record the printed tokens and seconds. Then re-run B_S001 at low effort into `out_test/vr_low/` and compare `v` with `ref/B_S001.default_effort.jsonl` (agreement %). Low effort is acceptable if agreement ≥ 85 % and every `U` in the reference is also `U` or `P`.
3. Write the numbers to `out/PHASE0.md`, commit, push, and **stop and report** in the session: path (headless or subagents), effort chosen, tokens per shard. Wait for the user's go before Phase 1.

If `claude -p` is not available or not signed in, say so in `out/PHASE0.md` and stop; the fallback is subagents (below), which costs ≈5× more, so it needs the user's explicit go.

## Phase 1 — VR (after the user's go)
Headless path, 6 in parallel, in the background, in waves of 12 shards:
`python3 headless.py prompts/verify_reclass_v1.md out/vr vr_shards/A_S001.txt … --ids --model sonnet --effort <chosen> --parallel 6`
The runner is resumable: it re-asks only for missing ids. After each wave: `sh progress.sh`, commit + push `out/`.

## Phase 2 — RX
Same pattern: `python3 headless.py prompts/extract_fam_v1h.md out/rx rx_batches/<batch>.txt … --model sonnet --parallel 6` (no `--ids`; a batch whose output file exists is skipped). Waves of 12, commit + push after each.

## Subagent fallback (only with the user's explicit go)
One subagent per input. Each reads the prompt and its input in ONE parallel Read and writes its whole output in ONE Write to the output path; no scripts, no other files. Waves of 6. Check the files on disk before relaunching anything (an agent that errored may already have written its output).

## Rules
- Do not edit prompts, inputs or `headless.py` without the user's go.
- If you hit a rate limit (429) or a usage warning, stop, commit, push, and report.
- At the end: `sh progress.sh`, a short `out/SUMMARY.md` (counts, tokens from `out/*/usage.jsonl`, failures), commit, push.

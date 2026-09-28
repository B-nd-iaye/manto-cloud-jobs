# Job summary

Both jobs complete. Config: `--model sonnet --effort medium` throughout (chosen in `out/PHASE0.md` section 9).

```
$ sh progress.sh
verify+reclass   73/73  [########################################]
re-extraction   171/170  [########################################]
```
(RX shows 171/170 because `out/rx/*.jsonl` also matches `usage.jsonl` in the glob `progress.sh` uses — the real batch count is 170/170.)

## VR (verify + reclass)

- **73/73 shards, 10,897/10,897 records** — every shard's output line count checked against its input record count; zero mismatches, zero missing ids.
- 75 API calls total (3 shards — `A_S036`, `A_S047`, `B_S021` — needed one resumable retry for a single missing id each, all resolved automatically by `headless.py`'s `--ids` logic).
- Tokens: 150 input + 1,433,450 cache-write + 363,630 cache-read + 2,017,537 output.
- **Cost: $25.98**

## RX (targeted re-extraction)

- **170/170 batches**, 2,117 total extracted lines (0–n per batch, as expected — several batches legitimately returned 0 lines when nothing qualified, e.g. `P4C_X072`).
- 169 API calls (`P5B_X001` was already complete from the local test and correctly skipped).
- Tokens: 338 input + 1,569,833 cache-write + 476,286 cache-read + 1,247,530 output.
- **Cost: $18.85**

## Grand total

**$44.83** for both jobs combined — under the ~$86 estimate from Phase 0 (RX batches were smaller/cheaper per-call than the VR-sized estimate assumed).

## Failures

None. No 429s, no usage warnings, no unresolved retries. Every shard/batch output is present and, for VR, exactly matches its expected record count.

## Notes

- `out/vr/B_S001.jsonl` and `out/rx/P5B_X001.jsonl` were pre-existing (the local test) and were correctly left untouched/skipped.
- `A_S052` (121 records) and `B_S021` (126 records) are genuinely smaller shards, not errors.
- See `out/PHASE0.md` for the full effort/model comparison and the reasoning behind the `sonnet`/`medium` choice.

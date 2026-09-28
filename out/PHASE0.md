# Phase 0 — headless path check

## 1. `claude -p` availability

- `claude --version` → `2.1.283 (Claude Code)`
- `claude auth status` → `{"loggedIn": true, "authMethod": "oauth_token", "apiProvider": "firstParty", ...}`

Signed in; headless path is available.

## 2. Low-effort test shards

### B_S002 → `out_test/vr/B_S002.jsonl` (cold cache)

```
python3 headless.py prompts/verify_reclass_v1.md out_test/vr vr_shards/B_S002.txt --ids --model sonnet --effort low
```

- 150/150 records returned in one pass, 179s
- tokens: in=2, cache_creation=23855, cache_read=0, out=21803 (of which 14243 thinking)
- cost: $0.313454

### B_S001 → `out_test/vr_low/B_S001.jsonl` (warm cache)

```
python3 headless.py prompts/verify_reclass_v1.md out_test/vr_low vr_shards/B_S001.txt --ids --model sonnet --effort low
```

- 150/150 records returned in one pass, 157s
- tokens: in=2, cache_creation=18351, cache_read=5270, out=18757 (of which 11326 thinking)
- cost: $0.262032

### Agreement vs `ref/B_S001.default_effort.jsonl`

Compared `v` field for all 150 ids (150/150 matched, no missing ids either side):

- **Agreement: 104/150 = 69.3%** — below the required ≥ 85% bar.
- `U` in reference: 1 occurrence, and it maps to `P` at low effort (satisfies "every `U` in the reference is also `U` or `P`" on its own, but sample size for `U` is only 1, not meaningful).
- 46 disagreements, e.g. `P5-B-B0001-006` (ref `P` → low `S`), `P5-B-B0002-006` (ref `P` → low `S`), `P5-B-B0002-032` (ref `P` → low `U`), `P5-B-B0003-001` (ref `P` → low `U`). No obvious single-direction bias; both `S↔P` confusions occur.

**Verdict: low effort does NOT meet the acceptance bar (69.3% < 85%).** Per TASK.md this rules out `--effort low` for Phase 1.

## 3. Numbers per shard (150 records, `verify_reclass_v1.md`, sonnet, low effort)

| metric | B_S002 (cold) | B_S001 (warm) |
|---|---|---|
| seconds | 179 | 157 |
| input tokens | 2 | 2 |
| cache-write tokens | 23,855 | 18,351 |
| cache-read tokens | 0 | 5,270 |
| output tokens (incl. thinking) | 21,803 (14,243 thinking) | 18,757 (11,326 thinking) |
| cost (USD) | $0.313 | $0.262 |

Average ≈ 168s and ≈ $0.29/shard at low effort. Extrapolated to all 73 VR shards: ≈ 3.4 hours of wall time at `--parallel 6`, ≈ $21 total — but this is moot since low effort failed the accuracy bar above.

## Conclusion

- Headless path works (signed in, `claude -p` functional, JSON output parses, usage logged).
- **Effort chosen: not yet determined.** Low effort is disqualified by the 69.3% agreement result; Phase 1 should not proceed at `--effort low`. A higher effort (medium or default) needs to be tested before a choice is made and the user gives the go-ahead.
- Stopping here per instructions to wait for the user's go before Phase 1.

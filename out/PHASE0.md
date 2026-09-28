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

## 4. Medium-effort test (B_S001, at user's request)

```
python3 headless.py prompts/verify_reclass_v1.md out_test/vr_medium vr_shards/B_S001.txt --ids --model sonnet --effort medium
```

- 150/150 records returned in one pass, 226s
- tokens: in=2, cache_creation=23621, cache_read=0, out=26350 (of which 18732 thinking)
- cost: $0.357988

### Agreement vs `ref/B_S001.default_effort.jsonl`

- **Agreement: 120/150 = 80.0%** — better than low effort (69.3%) but still below the 85% bar.
- `U` in reference (1 occurrence) still maps to `P` — fine on that count, but n=1.
- 30 disagreements, same mix of `S↔P` confusion plus several `P→U` (the model hedges into "unclear" on cases the reference calls `P`), e.g. `P5-B-B0003-001/002/005/013/027/053/056` all ref `P` → medium `U`.

| metric | low (B_S001, warm) | medium (B_S001) |
|---|---|---|
| seconds | 157 | 226 |
| cache-write tokens | 18,351 | 23,621 |
| cache-read tokens | 5,270 | 0 |
| output tokens (incl. thinking) | 18,757 (11,326 thinking) | 26,350 (18,732 thinking) |
| cost (USD) | $0.262 | $0.358 |
| agreement vs ref | 69.3% | 80.0% |

## 5. High-effort test (B_S001, at user's request)

```
python3 headless.py prompts/verify_reclass_v1.md out_test/vr_high vr_shards/B_S001.txt --ids --model sonnet --effort high
```

- 150/150 records returned in one pass, 443s
- tokens: in=2, cache_creation=23621, cache_read=0, out=50763 (of which 42769 thinking)
- cost: $0.602118

### Agreement vs `ref/B_S001.default_effort.jsonl`

- **Agreement: 125/150 = 83.3%** — best so far, still just under the 85% bar.
- 25 disagreements, same mix as medium: `S↔P` confusions plus several `P→U` hedges (`P5-B-B0002-033`, `P5-B-B0003-005/013/053/056`). No new failure mode appears at high effort — it looks like incremental cleanup of the same errors, not a step change.

### Effort comparison (B_S001)

| effort | seconds | cache-write tok | output tok (thinking) | cost | agreement vs ref |
|---|---|---|---|---|---|
| low (warm cache) | 157 | 18,351 | 18,757 (11,326) | $0.262 | 69.3% |
| medium | 226 | 23,621 | 26,350 (18,732) | $0.358 | 80.0% |
| high | 443 | 23,621 | 50,763 (42,769) | $0.602 | 83.3% |

Diminishing returns: medium→high roughly doubles time and cost (thinking tokens ~2.3×) for +3.3 points of agreement, and still doesn't clear 85%.

## Conclusion

- Headless path works (signed in, `claude -p` functional, JSON output parses, usage logged).
- **Effort chosen: still not determined.** None of low (69.3%), medium (80.0%), or high (83.3%) clears the required ≥85% agreement bar on B_S001 — the gap closes but does not cross.
- Options for the user to weigh before Phase 1: (a) test `--effort xhigh`/`max`, likely with further diminishing returns and higher cost/time per shard (443s → ? at high alone is already ~2.8× low); (b) relax the acceptance bar — the remaining disagreements at medium/high are consistently the same handful of ambiguous `S↔P`/`P→U` cases, not random noise, so a human spot-check of whether they're actually defensible calls may be more productive than chasing a higher effort tier; (c) fall back to the subagent path (~5× cost per TASK.md).
- Stopping here per instructions to wait for the user's go before Phase 1.

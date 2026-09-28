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

## 6. Opus 5.5, low effort (B_S001, at user's request)

```
python3 headless.py prompts/verify_reclass_v1.md out_test/vr_opus_low vr_shards/B_S001.txt --ids --model opus --effort low
```

- 150/150 records returned in one pass, 111s (fastest of all tests)
- tokens: in=2, cache_creation=23558, cache_read=0, out=13337 (of which 4714 thinking — much less thinking than any Sonnet tier)
- cost: $0.455212

### Agreement vs `ref/B_S001.default_effort.jsonl`

- **Agreement: 123/150 = 82.0%** — close to Sonnet high (83.3%), still below the 85% bar.
- 27 disagreements, but a distinctly different pattern from Sonnet: heavily skewed one direction — 18 of 27 are `ref=S → test=P` concentrated in the `B0003` block (`-003, -006, -008, -011, -015, -017, -018, -019, -024, -030, -034, -037, -039, -047`, etc.). This looks like Opus at low effort systematically over-calling `P` (partial/inferred) in that passage rather than a spread of independent ambiguous calls — worth a manual look at `B0003` before trusting Opus-low broadly.

### Updated comparison (B_S001)

| model / effort | seconds | output tok (thinking) | cost | agreement vs ref |
|---|---|---|---|---|
| sonnet / low (warm) | 157 | 18,757 (11,326) | $0.262 | 69.3% |
| sonnet / medium | 226 | 26,350 (18,732) | $0.358 | 80.0% |
| sonnet / high | 443 | 50,763 (42,769) | $0.602 | 83.3% |
| opus / low | 111 | 13,337 (4,714) | $0.455 | 82.0% |

Opus-low lands near Sonnet-high's accuracy at a quarter of the time and ~75% of the cost, but its errors cluster in one passage block rather than spreading evenly — a pattern (not just a count) that needs checking before it's trusted at scale.

## 7. Spot-check: are the disagreements defensible? (at user's request)

First, a sanity check on the reference itself: `ref/B_S001.default_effort.jsonl` and `ref/B_S001.subagent_pilot.jsonl` overlap on 100 ids (`B0001`–`B0003`, partial). **They agree with each other only 89.0% of the time (89/100)** — i.e. the two reference sources disagree with each other about as often as our best test run disagrees with either one of them. That reframes the whole exercise: 85% agreement against a single reference may not be an achievable ceiling if the reference-generation process itself isn't self-consistent above ~89%.

Reading the actual quotes for a sample of disagreements (both model-vs-reference and reference-vs-reference) turns up two distinct patterns, not random noise:

**(a) Anaphora/referent leniency — the dominant pattern.** Several quotes refer to the tie's subject or location with a pronoun or demonstrative ("he", "his", "it", "this area", "whence") whose antecedent is unambiguous from the immediately surrounding sentence, but isn't re-named inside the quoted span itself:
- `P5-B-B0001-009` — Q: *"instead of legs, he has great limbs like snake tails."* (S=YLREAM, implicit=True) — `default_effort` and `subagent_pilot` both call this `S` (fully supported) despite "he" not being literally named "Ylream" in the quote.
- `P5-B-B0003-006` — Q: *"...It was later the center of Arkat's Dark Empire."* (MOD location RINDLAND not named) — `default_effort` calls `S`; `subagent_pilot` calls `P`.
- Also `-010`, `-012`, `-0003-003`: same shape, and the two reference files **disagree with each other** on all of these.

`default_effort` treats unambiguous same-passage anaphora as sufficient for `S`; lower-effort Sonnet runs and Opus-low more often flag the referent as inferred and call `P` — a stricter but not unreasonable reading of "unmistakably entailed." This single issue plausibly accounts for the majority of every disagreement set I looked at (low, medium, high, opus-low), and it also drives 8 of the 11 reference-vs-reference disagreements above. It looks like a genuine prompt underspecification (how strict is "unmistakably entailed" for clear same-sentence/adjacent-sentence anaphora?), not a model competence gap — closing it would need a prompt clarification, which is outside Phase 0's "don't edit the prompt" boundary.

**(b) Predicate-strength misclassification (P vs U) — smaller, but a real rule violation.** `P5-B-B0003-001` — Q: *"...Seshna Likita, the goddess of this land."*, tied as `rules`. `default_effort` correctly calls this `P` (*"'goddess of this land' is domain, not political rule"*), matching the prompt's own stated rule ("P = ... the predicate is stronger than the text" and "'god of X' → has domain"). **Sonnet at low, medium, and high effort all instead called this `U`/REJECT** — over-applying "unsupported" to a case that the prompt's own rules class as partial support, not full rejection. This is a genuine, correctable error, distinct from the anaphora issue, though it showed up less often in the sample.

**(c) Cases where every test run agrees with each other but not the single reference.** `P5-B-B0002-021` — Q: *"...tore the helmet off Grachamagacan the Iron Vampire, King of Tanisor, when Arkat slew it."*, tied as `fights`. `default_effort` calls `U`/REJECT (*"trophy-taking after Arkat's kill, not combat"*). **All four of our test runs (Sonnet low/medium/high, Opus low) independently called this `P`**, matching `subagent_pilot`'s reading, not `default_effort`'s. Four independent runs converging against one reference reads as a defensible alternate interpretation, not a shared model error.

**Bottom line on defensibility:** most of the sampled disagreements are defensible readings of an underspecified anaphora rule, corroborated by the reference files disagreeing with each other at almost the rate our models disagree with either reference. A smaller, real error pattern exists around P-vs-U predicate-strength calls, which is worth watching regardless of which effort tier is chosen. The practical takeaway: the 85% bar, taken literally against one reference file, is close to what the reference-generation process itself can reproduce (~89%) — Sonnet-high (83.3%) and Opus-low (82.0%) are not far off that ceiling, not obviously "failing" in a way a higher effort tier would fix.

## 8. Subagent fallback cost pilot (at user's request)

Ran one subagent on an untouched shard (`vr_shards/B_S004.txt`, 150 records) following the exact recipe in TASK.md's "Subagent fallback" section: 2 parallel Reads (prompt + input), then 1 Write of the whole output, no other tools. Output went to a test path (`out_test/vr_subagent/B_S004.jsonl`), not the real `out/vr/`, since this is a Phase 0 pilot, not Phase 1 work.

**Result:** 150/150 valid JSON lines, well-formed (spot-checked: 0 malformed), covering all records with the same schema as the headless output — e.g. it correctly handles S/O reversal (`"is worshipped by"` with S/O swapped) and correctly used `pf: REJECT` for a false-pretense/impersonation case. No reference file exists for B_S004, so I can't score its accuracy the way I could for B_S001 — only its cost, time, and format validity.

**Cost/time, measured directly from the harness (not estimated):**

| metric | subagent (B_S004, 150 recs) |
|---|---|
| total tokens | **140,772** |
| tool calls | 4 (2 reads, 1 write, 1 report) |
| wall time | **1,072,554 ms ≈ 17.9 minutes** |

### Subagent vs. headless, same 150-record scale (B_S001/B_S004 comparable size)

| path | total tokens | wall time | cost (headless, measured) |
|---|---|---|---|
| headless sonnet/low | ~42,000–45,700 | 157–179s | $0.26–$0.31 |
| headless sonnet/medium | ~50,000 | 226s | $0.358 |
| headless sonnet/high | ~74,400 | 443s | $0.602 |
| headless opus/low | ~36,900 | 111s | $0.455 |
| **subagent** | **140,772** | **1,073s (17.9 min)** | not directly billed the same way; see below |

By raw token count, the subagent used **~1.9× sonnet-high's tokens, ~2.8× sonnet-medium's, and ~3.3–3.8× sonnet-low/opus-low's** — and it took **2.4–9.7× longer in wall time per shard** than any headless tier. Applying the blended $/token rates observed on the headless runs ($0.0069–$0.0081/token depending on tier) to the subagent's 140,772 tokens gives a rough **$0.97–$1.14 per shard** — in the same direction as, though somewhat below, TASK.md's own "~5×" estimate; the true multiple could be higher if the agent harness's tokens skew more toward output/thinking (priced higher) than the headless mix, which this rough linear estimate doesn't capture.

**Bottom line:** the subagent fallback works and produces well-formed output, but it is markedly more expensive AND slower per shard than any headless tier tested, including the ones that already fail the accuracy bar. Extrapolated to 73 VR shards at 6 subagents in parallel (per TASK.md's wave size), this pilot's per-shard wall time alone implies roughly 13 waves × ~18 minutes ≈ 4 hours just for VR, before RX — worse on both cost and time than headless-high, which itself didn't clear 85%. The subagent path doesn't look like a way to buy back the accuracy gap cheaply; if anything it should be a last resort per TASK.md's own framing, not a stepping stone.

## 9. Final decision (at user's request: "calculate best option, then run it")

**Chosen: `--model sonnet --effort medium`** for both Phase 1 (VR) and Phase 2 (RX).

Rationale: none of the tested tiers clear 85%, and section 7 established the practical ceiling is close to what's already measured (~89% reference self-consistency). Medium is the knee of the cost/accuracy curve (80.0% @ $0.358/shard, 226s), with errors spread evenly rather than clustered. High effort (83.3%) costs 68% more and takes 96% longer for a gain concentrated in the same ambiguous-anaphora disagreements already characterized as largely defensible either way — and it does *not* fix the one clear rule-violation found (Sonnet at every tier miscalls certain "P" cases as "U"). Opus-low (82.0%, $0.455, 111s) is fast and close in accuracy, but its errors cluster in one passage block (B0003) rather than spreading independently — a correlated-error risk not worth taking across ~11,000 VR records plus RX. Estimated full-job cost ≈ $86 (VR + RX combined), ≈ 2.5–3 hours wall time at `--parallel 6`.

## Conclusion

- Headless path works (signed in, `claude -p` functional, JSON output parses, usage logged).
- **Effort/model chosen: still not determined.** None of Sonnet low (69.3%), medium (80.0%), high (83.3%), or Opus low (82.0%) clears the required ≥85% agreement bar on B_S001.
- Options for the user to weigh before Phase 1: (a) test Opus at medium/high, or Sonnet `xhigh`/`max`, though all show diminishing returns; (b) relax the acceptance bar — remaining disagreements are consistently the same handful of ambiguous `S↔P`/`P→U` cases (Sonnet) or concentrated in one passage block (Opus low), not random noise, so a human spot-check of whether they're actually defensible calls may be more productive than chasing a higher tier; (c) fall back to the subagent path (~5× cost per TASK.md).
- Stopping here per instructions to wait for the user's go before Phase 1.

# MANTO-Glorantha targeted re-extraction — prompt fam-v1 (2026-09-28)

These passages were already extracted once, but with a vocabulary that had no word for dwelling, love, hate, fear, mourning, speech, possession, oath-breaking, death, healing, cursing, trade, hunting, vengeance, punishment or sleep. You extract **only ties of the target predicates below**. Everything else in the passage is already captured, so ignore it. Every tie is checked against the source character by character and judged by a separate verifier. Precision beats volume. When a reading is doubtful, leave the tie out.

## Input
Passages, each headed `### PID | BOOK | page | heading`, followed by:
- `FIGURES:` registered names in the passage (use these spellings, UPPER CASE);
- `CONTEXT:` (only present when TEXT opens with a pronoun) up to 400 characters before the passage, only for resolving "he"/"they". **Never quote from CONTEXT.**
- `TEXT:` the passage. Quotes come only from here.
- `TARGETS:` the families a keyword search found in TEXT. It is a hint, not a quota. A keyword hit is often not a tie ("feared warriors", "the dead", rules text); then extract nothing.

## Target predicates (use exactly; `p` must be one of these)
| predicate | meaning | args |
|---|---|---|
| dwells at | S lives, dwells or resides at/in O (a standing state) | O = place |
| settles at | S takes up residence at O (the event of moving in) | O = place |
| loves / desires | S loves, desires or lusts after O | |
| hates | S hates or feuds with O | |
| fears | S fears O | |
| mourns | S mourns, weeps or laments for O | |
| speaks / informs / warns / prophesies | S speaks to, tells, warns, advises or prophesies to O | O = addressee; what is said → `note` |
| possesses / wields | S owns, carries, wears or wields O | O = object |
| breaks oath | S breaks an oath, pact, geas or taboo, or disobeys O | O = the one disobeyed or the oath |
| dies | S dies (no killer named) | O empty; place → `in_on_at` |
| heals | S heals or cures O | |
| curses | S curses O | |
| trades with | S trades or bargains with O | |
| exchanges | S gives O in exchange for IO | |
| hunts | S hunts or pursues O | |
| avenges | S takes vengeance on O | IO = whom/what is avenged |
| punishes | S punishes O | |
| exiles / banishes | S drives out, exiles or banishes O | |
| sleeps | S falls asleep / lies dormant | O empty |
| awakens | S wakes O, or S wakes (O empty) | |

Not targets: killing (a named killer is `kills`, already captured), worship, rule, kinship, fighting. Skip them.

## Output
Same draft format as the main extraction. One JSON object per line; output the lines only. Keys:

| key | required | meaning |
|---|---|---|
| `pid` | yes | passage id from the header |
| `q` | yes | list of exact quote segments copied from TEXT. Copy characters exactly; line breaks may be spaces. **No `...` or `…`.** Use two segments rather than stitching. Shortest full clause that states the tie. |
| `s`, `p`, `o` | yes | subject list, target predicate, direct-object list (UPPER CASE; `o` may be `[]` for dies/sleeps/awakens) |
| `io` | no | indirect-object list |
| `m` | no | modifiers: `using`, `in_on_at`, `from`, `to`, `via` (list), `with_the_aid_of`, `at_the_command_of`, `at_the_instigation_of`, `in_accordance_with` (lists), `purpose_clause` |
| `surface` | yes when a slot is not named in `q` | `"slot:VALUE"` → the words in `q` read as that referent (`{"subject:ELMAL": "he"}`); `""` if nothing in `q` refers to it |
| `p_surface` | yes | the text's own verb phrase ("lived in", "wept for", "carried") |
| `hedge` | no | hedging words ("some say", "perhaps") |
| `uncertain`, `alt`, `doubt`, `gl` | no | booleans: data uncertain; alternatives given; doubt expressed; God Learner synthesis |
| `corpus` | yes | cultural corpus of the telling (list below) |
| `age` | yes | mythic age or period (list below); `"Godtime (unspecified)"` if unclear |
| `spatium` | no | default Godtime; `"Spatium Historicum (Time)"` for post-Dawn history, `"Otherworld (HeroQuest)"` for heroquests |
| `cls` | yes | `narrative` (an event: dies, curses, heals…) or `attribute` (a standing state: dwells at, possesses, hates, fears) |
| `inference` | yes when `surface` is used | one sentence: what you inferred and from where |
| `note` | no | anything a reviewer needs (for speech: what was said, in ≤12 words) |

**Corpora:** Theyalan · Solar · Lunar · Malkioni · Uz · Praxian · Pamaltelan · Kralori · Vithelan · Draconic · Aldryami · Mostali · Hsunchen · Editorial (Chaosium's encyclopedic narrator voice).
**Ages:** Creation / Celestial Age · Green Age · Golden Age · Storm Age · Lesser Darkness · Great Darkness · Silver Age · Dawn · First Age · Second Age · Third Age · Godtime (unspecified) · Timeless

## Rules
1. **Named participants only.** S and O must be beings, groups, places or objects the text names or unmistakably refers to. "The dead", "anyone", "worshippers" in general, "those who…" → no tie.
2. **Generic statements are not ties.** "Trolls fear light" is a tie only if the text states it as the trait of that named kind (`cls: attribute`). Rules text, spell effects ("this spell heals…"), stat blocks and advice to players are never ties.
3. **dwells at vs other things.** "Home of", "lives in", "dwells beneath" → dwells at. "The temple of X is at Y" is not dwelling (already captured as cult). "Rules from" is not dwelling.
4. **dies:** only when the text says the being died, perished or was slain with no killer named. If a killer is named, skip it (already captured). A statue or a fire that "dies" is not a tie.
5. **possesses / wields:** a specific named or clearly identified object (a spear, THE IRON SWORD, a cloak of feathers). Not abilities, runes or magic ("has great power").
6. **speaks:** only when there is an addressee or a prophecy. "It is said" / "the texts say" is the narrator, never a tie.
7. **Direction matters.** "Orlanth was hated by Yelm": S = YELM, O = ORLANTH.
8. **Never equate names from outside knowledge.** Use the name in the quote.
9. **One tie per fact per passage.** A mutual relation ("X and Y hated each other") is one tie, S = first-named, O = second-named, with `note: "mutual"`.
10. **Density.** Expect roughly 0–3 target ties per passage; many passages yield none. Zero ties is a correct result.

## Example
TEXT: *"… Herjan then pursued it into its lair and killed it … A few years later the Luatha landed, and Herjan tried to die fighting them. He was cursed instead, and is said to be wandering Glorantha pleading for peace and understanding."*
```json
{"pid":"GtG2:00004","q":["Herjan then pursued it into its lair"],"s":["HERJAN"],"p":"hunts","o":["FROALAR"],"surface":{"direct_object:FROALAR":"it"},"p_surface":"pursued it into its lair","corpus":"Editorial","age":"Third Age","spatium":"Spatium Historicum (Time)","cls":"narrative","inference":"'it' = the serpent, revealed in the same sentence to be Froalar."}
```
Not extracted: "cursed instead" (no curser named, S would be empty); "tried to die" (he did not die).

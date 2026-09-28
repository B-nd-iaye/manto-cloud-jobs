# MANTO-Glorantha — semantic verification + v2 predicate — prompt vr-v1 (2026-09-28)

You are an independent verifier. You did not write these records. For each record you do two things, judging **only from its quote** (no outside knowledge, no other files):
(1) verify the tie as extracted; (2) assign its v2 predicate.

Each record: `[ID] S=… P=… O=… [IO=…] [MOD={…}] implicit=… [ps="…"] [sug=…]`, then `Q:` the verbatim quote (segments separated by `||`).
`P` is the extractor's (old, v1) predicate, `ps` the text's own verb phrase, `sug` a pre-filled v2 suggestion (from a fixed rename table or the extractor's proposal): confirm it if the quote supports it, otherwise override it.

## Output
Exactly one JSON line per record, in input order, and nothing else (no prose, no code fences, no summary):
`{"id": "...", "v": "S|P|U", "inf": [slots], "why": "...", "pf": "<v2 predicate>"}` plus, only when needed, `"S"`, `"O"`, `"IO"`, `"qual"`.

### (1) Verification — `v`, `inf`, `why` (judge the tie as extracted, with its v1 predicate `P`)
- `S` = supports: every slot is stated or unmistakably entailed by the quote.
- `P` = partial: the gist is right, but some slot is inferred (pronoun, context, outside knowledge), generalised, attached to the wrong event, or the predicate is stronger than the text.
- `U` = unsupported: the quote does not say this, contradicts it, or reverses the direction.
- `inf`: slots inferred or over-strong. Names: subject, predicate, direct_object, indirect_object, using, in_on_at, from, to, via, with_the_aid_of, at_the_command_of, at_the_instigation_of, in_accordance_with, purpose_clause. `[]` for S.
- `why`: at most 15 words; required for P and U, omit for S.

### (2) v2 predicate — `pf` and optional `S`/`O`/`IO`/`qual`
- `pf`: exactly one term from the vocabulary below — the most specific one the quote supports. If `v` is U because the quote states no relation between these entities, `pf` = `REJECT`. If `v` is U only because the v1 predicate was wrong or reversed but the quote does state a relation between the same entities, give the correct `pf` (and arguments).
- `"S"`, `"O"`, `"IO"` (UPPER CASE lists): ONLY if the v2 predicate needs different arguments than the tie has — direction reversal (`is worshipped by`: S=deity, O=worshippers; `is epithet of`: S=epithet, O=bearer) or a restored agent named in the quote (`conceives`, `founds`, `crafts`, `appoints`: maker in S, thing made in O). Never invent a name absent from the quote; with no named creator use `comes into being`.
- `"qual"`: only where the vocabulary defines one (twin, wedding, blinding, monstrous|hybrid, equation|conflation|rationalisation|incarnation).

Principles: `is synonym of` = the same being under another NAME; `is epithet of` = a descriptive or honorific title; "god of X" → `has domain` (O = X). `conceives` = agentive creation without birth; births → `is born from` / `is child of`; artifacts → `crafts`; states, cities, orders → `founds`. Worship: people/polity → `is worshipped by` (S=deity); town/region → `is worshipped at`; temple/shrine/site → `receives cult at`. Dying without a named killer → `dies`. `manifests` and `alters mythic station` never survive: always a precise term.

## Vocabulary (v2)
- `comes into being` — S emerges spontaneously; NO agent is named or implied as maker [S=what emerges]
- `conceives` — S brings O into existence WITHOUT giving birth: makes, shapes, fashions, thinks, speaks or wills it into being (cosmogony, races, powers, concepts) [S=creator, O=created]
- `founds` — S establishes a polity, city, dynasty, school, order or institution [S=founder, O=thing founded]
- `is born from` — S is born, hatched, spawned or emanated from O (parent, body, substance) [S=offspring, O=source]
- `is child of` — S is the son/daughter/offspring of O [S=child, O=parent]
- `embodies` — S is essentially one with a Rune or cosmic element (Air, Death, Chaos...) [S=being, O=Rune/element]
- `has domain` — S is the god/goddess/spirit OF O: sphere, portfolio, function (war, sailors, harvest) [S=being, O=domain]
- `has anomalous form` — S has a monstrous or hybrid body; qual=monstrous|hybrid [S=being, O=form (optional)]
- `is sibling of` — S is brother/sister/half-sibling of O; qual=twin when twins [S, O siblings]
- `is spouse of` — S is husband/wife/consort of O; qual=wedding when the union itself is narrated [S, O spouses]
- `claims ancestry` — S descends from / claims O as ancestor (beyond one generation) [S=descendant, O=ancestor]
- `swears oath with` — S swears a formal oath/pact/vow with or to O [S, O parties]
- `allies with` — S forms an alliance or friendship with O [S, O allies]
- `makes peace with` — S ends hostility / negotiates peace or truce with O [S, O parties]
- `breaks oath` — S breaks an oath, pact, geas or taboo, or disobeys O [S=breaker, O=party/oath]
- `rules` — S governs a polity, people or realm O [S=ruler, O=ruled]
- `leads` — S commands an army, expedition, migration or group O [S=leader, O=group]
- `accedes to rule` — S becomes ruler/king/emperor of O (acclaimed, crowned, succeeds) [S=new ruler, O=realm]
- `appoints` — S installs O in an office or rank (IO=office or realm) [S=appointer, O=appointee]
- `serves` — S is servant, vassal, thane, retainer or follower of O [S=servant, O=master]
- `aids` — S helps, assists or supports O on an occasion [S=helper, O=helped]
- `submits to` — S yields to, acknowledges the supremacy of, or pays tribute to O [S=submitter, O=superior]
- `is member of` — S belongs to collective O (pantheon, tribe, group, council) [S=member, O=collective]
- `is part of` — S is a subcult, aspect or component of O [S=part, O=whole]
- `holds office in` — S is priest, officer or office-holder of O (cult, temple, order) [S=holder, O=institution]
- `is worshipped by` — deity S receives worship from a group, people or polity O [S=deity, O=worshippers]
- `is worshipped at` — deity S is worshipped in a settlement or region O [S=deity, O=settlement/region]
- `receives cult at` — deity S has a temple, shrine or sacred site O [S=deity, O=temple/shrine/site]
- `establishes cult` — S founds or spreads the worship of deity O (loc=where) [S=founder, O=deity/cult]
- `initiates into cult` — S initiates O into a cult, or S is initiated into cult O (keep the tie's direction) [as tie]
- `performs sacrifice` — S makes a ritual offering O to IO [S=sacrificer, O=offering, IO=recipient]
- `dedicates relic` — S dedicates an object/relic O (to IO) [S, O=relic]
- `survives as relic` — S persists as a relic/remnant O into later times [S=entity, O=relic]
- `teaches` — S teaches, instructs or trains O (IO=what is taught) [S=teacher, O=student]
- `bestows` — S gives a gift, power, magic or blessing O to IO [S=giver, O=gift, IO=recipient]
- `heals` — S heals or cures O [S=healer, O=healed]
- `bestows geas` — S lays a geas, taboo or binding obligation on O [S, O=bound party]
- `crafts` — S makes an artifact/object O (forges, weaves, builds, carves) [S=maker, O=artifact]
- `summons / invokes` — S calls O (spirit, god, power) into presence or action [S=summoner, O=summoned]
- `tricks` — S deceives, fools or tricks O [S=trickster, O=dupe]
- `seduces` — S seduces or beguiles O [S=seducer, O=seduced]
- `curses` — S curses O [S=curser, O=cursed]
- `imbues` — S infuses O with a power, spirit or Rune (IO=what is infused) [S, O=object/being imbued]
- `illuminates` — S brings Illumination/enlightenment to O [S, O]
- `fights` — S fights O with no stated outcome [S, O combatants]
- `wages war on` — S (polity/people/army) is at war with O [S, O]
- `invades / raids` — S invades, raids, attacks or ambushes O [S=attacker, O=target]
- `hunts` — S hunts or pursues O [S=hunter, O=prey]
- `betrays` — S betrays O [S=traitor, O=betrayed]
- `challenges` — S challenges, defies or confronts O [S, O]
- `defeats` — S overcomes O in a contest or battle, without killing [S=victor, O=loser]
- `conquers` — S conquers or subjugates territory/people O [S=conqueror, O=conquered]
- `exiles / banishes` — S drives out, exiles or banishes O [S=banisher, O=banished]
- `punishes` — S punishes O [S, O]
- `avenges` — S takes vengeance on O (IO=whom/what is avenged) [S=avenger, O=target]
- `kills` — S kills a being O (using=weapon) [S=killer, O=victim]
- `wounds` — S injures O without killing; qual=blinding when blinded [S, O]
- `dismembers` — S tears O into parts [S, O]
- `swallows / consumes` — S eats, devours or swallows O [S, O]
- `binds` — S imprisons, chains, traps or enslaves O [S=binder, O=bound]
- `captures` — S seizes or takes O captive [S=captor, O=captive]
- `shatters` — S destroys or breaks an object, place or structure O [S, O]
- `steals` — S steals or takes O by force/stealth (from=victim) [S=thief, O=stolen]
- `loses` — S loses O (a possession, power, body part, being) [S=loser, O=lost]
- `exchanges` — S gives O in exchange for IO [S, O=given, IO=received]
- `trades with` — S trades or bargains with O [S, O partners]
- `corrupts` — S taints O with Chaos or corruption [S=corrupter, O=corrupted]
- `grows tainted with Chaos` — S becomes tainted by Chaos (process) [S]
- `is tainted with Chaos` — S is Chaos-tainted (state) [S]
- `protects` — S guards, shields or is patron-protector of O [S=protector, O=protected]
- `rescues / frees` — S saves, rescues, frees or liberates O [S=rescuer, O=rescued]
- `loves / desires` — S loves, desires or lusts after O [S=lover, O=beloved]
- `hates` — S hates or feuds with O [S, O]
- `fears` — S fears O [S, O=feared]
- `mourns` — S mourns, weeps or laments for O [S, O=mourned]
- `speaks / informs / warns / prophesies` — S speaks to, tells, warns, advises or prophesies to O [S=speaker, O=addressee]
- `reveals` — S discloses hidden knowledge, a secret or an object O (to IO) [S, O=revealed, IO=to whom]
- `reveals itself` — S shows its presence or true nature to O [S, O=witness]
- `unmasks` — S exposes the true identity or nature of O [S, O]
- `brings back` — S brings O back (from=place) [S, O=returned]
- `dies` — S dies (not the killing act itself; use kills when a killer is named) [S, O=place/cause optional]
- `descends into` — S goes down into the Underworld / Hell / realm of the dead (alive or dead) [S, O=realm]
- `resurrects` — S returns O to life, or S returns to life (O empty) [S, O]
- `sleeps` — S falls asleep / lies dormant [S]
- `awakens` — S wakes O, or S wakes (O empty) [S, O]
- `transforms into` — S changes into O [S, O=new form]
- `becomes celestial body` — S becomes a star, planet or constellation O [S, O]
- `is deified` — S becomes a god/hero/immortal (apotheosis) [S, O=new status optional]
- `loses status` — S is demoted, stripped of powers or rank [S, O=what is lost optional]
- `takes title` — S assumes a title or new name O [S, O=title]
- `travels` — S journeys to/through a place (to/via/O) [S, O=destination optional]
- `departs from` — S leaves O [S, O=place/party left]
- `flees to` — S flees/escapes/hides (to O) [S, O]
- `rides` — S rides O (mount, vehicle) [S, O]
- `sends` — S sends O (to=destination, IO=addressee) [S, O=sent]
- `settles at` — S settles, founds a home or takes up residence at O [S=settlers, O=place]
- `dwells at` — S lives, dwells or resides at/in O (a standing state) [S, O=place]
- `enters Godtime / Otherworld` — S crosses into the Otherworld / Godtime / Hero Plane [S, O]
- `re-enacts` — S re-enacts a mythic event or path O (HeroQuest) [S, O]
- `substitutes` — S takes the mythic role of O [S, O]
- `discovers` — S finds, discovers or invents O [S, O]
- `appears` — S appears or manifests (to O / at loc) [S, O=witness optional]
- `manifests as` — S appears in the form of O (avatar) [S=being, O=form]
- `causes` — S brings about an event or phenomenon O [S, O=event]
- `possesses / wields` — S owns, carries, wears or wields O [S=owner, O=object]
- `is synonym of` — S is another NAME of the same being O: core lexical equivalence (regional, linguistic, alternative name) [S=name, O=main entity]
- `is epithet of` — S is a descriptive or honorific title/epithet of O (the Sun God, Lurker Upon the Veil) [S=epithet, O=bearer]
- `is identified as` — S is equated with O; qual=equation|conflation|rationalisation|incarnation [S, O]
- `REJECT` — the tie is not a relation between the named entities, or its quote does not support it [note=reason]

#!/usr/bin/env python3
"""Headless batch runner: one `claude -p` call per input file — no tools, no session, the prompt file as the
system prompt, the input on stdin, JSON lines on stdout. Logs metered usage to <outdir>/usage.jsonl.
For id-keyed tasks (--ids) a partial answer is re-asked for the missing records only.

  python3 headless.py PROMPT OUTDIR INPUT... [--model sonnet] [--effort low|medium|high] [--parallel 6] [--ids]"""
import argparse, json, pathlib, re, subprocess, time
from concurrent.futures import ThreadPoolExecutor
ap = argparse.ArgumentParser(); ap.add_argument("prompt"); ap.add_argument("outdir"); ap.add_argument("inputs", nargs="+")
ap.add_argument("--model", default="sonnet"); ap.add_argument("--effort"); ap.add_argument("--parallel", type=int, default=6)
ap.add_argument("--ids", action="store_true", help="records start with [ID]; retry missing ids"); a = ap.parse_args()
SYS = re.sub(r"\n(Writing|Then write|Write ALL)[^\n]*", "", pathlib.Path(a.prompt).read_text(encoding="utf-8"))
SYS += "\n\nOutput: JSON lines only, one object per line — no prose, no code fences, no summary. An empty output is allowed when nothing qualifies.\n"
out = pathlib.Path(a.outdir); out.mkdir(parents=True, exist_ok=True)

def call(text):
    cmd = ["claude", "-p", "--model", a.model, "--tools", "", "--no-session-persistence", "--output-format", "json",
           "--system-prompt", SYS] + (["--effort", a.effort] if a.effort else []) + ["Process this input:"]
    t0 = time.time(); p = subprocess.run(cmd, input=text, capture_output=True, text=True, timeout=3600)
    d = json.loads(p.stdout)
    if d.get("is_error"): raise RuntimeError(d.get("result"))
    return d["result"], d.get("usage", {}), d.get("total_cost_usd"), time.time() - t0

def lines(res):
    for l in res.splitlines():
        l = l.strip().strip("`")
        if l.startswith("{"):
            try: yield json.loads(l)
            except Exception: pass

def run(inp):
    inp = pathlib.Path(inp); dst = out / (inp.stem + ".jsonl")
    recs = [r for r in re.split(r"\n(?=\[)", inp.read_text(encoding="utf-8")) if r.strip()] if a.ids else None
    for attempt in range(3):
        have = {json.loads(l)["id"] for l in open(dst)} if (a.ids and dst.exists()) else set()
        if a.ids:
            todo = [r for r in recs if r[1:r.index("]")] not in have]
            if not todo: return inp.stem, "complete"
            text = "\n".join(todo) + "\n"
        else:
            if dst.exists(): return inp.stem, "exists"
            text = inp.read_text(encoding="utf-8")
        try: res, u, cost, dt = call(text)
        except Exception as e:
            print(inp.stem, "error", e); time.sleep(20); continue
        got = list(lines(res))
        if a.ids: got = [g for g in got if "id" in g and g["id"] not in have]
        with open(dst, "a") as f: f.writelines(json.dumps(g, ensure_ascii=False) + "\n" for g in got)
        with open(out / "usage.jsonl", "a") as f:
            f.write(json.dumps({"input": inp.stem, "attempt": attempt, "lines": len(got), "sec": round(dt), "usage": u,
                                "cost_usd": cost, "model": a.model, "effort": a.effort}) + "\n")
        print(f"{inp.stem}: {len(got)} lines, {round(dt)}s, in={u.get('input_tokens',0)}+cw{u.get('cache_creation_input_tokens',0)}+cr{u.get('cache_read_input_tokens',0)} out={u.get('output_tokens',0)}", flush=True)
        if not a.ids: return inp.stem, "done"
    return inp.stem, "incomplete"

with ThreadPoolExecutor(a.parallel) as ex:
    for r in ex.map(run, a.inputs): print(*r)

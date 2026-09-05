#!/usr/bin/env python3
"""Synthesis run. Reads a block of entries plus any prior staff reports,
runs three personas in parallel, writes a combined Staff Report to
`synthesis/output/latest.json` for the dashboard and prints it to stdout.

Usage:
  python synthesis/run.py --demo               # block 3 of sample_data/
  python synthesis/run.py --demo --block 2     # any block in sample_data/
  python synthesis/run.py --entries path/ --reports path/ --block N
"""
import os, sys, json, glob, argparse, datetime, pathlib
from concurrent.futures import ThreadPoolExecutor

try:
    from anthropic import Anthropic
except ImportError:
    sys.exit("pip install -r requirements.txt first")

ROOT = pathlib.Path(__file__).resolve().parent.parent
PROMPTS = ROOT / "prompts"
DEMO_ENTRIES = ROOT / "sample_data" / "entries"
DEMO_REPORTS = ROOT / "sample_data" / "reports"
OUT = ROOT / "synthesis" / "output"
MODEL = os.environ.get("SYNTHESIS_MODEL", "claude-sonnet-5")
PERSONAS = ["coach", "psychologist", "tactics"]
HEADINGS = {
    "coach": "Coach — Technical",
    "psychologist": "Sport Psychologist — Mental",
    "tactics": "Tactics Analyst — Strategy",
}


def load_persona(name):
    shared = (PROMPTS / "_shared_rules.md").read_text()
    role = (PROMPTS / f"{name}.md").read_text()
    return shared + "\n\n---\n\n" + role


def load_entries(entries_dir, block):
    files = sorted(glob.glob(str(pathlib.Path(entries_dir) / "*.json")))
    entries = [json.loads(pathlib.Path(f).read_text()) for f in files]
    return [e for e in entries if e.get("block") == block]


def load_prior_reports(reports_dir, block):
    reports = []
    for i in range(1, block):
        p = pathlib.Path(reports_dir) / f"block_{i}.md"
        if p.exists():
            reports.append((i, p.read_text()))
    return reports


def format_input(entries, prior_reports, block):
    if not entries:
        return None, None
    date_range = [entries[0]["date"], entries[-1]["date"]]
    sessions = [e["session"] for e in entries]

    parts = [f"Block {block}, sessions {sessions[0]}-{sessions[-1]} ({date_range[0]} to {date_range[1]}).\n"]

    if prior_reports:
        parts.append("Prior staff reports:\n")
        for b, body in prior_reports:
            parts.append(f"--- Block {b} report ---\n{body}\n")

    parts.append("Entries:\n")
    for e in entries:
        parts.append(
            f"S{e['session']} ({e['date']}, {e['type']}, {e.get('duration_min', '?')} min, "
            f"{', '.join(e.get('partners_or_opponents', []))}):\n"
            f"  Arrived: {e['arrived']}\n"
            f"  {e['session_narrative']}\n"
            f"  Tracked: {json.dumps(e['tracked'])}\n"
            f"  Take-away: {e['take_away']}\n"
        )
    return "\n".join(parts), {"date_range": date_range, "sessions": sessions}


def run_persona(client, name, user_input):
    out = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=load_persona(name),
        messages=[{"role": "user", "content": user_input}],
    )
    return name, out.content[0].text.strip()


def synthesize(client, entries, prior_reports, block):
    user_input, meta = format_input(entries, prior_reports, block)
    if user_input is None:
        sys.exit(f"no entries found for block {block}")

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = dict(pool.map(lambda n: run_persona(client, n, user_input), PERSONAS))

    sections = {name: {"heading": HEADINGS[name], "body": results[name]} for name in PERSONAS}
    markdown = (
        f"# Staff Report — Block {block} "
        f"(sessions {meta['sessions'][0]}-{meta['sessions'][-1]}, "
        f"{meta['date_range'][0]} to {meta['date_range'][-1]})\n\n"
        + "\n\n".join(results[name] for name in PERSONAS)
    )
    return {
        "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "athlete": "Olivia",
        "block": block,
        "date_range": meta["date_range"],
        "sessions_covered": meta["sessions"],
        "model": MODEL,
        "sections": sections,
        "staff_report_markdown": markdown,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="use sample_data/")
    ap.add_argument("--entries", help="path to a directory of entry JSON files")
    ap.add_argument("--reports", help="path to a directory of prior block_N.md reports")
    ap.add_argument("--block", type=int, default=3)
    args = ap.parse_args()

    if args.demo:
        entries_dir, reports_dir = DEMO_ENTRIES, DEMO_REPORTS
    elif args.entries and args.reports:
        entries_dir, reports_dir = args.entries, args.reports
    else:
        sys.exit("pass --demo, or both --entries and --reports")

    entries = load_entries(entries_dir, args.block)
    prior_reports = load_prior_reports(reports_dir, args.block)

    client = Anthropic()
    report = synthesize(client, entries, prior_reports, args.block)

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "latest.json").write_text(json.dumps(report, indent=2))
    print(report["staff_report_markdown"])
    print(f"\n[wrote {OUT / 'latest.json'}]", file=sys.stderr)


if __name__ == "__main__":
    main()

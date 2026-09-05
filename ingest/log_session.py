#!/usr/bin/env python3
"""Ingest one session. Takes a raw dump (voice-note or typed), uses Claude
to extract the four-section structured entry that the synthesis run expects,
prints it as JSON, and optionally appends it to a Notion page.

The rigid four-section format (arrived / session_narrative / tracked /
take_away) is the price of cross-session comparison. If the ingest is
loose, the synthesis is useless.

Usage:
  python ingest/log_session.py --demo
  python ingest/log_session.py --input path/to/dump.txt
  cat dump.txt | python ingest/log_session.py
  python ingest/log_session.py --demo --notion   # requires NOTION_TOKEN, NOTION_PARENT_PAGE
"""
import os, sys, json, argparse, pathlib

try:
    from anthropic import Anthropic
except ImportError:
    sys.exit("pip install -r requirements.txt first")

MODEL = os.environ.get("INGEST_MODEL", "claude-sonnet-5")

DEMO_DUMP = """Okay, session eleven. Sunday group at GG Park with Rhea, doubles.
Lost four-six, six-three, four-six. Serve was a disaster in my head the
whole time, honestly one double fault the whole match but I could not
trust it. First set I kept driving returns straight back at the net player
instead of down the middle or crosscourt away from her. Caught myself
doing it about halfway through the first set. Second set I actively aimed
away from her and it opened up, we won it three-six. Third set fell right
back into the same pattern under pressure. Ugh. First serve percentage
felt about the same as last week, sixty-three ish. Arrived tired, same as
last week, haven't slept well in weeks."""

EXTRACTION_PROMPT = """You extract structured session entries from raw athlete dumps.

Return ONLY a JSON object with exactly these fields, no prose, no code fences:
{
  "session": null,
  "block": null,
  "date": "YYYY-MM-DD or null",
  "type": "practice | drill | match | class",
  "duration_min": number or null,
  "partners_or_opponents": ["string"],
  "location": "string or null",
  "arrived": "one line on entry state — sleep, mood, energy, day",
  "session_narrative": "what happened, in the athlete's voice, factual",
  "tracked": {"first_serve_pct": number or null, "double_faults": number or null, "unforced_errors": "not tracked or number"},
  "take_away": "one or two lines the athlete thinks the session showed"
}

Rules:
- Preserve the athlete's voice in narrative and take_away. Do not tidy.
- Do not invent numbers. If she says "about 60%," write 60. If she does not say, use null.
- session and block are usually null at ingest; a later step assigns them.
- Take type from the dump; if ambiguous, use "practice"."""


def extract(client, dump):
    out = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system=EXTRACTION_PROMPT,
        messages=[{"role": "user", "content": dump}],
    ).content[0].text.strip()
    if out.startswith("```"):
        out = out.strip("`").lstrip("json").strip()
    return json.loads(out)


def write_to_notion(entry):
    """Append the entry as a page under NOTION_PARENT_PAGE.

    Kept intentionally minimal. The Notion API contract for creating a page
    with a title and a code block for the JSON is stable enough that this
    reference implementation covers the common case. Production would add
    retries, block-level formatting, and idempotency.
    """
    import urllib.request, urllib.error
    token = os.environ.get("NOTION_TOKEN")
    parent = os.environ.get("NOTION_PARENT_PAGE")
    if not token or not parent:
        sys.exit("--notion requires NOTION_TOKEN and NOTION_PARENT_PAGE env vars")

    title = f"S{entry.get('session') or '?'} — {entry.get('date') or 'undated'} — {entry.get('type', 'session')}"
    payload = {
        "parent": {"page_id": parent},
        "properties": {"title": [{"text": {"content": title}}]},
        "children": [
            {"object": "block", "type": "code",
             "code": {"language": "json",
                      "rich_text": [{"type": "text", "text": {"content": json.dumps(entry, indent=2)}}]}}
        ],
    }
    req = urllib.request.Request(
        "https://api.notion.com/v1/pages",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())["url"]
    except urllib.error.HTTPError as e:
        sys.exit(f"Notion API error {e.code}: {e.read().decode()}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--demo", action="store_true", help="use a baked-in raw dump")
    ap.add_argument("--input", help="path to a raw dump file")
    ap.add_argument("--notion", action="store_true", help="also append to Notion")
    args = ap.parse_args()

    if args.demo:
        dump = DEMO_DUMP
    elif args.input:
        dump = pathlib.Path(args.input).read_text()
    elif not sys.stdin.isatty():
        dump = sys.stdin.read()
    else:
        sys.exit("pass --demo, --input path, or pipe a dump on stdin")

    client = Anthropic()
    entry = extract(client, dump)
    print(json.dumps(entry, indent=2))

    if args.notion:
        url = write_to_notion(entry)
        print(f"\n[wrote to Notion: {url}]", file=sys.stderr)


if __name__ == "__main__":
    main()

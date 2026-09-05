# Personal Intelligence

**Give an LLM your daily narrative for long enough and it will find what you can't: the pattern across sessions, not the noise inside one.**

This is a working system, not a template. Eleven weeks of tennis practice went in as voice notes. What came out was a diagnosis no single session could have produced: the problem was never the serve mechanics, it was trust in a motion that already worked. The system saw it in the log before the player felt it on court.

Three parts, all in this repo:

1. **Ingest.** A voice or text dump goes in; a structured entry comes out and lands in Notion. Same four sections every time, because consistency is what makes cross-session reading possible.
2. **Synthesis.** Every N sessions, a panel of personas (coach, sport psychologist, physio, nutritionist, tactics analyst) reads the whole log and writes what's progressing, what's stuck, and what to work on next.
3. **Dashboard.** A one-page view built from the synthesis output: skill trajectories, the current bottleneck, ranked development priorities.

Tennis is the worked example. Nothing here is tennis-specific except the personas and the sample data.

## Run it

```bash
git clone https://github.com/oliviameng/personal-intelligence.git
cd personal-intelligence
pip install -r requirements.txt
cp .env.example .env                  # ANTHROPIC_API_KEY, NOTION_TOKEN, NOTION_PARENT_PAGE
python ingest/log_session.py --demo   # writes a sample entry
python synthesis/run.py --demo        # runs the panel over sample_data/
open dashboard/index.html
```

## What's in the box

| Folder | What it is |
| --- | --- |
| `protocol/` | The entry framework and synthesis protocol as plain documents. Read these first. |
| `prompts/` | Persona prompts for the synthesis panel. The intellectual core; edit freely. |
| `ingest/` | Dump-to-entry script, writes to Notion. |
| `synthesis/` | Every-N-sessions job producing Coach's Notes and the Staff Report. |
| `dashboard/` | Static HTML that reads `synthesis/output/latest.json`. |
| `sample_data/` | A fabricated athlete. Twelve entries, two synthesis reports. |
| `scripts/ip_scan.py` | Pre-commit scan that blocks employer or personal references from ever being committed. |

## Why this is product work, not model work

No fine-tuning. No RAG pipeline. No agent framework. The entire lift is in three decisions: what shape the input takes, when synthesis runs, and how much judgment the panel gets before a human reads it. Get those right and a frontier model does the rest. Get them wrong and no model saves you.

Longer version: [essay on Soft Intelligence](https://substack.com/@oliviaxmeng).

## Privacy

The sample data is invented. My real journal is not in this repository and never will be. If you run this on your own life, keep exports in `private/` (gitignored) and enable the pre-commit hook (`docs/SETUP_HOOK.md`).

## License

Apache-2.0.

---

*Personal project. Built on my own time with my own tools; not affiliated with or endorsed by any employer.*

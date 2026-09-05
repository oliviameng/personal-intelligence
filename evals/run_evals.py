#!/usr/bin/env python3
"""Run persona evals. Each case tempts one failure; a case passes if the
persona resists. Grading is model-assisted because the failures are semantic.

Usage:
  python run_evals.py            # all cases
  python run_evals.py --case ID  # one case
"""
import os, sys, json, glob, pathlib, argparse

try:
    from anthropic import Anthropic
except ImportError:
    sys.exit("pip install anthropic first")

MODEL = os.environ.get("EVAL_MODEL", "claude-opus-4-8")
PROMPTS = pathlib.Path(__file__).parent.parent / "prompts"

def load_persona(name):
    shared = (PROMPTS / "_shared_rules.md").read_text()
    role = (PROMPTS / f"{name}.md").read_text()
    return shared + "\n\n---\n\n" + role

def run_case(client, case):
    system = load_persona(case["persona"])
    out = client.messages.create(
        model=MODEL, max_tokens=1024, system=system,
        messages=[{"role": "user", "content": case["input"]}],
    ).content[0].text

    grader = (
        "You are grading whether a persona output avoided a specific failure.\n\n"
        f"PASS CRITERIA:\n{case['pass_criteria']}\n\n"
        f"FAIL IF ANY OF THESE:\n{case['fail_if']}\n\n"
        f"OUTPUT TO GRADE:\n{out}\n\n"
        "Respond with a JSON object only: "
        '{\"verdict\": \"pass\" or \"fail\", \"reason\": \"one sentence\"}'
    )
    g = client.messages.create(
        model=MODEL, max_tokens=300,
        messages=[{"role": "user", "content": grader}],
    ).content[0].text
    try:
        verdict = json.loads(g.strip().strip("`").replace("json", "", 1).strip())
    except Exception:
        verdict = {"verdict": "error", "reason": "grader did not return JSON"}
    return out, verdict

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case")
    args = ap.parse_args()
    client = Anthropic()
    files = sorted(glob.glob(str(pathlib.Path(__file__).parent / "cases" / "*.json")))
    if args.case:
        files = [f for f in files if json.load(open(f))["id"] == args.case]
        if not files:
            sys.exit(f"no case with id {args.case}")
    passed = 0
    for f in files:
        case = json.load(open(f))
        _, v = run_case(client, case)
        mark = "PASS" if v["verdict"] == "pass" else v["verdict"].upper()
        print(f"[{mark}] {case['id']}  ({case['persona']})")
        print(f"       tests: {case['tests']}")
        print(f"       {v['reason']}\n")
        passed += v["verdict"] == "pass"
    print(f"{passed}/{len(files)} passed")

if __name__ == "__main__":
    main()

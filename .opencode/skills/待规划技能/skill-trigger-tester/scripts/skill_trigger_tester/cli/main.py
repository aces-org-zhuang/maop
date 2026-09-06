#!/usr/bin/env python3
import argparse
import sys
import json
import os
import shutil
import subprocess
import concurrent.futures
import threading
from pathlib import Path
from typing import Dict, List, Any

from .utils.process import ProcExecutor


def _safe_print_line(prefix: str, line: str) -> None:
    """Print without crashing on GBK consoles."""
    text = f"{prefix} {line}" if prefix else line
    enc = getattr(sys.stdout, "encoding", None) or "utf-8"
    try:
        print(text)
    except UnicodeEncodeError:
        safe = text.encode(enc, errors="backslashreplace").decode(enc, errors="ignore")
        print(safe)


test_cases_path = os.path.join(os.path.dirname(__file__), "templates", "test_cases.md")
optimization_map = os.path.join(
    os.path.dirname(__file__), "templates", "optimization_map.md"
)
opencode_cmd_path = (
    shutil.which("opencode")
    or r"C:\Users\Administrator\AppData\Roaming\npm\opencode.cmd"
)
# Keep run artifacts under a stable ASCII path to avoid console encoding issues.
TEST_DIR = Path(".aces") / "projects" / "skill-trigger-tester"


def _sanitized_opencode_env() -> Dict[str, str]:
    # Some environments (notably Desktop client integration) set OPENCODE_* vars
    # that cause `opencode run` to attempt desktop session attach, which can fail
    # in headless CLI runs with "Session not found".
    env = dict(os.environ)
    for k in (
        "OPENCODE_CLIENT",
        "OPENCODE_PID",
        "OPENCODE_SERVER_USERNAME",
        "OPENCODE_SERVER_PASSWORD",
    ):
        env.pop(k, None)
    return env


def test_skill_trigger(case) -> Dict[str, Any]:
    skill_name = case["skill_name"]
    trigger_phrase = case["trigger_phrase"]
    skill_id = case.get("skill_id")

    result = {
        "skill_id": skill_id,
        "skill_name": skill_name,
        "trigger_phrase": trigger_phrase,
        "success": False,
        "output": "",
        "error": None,
        "triggered": False,
        "test_type": case.get("test_type", "positive"),
        "expected_trigger": case.get("expected_trigger", "yes"),
    }

    # Check if opencode command exists
    if not opencode_cmd_path:
        result["error"] = (
            "opencode command not found. Please install opencode or ensure it's in your PATH."
        )
        return result

    try:
        cmd = [opencode_cmd_path, "run", trigger_phrase]
        output_lines: List[str] = []
        triggered = False
        line_count = 0

        def on_line(line: str, _executor: ProcExecutor) -> None:
            nonlocal triggered, line_count

            if line.startswith("[SYS] "):
                return
            if not line.strip():
                return
            line_count += len(line)
            output_lines.append(line)
            _safe_print_line("[OpenCode]", line)

            # Prefer the explicit skill banner line.
            skill_banner = f'Skill "{skill_name}"'
            if skill_banner in line:
                triggered = True
                _executor.kill_tree()
            elif line_count >= 500:
                _executor.kill_tree()

        ex = ProcExecutor(callback=on_line)
        cwd = TEST_DIR / skill_name

        # Cache per test case, not per skill, to avoid reusing one result
        # for positive/negative/edge cases of the same skill.
        import hashlib

        h = hashlib.sha1(
            (
                f"{skill_name}|{result['test_type']}|{trigger_phrase}|{result['expected_trigger']}"
            ).encode("utf-8", errors="replace")
        ).hexdigest()[:12]
        cwd = cwd / f"case_{h}"
        cwd.mkdir(parents=True, exist_ok=True)
        result_path = cwd / f"result.json"
        if result_path.exists():
            result = json.loads(result_path.read_text(encoding="utf-8"))
            return result
        # Keep each test bounded; we only need enough output to detect skill selection.
        rc = ex.run(
            cmd,
            timeout_s=300,
            inherit_stdin=False,
            cwd=cwd,
            env=_sanitized_opencode_env(),
        )

        result["output"] = "".join(output_lines)
        # Defensive: if callback missed for any reason, do a final scan.
        result["triggered"] = triggered or (f'Skill "{skill_name}"' in result["output"])
        result["success"] = (
            result["triggered"]
            if case["expected_trigger"] == "yes"
            else not result["triggered"]
        )

        if rc != 0 and not result["triggered"]:
            # ProcExecutor merges stderr into stdout; preserve full output as error context.
            result["error"] = (
                result["output"].strip() or f"opencode exited with code {rc}"
            )
    except Exception as e:
        result["error"] = str(e)

    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=4), encoding="utf-8"
    )
    return result


def test_skill_batch(skill_tests: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    # Run in parallel to improve throughput. Each test is subprocess-bound.
    # Default to a conservative worker count to avoid overwhelming the local machine.
    try:
        workers = int(os.environ.get("SKILL_TRIGGER_TEST_WORKERS", "4"))
    except Exception:
        workers = 4
    workers = max(1, min(workers, 16))

    # Keep result order stable for reporting.
    results: List[Any] = [None] * len(skill_tests)
    print_lock = threading.Lock()

    def _run_one(idx: int, test: Dict[str, str]) -> Dict[str, Any]:
        # Prevent interleaved progress logs from becoming unreadable.
        with print_lock:
            print(
                f"[BATCH] {idx + 1}/{len(skill_tests)} {test.get('skill_name')} {test.get('test_type')}"
            )
        return test_skill_trigger(test)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [pool.submit(_run_one, i, t) for i, t in enumerate(skill_tests)]
        for i, fut in enumerate(futs):
            try:
                results[i] = fut.result()
            except Exception as e:
                results[i] = {
                    "skill_id": skill_tests[i].get("skill_id"),
                    "skill_name": skill_tests[i].get("skill_name"),
                    "trigger_phrase": skill_tests[i].get("trigger_phrase"),
                    "success": False,
                    "output": "",
                    "error": f"batch worker error: {e}",
                    "triggered": False,
                    "test_type": skill_tests[i].get("test_type"),
                    "expected_trigger": skill_tests[i].get("expected_trigger"),
                }

    # Persist latest run results for downstream analysis.
    try:
        out_dir = Path(".aces") / "projects" / "skill-trigger-tester" / "outputs"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "test_results.json").write_text(
            json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception:
        # Non-fatal: reporting to stdout is still available.
        pass

    print(generate_report(results))
    print(
        f"NextStep: 对触发质量不好的技能描述description进行优化，参照{optimization_map}"
    )
    return results


def load_test_cases_from_file(file_path: str) -> List[Dict[str, Any]]:
    required_fields = [
        "skill_id",
        "skill_name",
        "test_type",
        "trigger_phrase",
        "expected_trigger",
    ]
    valid_test_types = ["positive", "negative", "edge"]
    valid_expected_triggers = ["yes", "no"]
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            test_cases = data
        elif isinstance(data, dict) and "test_cases" in data:
            test_cases = data["test_cases"]
        else:
            test_cases = [data]
        validated_cases = []
        for i, test_case in enumerate(test_cases):
            if not isinstance(test_case, dict):
                print(f"Warning: Test case {i + 1} is not a dictionary, skipping")
                continue
            missing_fields = [
                field for field in required_fields if field not in test_case
            ]
            if missing_fields:
                print(
                    f"Warning: Test case {i + 1} missing fields: {missing_fields}, skipping"
                )
                continue
            try:
                skill_id = test_case["skill_id"]
                skill_name = test_case["skill_name"]
                test_type = test_case["test_type"]
                trigger_phrase = test_case["trigger_phrase"]
                expected_trigger = test_case["expected_trigger"]
                if not isinstance(skill_id, int):
                    print(f"Warning: Test case {i + 1} skill_id must be integer")
                    continue
                if not isinstance(skill_name, str) or not skill_name.strip():
                    print(
                        f"Warning: Test case {i + 1} skill_name must be non-empty string"
                    )
                    continue
                if not isinstance(test_type, str) or test_type not in valid_test_types:
                    print(f"Warning: Test case {i + 1} test_type invalid")
                    continue
                if not isinstance(trigger_phrase, str) or not trigger_phrase.strip():
                    print(
                        f"Warning: Test case {i + 1} trigger_phrase must be non-empty string"
                    )
                    continue
                if (
                    not isinstance(expected_trigger, str)
                    or expected_trigger not in valid_expected_triggers
                ):
                    print(f"Warning: Test case {i + 1} expected_trigger invalid")
                    continue
                validated_cases.append(
                    {
                        "skill_id": skill_id,
                        "skill_name": skill_name,
                        "test_type": test_type,
                        "trigger_phrase": trigger_phrase,
                        "expected_trigger": expected_trigger,
                    }
                )
            except Exception as e:
                print(f"Warning: Error validating test case {i + 1}: {e}, skipping")
                continue
        return validated_cases
    except FileNotFoundError:
        print(f"Error: Test case file not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Error loading test cases from {file_path}: {e}")
        return []


def generate_report(results: List[Dict[str, Any]]) -> str:
    if not results:
        return "No test results to report."

    # Group results by skill
    skill_results = {}
    for result in results:
        skill_name = result["skill_name"]
        if skill_name not in skill_results:
            skill_results[skill_name] = {"total": 0, "triggered": 0, "tests": []}
        skill_results[skill_name]["total"] += 1
        if result["triggered"]:
            skill_results[skill_name]["triggered"] += 1
        skill_results[skill_name]["tests"].append(result)

    total_tests = 0
    total_triggered = 0

    from datetime import datetime

    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = f"""# Skill Trigger Test Report

Generated: {report_time}

## Overall Statistics

| Skill | Total Tests | Triggered | Trigger Rate |
|-------|-------------|-----------|--------------|
"""

    for skill_name, data in sorted(skill_results.items()):
        total = data["total"]
        triggered = data["triggered"]
        trigger_rate = (triggered / total * 100) if total > 0 else 0
        report += f"| {skill_name} | {total} | {triggered} | {trigger_rate:.1f}% |\n"
        total_tests += total
        total_triggered += triggered

    overall_trigger_rate = (
        (total_triggered / total_tests * 100) if total_tests > 0 else 0
    )

    # Calculate detailed metrics
    false_positives = 0
    false_negatives = 0
    for skill_name, data in skill_results.items():
        for test in data["tests"]:
            expected = test.get("expected_trigger", "yes") == "yes"
            actual = test["triggered"]
            if expected and not actual:
                false_negatives += 1
            elif not expected and actual:
                false_positives += 1

    report += f"""
## Overall Performance

- Overall Trigger Rate: {overall_trigger_rate:.1f}%
- Total False Positives: {false_positives}
- Total False Negatives: {false_negatives}

## Detailed Test Results

| Skill | Test Type | Trigger Phrase | Expected | Actual | Status |
|-------|-----------|----------------|----------|--------|--------|
"""

    for skill_name, data in sorted(skill_results.items()):
        for test in data["tests"]:
            test_type = test.get("test_type")
            trigger_phrase = test["trigger_phrase"]
            expected = test.get("expected_trigger")
            actual = "yes" if test["triggered"] else "no"
            status = "PASS" if (expected == actual) else "FAIL"
            report += f"| {skill_name} | {test_type} | {trigger_phrase} | {expected} | {actual} | {status} |\n"

    return report


def list_available_skills() -> List[str]:
    # Check if opencode command exists
    if not opencode_cmd_path:
        print(
            "Warning: opencode command not found. Returning skills from local skills directory."
        )
        # Fallback to listing skills from local directory
        skills_dir = Path(__file__).parent.parent.parent.parent.parent
        skills = []
        if skills_dir.exists():
            for item in skills_dir.iterdir():
                if item.is_dir() and (item / "SKILL.md").exists():
                    skills.append(item.name)
        return sorted(skills)

    result = subprocess.run(
        [opencode_cmd_path, "debug", "skill"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
        env=_sanitized_opencode_env(),
        timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr or "opencode debug skill failed")

    skills_data = json.loads(result.stdout)
    skills = set()
    for skill_info in skills_data:
        if isinstance(skill_info, dict) and "name" in skill_info:
            skills.add(skill_info["name"])
    return sorted(list(skills))


def main():
    parser = argparse.ArgumentParser(description="Skill Trigger Tester")
    parser.add_argument("--skill", "-s", help="Name of the skill to test")
    parser.add_argument("--trigger", "-t", help="Trigger phrase to test")
    parser.add_argument("--file", "-f", help="JSON file containing test cases")
    parser.add_argument(
        "--list-skills", action="store_true", help="List all available skills"
    )
    parser.add_argument(
        "--fix", action="store_true", help="Update SKILL.md descriptions from JSON file"
    )
    parser.add_argument(
        "--fix-file", help="JSON file with optimized descriptions for --fix mode"
    )
    args = parser.parse_args()
    if args.list_skills:
        skills = list_available_skills()
        if skills:
            print("Available skills:")
            for skill in skills:
                print(f"  - {skill}")
        else:
            print("No skills found in ./ directory")
        print(
            f"\nNext Step:\n[ ] Create test cases, refer to template at: {test_cases_path}"
        )
        return
    if args.skill and args.trigger:
        print("--trigger 只支持positive用例即默认期望触发")
        case = {"skill_name": args.skill, "trigger_phrase": args.trigger}
        result = test_skill_trigger(case)
        print(generate_report([result]))
        return
    if args.file:
        test_cases = load_test_cases_from_file(args.file)
        if test_cases:
            results = test_skill_batch(test_cases)

        else:
            print("No test cases loaded from file")
        return
    if args.fix:
        if not args.fix_file:
            print("Error: --fix requires --fix-file")
            print(
                "Usage: skill-trigger-test --fix --fix-file <optimized_descriptions.json>"
            )
            return
        try:
            with open(args.fix_file, "r", encoding="utf-8") as f:
                optimized_descriptions = json.load(f)
        except FileNotFoundError:
            print(f"Error: File '{args.fix_file}' not found.")
            return
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in '{args.fix_file}': {e}")
            return
        except Exception as e:
            print(f"Error reading '{args.fix_file}': {e}")
            return
        if not isinstance(optimized_descriptions, dict):
            print(
                f"Error: Root must be object/dict, got {type(optimized_descriptions).__name__}"
            )
            return
        invalid_entries = []
        for key, value in optimized_descriptions.items():
            if not isinstance(key, str):
                invalid_entries.append(
                    f"Key '{key}' is not string (got {type(key).__name__})"
                )
            if not isinstance(value, str):
                invalid_entries.append(
                    f"Value for key '{key}' is not string (got {type(value).__name__})"
                )
        if invalid_entries:
            print("Error: Invalid entries in JSON file:")
            for entry in invalid_entries[:5]:
                print(f"  - {entry}")
            if len(invalid_entries) > 5:
                print(f"  - ... and {len(invalid_entries) - 5} more errors")
            return
        skills_dir = Path(__file__).parent.parent.parent.parent.parent
        print(f"Looking for skills in: {skills_dir}")
        if not skills_dir.exists():
            print(f"Error: Skills directory not found at {skills_dir}")
            return
        updated_count = 0
        not_found_count = 0
        for skill_name, new_description in optimized_descriptions.items():
            skill_found = False
            print(f"Searching for skill: {skill_name}")
            for domain_dir in skills_dir.iterdir():
                if domain_dir.is_dir():
                    print(f"Found domain: {domain_dir.name}")
                    if domain_dir.name == skill_name:
                        skill_path = domain_dir / "SKILL.md"
                        print(f"Checking skill path: {skill_path}")
                        if skill_path.exists():
                            skill_found = True
                            print(f"Found skill: {skill_name}")
                        try:
                            with open(skill_path, "r", encoding="utf-8") as f:
                                content = f.read()
                            lines = content.split("\n")
                            in_frontmatter = False
                            frontmatter_end = -1
                            for i, line in enumerate(lines):
                                if line.strip() == "---":
                                    if not in_frontmatter:
                                        in_frontmatter = True
                                    else:
                                        frontmatter_end = i
                                        break
                            if frontmatter_end != -1:
                                for i in range(1, frontmatter_end):
                                    if lines[i].strip().startswith("description:"):
                                        lines[i] = f'description: "{new_description}"'
                                        break
                                with open(skill_path, "w", encoding="utf-8") as f:
                                    f.write("\n".join(lines))
                                print(f"Updated {skill_name} SKILL.md")
                                updated_count += 1
                            else:
                                print(
                                    f"Warning: Could not find frontmatter end in {skill_path}"
                                )
                        except Exception as e:
                            print(f"Error updating {skill_name}: {e}")
                        break
            if not skill_found:
                print(f"Warning: Skill '{skill_name}' not found in {skills_dir}")
                not_found_count += 1
        print(f"\nFinished. Updated: {updated_count}, Not found: {not_found_count}")
        return
    parser.print_help()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Single-document CLI for structured Markdown generation."""

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

STATE_NAME = ".doc-state.json"
DOC_NAME = "document.md"
TEMPLATE_NAME = "template.md"
FEATURE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_META = ("title", "version", "author", "date", "last-update", "status")
DEFAULT_PLAN = [
    {
        "step_id": "intro",
        "instruction": "submit an intro block with next-step",
        "next_step": "complete",
        "allowed_blocks": [],
        "schema": {"type": "object", "required": ["id"]},
    }
]


def now():
    return datetime.now(timezone.utc).isoformat()


def feature_dir(root, feature):
    if not FEATURE_RE.fullmatch(feature):
        raise ValueError("feature name must use k-case, for example payment-flow")
    path = Path(root) / ".aces" / "features" / feature
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_state(directory):
    path = directory / STATE_NAME
    if not path.exists():
        raise ValueError(f"missing {STATE_NAME}; run init first")
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(directory, state):
    state["updated_at"] = now()
    (directory / STATE_NAME).write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def load_json_or_path(raw):
    if raw is None:
        return None
    path = Path(raw)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return json.loads(raw)


def normalize_plan(plan):
    if not plan:
        return DEFAULT_PLAN
    if not isinstance(plan, list):
        raise ValueError("steps plan must be a JSON array")
    normalized = []
    for index, step in enumerate(plan):
        if not isinstance(step, dict):
            raise ValueError("each step must be an object")
        step_id = str(step.get("step_id", "")).strip()
        if not step_id:
            raise ValueError("each step requires step_id")
        normalized.append({
            "step_id": step_id,
            "instruction": str(step.get("instruction", "submit blocks for this step")),
            "next_step": str(step.get("next_step", "complete")),
            "allowed_blocks": list(step.get("allowed_blocks", [])),
            "schema": step.get("schema", {"type": "object", "required": ["id"]}),
            "order": index,
        })
    return normalized


def validate_document_name(name):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", name):
        raise ValueError("document name must be a single safe file name")
    return name


def current_step(state):
    progression = state.get("progression", {})
    steps = progression.get("steps", DEFAULT_PLAN)
    current_id = progression.get("current_step_id", steps[0]["step_id"] if steps else "complete")
    if current_id == "complete":
        return {"step_id": "complete", "instruction": "document generation is complete", "next_step": "complete", "allowed_blocks": [], "schema": {}}
    for step in steps:
        if step.get("step_id") == current_id:
            return step
    return steps[-1] if steps else {"step_id": "complete", "instruction": "complete", "next_step": "complete", "allowed_blocks": [], "schema": {}}


def advance_step(state, next_step_id):
    progression = state.setdefault("progression", {})
    steps = progression.get("steps", DEFAULT_PLAN)
    if next_step_id == "complete":
        progression["current_step_id"] = "complete"
        return
    for step in steps:
        if step.get("step_id") == next_step_id:
            progression["current_step_id"] = next_step_id
            return
    raise ValueError(f"unknown next step: {next_step_id}")


def validate_block_schema(block, schema):
    schema = schema or {}
    if schema.get("type") == "object" and not isinstance(block, dict):
        raise ValueError("block must be an object")
    if schema.get("type") == "array" and not isinstance(block, list):
        raise ValueError("block must be an array")
    required = schema.get("required", [])
    if isinstance(block, dict):
        missing = [key for key in required if key not in block]
        if missing:
            raise ValueError("missing required fields: " + ", ".join(missing))
        properties = schema.get("properties", {})
        for key, prop in properties.items():
            if key not in block:
                continue
            if "const" in prop and block[key] != prop["const"]:
                raise ValueError(f"field {key} must equal {prop['const']}")
            enum = prop.get("enum")
            if enum is not None and block[key] not in enum:
                raise ValueError(f"field {key} must be one of {enum}")


def step_payload_summary(step):
    return {
        "step_id": step.get("step_id"),
        "instruction": step.get("instruction"),
        "next_step": step.get("next_step"),
        "allowed_blocks": step.get("allowed_blocks", []),
        "schema": step.get("schema", {}),
    }


def render_meta(meta):
    lines = ["---"]
    lines.extend(f"{key}: {json.dumps(str(meta[key]), ensure_ascii=False)}" for key in REQUIRED_META)
    lines.append("---")
    return "\n".join(lines)


def render_block(block):
    kind = block.get("type", "paragraph")
    content = block.get("content", "")
    if kind == "table":
        rows = block.get("rows", [])
        if not rows:
            raise ValueError("table requires non-empty rows")
        width = len(rows[0])
        if width == 0 or any(len(row) != width for row in rows):
            raise ValueError("table rows must have equal non-zero column counts")
        return "\n".join(
            ["| " + " | ".join(map(str, rows[0])) + " |",
             "| " + " | ".join("---" for _ in rows[0]) + " |"]
            + ["| " + " | ".join(map(str, row)) + " |" for row in rows[1:]]
        )
    if kind == "ascii":
        return "```text\n" + str(content).rstrip("\n") + "\n```"
    if kind == "heading":
        level = int(block.get("level", 2))
        if level < 1 or level > 6:
            raise ValueError("heading level must be between 1 and 6")
        return "#" * level + " " + str(content)
    if kind == "placeholder":
        name = str(block.get("name", "")).strip()
        if not re.fullmatch(r"[a-z][a-z0-9_-]*", name):
            raise ValueError("placeholder name must match {name} format")
        return "{" + name + "}"
    return str(content)


def render_document(state):
    document_name = state.get("document_name", DOC_NAME)
    chunks = [render_meta(state["metadata"]), ""]
    for block in state.get("blocks", []):
        chunks.extend([render_block(block), ""])
    return "\n".join(chunks).rstrip() + "\n"


def validate(directory):
    errors = []
    try:
        state = load_state(directory)
    except (ValueError, json.JSONDecodeError) as exc:
        return {"valid": False, "errors": [str(exc)]}
    if not (directory.parent.name == "features" and directory.parent.parent.name == ".aces"
            and FEATURE_RE.fullmatch(directory.name)):
        errors.append("document directory must be .aces/features/<k-case>")
    missing = [key for key in REQUIRED_META if key not in state.get("metadata", {})]
    if missing:
        errors.append("missing metadata: " + ", ".join(missing))
    for block in state.get("blocks", []):
        if not block.get("id"):
            errors.append("every block requires a stable id")
        try:
            render_block(block)
        except (ValueError, TypeError) as exc:
            errors.append(f"block {block.get('id', '<unknown>')}: {exc}")
    expected = render_document(state)
    document = directory / state.get("document_name", DOC_NAME)
    if not document.exists() or document.read_text(encoding="utf-8") != expected:
        errors.append(f"{document.name} is out of sync with {STATE_NAME}")
    return {"valid": not errors, "errors": errors, "document": str(document)}


def emit(payload):
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload.get("valid", True) else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description="single-document generation CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("root")
    init.add_argument("feature")
    init.add_argument("--title", default="Untitled document")
    init.add_argument("--author", default="unknown")
    init.add_argument("--document-name", default=DOC_NAME)
    init.add_argument("--steps-plan")
    init.add_argument("--force", action="store_true")
    for name in ("status", "next-step", "validate"):
        command = sub.add_parser(name)
        command.add_argument("directory")
    for name in ("update", "template"):
        command = sub.add_parser(name)
        command.add_argument("directory")
        command.add_argument("payload", help="JSON string or path to a JSON file")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            directory = feature_dir(args.root, args.feature)
            if (directory / STATE_NAME).exists() and not args.force:
                raise ValueError("document already initialized; use status or explicit --force")
            today = date.today().isoformat()
            plan = normalize_plan(load_json_or_path(args.steps_plan))
            document_name = validate_document_name(args.document_name)
            state = {"metadata": {"title": args.title, "version": "0.1.0", "author": args.author,
                                   "date": today, "last-update": today, "status": "draft"},
                     "blocks": [], "document_name": document_name,
                     "progression": {"steps": plan, "current_step_id": plan[0]["step_id"] if plan else "complete"},
                     "created_at": now(), "updated_at": now()}
            save_state(directory, state)
            (directory / state["document_name"]).write_text(render_document(state), encoding="utf-8")
            return emit({"valid": True, "action": "init", "directory": str(directory),
                         "next_step": step_payload_summary(current_step(state))})
        directory = Path(args.directory)
        state = load_state(directory)
        if args.command == "status":
            return emit({"valid": True, "metadata": state["metadata"], "next_step": step_payload_summary(current_step(state)),
                         "blocks": [block["id"] for block in state.get("blocks", [])]})
        if args.command == "validate":
            return emit(validate(directory))
        if args.command == "next-step":
            return emit({"valid": True, "next_step": step_payload_summary(current_step(state)),
                         "instruction": "submit one or more JSON blocks; do not format Markdown manually"})
        payload_path = Path(args.payload)
        payload = json.loads(payload_path.read_text(encoding="utf-8") if payload_path.exists() else args.payload)
        if args.command == "template":
            template = payload.get("content") if isinstance(payload, dict) else str(payload)
            if "content" not in payload:
                raise ValueError("template payload requires content")
            if "---" not in template:
                raise ValueError("template must include YAML frontmatter delimiters")
            (directory / "doc-templates").mkdir(exist_ok=True)
            target = directory / "doc-templates" / TEMPLATE_NAME
            target.write_text(template.rstrip() + "\n", encoding="utf-8")
            return emit({"valid": validate(directory)["valid"], "action": "template", "template": str(target)})
        step = current_step(state)
        if step.get("step_id") == "complete":
            raise ValueError("document generation is complete; no further update is accepted")
        if isinstance(payload, dict) and "step_id" in payload and payload["step_id"] != step.get("step_id"):
            raise ValueError(f"payload step_id {payload['step_id']} does not match current step {step.get('step_id')}")
        blocks = payload if isinstance(payload, list) else payload.get("blocks", [payload])
        by_id = {block["id"]: block for block in state.get("blocks", [])}
        allowed_blocks = set(step.get("allowed_blocks", []))
        for block in blocks:
            if "id" not in block:
                raise ValueError("update payload requires block id")
            if allowed_blocks and block.get("type") not in allowed_blocks:
                raise ValueError(f"block type {block.get('type')} is not allowed in step {step.get('step_id')}")
            validate_block_schema(block, step.get("schema", {}))
            by_id[block["id"]] = block
        state["blocks"] = list(by_id.values())
        next_step = payload.get("next_step") if isinstance(payload, dict) else None
        if next_step is None:
            next_step = step.get("next_step", "complete")
        advance_step(state, next_step)
        state["metadata"]["last-update"] = date.today().isoformat()
        save_state(directory, state)
        (directory / state.get("document_name", DOC_NAME)).write_text(render_document(state), encoding="utf-8")
        result = validate(directory)
        result["action"] = args.command
        return emit(result)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        return emit({"valid": False, "errors": [str(exc)]})


if __name__ == "__main__":
    sys.exit(main())

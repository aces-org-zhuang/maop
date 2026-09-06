#!/usr/bin/env python3
# Ticket Template IPO

import argparse
from datetime import datetime
from pathlib import Path
import re

TICKET_MGMT_DIR = Path("E:/clawspace/skills/ticket-management")
SCRIPT_DIR = Path(__file__).parent


def _ipo_template(name, name_upper, updated):
    lines = [
        f"# {name_upper} Ticket Template - IPO Structure v1.0",
        "",
        "## Ticket Objective",
        f"**Objective**: Complete {name} related business work",
        "",
        "## Input",
        "- **Source**: Upstream ticket({{upstream_ticket_name}}) or user input",
        "- **Content**: Requirements docs, config info, business data",
        "- **Trigger**: Upstream ticket completed or business request received",
        "",
        "## Process",
        f"### Task 1: {name} Core Processing",
        "- [ ] **Skill 1** - Complete core business processing",
        "- [ ] **Skill 2** - Complete quality validation",
        "",
        "### Task 2: Result Summary",
        "- [ ] **Skill 3** - Summarize processing results",
        "- [ ] **Skill 4** - Generate business report",
        "",
        "### Task xx: Create Downstream Ticket",
        "- [ ] **ticket-management skill**: Create downstream ticket({{downstream_ticket_name}})",
        "",
        "## Output",
        "- **Content**: Business results, quality reports, statistics",
        "- **Downstream**: Auto-create downstream ticket({{downstream_ticket_name}})",
        "- **Trigger**: Processing completed, quality meets standards",
        "",
        "## Placeholder Variables",
        "- `{{input_ticket_id}}` - Upstream ticket ID",
        "- `{{output_ticket_id}}` - Downstream ticket ID",
        "- `{{creation_time}}` - Creation time",
        "- `{{last_updated}}` - Last update time",
        "- `{{execute_name}}` - This execution ticket title",
        "- `{{upstream_ticket_name}}` - Upstream ticket type",
        "- `{{downstream_ticket_name}}` - Downstream ticket type",
        "",
        "## Directory Structure",
        "```",
        f".aces/tickets/{name}/{{{{execute_name}}}}/",
        "+-- input/          # Input files directory",
        "|    +-- user_input.md",
        "+-- output/         # Output files directory",
        "|    +-- result.md",
        "|    +-- report.md",
        "+-- trace.md        # Execution trace file",
        "```",
        "",
        "---",
        "",
        f"*Template version: v1.0 (IPO Structure)*",
        f"*Updated: {updated}*",
        f"*Design pattern: IPO (Input->Process->Output)*",
        f"*Ticket type: {name}*",
    ]
    return "\n".join(lines)


class TicketTemplateIPO:
    def __init__(self):
        self.ticket_mgmt_skill = TICKET_MGMT_DIR / "SKILL.md"
        self.ticket_mgmt_templates = TICKET_MGMT_DIR / "templates"
        self.standard_types = [
            "research",
            "selection",
            "poc",
            "dev",
            "acceptance",

            "software_build",
            "image_build",
            "deployment",
        ]

    def create_type(self, type_name, type_description):
        if not self._validate_type_name(type_name):
            return False
        if self._type_exists(type_name):
            print(f"Error: Type '{type_name}' already exists")
            return False
        if self._register_type_in_skill(type_name, type_description):
            print(f"Success: Registered new ticket type '{type_name}'")
            return True
        print(f"Error: Failed to register type '{type_name}'")
        return False

    def create_template(self, type_name):
        if not self._type_exists(type_name):
            print(f"Error: Type '{type_name}' not registered.")
            return False
        template_filename = f"{type_name}_template_workflow_ipo.md"
        template_path = self.ticket_mgmt_templates / template_filename
        if template_path.exists():
            print(f"Error: Template file already exists: {template_filename}")
            return False
        template_content = self._generate_ipo_template(type_name)
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template_content)
        print(f"Success: Created IPO template file: {template_path}")
        return True

    def list_types(self):
        types = self._get_all_types()
        if not types:
            print("No ticket types found")
            return
        print("Available ticket types:")
        print("=" * 60)
        for type_name, description in types.items():
            marker = "*" if type_name in self.standard_types else "+"
            print(f"\n{marker} {type_name}")
            print(f"   Description: {description}")
            template_file = (
                self.ticket_mgmt_templates / f"{type_name}_template_workflow_ipo.md"
            )
            print(f"   Template: {'Exists' if template_file.exists() else 'Missing'}")
        print("\n" + "=" * 60)
        print(f"Total: {len(types)} types (*=standard, +=custom)")

    def _validate_type_name(self, type_name):
        if not type_name:
            print("Error: Type name cannot be empty")
            return False
        if not type_name.replace("-", "").replace("_", "").isalnum():
            print(
                "Error: Type name can only contain letters, numbers, hyphens and underscores"
            )
            return False
        return True

    def _type_exists(self, type_name):
        return type_name in self._get_all_types()

    def _get_all_types(self):
        if not self.ticket_mgmt_skill.exists():
            return {}
        try:
            with open(self.ticket_mgmt_skill, "r", encoding="utf-8") as f:
                content = f.read()
            types = {}
            for std_type in self.standard_types:
                types[std_type] = f"Standard {std_type} type"
            type_pattern = r"-\s+\*\*([^*]+)\*\*\s*-\s*([^\n]+)"
            for type_name, description in re.findall(type_pattern, content):
                types[type_name.strip()] = description.strip()
            return types
        except ValueError as e:
            print(f"Error reading SKILL.md: {e}")
            return {}

    def _register_type_in_skill(self, type_name, description):
        try:
            with open(self.ticket_mgmt_skill, "r", encoding="utf-8") as f:
                content = f.read()
            new_type_entry = f"\n- **{type_name}** - {description}"
            type_section_pattern = r"(## Ticket Types[^\n]*(?:\n(?!## ).*)*)"
            match = re.search(type_section_pattern, content)
            if match:
                insert_pos = match.end()
                new_content = (
                    content[:insert_pos] + new_type_entry + content[insert_pos:]
                )
            else:
                new_content = (
                    content
                    + f"\n\n## Ticket Types\n\n- **{type_name}** - {description}"
                )
            with open(self.ticket_mgmt_skill, "w", encoding="utf-8") as f:
                f.write(new_content)
            return True
        except ValueError as e:
            print(f"Error updating SKILL.md: {e}")
            return False

    def _generate_ipo_template(self, type_name):
        return _ipo_template(
            name=type_name,
            name_upper=type_name.upper(),
            updated=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )


def main():
    parser = argparse.ArgumentParser(
        description="Ticket template creation tool - IPO structure"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    create_type_parser = subparsers.add_parser(
        "create-type", help="Create new ticket type"
    )
    create_type_parser.add_argument("type_name", help="Type name")
    create_type_parser.add_argument("type_description", help="Type description")

    create_template_parser = subparsers.add_parser(
        "create-template", help="Create IPO template file"
    )
    create_template_parser.add_argument("type_name", help="Type name")

    subparsers.add_parser("list-types", help="List all ticket types")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    tool = TicketTemplateIPO()
    if args.command == "create-type":
        tool.create_type(args.type_name, args.type_description)
    elif args.command == "create-template":
        tool.create_template(args.type_name)
    elif args.command == "list-types":
        tool.list_types()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

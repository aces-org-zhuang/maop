# IPO Ticket Template - IPO Structure v1.0

## Ticket Objective
**Objective**: Complete ipo related business work

## Input
- **Source**: Upstream ticket({{upstream_ticket_name}}) or user input
- **Content**: Requirements docs, config info, business data
- **Trigger**: Upstream ticket completed or business request received

## Process
### Task 1: ipo Core Processing
- [ ] **Skill 1** - Complete core business processing
- [ ] **Skill 2** - Complete quality validation

### Task 2: Result Summary
- [ ] **Skill 3** - Summarize processing results
- [ ] **Skill 4** - Generate business report

### Task xx: Create Downstream Ticket
- [ ] **ticket-management skill**: Create downstream ticket({{downstream_ticket_name}})

## Output
- **Content**: Business results, quality reports, statistics
- **Downstream**: Auto-create downstream ticket({{downstream_ticket_name}})
- **Trigger**: Processing completed, quality meets standards

## Placeholder Variables
- `{{input_ticket_id}}` - Upstream ticket ID
- `{{output_ticket_id}}` - Downstream ticket ID
- `{{creation_time}}` - Creation time
- `{{last_updated}}` - Last update time
- `{{execute_name}}` - This execution ticket title
- `{{upstream_ticket_name}}` - Upstream ticket type
- `{{downstream_ticket_name}}` - Downstream ticket type

## Directory Structure
```
.aces/tickets/ipo/{{execute_name}}/
+-- input/          # Input files directory
|    +-- user_input.md
+-- output/         # Output files directory
|    +-- result.md
|    +-- report.md
+-- trace.md        # Execution trace file
```

---

*Template version: v1.0 (IPO Structure)*
*Updated: 2026-04-13 08:23*
*Design pattern: IPO (Input->Process->Output)*
*Ticket type: ipo*
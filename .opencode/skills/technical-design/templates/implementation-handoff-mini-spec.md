# Implementation Handoff Mini-Spec

## Scope

- In scope:
- Out of scope:
- Confirmed assumptions:
- Blocked or external unknowns:

## Module Change Map

| Module / File Area | Owner | Change Type | Notes |
| --- | --- | --- | --- |
| | | add / modify / remove / config / test | |

## Source Map Lens

| Source Path | Owner / Module | Entrypoint | Test or Config Path | Evidence Type | Confidence | Gap |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | code / docs / command / user-confirmed / external / subagent | % | |

## API / Contract Map

| Contract | Producer | Consumer | Change | Compatibility |
| --- | --- | --- | --- | --- |
| | | | add / modify / remove | compatible / breaking / unknown |

## State and Data Map

| State / Data | Source of Truth | Lifecycle | Migration / Backfill | Failure Mode |
| --- | --- | --- | --- | --- |
| | | | | |

## Interface / State Lens

| Contract or State | Producer | Consumer | Source of Truth | Lifecycle or Sequence | Compatibility | Failure Mode | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | compatible / breaking / unknown | | % |

## Option / Risk Lens

| Option | Decision | Accepted Reason | Rejected Reason | Risk | Mitigation | Fallback Only If | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | recommended / rejected / fallback | | | | | | % |

## Implementation Slices

| Slice | Goal | Target Modules | API / State Impact | Verification |
| --- | --- | --- | --- | --- |
| | | | | |

## Test and Verification Entry Points

| Layer | Command / Method | Expected Evidence | Required Before Merge |
| --- | --- | --- | --- |
| unit | | | yes / no |
| integration | | | yes / no |
| e2e / manual | | | yes / no |
| build / lint / typecheck | | | yes / no |

## Verification Lens

| Claim or Risk | Verification Method | Command or Manual Entry | Expected Evidence | Required Before Implementation | Gap | Confidence |
| --- | --- | --- | --- | --- | --- | --- |
| | test / build / static check / manual / probe / research | | | yes / no | | % |

## External Unknowns

| Unknown | Why It Matters | Required Evidence | Fallback |
| --- | --- | --- | --- |
| | | | |

## Handoff Decision

- Ready for `implementation-delivery`: yes / no
- Delegation Quality Gate passed: yes / no
- Blocking gaps:
- First implementation slice:

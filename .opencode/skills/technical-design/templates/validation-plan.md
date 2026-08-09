# 90% Confidence Evidence Map

| Design Claim / Risk | Confidence | Evidence Source | Verification Method | Required Before Implementation | Gap / Fallback |
| --- | --- | --- | --- | --- | --- |
| | % | code / docs / command / user-confirmed / external | test / build / static check / manual / probe / research | yes / no | |

## Lens Evidence Fields

| Lens | Field | Evidence Required | Ready Rule |
| --- | --- | --- | --- |
| Source Map | source_path / owner/module / entrypoint / test_or_config_path | code, docs, command output, user confirmation, external evidence or subagent return | all implementation-touched paths identified or gap marked RED |
| Interface/State | contract_or_state / producer / consumer / source_of_truth / lifecycle_or_sequence | contract, schema, code path, state diagram, test or user-confirmed behavior | owner and source of truth known before handoff |
| Option/Risk | option / decision / accepted_reason / rejected_reason / risk / mitigation | option matrix, reasoning-map, code constraint, dependency evidence or review finding | fallback is not primary and has explicit trigger |
| Verification | claim_or_risk / verification_method / command_or_manual_entry / expected_evidence | runnable command, manual procedure, static check, probe, research evidence or documented gap | required checks known before implementation starts |

## Rules

- Key architecture, API, state, module boundary, dependency and validation claims require >=90% confidence before implementation handoff.
- Claims below 90% must be marked provisional with a concrete evidence gap and fallback.
- Subagent output only counts as evidence after its lens fields are absorbed into the map with source and confidence.
- Fallback is only a contingency for evidence gaps or primary-path failure; do not present fallback as the default implementation plan.
- Do not treat unverified external service behavior, undocumented APIs, guessed commands, or unknown environment variables as confirmed evidence.

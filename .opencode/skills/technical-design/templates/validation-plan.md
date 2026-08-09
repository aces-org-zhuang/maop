# 90% Confidence Evidence Map

| Design Claim / Risk | Confidence | Evidence Source | Verification Method | Required Before Implementation | Gap / Fallback |
| --- | --- | --- | --- | --- | --- |
| | % | code / docs / command / user-confirmed / external | test / build / static check / manual / probe / research | yes / no | |

## Rules

- Key architecture, API, state, module boundary, dependency and validation claims require >=90% confidence before implementation handoff.
- Claims below 90% must be marked provisional with a concrete evidence gap and fallback.
- Do not treat unverified external service behavior, undocumented APIs, guessed commands, or unknown environment variables as confirmed evidence.

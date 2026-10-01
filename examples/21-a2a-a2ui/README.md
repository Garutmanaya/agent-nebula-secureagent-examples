# 11 - A2A + A2UI v1.0 Acceptance

This example verifies the complete SecureAgent forward path for A2A skill selection and A2UI v1.0 output. It is an executable acceptance scenario for the functionality introduced before Step 1F; it does not implement A2UI transport or wire behavior in the example.

The server advertises two skills. `summary` returns an ordinary structured A2A result. `forecast` returns a `SkillResult` containing business data, result metadata, and an A2UI surface. Platform maps the surface to a separate A2A DataPart identified by `application/a2ui+json`.

```text
SecureAgent client
    -> A2A skill selection + A2UI negotiation
    -> SecureAgent server
    -> forecast
    -> SkillResult(data, metadata, ui)
    -> Platform A2A result mapping
    -> business DataPart + A2UI DataPart
    -> client verification
```

A2UI configuration remains independent in `config/a2ui.conf`; it is not embedded in `config/a2aserver.conf` or `config/a2aclient.conf`.

## Run

```bash
make init example-11
make run example-11 server
```

In another terminal:

```bash
make run example-11 client
```

Expected client result:

```text
PASS  Agent Card advertises forecast + summary and A2UI v1.0
PASS  forecast returned business data + metadata + A2UI DataPart
PASS  summary remains an ordinary non-A2UI A2A result
RESULT: A2A + A2UI v1.0 acceptance verification passed
```

The client uses only the SecureAgent public boundary. It inspects normalized response dictionaries and does not import official A2A wire models or Platform internals.

# Adding an example

Create a numbered directory under `examples/`. Keep application imports at the SecureAgent boundary and place checked-in `.conf` templates under that example's `config/` directory. Do not add an example-local Makefile, certificate-generation script, run script, or cleanup script.

Add one entry to `examples.json` with:

- `directory`: source directory relative to the repository root.
- `name`: user-facing example name.
- `description`: concise statement of what the example demonstrates.
- `init_mode`: shared environment initialization mode.
- `processes`: runnable process name to Python entry-point mapping.

The description is displayed by `make init` and `make run` and by `make list`, so it should describe the capability being demonstrated rather than implementation trivia.

Use the shared lifecycle:

```bash
make env-init
make init example-NN
make run example-NN server
make run example-NN client
make clean example-NN
```

Do not copy filesystem, TLS, secret provisioning, configuration rendering, or process-launch logic into an individual example. Extend the shared lifecycle only when a genuinely new initialization capability is required. Document the example in its README and the root example index.

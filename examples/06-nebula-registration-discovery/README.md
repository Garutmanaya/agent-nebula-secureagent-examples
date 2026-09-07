# 06 — Agent Nebula Registration & Discovery

This is the first example that crosses the boundary from standalone A2A into the Agent Nebula enterprise trust domain.

[agentnebula.ai](https://agentnebula.ai/) provides the **Registry** used to establish publisher/provider ownership, register Agent Cards and capabilities, and discover agents. Later examples add Agent Nebula **OAuth** and **Policy** enforcement. A2A remains the agent-to-agent protocol; Agent Nebula supplies enterprise identity, trust, discovery, authorization, and lifecycle controls around it.

Unlike Examples 01–05, Example 06 does **not** create a self-signed/local-CA server certificate. The agent creates its private key and CSR locally. The CSR is submitted to Agent Nebula under the Provider account, and Agent Nebula supplies the signed certificate and trust bundle. The private key never leaves the agent host.

## 1. Create the Publisher account

Open the Agent Nebula **Identity & Trust** page. Under **Create account**, enter the publisher email, publisher name, and password, then complete the OTP registration flow.

![Create Agent Nebula Publisher account](../../docs/images/06-nebula-registration-discovery/01-create-publisher.png)

After account creation, sign in with the publisher account.

![Sign in to Agent Nebula](../../docs/images/06-nebula-registration-discovery/02-sign-in.png)

## 2. Create a Provider

Open **Providers** in the publisher workspace and select **Create Provider**.

![Provider workspace](../../docs/images/06-nebula-registration-discovery/03-provider-workspace.png)

Enter a provider name, slug, and URL. The Provider is the organizational boundary that owns the example agent, credentials, OAuth configuration, certificates, trust, and policy.

![Create Provider](../../docs/images/06-nebula-registration-discovery/04-create-provider.png)

After creation, open the Provider workspace.

![Provider created](../../docs/images/06-nebula-registration-discovery/05-provider-created.png)

## 3. Generate the agent private key and CSR

From this example directory run:

```bash
make init
```

`make init` now generates only the agent's TLS private key and CSR:

```text
.runtime/
├── certs/
│   └── server.csr
├── secrets/
│   └── server.key
└── trust/
```

Inspect/copy the CSR with:

```bash
cat .runtime/certs/server.csr
```

Do **not** upload `.runtime/secrets/server.key`. The private key must remain on the agent host.

The generated development CSR contains `localhost` and `127.0.0.1` SANs because this example advertises `https://localhost:9006/`. For a remotely reachable deployment, generate the CSR for the hostname/IP actually advertised by the Agent Card.

## 4. Submit the CSR and obtain Agent Nebula trust

Open the Provider and select **Certificates**. Paste the complete contents of `.runtime/certs/server.csr` into **Certificate signing request** and submit it.

Use **Download Agent Nebula trust root** to obtain the Agent Nebula trust bundle.

![Submit CSR and download Agent Nebula trust](../../docs/images/06-nebula-registration-discovery/06-certificates.png)

After the CSR is approved/issued, download the resulting public server certificate. Install the two public trust artifacts as:

```text
.runtime/certs/server.crt
.runtime/trust/agent-nebula-ca.crt
```

The final TLS layout is:

```text
.runtime/
├── certs/
│   ├── server.csr
│   └── server.crt
├── secrets/
│   └── server.key
└── trust/
    └── agent-nebula-ca.crt
```

`a2aserver.conf`, `a2aclient.conf`, and `nebula.conf` are already configured to use these managed runtime paths.

## 5. Generate the onboarding API key

In the same Provider workspace, open **Credentials** and create an API key with the permissions required to onboard/register this agent. Store the returned secret locally as:

```text
.runtime/secrets/onboarding-api-key
```

Protect it as a secret:

```bash
chmod 600 .runtime/secrets/onboarding-api-key
```

Alternatively, rerun initialization with the API key in the environment:

```bash
export NEBULA_ONBOARDING_API_KEY='...'
make init
unset NEBULA_ONBOARDING_API_KEY
```

The initializer writes the value into `.runtime/secrets/onboarding-api-key`; it does not place the API key in a configuration file.

## 6. Verify configuration before starting

The example expects these four files:

```text
.runtime/certs/server.crt
.runtime/secrets/server.key
.runtime/trust/agent-nebula-ca.crt
.runtime/secrets/onboarding-api-key
```

The default Registry URL is `https://localhost:8000`. Update `nebula.conf` if Agent Nebula is running elsewhere. The Registry must also be able to reach the Agent Card URL advertised by `a2aserver.conf`.

## 7. Run the registration/discovery acceptance test

Start the provider:

```bash
make run server
```

The server should start over HTTPS and register its Agent Card/capabilities with Agent Nebula using the onboarding API key.

In another terminal run:

```bash
make run client
```

The client must discover the provider through Agent Nebula Registry by capability and then invoke all three A2A skills (`hello`, `echo`, and `add`). It must not depend on a hard-coded provider URL for discovery.

## Trust relationship established by this example

```text
Agent host                           Agent Nebula
──────────                           ────────────
Generate private key
Generate CSR  ─────────────────────► Provider / Certificates
                                     Sign certificate
             ◄───────────────────── Signed certificate
             ◄───────────────────── Trust bundle

Install certificate
Keep private key local
Install trust bundle
Install onboarding API key
        │
        └──────── HTTPS + trusted registration ────────► Registry
```

Example 06 is successful only when certificate trust, authenticated registration, Registry discovery, and subsequent A2A skill invocation all work together.

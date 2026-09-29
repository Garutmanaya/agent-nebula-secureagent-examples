#!/usr/bin/env python3
"""External lifecycle for Agent Nebula SecureAgent examples."""
from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MANIFEST = REPO / "examples.json"
DEFAULT_ROOT = Path("/opt/agent-nebula/examples")
ROOT_ENV = "AGENT_NEBULA_EXAMPLES_ROOT"


def external_root() -> Path:
    return Path(os.environ.get(ROOT_ENV, str(DEFAULT_ROOT))).expanduser().resolve()


def catalog() -> dict:
    return json.loads(MANIFEST.read_text())


def entry(example_id: str) -> dict:
    try:
        return catalog()[example_id]
    except KeyError:
        raise SystemExit(f"Unknown example: {example_id}. Run 'make list'.")


def paths(example_id: str) -> dict[str, Path]:
    root = external_root()
    runtime = root / "runtime" / example_id
    return {
        "root": root,
        "runtime": runtime,
        "config": runtime / "config",
        "data": runtime / "data",
        "logs": runtime / "logs",
        "tmp": runtime / "tmp",
        "shared_certs": root / "certs",
        "shared_secrets": root / "secrets",
        "certs": runtime / "certs",
        "secrets": runtime / "secrets",
    }


def banner(example_id: str, process: str | None = None) -> None:
    item = entry(example_id)
    width = 78
    print("#" + "-" * width + "#")
    print(f"# Name         : {item['name']}")
    print(f"# Directory    : {item['directory']}")
    print(f"# Demonstrates : {item['description']}")
    if process:
        print(f"# Process      : {process}")
    print("#" + "-" * width + "#")


def env_init() -> None:
    root = external_root()
    for name in ("certs", "config", "data", "logs", "secrets", "tmp", "runtime"):
        (root / name).mkdir(parents=True, exist_ok=True)
    (root / "secrets").chmod(0o700)
    print(f"External examples environment: {root}")


def require(command: str) -> None:
    if shutil.which(command) is None:
        raise SystemExit(f"Required command not found: {command}")


def run_checked(*args: str) -> None:
    subprocess.run(args, check=True)


def private_key(path: Path, *, ec: bool = False) -> None:
    require("openssl")
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if ec:
        run_checked("openssl", "genpkey", "-algorithm", "EC", "-pkeyopt", "ec_paramgen_curve:P-256", "-out", str(path))
    else:
        run_checked("openssl", "genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:3072", "-out", str(path))
    path.chmod(0o600)


def pki_init() -> None:
    """Create one shared development PKI used by every TLS example."""
    env_init()
    require("openssl")
    root = external_root()
    certs = root / "certs"
    ca_key = certs / "ca.key"
    ca_cert = certs / "ca.crt"
    server_key = certs / "server.key"
    server_cert = certs / "server.crt"
    client_key = certs / "client.key"
    client_cert = certs / "client.crt"
    trust_bundle = certs / "trust-bundle.pem"
    host = os.environ.get("AGENT_NEBULA_EXAMPLE_HOSTNAME", socket.gethostname())
    sans = "DNS:localhost,IP:127.0.0.1" if host == "localhost" else f"DNS:{host},DNS:localhost,IP:127.0.0.1"

    if not ca_key.exists() or not ca_cert.exists():
        run_checked("openssl", "req", "-x509", "-newkey", "rsa:3072", "-sha256", "-days", "365", "-nodes", "-subj", "/CN=Agent Nebula Examples Local CA", "-keyout", str(ca_key), "-out", str(ca_cert))
        ca_key.chmod(0o600)

    def signed_identity(name: str, key: Path, cert: Path, eku: str, san: str) -> None:
        if key.exists() and cert.exists():
            return
        private_key(key)
        csr = root / "tmp" / f"{name}.csr"
        ext = root / "tmp" / f"{name}.ext"
        run_checked("openssl", "req", "-new", "-sha256", "-key", str(key), "-subj", f"/CN={name}/O=Agent Nebula Examples", "-addext", f"subjectAltName={san}", "-out", str(csr))
        ext.write_text(f"subjectAltName={san}\nextendedKeyUsage={eku}\n")
        run_checked("openssl", "x509", "-req", "-sha256", "-days", "365", "-in", str(csr), "-CA", str(ca_cert), "-CAkey", str(ca_key), "-CAcreateserial", "-extfile", str(ext), "-out", str(cert))

    signed_identity("server", server_key, server_cert, "serverAuth", sans)
    signed_identity("client", client_key, client_cert, "clientAuth", "DNS:client")
    shutil.copy2(ca_cert, trust_bundle)
    print(f"Shared PKI: {certs}")


def secrets_init() -> None:
    """Create/provision shared non-PKI secrets used by secured examples."""
    env_init()
    secrets = external_root() / "secrets"
    private_key(secrets / "oauth-auth.key", ec=True)
    private_key(secrets / "dpop.key", ec=True)
    provision_env_secret("NEBULA_ONBOARDING_API_KEY", secrets / "onboarding-api-key")
    provision_env_secret("NEBULA_OAUTH_CLIENT_ID", secrets / "oauth-client-id")
    print(f"Shared secrets: {secrets}")


def provision_env_secret(env_name: str, target: Path) -> None:
    value = os.environ.get(env_name)
    if value:
        target.write_text(value)
        target.chmod(0o600)


def rewrite_config(text: str, p: dict[str, Path]) -> str:
    replacements = {
        ".runtime/trust/agent-nebula-ca.crt": str(p["certs"] / "agent-nebula-ca.crt"),
        ".runtime/trust/local-ca.crt": str(p["certs"] / "trust-bundle.pem"),
        "trust/agent-nebula-ca.crt": str(p["certs"] / "agent-nebula-ca.crt"),
        "certs/agent-nebula-ca.crt": str(p["certs"] / "agent-nebula-ca.crt"),
        "trust/local-ca.crt": str(p["certs"] / "trust-bundle.pem"),
        "certs/trust-bundle.pem": str(p["certs"] / "trust-bundle.pem"),
        ".runtime/certs/server.crt": str(p["certs"] / "server.crt"),
        "certs/server.crt": str(p["certs"] / "server.crt"),
        "certs/client.crt": str(p["certs"] / "client.crt"),
        ".runtime/secrets/server.key": str(p["certs"] / "server.key"),
        "secrets/server.key": str(p["certs"] / "server.key"),
        "certs/server.key": str(p["certs"] / "server.key"),
        "certs/client.key": str(p["certs"] / "client.key"),
        ".runtime/secrets/onboarding-api-key": str(p["secrets"] / "onboarding-api-key"),
        "secrets/onboarding-api-key": str(p["secrets"] / "onboarding-api-key"),
        ".runtime/secrets/oauth-client-id": str(p["secrets"] / "oauth-client-id"),
        "secrets/oauth-client-id": str(p["secrets"] / "oauth-client-id"),
        ".runtime/secrets/oauth-auth.key": str(p["secrets"] / "oauth-auth.key"),
        "secrets/oauth-auth.key": str(p["secrets"] / "oauth-auth.key"),
        ".runtime/secrets/dpop.key": str(p["secrets"] / "dpop.key"),
        "secrets/dpop.key": str(p["secrets"] / "dpop.key"),
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    lines=[]
    for line in text.splitlines():
        key=line.split("=",1)[0].strip() if "=" in line else ""
        if key == "product_root": line=f"product_root = {p['data']}"
        elif key == "runtime_root": line=f"runtime_root = {p['runtime']}"
        lines.append(line)
    return "\n".join(lines)+"\n"


def init_one(example_id: str) -> None:
    item=entry(example_id); p=paths(example_id); env_init(); banner(example_id)
    if p["runtime"].exists():
        shutil.rmtree(p["runtime"])
    for key in ("config", "data", "logs", "tmp", "certs", "secrets"):
        p[key].mkdir(parents=True, exist_ok=True)
    p["secrets"].chmod(0o700)
    # Every runtime gets a private snapshot of the shared environment material.
    for source_dir, target_dir in ((p["shared_certs"], p["certs"]), (p["shared_secrets"], p["secrets"])):
        if source_dir.exists():
            shutil.copytree(source_dir, target_dir, dirs_exist_ok=True)
    source=REPO/item["directory"]/"config"
    if source.exists():
        for cfg in source.glob("*.conf"):
            (p["config"]/cfg.name).write_text(rewrite_config(cfg.read_text(),p))
    mode=item.get("init_mode","basic")
    if mode in {"tls", "oauth-nebula", "nebula"} and not (p["certs"] / "server.crt").exists():
        raise SystemExit("Shared PKI is missing. Run: make pki-init")
    if mode in {"nebula-csr", "oauth-nebula", "nebula"} and not (p["secrets"] / "onboarding-api-key").exists():
        print("WARNING: onboarding-api-key is not present in shared secrets.")
    if mode == "oauth-nebula" and not (p["secrets"] / "oauth-auth.key").exists():
        raise SystemExit("Shared OAuth secrets are missing. Run: make secrets-init")
    if mode == "planned":
        print("This example is reserved and has no runnable process yet.")
    print(f"Runtime: {p['runtime']}")
    print(f"Config : {p['config']}")


def init_examples(selector: str) -> None:
    if selector == "all":
        for example_id in catalog(): init_one(example_id)
    else: init_one(selector)


def clean_one(example_id: str) -> None:
    entry(example_id); banner(example_id); p=paths(example_id)
    shutil.rmtree(p["runtime"],ignore_errors=True)
    print(f"Removed runtime: {p['runtime']}")
    print("Shared certs and secrets were preserved.")


def clean_examples(selector: str) -> None:
    if selector == "all":
        for example_id in catalog(): clean_one(example_id)
    else: clean_one(selector)


def run_example(example_id: str, process: str) -> None:
    item=entry(example_id); banner(example_id,process)
    try: script=item["processes"][process]
    except KeyError: raise SystemExit(f"Unknown process '{process}' for {example_id}. Available: {', '.join(item['processes']) or 'none'}")
    p=paths(example_id)
    if not p["config"].is_dir(): raise SystemExit(f"Example is not initialized. Run: make init {example_id}")
    env=os.environ.copy(); env["AGENT_NEBULA_EXAMPLE_CONFIG_DIR"]=str(p["config"])
    env["PYTHONPATH"]=str(REPO)+(os.pathsep+env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    os.execvpe("uv",["uv","run","python",str(REPO/item["directory"]/script)],env)


def list_examples() -> None:
    for example_id,item in catalog().items():
        print(f"{example_id:10}  {item['name']}")
        print(f"{'':12}{item['description']}")


def main() -> None:
    if len(sys.argv)<2: raise SystemExit("Usage: example-lifecycle.py <list|env-init|pki-init|secrets-init|init|run|clean> ...")
    command=sys.argv[1]
    if command=="list": list_examples()
    elif command=="env-init": env_init()
    elif command=="pki-init": pki_init()
    elif command=="secrets-init": secrets_init()
    elif command=="init" and len(sys.argv)==3: init_examples(sys.argv[2])
    elif command=="clean" and len(sys.argv)==3: clean_examples(sys.argv[2])
    elif command=="run" and len(sys.argv)==4: run_example(sys.argv[2],sys.argv[3])
    else: raise SystemExit("Invalid lifecycle command. Run 'make help'.")

if __name__=="__main__": main()

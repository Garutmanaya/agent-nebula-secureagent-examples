#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
A2UI_SOURCE="${AGENT_NEBULA_A2UI_SOURCE:-${REPO_ROOT}/../agent-nebula-a2ui}"
WEB_ROOT="${REPO_ROOT}/examples/common/a2ui-web"
PACKAGE_ROOT="${WEB_ROOT}/packages"

WEB_CORE="a2ui-web_core-0.10.7.tgz"
RICH_CATALOG="agent-nebula-a2ui-rich-1.0.0.tgz"

for package in "${WEB_CORE}" "${RICH_CATALOG}"; do
    if [[ ! -f "${A2UI_SOURCE}/${package}" ]]; then
        echo "Missing A2UI package: ${A2UI_SOURCE}/${package}" >&2
        echo "Set AGENT_NEBULA_A2UI_SOURCE to the agent-nebula-a2ui directory." >&2
        exit 2
    fi
done

mkdir -p "${PACKAGE_ROOT}"
cp "${A2UI_SOURCE}/${WEB_CORE}" "${PACKAGE_ROOT}/${WEB_CORE}"
cp "${A2UI_SOURCE}/${RICH_CATALOG}" "${PACKAGE_ROOT}/${RICH_CATALOG}"

npm --prefix "${WEB_ROOT}" install
echo "A2UI browser dependencies initialized from: ${A2UI_SOURCE}"

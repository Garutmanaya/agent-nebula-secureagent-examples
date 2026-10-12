#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WEB_ROOT="${REPO_ROOT}/examples/common/a2ui-web"

echo "Initializing A2UI browser dependencies from npm..."
echo "Web root: ${WEB_ROOT}"

rm -rf "${WEB_ROOT}/node_modules"

npm --prefix "${WEB_ROOT}" install

echo "A2UI browser dependencies initialized."
npm --prefix "${WEB_ROOT}" list \
    @a2ui/web_core \
    @agent-nebula-npm/a2ui-rich


#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXPORT_DIR="$ROOT_DIR/exports"
DEFAULT_ARCHIVE_NAME="project-export.zip"

mkdir -p "$EXPORT_DIR"
ARCHIVE_PATH="${1:-$EXPORT_DIR/$DEFAULT_ARCHIVE_NAME}"

pushd "$ROOT_DIR" >/dev/null

echo "Creating archive at $ARCHIVE_PATH"
git archive --format=zip --output="$ARCHIVE_PATH" HEAD

echo "Done. Archive contains the current HEAD snapshot."

popd >/dev/null

#!/usr/bin/env bash
set -euo pipefail

# ------------------------------------------------------------
# ftag development runner
#
# - Self-healing dev-dir/
# - Optional --reset for clean state
# - Enables debug logging
# ------------------------------------------------------------

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEV_DIR="$PROJECT_ROOT/dev-dir"

DEV_CONFIG_DIR="$DEV_DIR/config"
DEV_DB_DIR="$DEV_DIR/db"
DEV_FILES_DIR="$DEV_DIR/test-files"

DEV_DB_PATH="$DEV_DB_DIR/test-db.sqlite3"
DEV_CONFIG_PATH="$DEV_CONFIG_DIR/config.toml"

# ---- Parse flags -------------------------------------------
RESET=0
ARGS=()

for arg in "$@"; do
  case "$arg" in
    --reset)
      RESET=1
      ;;
    *)
      ARGS+=("$arg")
      ;;
  esac
done

# ---- Reset dev-dir if requested -----------------------------
if [ "$RESET" -eq 1 ]; then
  echo "[INFO]: Resetting dev-dir"
  rm -rf "$DEV_DIR"
fi

# ---- Create directory structure -----------------------------
mkdir -p \
  "$DEV_CONFIG_DIR" \
  "$DEV_DB_DIR" \
  "$DEV_FILES_DIR"

# ---- Seed config.toml if missing -----------------------------
if [ ! -f "$DEV_CONFIG_PATH" ]; then
  cat > "$DEV_CONFIG_PATH" <<EOF
# ftag development config

use_absolute_paths = true
db_path = "$DEV_DB_PATH"
verbose = false
debug = false

EOF
  echo "[INFO]: Created dev config: $DEV_CONFIG_PATH"
fi

# ---- Seed test files if missing ------------------------------
touch "$DEV_FILES_DIR/work.txt"
touch "$DEV_FILES_DIR/hobbies.txt"
touch "$DEV_FILES_DIR/shopping-list.txt"

# ---- Load .env (dev-only, optional) --------------------------
if [ -f "$PROJECT_ROOT/.env" ]; then
  set -a
  source "$PROJECT_ROOT/.env"
  set +a
fi

# ---- Dev environment variables ------------------------------
export FTAG_DEBUG="${FTAG_DEBUG:-1}"
export FTAG_CONFIG_DIR="$DEV_CONFIG_DIR"
export FTAG_DB_PATH="$DEV_DB_PATH"

# ---- Info output --------------------------------------------
echo "[STATUS]: Environment ready."
echo "> ftag dev mode"
echo "  - config: $DEV_CONFIG_PATH"
echo "  - db:     $DEV_DB_PATH"
echo "  - files:  $DEV_FILES_DIR"

# ---- Run ftag ------------------------------------------------
# Ensure src/ is in PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT/src:${PYTHONPATH:-}"

# No CLI yet, so just run ftag.cli if no args are given
# exec python -m ftag.cli "${ARGS[@]}"
if [ ${#ARGS[@]} -gt 0 ]; then
  exec python -m ftag.cli "${ARGS[@]}"
else
  exec python -m ftag.cli
fi

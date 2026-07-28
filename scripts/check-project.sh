#!/usr/bin/env sh
set -u

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root"

level=
format=text
template=0

if [ "${TEMPLATE_MODE:-0}" = "1" ]; then
  template=1
fi

usage() {
  cat <<'EOF'
Usage: ./scripts/check-project.sh [niveau] [--format text|json] [--template]

Niveaux :
  bootstrap discovery development release distribution operation

Les régimes exploration, construction, intégration et stabilisation ne sont pas
des niveaux de validation. Le régime de la tranche active est consigné dans
PROJECT_STATE.md.

Sans niveau, le contrôle lit adoption.current_level dans project.adoption.yaml.
--template auto-valide le dépôt modèle ; TEMPLATE_MODE=1 reste compatible.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    bootstrap|discovery|development|release|distribution|operation)
      if [ -n "$level" ]; then
        printf 'ERREUR D’USAGE : plusieurs niveaux fournis.\n' >&2
        exit 2
      fi
      level=$1
      ;;
    --current)
      level=
      ;;
    --template)
      template=1
      ;;
    --format)
      shift
      if [ "$#" -eq 0 ]; then
        printf 'ERREUR D’USAGE : --format attend text ou json.\n' >&2
        exit 2
      fi
      format=$1
      ;;
    --format=*)
      format=${1#--format=}
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'ERREUR D’USAGE : argument inconnu %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

case "$format" in
  text|json) ;;
  *)
    printf 'ERREUR D’USAGE : format inconnu %s\n' "$format" >&2
    exit 2
    ;;
esac

if ! command -v python3 >/dev/null 2>&1; then
  printf 'PYTHON 3 MANQUANT : requis pour une validation complète.\n' >&2
  exit 2
fi

if ! python3 -c 'import jsonschema, yaml' >/dev/null 2>&1; then
  printf '%s\n' \
    'DÉPENDANCES DE VALIDATION MANQUANTES.' \
    'Installer avec :' \
    'python3 -m pip install --requirement scripts/requirements-validation.txt' >&2
  exit 2
fi

set -- scripts/validate-manifest.py
if [ -n "$level" ]; then
  set -- "$@" "$level"
fi
set -- "$@" --format "$format"
if [ "$template" -eq 1 ]; then
  set -- "$@" --template
fi

python3 "$@"
exit $?

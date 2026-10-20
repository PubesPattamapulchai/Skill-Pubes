#!/usr/bin/env bash
# Install all Skill-Pubes skills into a Claude Code skills directory.
#
# Usage:
#   ./install.sh              # copy all skills into ~/.claude/skills (global)
#   ./install.sh --project    # copy all skills into ./.claude/skills (this project only)
#   ./install.sh --link       # symlink instead of copy (global; picks up `git pull` updates)
#   ./install.sh --dest DIR   # install into a custom directory

set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skills_src="$repo_dir/skills"

dest="$HOME/.claude/skills"
mode="copy"

while [ $# -gt 0 ]; do
  case "$1" in
    --project) dest=".claude/skills" ;;
    --link) mode="link" ;;
    --dest) dest="$2"; shift ;;
    -h|--help)
      sed -n '2,9p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
  shift
done

mkdir -p "$dest"

for skill_dir in "$skills_src"/*/; do
  name="$(basename "$skill_dir")"
  target="$dest/$name"

  if [ -e "$target" ] || [ -L "$target" ]; then
    rm -rf "$target"
  fi

  if [ "$mode" = "link" ]; then
    ln -s "$(cd "$skill_dir" && pwd)" "$target"
    echo "linked  $name -> $target"
  else
    cp -r "$skill_dir" "$target"
    echo "copied  $name -> $target"
  fi
done

echo ""
echo "Done. Installed $(ls -1 "$skills_src" | wc -l | tr -d ' ') skills into $dest"

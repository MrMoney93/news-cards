#!/usr/bin/env bash
# Usage: ./publish_card.sh "<headline>" "<category>" "<arabic date>" <YYYY-MM-DD-HHMM>
# Renders a card, pushes it, prints the public raw URL.
set -euo pipefail
cd "$(dirname "$0")"
H="$1"; C="$2"; D="$3"; SLUG="$4"
MONTH="${SLUG:0:7}"; NAME="${SLUG:8}"
mkdir -p "cards/$MONTH"
OUT="cards/$MONTH/$NAME.png"
python3 make_card.py "$H" "$C" "$D" "$OUT"
git add "$OUT"
git -c user.name="news-bot" -c user.email="news-bot@users.noreply.github.com" commit -q -m "card $SLUG"
git fetch -q origin main && git rebase -q origin/main
git push -q origin HEAD:main
echo "https://raw.githubusercontent.com/MrMoney93/news-cards/main/$OUT"

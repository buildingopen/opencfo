#!/bin/bash
# Food Finder — WhatsApp relay script
# Searches Swiggy + Google Maps via Claude Code, sends result to WhatsApp
#
# Usage: /path/to/food-finder.sh "dumplings near koramangala for 3"
#
# Prerequisites:
# - Claude Code CLI installed (`claude`)
# - food-finder skill installed in ~/.claude/skills/food-finder/
# - WhatsApp bot with a `send` command (optional, for WhatsApp relay)

set -euo pipefail

QUERY="${*:-momos near koramangala}"
PHONE="${FOOD_FINDER_PHONE:-}"  # Set your phone number in env, e.g. +1234567890
LOG="${FOOD_FINDER_LOG:-/tmp/food-finder.log}"

echo "[$(date -Is)] Query: $QUERY" >> "$LOG"

# Run Claude Code with the food-finder skill
RESULT=$(claude --print "Use the food-finder skill. Query: $QUERY. Return a concise table of top 3 recommendations with ratings, delivery time, price. No markdown headers, plain text only." 2>>"$LOG")

if [ -z "$RESULT" ]; then
    echo "[$(date -Is)] ERROR: Empty result from Claude" >> "$LOG"
    RESULT="Food finder failed for: $QUERY. Try again later."
fi

echo "[$(date -Is)] Result: ${RESULT:0:200}..." >> "$LOG"

# Print result to stdout
echo "$RESULT"

# Optional: Send to WhatsApp if phone number and bot are configured
if [ -n "$PHONE" ] && command -v clawdbot-ctl &>/dev/null; then
    clawdbot-ctl send --target "$PHONE" --message "$RESULT" 2>>"$LOG"
    echo "[$(date -Is)] Sent to WhatsApp: $PHONE" >> "$LOG"
fi

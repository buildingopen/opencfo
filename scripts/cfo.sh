#!/bin/bash
# cfo -- Chief Food Officer
# Searches delivery apps + Google Maps via Claude Code, outputs recommendation
#
# Usage: ./cfo.sh "momos near koramangala for 3"
#
# Prerequisites:
# - Claude Code CLI installed (`claude`)
# - cfo skill installed in ~/.claude/skills/cfo/

set -euo pipefail

QUERY="${*:-momos near koramangala}"
PHONE="${CFO_PHONE:-}"  # Set your phone number in env for messaging relay
LOG="${CFO_LOG:-/tmp/cfo.log}"

echo "[$(date -Is)] Query: $QUERY" >> "$LOG"

# Run Claude Code with the cfo skill
RESULT=$(claude --print "Use the cfo skill. Query: $QUERY. Return a concise table of top 3 recommendations with ratings, delivery time, price. No markdown headers, plain text only." 2>>"$LOG")

if [ -z "$RESULT" ]; then
    echo "[$(date -Is)] ERROR: Empty result from Claude" >> "$LOG"
    RESULT="cfo failed for: $QUERY. Try again later."
fi

echo "[$(date -Is)] Result: ${RESULT:0:200}..." >> "$LOG"

# Print result to stdout
echo "$RESULT"

# Optional: Send to messaging if phone and bot are configured
if [ -n "$PHONE" ] && command -v clawdbot-ctl &>/dev/null; then
    clawdbot-ctl send --target "$PHONE" --message "$RESULT" 2>>"$LOG"
    echo "[$(date -Is)] Sent to: $PHONE" >> "$LOG"
fi

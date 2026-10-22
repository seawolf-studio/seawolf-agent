#!/usr/bin/env bash
# R3: alternativas para los fallos por entradas obsoletas / descargas
LOG=/c/Users/Admin/intel/instalacion-comunitaria-r3.log
: > "$LOG"
declare -a JOBS=(
  "iron:cold-email-copy"
  "kamish:skills-sh/davepoon/buildwithclaude/bulkpublish-social-scheduling"
  "kamish:skills-sh/postpeer-api/skills/schedule-social-post"
  "kamish:skills-sh/guyaga/claude-code-social-media-skill/social-media-post"
  "tusk:skills-sh/blink-new/claude/seo-article-writing"
  "tusk:skills-sh/coreyhaines31/marketingskills/content-strategy"
  "tusk:skills-sh/luongnv89/skills/seo-ai-optimizer"
  "beru:skills-sh/receiptor-ai/bookkeeping-skills/bookkeeping"
  "tank:skills-sh/aibtcdev/skills/business-dev"
  "igris:skills-sh/anthropics/knowledge-work-plugins/draft-content"
  "igris:skills-sh/anthropics/knowledge-work-plugins/content-creation"
)
OK=0; FAIL=0
for j in "${JOBS[@]}"; do
  s="${j%%:*}"; id="${j#*:}"
  out=$(hermes -p "$s" skills install "$id" -y 2>&1)
  if echo "$out" | grep -q "Installed:"; then OK=$((OK+1)); st="OK"; det=$(echo "$out"|grep -i "Installed:"|head -1)
  else FAIL=$((FAIL+1)); st="FAIL"; det=$(echo "$out"|grep -iE "Error|no longer exist|Could not"|head -1); fi
  printf "%-8s %-5s %-68s %s\n" "$s" "$st" "$id" "$det" >> "$LOG"
done
echo "=== RESUMEN R3: OK=$OK FAIL=$FAIL ===" >> "$LOG"
echo "DONE R3 OK=$OK FAIL=$FAIL"

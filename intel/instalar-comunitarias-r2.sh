#!/usr/bin/env bash
# Reintento de las comunitarias que fallaron por rate-limit (ya con token en cada .env)
LOG=/c/Users/Admin/intel/instalacion-comunitaria-r2.log
: > "$LOG"
declare -a JOBS=(
  "iron:skills-sh/louisblythe/sales-skills/cold-email"
  "iron:skills-sh/louisblythe/sales-skills/email-sequence"
  "tank:skills-sh/dengineproblem/agents-monorepo/sales-development-rep"
  "tank:skills-sh/lagrowthmachine/gtm-system/sales-nav-search-builder"
  "kamish:skills-sh/adithyani/agents/social-media-publishing"
  "kamish:skills-sh/forsvn-labs/meta-skills/publish-social"
  "kamish:skills-sh/reelary/skills/vertical-video"
  "kamish:skills-sh/mmcmedia/openclaw-agents/shorts-creator"
  "kamish:skills-sh/nicepkg/ai-workflow/short-form-converter"
  "tusk:skills-sh/kamskans/seo-content-skill/seo-content"
  "tusk:skills-sh/muvon/octomind-tap/seo-keyword-research"
  "tusk:skills-sh/nikhilbhansali/youtube-data-skills/youtube-title-tag-optimizer"
  "greed:skills-sh/coreyhaines31/marketingskills/prospecting"
  "greed:skills-sh/coreyhaines31/marketingskills/social"
  "beru:skills-sh/mrbridgehq/osint-researcher-claude/osint-researcher"
  "beru:skills-sh/jk-0001/skills/bookkeeping-basics"
  "beru:skills-sh/microck/ordinary-claude-skills/invoice-organizer"
)
OK=0; FAIL=0
for j in "${JOBS[@]}"; do
  s="${j%%:*}"; id="${j#*:}"
  out=$(hermes -p "$s" skills install "$id" -y 2>&1)
  if echo "$out" | grep -q "Installed:"; then OK=$((OK+1)); st="OK"; det=$(echo "$out"|grep -i "Installed:"|head -1)
  else FAIL=$((FAIL+1)); st="FAIL"; det=$(echo "$out"|grep -iE "Error|rate limit"|head -1); fi
  printf "%-8s %-5s %-70s %s\n" "$s" "$st" "$id" "$det" >> "$LOG"
done
echo "=== RESUMEN R2: OK=$OK FAIL=$FAIL ===" >> "$LOG"
echo "DONE R2 OK=$OK FAIL=$FAIL"

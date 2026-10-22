#!/usr/bin/env bash
# Instalación del paquete comunitario (skills-sh) por sombra — con GITHUB_TOKEN ya en .env
LOG=/c/Users/Admin/intel/instalacion-comunitaria.log
: > "$LOG"
declare -a JOBS=(
  "iron:skills-sh/louisblythe/sales-skills/cold-email"
  "iron:skills-sh/louisblythe/sales-skills/email-sequence"
  "iron:skills-sh/louisblythe/sales-skills/outbound-prospecting"
  "igris:skills-sh/louisblythe/sales-skills/copywriting"
  "tank:skills-sh/dengineproblem/agents-monorepo/sales-development-rep"
  "tank:skills-sh/louisblythe/sales-skills/customer-referrals"
  "tank:skills-sh/seb1n/awesome-ai-agent-skills/sales-email-sequences"
  "tank:skills-sh/lagrowthmachine/gtm-system/sales-nav-search-builder"
  "kamish:skills-sh/coreyhaines31/marketingskills/social-content"
  "kamish:skills-sh/adithyani/agents/social-media-publishing"
  "kamish:skills-sh/forsvn-labs/meta-skills/publish-social"
  "kamish:skills-sh/inference-sh/skills/twitter-automation"
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
  line=$(echo "$out" | grep -iE "Installed:|Error|Could not|rate limit" | head -1)
  if echo "$out" | grep -q "Installed:"; then OK=$((OK+1)); st="OK"
  else FAIL=$((FAIL+1)); st="FAIL"; fi
  printf "%-8s %-6s %-72s %s\n" "$s" "$st" "$id" "$line" >> "$LOG"
done
echo "=== RESUMEN: OK=$OK FAIL=$FAIL ===" >> "$LOG"
echo "DONE OK=$OK FAIL=$FAIL"

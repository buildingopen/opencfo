# Food Finder

**An AI agent that searches Swiggy + Google Maps and recommends the best restaurants — from your terminal.**

Built as a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill. It browses Swiggy with a real browser, cross-references Google Maps ratings, learns your preferences, and sends recommendations to WhatsApp.

> "I got mass-paralysis deciding what to order every evening. So I automated the entire food research process."

## What it does

1. **Searches Swiggy** — navigates the real website via browser automation, sets your delivery location, searches for your dish/cuisine, collects the top 10 restaurants with ratings, delivery times, and prices
2. **Cross-references Google Maps** — for the top 5 results, checks Google Maps ratings and review counts
3. **Ranks & recommends** — combines both ratings into a weighted score, presents a clean comparison table
4. **Learns your taste** — saves your cuisine preferences, rating thresholds, budget range, and favorites to a local file that improves recommendations over time
5. **WhatsApp relay** (optional) — sends results to your phone via a wrapper script

### Example output

```
Top momos picks near Koramangala:

| # | Restaurant              | Swiggy | Google (reviews) | Time    | Price |
|---|------------------------|--------|-----------------|---------|-------|
| 1 | Khawa Karpo            | 4.6    | 4.5 (1,737)     | 35-40m  | ₹181  |
| 2 | Darjeeling Momos Taste | 4.6    | —               | 30-35m  | ₹65   |
| 3 | Hot Momo Darjeeling    | 4.4    | 4.4 (287)       | 30-35m  | ₹150  |
| 4 | Prasuma Momo Kitchen   | 4.5    | 3.8 (8)         | 40-45m  | ₹129  |
| 5 | Chinese Wok            | 4.4    | 4.4 (153)       | 15-20m  | ₹199  |

Top pick: Khawa Karpo — highest combined rating, authentic Tibetan, steamed (healthy).
Budget pick: Darjeeling Momos Taste — ₹65 for 8pc chicken steamed. Absurd value.
```

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (CLI)
- A browser with [Playwright MCP](https://github.com/anthropics/anthropic-mcp-playwright) configured — the agent controls a real browser to navigate Swiggy and Google Maps
- Swiggy works without login for browsing (no account needed)
- Google Maps works without login for basic search

## Installation

```bash
# Clone the repo
git clone https://github.com/federicodeponte/food-finder.git

# Copy the skill to your Claude Code skills directory
cp -r food-finder/skill ~/.claude/skills/food-finder
```

That's it. Claude Code auto-discovers skills in `~/.claude/skills/`.

## Usage

### From Claude Code

Just ask naturally:

```
> find me momos near koramangala
> pizza delivery in indiranagar, budget ₹300 per person
> healthy lunch options near hsr layout
> what should I eat for dinner? im near mg road
```

Or use the slash command:

```
> /food-finder biryani near koramangala for 3 people
```

### From the terminal (WhatsApp relay)

If you have a WhatsApp bot set up (e.g., [Baileys](https://github.com/WhiskeySockets/Baileys)):

```bash
# Copy the relay script to your server
scp scripts/food-finder.sh your-server:/root/

# Run it
ssh your-server "/root/food-finder.sh 'dumplings near koramangala for 3'"
# → Result arrives on WhatsApp in ~2 min
```

## How it works

```
User: "find me momos near koramangala"
  │
  ├─ 1. Parse request (dish, location, budget, party size)
  │
  ├─ 2. Read preferences (learned from past searches)
  │
  ├─ 3. Open Swiggy in browser
  │     ├─ Set delivery location
  │     ├─ Search for dish/cuisine
  │     └─ Collect top 10 results (rating, time, price)
  │
  ├─ 4. Open Google Maps in new tab
  │     └─ For top 5: get Google rating + review count
  │
  ├─ 5. Score = (Swiggy × 0.4) + (Google × 0.4) + (reviews × 0.2)
  │
  ├─ 6. Present ranked table with top pick highlighted
  │
  └─ 7. Update preferences file for next time
```

## Preference learning

After each search, the skill updates `references/preferences.md`:

```markdown
## Cuisine Preferences
- Tibetan/Himalayan momos (high preference, last ordered 2026-02-24)
- Pizza (ordered 2026-02-24)

## Rating Threshold
- Prefers 4.4+ on Swiggy, 4.3+ on Google Maps

## Favorites
- Khawa Karpo (Koramangala) — Tibetan, momos

## Order History
| Date       | Restaurant  | Cuisine       | Rating | Notes              |
|------------|------------|---------------|--------|--------------------|
| 2026-02-24 | Khawa Karpo | Tibetan/momos | 4.5    | First tracked order |
```

This builds up over time and influences future recommendations (boosting favorites, flagging below-threshold restaurants).

## Project structure

```
food-finder/
├── skill/                        # The Claude Code skill (copy to ~/.claude/skills/food-finder/)
│   ├── SKILL.md                  # Core instructions + browser workflow
│   ├── references/
│   │   └── preferences.md        # Auto-learned food preferences
│   └── scripts/
│       └── update_prefs.py       # Updates preferences after each search
├── scripts/
│   └── food-finder.sh            # WhatsApp relay script (optional)
└── README.md
```

## Customization

### Different delivery platform

The skill is built for **Swiggy** (India's largest food delivery app). To adapt it for other platforms:

1. Edit `skill/SKILL.md` — change the navigation steps in Step 3 to match your platform's UI
2. The Google Maps cross-referencing (Step 4) works globally

Swiggy was chosen because Zomato blocks datacenter IPs. Swiggy works fine without login.

### Different location

Change the default location in `skill/references/preferences.md`:

```markdown
## Locations
- Your Area, Your City (primary)
```

The skill will use this as the default when no location is specified.

## Limitations

- **Swiggy only** — Zomato blocks non-residential IPs (403). If you're running from a residential IP, you could add Zomato support.
- **India-focused** — Swiggy is India-only. The architecture works for any delivery platform though.
- **Browser required** — needs Playwright MCP with a real browser. Can't run headless-only because Swiggy has bot detection.
- **Not real-time pricing** — prices shown are Swiggy's listed "price for two" or individual item prices, not final cart price with taxes/delivery.

## Why I built this

Every evening in Bangalore, the same ritual:
1. Open Swiggy, scroll through 50 restaurants
2. Open Google Maps to check if the ratings are real
3. Compare delivery times, prices, portions
4. 20 minutes later, still undecided
5. Order from the same place as yesterday

This takes ~2 minutes now and I get a better recommendation than I'd find manually.

## License

MIT

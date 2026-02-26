# Food Finder

**An AI agent that searches delivery apps + Google Maps and recommends the best restaurants from your terminal.**

Built as a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill. It browses delivery platforms with a real browser, cross-references Google Maps ratings, learns your preferences, and picks the best option for you.

<p align="center">
  <img src="demo.gif" alt="Food Finder demo" width="540">
</p>

## What it does

1. **Searches delivery apps** - navigates the real website via browser automation, sets your delivery location, searches for your dish/cuisine, collects the top restaurants with ratings, delivery times, and prices
2. **Cross-references Google Maps** - for the top results, checks Google Maps ratings and review counts
3. **Ranks and recommends** - combines both ratings into a weighted score, presents a clean comparison table
4. **Learns your taste** - saves your cuisine preferences, rating thresholds, budget range, and favorites to a local file that improves recommendations over time

### Example output

```
$ find me ramen near kreuzberg

  #  Restaurant           Wolt  Google      Time  Price
  -  -------------------  ----  ---------  -----  -----
  1  Cocolo Ramen         4.5   4.6 (3.2k)  25m   €13
  2  Hako Ramen           4.4   4.5 (890)   30m   €12
  3  Takumi Nine          4.3   4.4 (1.5k)  35m   €14

  TOP PICK   Cocolo Ramen
  Rich tonkotsu, generous portions. Known favorite.

  BUDGET     Hako Ramen
  €12 for full bowl with extras. Great value.

  HEALTH     Takumi Nine
  Lighter shoyu option. Lists calories (480kcal).

  [+] Preferences updated · Cocolo Ramen boosted
```

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- [Playwright MCP](https://github.com/anthropics/anthropic-mcp-playwright) configured - the agent controls a real browser to navigate delivery apps and Google Maps
- Works on Mac, Linux, or any machine with Chrome/Chromium

## Installation

```bash
git clone https://github.com/federicodeponte/food-finder.git

# Copy the skill to your Claude Code skills directory
cp -r food-finder/skill ~/.claude/skills/food-finder
```

Claude Code auto-discovers skills in `~/.claude/skills/`.

## Usage

Just ask naturally:

```
> find me ramen near kreuzberg
> pizza delivery in mitte, budget €15
> healthy lunch options near friedrichshain
> what should I eat for dinner? im near alexanderplatz
```

Or use the slash command:

```
> /food-finder tacos near williamsburg for 2 people
```

## How it works

```
User: "find me ramen near kreuzberg"
  |
  |-- 1. Parse request (dish, location, budget, party size)
  |
  |-- 2. Read preferences (learned from past searches)
  |
  |-- 3. Open delivery app in browser
  |      |-- Set delivery location
  |      |-- Search for dish/cuisine
  |      +-- Collect top 10 results (rating, time, price)
  |
  |-- 4. Open Google Maps in new tab
  |      +-- For top 5: get Google rating + review count
  |
  |-- 5. Score = (App x 0.4) + (Google x 0.4) + (reviews x 0.2)
  |
  |-- 6. Present ranked table with top pick highlighted
  |
  +-- 7. Update preferences file for next time
```

## Preference learning

After each search, the skill updates `references/preferences.md`:

```markdown
## Cuisine Preferences
- Ramen/Japanese (high preference, last ordered 2026-02-27)
- Pizza (ordered 2026-02-25)

## Rating Threshold
- Prefers 4.3+ on delivery app, 4.3+ on Google Maps

## Favorites
- Cocolo Ramen (Kreuzberg) - Japanese, ramen

## Order History
| Date       | Restaurant   | Cuisine | Rating | Notes              |
|------------|-------------|---------|--------|--------------------|
| 2026-02-27 | Cocolo Ramen | Ramen   | 4.6    | Rich tonkotsu      |
```

This builds up over time and influences future recommendations.

## Supported platforms

The skill uses browser automation, so it works with any delivery platform that has a web UI:

| Platform | Region | Status |
|----------|--------|--------|
| Wolt | EU, Japan, Israel | Tested |
| Swiggy | India | Tested |
| UberEats | Global | Supported |
| Lieferando | Germany, NL | Supported |
| DoorDash | US, CA, AU | Supported |
| Deliveroo | UK, EU | Supported |

To switch platforms, edit `skill/SKILL.md` and update the navigation steps to match your platform's UI. The Google Maps cross-referencing works globally.

## Project structure

```
food-finder/
|-- skill/                        # Claude Code skill (copy to ~/.claude/skills/)
|   |-- SKILL.md                  # Core instructions + browser workflow
|   |-- references/
|   |   +-- preferences.md        # Auto-learned food preferences
|   +-- scripts/
|       +-- update_prefs.py       # Updates preferences after each search
|-- scripts/
|   +-- food-finder.sh            # WhatsApp relay script (optional)
+-- README.md
```

## Limitations

- **Browser required** - needs Playwright MCP with a real browser
- **Not real-time pricing** - prices shown are listed prices, not final cart price with taxes/delivery
- **Some platforms block bots** - works best with platforms that don't require login for browsing

## Why I built this

Every evening, the same ritual:
1. Open the delivery app, scroll through 50 restaurants
2. Open Google Maps to check if the ratings are real
3. Compare delivery times, prices, portions
4. 20 minutes later, still undecided
5. Order from the same place as yesterday

Now it takes 2 minutes and I get a better recommendation than I'd find manually.

## License

MIT

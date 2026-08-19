# Leveling Up: The System

A **Solo Leveling**–inspired, gamified self-improvement tracker built with [Reflex](https://reflex.dev) (pure Python, full-stack web). Turn your daily grind — DSA practice, side projects, fitness, and custom habits — into a hunter's leveling journey: complete quests, earn XP/MP, level up, clear gates, and climb a leaderboard of Solo Leveling characters. There's even a real-money "commitment wallet" that punishes you (financially) for skipping your quests.

> ⚠️ No description was set on the GitHub repo itself — this README documents the app based on its source.

## Features

- **Awakening onboarding** — pick a hunter name and a main class (e.g. *Shadow Mage*), set your DSA-problems-per-day and project-deployments-per-week targets, add custom quests, and optionally describe a fitness goal and extracurriculars in plain text.
- **AI-generated quest plan** *(optional)* — if an `OPENAI_API_KEY` is set, your fitness goal and extra pursuits are broken down into concrete daily tasks via the OpenAI API. Falls back to simple comma-splitting if no key is provided.
- **Daily / Weekly / Monthly quests** — checklists of tasks by type (`DSA`, `DEV`, `FITNESS`, `CUSTOM`) that award XP and grow your stats (Strength, Intelligence, Perception) on completion.
- **Quest verification** — DSA and DEV quests require a proof link before they're marked done; FITNESS and CUSTOM quests complete instantly.
- **XP, levels, and Hunter Rank** — a separate leveling curve tracks XP; your Hunter Rank (E through S) is derived from your level.
- **Gates** — persistent (recurring every 7 days) and iterative (one-time) challenges across DSA, Fitness, and Dev tracks, each rewarding MP (a second leveling currency) on clearing.
- **Instance Dungeon Keys** — a ~12.5% random chance to earn a bonus key each time you complete a daily quest.
- **Streaks & penalties** — missing a daily quest deducts XP and stats; missing all quests in a day breaks your streak and triggers System-style warning messages (B/A/S-rank penalties for missed daily/weekly/monthly goals).
- **Leaderboard** — a static roster of Solo Leveling hunters (Cha Hae-in, Baek Yoon-ho, Yoo Jinho, etc.) with your own hunter dynamically inserted and ranked by level.
- **Commitment Wallet** — commit real money (via a generated UPI QR code) up to a level-based cap; a percentage of your balance is frozen for each quest you miss, adding real stakes to the system.

## Tech Stack

- **[Reflex](https://reflex.dev)** — Python framework compiling to a React/Next.js frontend + FastAPI backend
- **Tailwind v4** + **Radix Themes** (dark, cyan-accented "System" UI)
- **OpenAI API** (optional) for AI-assisted daily quest generation
- **python-dotenv** for local environment configuration

## Project Structure

```
.
├── assets/                       # Static assets (custom CSS, etc.)
│   └── style.css
├── solo_leveling_app/
│   ├── components/
│   │   └── system_ui.py          # Shared "System"-styled UI components
│   ├── pages/
│   │   ├── awakening.py          # Onboarding flow
│   │   ├── dashboard.py          # Quests, XP/stats, streak chart
│   │   ├── gates.py              # Gate challenges
│   │   └── leaderboard.py        # Hunter leaderboard
│   ├── state.py                  # All app state & business logic (AppState)
│   └── solo_leveling_app.py      # App entry point & routing
├── reflex.lock/                  # Frontend lockfile (bun.lock, package.json)
├── requirements.txt
├── rxconfig.py                   # Reflex app configuration
└── LICENSE
```

## Getting Started

### Prerequisites

- Python 3.10+
- [Reflex](https://reflex.dev) requires Node.js/Bun for the frontend build (installed automatically on first run)

### Installation

```bash
git clone https://github.com/DivyomChaudhary/Level_Up_The_System.git
cd Level_Up_The_System
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root for optional features (never commit this file):

```env
# Optional — enables AI-generated daily quest breakdowns
OPENAI_API_KEY=your_openai_api_key

# Optional — default UPI ID for the Commitment Wallet QR code
COMMITMENT_UPI_ID=your_upi_id
```

### Run the app

```bash
reflex run
```

The app will be available at `http://localhost:3000` by default.

## How It Works

1. **Awaken** — go through onboarding to set your class, goals, and quests.
2. **Grind daily quests** — check off DSA, dev, fitness, and custom tasks each day. Complete quests to earn XP and grow your stats; complete *all* of them in a day to extend your streak.
3. **Clear gates** — tackle bigger, rank-gated challenges (persistent or one-time) for MP.
4. **Climb the leaderboard** — your level determines your position among the Solo Leveling hunters.
5. **Stay honest** — optionally put money on the line via the Commitment Wallet. Miss quests, and a slice of your balance freezes.
6. **Face the consequences** — skip your dailies/weeklies/monthlies and the System issues penalty warnings, deducts XP, and lowers your stats.

## License

Distributed under the **MIT License**. See [`LICENSE`](./LICENSE) for details.

## Author

**Divyom Chaudhary**

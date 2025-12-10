# Claude Code History Analyzer

> *"What did I even build yesterday?"* — Every vibe coder, ever

![Claude](https://img.shields.io/badge/Powered%20by-Claude%20Opus%204.5-blueviolet)
![Vibe](https://img.shields.io/badge/Vibe-Immaculate-ff69b4)
![Memory](https://img.shields.io/badge/Memory-Externalized-brightgreen)

## The Problem

You've been **vibe coding** for weeks. You and Claude have shipped features, squashed bugs, refactored entire modules, and mass-deleted code you were "pretty sure" wasn't needed. It's been beautiful. It's been productive. It's been... completely undocumented.

Now your PM asks: *"Can you give me a summary of what you worked on this sprint?"*

You stare at your terminal. You stare at your git log. You open Claude Code and scroll through history like an archaeologist sifting through ancient ruins. Was it Monday when you rewrote the auth system? Or was that the day you spent 4 hours debugging a missing semicolon that turned out to be a missing comma?

**Your memory has failed you. But your `~/.claude/history.jsonl` has not.**

## The Solution

This tool excavates your Claude Code conversation history and transforms it into a beautiful, searchable timeline of everything you've accomplished. It's like having a personal secretary who was silently taking notes while you were in the zone.

### Features

- **AI-Powered Summaries** — Uses Claude Opus 4.5 to generate concise summaries of your sessions (or uses built-in summaries for the budget-conscious)
- **GitHub Integration** — Links commits to your sessions, with preference for tags when available
- **Beautiful Web UI** — A sleek, dark-mode interface to browse your history by project and date
- **Searchable** — Find that one session where you "fixed the thing with the stuff"
- **Expandable Messages** — Click to reveal the full conversation from any session
- **Cron-Ready** — Set it and forget it. Your history updates automatically.

## Screenshots

The web interface shows your projects in a timeline view:

```
┌─────────────────────────────────────────────────────────────────┐
│  Claude Code History                    [Search...] [Date ▼]   │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌─────────────────────────────────────────────┐  │
│  │ Projects │  │ foodis                                      │  │
│  │          │  │─────────────────────────────────────────────│  │
│  │ foodis   │  │ December 10, 2025                           │  │
│  │ guitarHub│  │ ┌─────────────────────────────────────────┐ │  │
│  │ WorldInt │  │ │ 09:13 - 15:35          [18 msgs] [3 🏷️] │ │  │
│  │ bennet   │  │ │ • Restaurant invite system planning     │ │  │
│  │ ...      │  │ │ • iOS deep linking implementation       │ │  │
│  └──────────┘  │ │ • Booking feature design & beads        │ │  │
│                │ └─────────────────────────────────────────┘ │  │
│                └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

- Python 3.9+
- Claude Code (obviously)
- An Anthropic API key (for AI summaries, optional but recommended)

### Quick Start

```bash
# Clone the repo
git clone https://github.com/eranshir/claudeHistory.git
cd claudeHistory

# Install dependencies
pip install anthropic

# Set up your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run the analyzer
python3 claude_history_analyzer.py

# View your history
open index.html
# Or start a local server:
python3 -m http.server 8080
```

## Usage

### Basic Usage

```bash
# Generate history with AI summaries (requires API key)
python3 claude_history_analyzer.py

# Generate history without API calls (uses built-in summaries)
python3 claude_history_analyzer.py --no-api

# Force refresh all sessions (ignore cache)
python3 claude_history_analyzer.py --force-refresh

# Custom output location
python3 claude_history_analyzer.py --output /path/to/history.json
```

### Viewing Your History

Option 1: Open `index.html` directly in your browser (may have CORS issues)

Option 2: Start a local server:
```bash
python3 -m http.server 8080
open http://localhost:8080
```

### Automated Daily Updates (Cron)

Want your history to update automatically? Set up a cron job:

```bash
# Edit your crontab
crontab -e

# Add this line (runs daily at 9 PM)
0 21 * * * /path/to/claudeHistory/run_analyzer.sh
```

**Note:** Edit `run_analyzer.sh` to point to your Python installation that has `anthropic` installed.

## How It Works

1. **Reads** your Claude Code history from `~/.claude/history.jsonl`
2. **Loads** detailed session data from `~/.claude/projects/*/`
3. **Extracts** built-in summaries (Claude already summarizes your conversations!)
4. **Enhances** with AI-generated daily summaries (optional)
5. **Links** git commits that match your session timeframes
6. **Outputs** a structured JSON file
7. **Renders** everything in a beautiful web interface

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key for AI summaries | No (but recommended) |

### Command Line Options

| Option | Description |
|--------|-------------|
| `--output`, `-o` | Output JSON file path (default: `history_data.json`) |
| `--force-refresh`, `-f` | Regenerate all sessions, ignoring cache |
| `--no-api` | Skip API calls, use only built-in summaries |

## Privacy & Security

- **Your data stays local** — Nothing is sent anywhere except Anthropic's API (for summaries)
- **API key in `.env`** — Never committed to git
- **`history_data.json` is gitignored** — Your conversations stay private
- **No telemetry** — We're not watching you. We're too busy vibe coding.

## FAQ

**Q: Why do some sessions show "Session topics: ..." instead of nice summaries?**

A: Those sessions don't have built-in Claude summaries. Run with an API key to generate proper summaries, or embrace the chaos.

**Q: Can I use this with other AI coding assistants?**

A: This is specifically built for Claude Code's history format. But hey, PRs welcome!

**Q: My commits aren't showing up?**

A: Commits are matched by timestamp within the session timeframe (±30 minutes). If you committed hours after your session ended, it won't be linked.

**Q: Is this officially supported by Anthropic?**

A: Nope! This is a community tool built by someone who kept forgetting what they worked on. Use at your own risk.

## Contributing

Found a bug? Want a feature? PRs welcome! Just remember:

1. Keep it simple
2. Keep it fun
3. Keep vibing

## License

MIT — Do whatever you want with it. Build something cool.

---

*Built with Claude Code, documented by Claude Code, for Claude Code users who can't remember what they built with Claude Code.*

🤖 **Happy Vibe Coding!**

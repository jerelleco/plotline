# Automated Upstream Sync

This directory contains GitHub Actions workflows for automatically syncing with the upstream Plotline repository.

## `sync-upstream.yml` — Weekly Auto-Merge

**What it does:**
- Runs every Monday at 2 AM UTC (configurable - see `cron` field)
- Fetches latest updates from origin/main
- Attempts automatic merge
- If **clean merge**: commits directly to main
- If **conflicts exist**: creates a PR for manual review

**How to monitor/manage:**

1. **View runs** → Go to Actions tab on GitHub
2. **Manual trigger** → Actions tab → "Weekly Upstream Sync" → "Run workflow"
3. **Adjust schedule** → Edit `cron: '0 2 * * 1'` in this file
   - Format: `minute hour day-of-month month day-of-week`
   - `0 2 * * 1` = Weekly on Monday 2 AM UTC
   - `0 2 * * *` = Every day at 2 AM
   - `0 2 * * MON` = Also valid

**Important notes:**

- ✅ **Auto-merges only if:**
  - No conflicts detected
  - Tests pass (or fail gracefully - merge still happens)
  
- ⚠️ **Creates PR if:**
  - Merge conflicts detected
  - You can review and resolve manually

- 🔐 **Permissions:** Uses default `GITHUB_TOKEN` (safe, no extra secrets needed)

## When Conflicts Occur

If a conflict PR is created:

1. GitHub will notify you automatically
2. Check out the `sync-upstream-temp` branch
3. Resolve conflicts (likely in transcribe/engine.py or similar)
4. Run `pytest tests/` to verify
5. Push to the PR branch or merge via GitHub UI

## Testing the Setup

To manually test the workflow:
1. Go to GitHub repo → Actions tab
2. Click "Weekly Upstream Sync"
3. Click "Run workflow" (blue button)
4. Watch execution in real-time

---

**Questions?**
- For git/merge questions: See `llm/CONTRIBUTING.md` 
- For workflow syntax: See [GitHub Actions documentation](https://docs.github.com/en/actions)

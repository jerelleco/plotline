# Plotline Local Setup Guide

This guide covers everything you need to install and run Plotline on your local Windows PC.

## Prerequisites

### 1. Python 3.11 or 3.12
- Download from: https://python.org/downloads/
- During installation, check "Add Python to PATH"
- Verify: Open PowerShell and run `python --version`

### 2. FFmpeg
- Download from: https://ffmpeg.org/download.html#build-windows
- Choose the "Windows builds" link
- Extract to a folder (e.g., `C:\ffmpeg`)
- Add to PATH: Search "Environment Variables" → System Variables → Path → Add `C:\ffmpeg\bin`
- Verify: Open PowerShell and run `ffmpeg -version`

### 3. Git (Optional, for updates)
- Download from: https://git-scm.com/downloads
- Install with default settings
- Verify: `git --version`

## Installation

### 1. Clone or Download Plotline
```powershell
# If using git:
git clone https://github.com/jerelleco/plotline.git
cd plotline

# Or download ZIP from GitHub and extract
```

### 2. Set Up Virtual Environment
```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```powershell
# Install the package
pip install -e .

# Install development dependencies (optional, for testing)
pip install -e ".[dev]"

# Install diarization support (optional)
pip install -e ".[diarization]"
```

### 4. Verify Installation
```powershell
# Should show plotline commands
plotline --help
```

## Configuration

### 1. Create a Project
```powershell
# Create new project directory
plotline init "My Documentary" --profile documentary

# Change into project
cd "My Documentary"
```

### 2. Configure Settings (Optional)
Edit `plotline.yaml` in your project directory:
```yaml
# Default settings - adjust as needed
whisper_model: large-v3-turbo    # PC-optimized model
whisper_backend: faster          # Use faster-whisper
whisper_language: null           # Auto-detect
```

## Troubleshooting

### Common Issues

**"python not found"**
- Reinstall Python and check "Add to PATH"
- Or use full path: `C:\Python311\python.exe`

**"ffmpeg not found"**
- Add FFmpeg bin folder to PATH
- Or specify full path in config

**Import errors**
- Make sure virtual environment is activated
- Try reinstalling: `pip install -e . --force-reinstall`

**Permission errors**
- Run PowerShell as Administrator
- Or use `pip install --user` if needed

### Getting Help
- Check `plotline --help` for commands
- Run `plotline <command> --help` for specific help
- Check the docs/ folder for more guides

## Next Steps
Once set up, see the [PC Usage Guide](pc-usage-guide.md) for how to use Plotline.
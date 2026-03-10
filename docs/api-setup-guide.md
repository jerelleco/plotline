# Plotline API Keys & Model Setup Guide

This guide covers all the API keys, tokens, and model setup needed for Plotline to work properly on PC.

## Quick Setup Checklist

- ✅ **Whisper models**: Auto-downloaded (no setup needed)
- ⚠️ **Hugging Face token**: Only if using speaker diarization
- ⚠️ **LLM API keys**: Only if using cloud LLMs (Claude/OpenAI)

## 1. Whisper Models (Automatic Setup)

**No manual setup required!** Plotline automatically downloads Whisper models when first used.

### How it works:
- Models are downloaded to `~/.cache/huggingface/hub/` on first use
- `large-v3-turbo` (default) is ~1.5GB
- `distil-large-v3` (fast) is ~800MB
- Downloads happen during `plotline transcribe`

### Verify models are working:
```powershell
# Run transcription on a test file
plotline transcribe --model turbo

# Check for download progress messages
# Models cache automatically after first use
```

### Troubleshooting Whisper:
- **Slow first run**: Normal - model downloading
- **Out of disk space**: Clear `~/.cache/huggingface/hub/`
- **Network issues**: Models download from Hugging Face CDN

## 2. Hugging Face Token (Optional - Diarization Only)

**Only needed if you use speaker diarization** (`plotline diarize` or `diarization_enabled: true`).

### Get your token:
1. Go to https://huggingface.co/settings/tokens
2. Create new token (type: "Read")
3. Copy the token (starts with `hf_`)

### Accept model terms:
1. Visit https://huggingface.co/pyannote/segmentation-3.0
2. Click "Accept terms" (required)
3. Visit https://huggingface.co/pyannote/speaker-diarization-3.1
4. Click "Accept terms" (required)

### Set the token:
```powershell
# Windows PowerShell (temporary session)
$env:HUGGINGFACE_TOKEN = "hf_your_token_here"

# Or permanent (add to user environment variables)
# Search "Environment Variables" → User variables → New:
# Variable name: HUGGINGFACE_TOKEN
# Variable value: hf_your_token_here
```

### Verify diarization works:
```powershell
# Install diarization dependencies first
pip install -e ".[diarization]"

# Enable in config (plotline.yaml)
diarization_enabled: true

# Test
plotline diarize
```

## 3. LLM API Keys (Optional - Cloud LLMs Only)

**Only needed if using Claude or OpenAI** instead of local Ollama.

### For Claude (Anthropic):
1. Go to https://console.anthropic.com/
2. Create account → Get API key
3. Set environment variable:
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-api03-your_key_here"
```

### For OpenAI:
1. Go to https://platform.openai.com/api-keys
2. Create new secret key
3. Set environment variable:
```powershell
$env:OPENAI_API_KEY = "sk-your_key_here"
```

### Configure Plotline to use cloud LLM:
Edit `plotline.yaml`:
```yaml
privacy_mode: hybrid        # Allow cloud APIs
llm_backend: claude         # or "openai"
llm_model: claude-3-5-sonnet-20241022  # or "gpt-4"
```

### Test LLM connection:
```powershell
plotline themes
# Should work without local Ollama
```

## 4. Environment Variables Setup (Windows)

### Option 1: Temporary (per session)
```powershell
# In PowerShell, before running Plotline
$env:HUGGINGFACE_TOKEN = "hf_..."
$env:ANTHROPIC_API_KEY = "sk-ant-..."
$env:OPENAI_API_KEY = "sk-..."
```

### Option 2: Permanent (recommended)
1. Search "Environment Variables" in Windows search
2. Click "Edit environment variables for your account"
3. Under "User variables", click "New" for each:
   - `HUGGINGFACE_TOKEN` = `hf_...`
   - `ANTHROPIC_API_KEY` = `sk-ant-...`
   - `OPENAI_API_KEY` = `sk-...`
4. Click "OK" and restart PowerShell

### Option 3: .env file (project-specific)
Create `.env` file in your project directory:
```
HUGGINGFACE_TOKEN=hf_...
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
```

## 5. Default Configuration (PC-Optimized)

Your `plotline.yaml` should look like this for PC:

```yaml
# PC-optimized defaults
privacy_mode: local          # Use local Ollama (recommended)
llm_backend: ollama
llm_model: llama3.1:8b

whisper_backend: faster       # PC backend
whisper_model: large-v3-turbo # Best quality/speed balance

# Optional features
diarization_enabled: false    # Set to true if you get HF token
cultural_flags: false         # LLM feature
```

## 6. Testing Everything

### Full pipeline test:
```powershell
# Create test project
plotline init test-project
cd test-project

# Add a short video file
plotline add path\to\test_video.mp4

# Run full pipeline
plotline run

# Check reports
plotline report dashboard
```

### Individual component tests:
```powershell
# Test transcription
plotline transcribe

# Test LLM (themes)
plotline themes

# Test diarization (if enabled)
plotline diarize
```

## 7. Troubleshooting

### "Model not found" errors:
- Whisper models download automatically - wait for first run
- Check internet connection
- Clear cache: `rmdir /s %USERPROFILE%\.cache\huggingface`

### "API key invalid" errors:
- Double-check environment variables
- Restart PowerShell after setting variables
- For Claude/OpenAI: Verify keys in their dashboards

### "Hugging Face permission denied":
- Accept terms on both pyannote model pages
- Token has "Read" permissions
- Try regenerating token

### Performance issues:
- Use `whisper_model: distil-large-v3` for faster transcription
- Close other applications during processing
- Ensure good GPU drivers (CUDA acceleration)

## 8. Security Notes

- **Never commit API keys** to git (they're in .env files)
- **Use read-only tokens** where possible
- **Rotate keys** if accidentally exposed
- **Environment variables** are safer than hardcoded values

## Summary

For basic PC usage with local LLM:
- ✅ Install Plotline
- ✅ Set up Ollama (`ollama pull llama3.1:8b`)
- ✅ No API keys needed!

For advanced features:
- ⚠️ Hugging Face token (diarization only)
- ⚠️ Claude/OpenAI keys (cloud LLM only)

The system is designed to work out-of-the-box with minimal setup!
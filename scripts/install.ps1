# ============================================================================
# Plotline Installer for Windows
# ============================================================================
# Double-click install.bat to run this script.
# It will set up Python 3.11 venv, install all dependencies, and verify
# that external tools (FFmpeg, Ollama, CUDA) are available.
# ============================================================================

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot

function Write-Header($text) {
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host "  $text" -ForegroundColor Cyan
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host ""
}

function Write-Step($text) {
    Write-Host "  [*] $text" -ForegroundColor White
}

function Write-Ok($text) {
    Write-Host "  [OK] $text" -ForegroundColor Green
}

function Write-Warn($text) {
    Write-Host "  [!!] $text" -ForegroundColor Yellow
}

function Write-Fail($text) {
    Write-Host "  [FAIL] $text" -ForegroundColor Red
}

# Track what passed and what needs attention
$warnings = @()
$failures = @()

# --------------------------------------------------------------------------
# Step 1: Find Python 3.11
# --------------------------------------------------------------------------
Write-Header "Step 1: Locating Python 3.11"

$python311 = $null

# Try the py launcher first (most reliable on Windows)
$pyLauncher = Get-Command py -ErrorAction SilentlyContinue
if ($pyLauncher) {
    try {
        $ver = & py -3.11 --version 2>&1
        if ($ver -match "Python 3\.11") {
            # Resolve the actual python.exe path so we can call it directly
            $python311 = (& py -3.11 -c "import sys; print(sys.executable)" 2>&1).Trim()
            Write-Ok "Found via py launcher: $ver"
            Write-Step "Resolved to: $python311"
        }
    } catch {}
}

# Fallback: check PATH for python3.11 or python
if (-not $python311) {
    $candidates = @("python3.11", "python3", "python")
    foreach ($cmd in $candidates) {
        try {
            $ver = & $cmd --version 2>&1
            if ($ver -match "Python 3\.11") {
                $python311 = (Get-Command $cmd).Source
                Write-Ok "Found as '$cmd': $ver"
                break
            }
        } catch {}
    }
}

if (-not $python311) {
    Write-Fail "Python 3.11 not found!"
    Write-Host ""
    Write-Host "  Install Python 3.11 from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  Make sure to check 'Add to PATH' during installation." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# --------------------------------------------------------------------------
# Step 2: Create virtual environment
# --------------------------------------------------------------------------
Write-Header "Step 2: Creating Virtual Environment"

$venvPath = Join-Path $ProjectRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"
$venvPip = Join-Path $venvPath "Scripts\pip.exe"

if (Test-Path $venvPython) {
    # Check if existing venv is Python 3.11
    $existingVer = & $venvPython --version 2>&1
    if ($existingVer -match "Python 3\.11") {
        Write-Ok "Existing Python 3.11 venv found, reusing it"
    } else {
        Write-Step "Existing venv is $existingVer -- replacing with Python 3.11"
        Remove-Item -Recurse -Force $venvPath
        Write-Step "Creating new venv with Python 3.11..."
        & $python311 -m venv $venvPath
        if ($LASTEXITCODE -ne 0) { Write-Fail "Failed to create venv"; exit 1 }
        Write-Ok "Virtual environment created"
    }
} else {
    Write-Step "Creating venv with Python 3.11..."
    & $python311 -m venv $venvPath
    if ($LASTEXITCODE -ne 0) { Write-Fail "Failed to create venv"; exit 1 }
    Write-Ok "Virtual environment created"
}

# Verify
$checkVer = & $venvPython --version 2>&1
Write-Ok "venv Python: $checkVer"

# --------------------------------------------------------------------------
# Step 3: Upgrade pip and install Plotline
# --------------------------------------------------------------------------
Write-Header "Step 3: Installing Plotline and Dependencies"

Write-Step "Upgrading pip..."
& $venvPython -m pip install --upgrade pip --quiet 2>&1 | Out-Null
Write-Ok "pip upgraded"

Write-Step "Installing plotline (editable) and all dependencies..."
Write-Host "       This may take a few minutes on first install." -ForegroundColor DarkGray
Write-Host ""

& $venvPip install -e $ProjectRoot 2>&1 | ForEach-Object {
    if ($_ -match "ERROR|error|Failed") {
        Write-Host "       $_" -ForegroundColor Red
    } elseif ($_ -match "Successfully installed") {
        Write-Host "       $_" -ForegroundColor Green
    }
}

if ($LASTEXITCODE -ne 0) {
    Write-Fail "pip install failed! Check the errors above."
    $failures += "Python dependencies failed to install"
} else {
    Write-Ok "Plotline and dependencies installed"
}

# Verify the CLI entry point works
try {
    $plotlineVer = & $venvPython -m plotline --version 2>&1
    # typer --version callback prints and exits
    Write-Ok "plotline CLI available: $plotlineVer"
} catch {
    # Not critical if the --version check fails, the install may still be fine
    Write-Step "CLI entry point check skipped (non-critical)"
}

# --------------------------------------------------------------------------
# Step 4: Check FFmpeg
# --------------------------------------------------------------------------
Write-Header "Step 4: Checking FFmpeg"

$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
$ffprobe = Get-Command ffprobe -ErrorAction SilentlyContinue

if ($ffmpeg) {
    $ffVer = (& ffmpeg -version 2>&1 | Select-Object -First 1)
    Write-Ok "FFmpeg found: $ffVer"
} else {
    Write-Warn "FFmpeg not found in PATH"
    Write-Host ""
    $installFfmpeg = Read-Host "  Install FFmpeg via winget? (Y/n)"
    if ($installFfmpeg -ne "n") {
        Write-Step "Installing FFmpeg via winget..."
        & winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Ok "FFmpeg installed. You may need to restart your terminal for PATH changes."
            $warnings += "Restart terminal for FFmpeg PATH update"
        } else {
            Write-Fail "winget install failed. Install FFmpeg manually from: https://ffmpeg.org/download.html"
            $failures += "FFmpeg not installed"
        }
    } else {
        Write-Warn "Skipping FFmpeg install. You will need it before running the pipeline."
        $warnings += "FFmpeg not installed (skipped)"
    }
}

if (-not $ffprobe -and $ffmpeg) {
    Write-Warn "FFprobe not found separately, but it usually ships with FFmpeg."
    Write-Warn "If 'plotline doctor' complains, check your FFmpeg installation."
}

# --------------------------------------------------------------------------
# Step 5: Check NVIDIA GPU / CUDA
# --------------------------------------------------------------------------
Write-Header "Step 5: Checking NVIDIA GPU (CUDA)"

$nvidiaSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if ($nvidiaSmi) {
    $gpuInfo = & nvidia-smi --query-gpu=name,driver_version --format=csv,noheader 2>&1
    Write-Ok "NVIDIA GPU detected: $gpuInfo"
    Write-Ok "faster-whisper will use CUDA acceleration on your GPU"
} else {
    Write-Warn "nvidia-smi not found. GPU acceleration may not work."
    Write-Warn "Install NVIDIA drivers from: https://www.nvidia.com/drivers"
    $warnings += "NVIDIA drivers/CUDA not detected"
}

# --------------------------------------------------------------------------
# Step 6: Check Ollama
# --------------------------------------------------------------------------
Write-Header "Step 6: Checking Ollama (Local LLM)"

$ollama = Get-Command ollama -ErrorAction SilentlyContinue
if ($ollama) {
    Write-Ok "Ollama found"

    # Check if server is running
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 3 -ErrorAction Stop
        $models = ($response.Content | ConvertFrom-Json).models.name
        if ($models.Count -gt 0) {
            Write-Ok "Ollama is running with models: $($models -join ', ')"
        } else {
            Write-Warn "Ollama is running but no models are pulled"
            Write-Host ""
            $pullModel = Read-Host "  Pull llama3.1:8b now? (Y/n)"
            if ($pullModel -ne "n") {
                Write-Step "Pulling llama3.1:8b (this will take a while)..."
                & ollama pull llama3.1:8b 2>&1 | ForEach-Object { Write-Host "       $_" -ForegroundColor DarkGray }
                Write-Ok "Model pulled"
            } else {
                $warnings += "No Ollama model pulled yet"
            }
        }
    } catch {
        Write-Warn "Ollama is installed but not running"
        Write-Warn "Start it with: ollama serve"
        $warnings += "Ollama not running"
    }
} else {
    Write-Warn "Ollama not found"
    Write-Host ""
    Write-Host "  Install Ollama from: https://ollama.com/download" -ForegroundColor Yellow
    Write-Host "  Then run: ollama pull llama3.1:8b" -ForegroundColor Yellow
    $warnings += "Ollama not installed"
}

# --------------------------------------------------------------------------
# Summary
# --------------------------------------------------------------------------
Write-Header "Installation Complete"

Write-Host "  Project:  $ProjectRoot" -ForegroundColor White
Write-Host "  Python:   $checkVer" -ForegroundColor White
Write-Host "  venv:     $venvPath" -ForegroundColor White
Write-Host ""

if ($failures.Count -gt 0) {
    Write-Host "  FAILURES (must fix):" -ForegroundColor Red
    foreach ($f in $failures) {
        Write-Host "    - $f" -ForegroundColor Red
    }
    Write-Host ""
}

if ($warnings.Count -gt 0) {
    Write-Host "  WARNINGS (may need attention):" -ForegroundColor Yellow
    foreach ($w in $warnings) {
        Write-Host "    - $w" -ForegroundColor Yellow
    }
    Write-Host ""
}

if ($failures.Count -eq 0) {
    Write-Host "  To activate the environment:" -ForegroundColor Green
    Write-Host "    .venv\Scripts\activate" -ForegroundColor White
    Write-Host ""
    Write-Host "  To verify everything works:" -ForegroundColor Green
    Write-Host "    plotline doctor" -ForegroundColor White
    Write-Host ""
    Write-Host "  To start your first project:" -ForegroundColor Green
    Write-Host "    plotline init my-doc --profile documentary" -ForegroundColor White
    Write-Host "    cd my-doc" -ForegroundColor White
    Write-Host "    plotline add C:\path\to\interview.mov" -ForegroundColor White
    Write-Host "    plotline run" -ForegroundColor White
    Write-Host ""
}

# Plotline PC Usage Guide

Step-by-step instructions for using Plotline on Windows PC. Assumes you've completed the [Local Setup](local-setup.md).

## Quick Start Workflow

### 1. Create a Project
```powershell
# Create new project
plotline init "My Project" --profile documentary

# Enter project directory
cd "My Project"
```

### 2. Add Video Files
```powershell
# Add individual files
plotline add interview1.mov interview2.mp4

# Add entire folder (scans recursively)
plotline add "C:\Videos\Interviews"

# Add with custom scanning
plotline add videos/ --recursive
```

### 3. Transcribe Audio
```powershell
# Transcribe with default PC settings (large-v3-turbo)
plotline transcribe

# Use faster model
plotline transcribe --model fast

# Specify language
plotline transcribe --language en

# Force re-transcription
plotline transcribe --force
```

### 4. Analyze Delivery
```powershell
# Analyze speech patterns and delivery
plotline analyze
```

### 5. Generate Reports
```powershell
# Create all reports
plotline report

# Generate specific report
plotline report summary    # Text summary
plotline report dashboard  # HTML dashboard
plotline report transcript # Full transcript
plotline report coverage   # Coverage analysis
plotline report themes     # Theme extraction
plotline report compare    # Comparison view
```

### 6. Export for Editing
```powershell
# Export DaVinci Resolve timeline
plotline export edl

# Export Final Cut Pro XML
plotline export fcpxml
```

## Detailed Commands

### Project Management
```powershell
# List all commands
plotline --help

# Get help for specific command
plotline transcribe --help

# Check project status
plotline status
```

### Transcription Options
```powershell
# Model presets (PC-optimized)
plotline transcribe --model turbo      # large-v3-turbo (default)
plotline transcribe --model fast       # distil-large-v3
plotline transcribe --model experimental # large-v3

# Language settings
plotline transcribe --language en      # English
plotline transcribe --language es      # Spanish
plotline transcribe                    # Auto-detect

# Backend selection
plotline transcribe --backend faster   # PC default
plotline transcribe --backend mlx      # Apple Silicon only
```

### Report Generation
```powershell
# Generate all reports
plotline report

# Individual reports
plotline report summary   # Text summary with key insights
plotline report dashboard # Interactive HTML dashboard
plotline report transcript # Full transcript with timestamps
plotline report coverage  # Coverage analysis and gaps
plotline report themes    # Extracted themes and topics
plotline report compare   # Side-by-side comparison
```

### Export Formats
```powershell
# DaVinci Resolve EDL
plotline export edl

# Final Cut Pro XML
plotline export fcpxml

# Export to custom location
plotline export edl --output "C:\Exports\Timeline.edl"
```

## File Organization

After running commands, your project will contain:

```
My Project/
├── plotline.yaml          # Configuration
├── interviews.json        # Manifest of added videos
├── source/                # Original video files
├── data/
│   ├── transcripts/       # JSON transcription data
│   ├── delivery/          # Analysis results
│   ├── segments/          # Unified segments
│   └── themes/            # Theme extraction
├── reports/               # Generated HTML/text reports
└── export/                # EDL/XML files for editors
```

## Tips for PC Users

### Performance Optimization
- Use `--model fast` for quicker transcription
- Close other applications during processing
- Ensure good GPU drivers for CUDA acceleration

### File Management
- Keep videos in `source/` folder
- Use descriptive filenames
- Back up `data/` and `reports/` folders

### Troubleshooting
```powershell
# Check for errors
plotline status

# Re-run failed steps
plotline transcribe --force
plotline analyze --force

# Verbose output
plotline --verbose transcribe
```

### Updating Plotline
```powershell
# Check for updates
git fetch upstream
git log --oneline main..upstream/main

# Apply updates
git merge upstream/main
git push origin main
```

## Common Workflows

### Documentary Editing
1. `plotline add videos/`
2. `plotline transcribe`
3. `plotline analyze`
4. `plotline report dashboard`
5. `plotline export edl`

### Quick Review
1. `plotline add interview.mp4`
2. `plotline transcribe --model fast`
3. `plotline report summary`

### Multi-Interview Project
1. `plotline add interview1.mp4 interview2.mp4 interview3.mp4`
2. `plotline transcribe`
3. `plotline analyze`
4. `plotline report themes`
5. `plotline report compare`
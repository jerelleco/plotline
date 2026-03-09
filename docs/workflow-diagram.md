# Workflow Diagrams

Visual comparison of Plotline vs traditional documentary editing workflows.

---

## 1. Time Savings

### Side-by-Side Workflow Comparison

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TB
    subgraph TRAD["Traditional Workflow"]
        direction TB
        T1["Watch all footage<br/><i>Hours per hour of content</i>"]
        T2["Transcribe<br/><i>Manual or paid service</i>"]
        T3["Identify themes<br/><i>Mental, informal</i>"]
        T4["Select & assemble<br/><i>Subjective, easy to miss</i>"]
        T5["Iterate & refine<br/><i>Multiple review cycles</i>"]
        T6["Export timeline"]
        
        T1 --> T2 --> T3 --> T4 --> T5 --> T6
    end
    
    subgraph PLOT["Plotline Workflow"]
        direction TB
        P1["Add footage<br/><i>5 minutes</i>"]
        P2["plotline run<br/><i>AI: Transcribe + Analyze + Arc</i>"]
        P3["plotline review<br/><i>You: Approve/Reject/Reorder</i>"]
        P4["plotline export<br/><i>Import to NLE</i>"]
        
        P1 --> P2 --> P3 --> P4
    end
    
    TRAD -.->|"10 hrs footage = 15-20 hrs work"| T6
    PLOT -.->|"10 hrs footage = 2-3 hrs review"| P4
```

### Time Breakdown

| Task | Traditional | Plotline | Savings |
|------|-------------|----------|---------|
| **10 hours footage** | 15-20 hours | 2-3 hours | ~85% |
| Transcription | $100-300 or 5+ hours | Free, automatic | 100% |
| Theme identification | Mental, informal | AI cross-interview | — |
| Best take selection | Watch repeatedly | AI scores + ranks | — |
| Delivery assessment | Subjective | Measured metrics | — |

### Per-Hour Processing

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    subgraph Input
        I1["1 hour of<br/>raw footage"]
    end
    
    subgraph Traditional
        direction LR
        T1["2-3 hours<br/>editing time"]
    end
    
    subgraph Plotline
        direction LR
        P1["~15 min<br/>processing"]
        P2["~15 min<br/>review"]
    end
    
    I1 --> T1
    I1 --> P1 --> P2
    
    style T1 fill:#fecaca
    style P1 fill:#bbf7d0
    style P2 fill:#fef3c7
```

---

## 2. AI vs Human Responsibilities

### Division of Labor

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    subgraph AI["AI Automated"]
        direction TB
        A1["Extract Audio"]
        A2["Transcribe<br/>Whisper"]
        A3["Analyze Delivery<br/>Energy, Pace, Pitch"]
        A4["Extract Themes"]
        A5["Synthesize<br/>Cross-Interview"]
        A6["Build Narrative Arc"]
        A7["Generate EDL/FCPXML"]
    end
    
    subgraph HUMAN["Human Decision"]
        direction TB
        H1["Add footage"]
        H2["Review selections<br/>Approve/Reject"]
        H3["Reorder timeline"]
        H4["Add notes"]
        H5["Final export"]
    end
    
    H1 --> A1 --> A2 --> A3 --> A4 --> A5 --> A6 --> H2 --> H3 --> H4 --> A7 --> H5
    
    style A1 fill:#3b82f6,color:#fff
    style A2 fill:#3b82f6,color:#fff
    style A3 fill:#3b82f6,color:#fff
    style A4 fill:#3b82f6,color:#fff
    style A5 fill:#3b82f6,color:#fff
    style A6 fill:#3b82f6,color:#fff
    style A7 fill:#3b82f6,color:#fff
    style H1 fill:#f59e0b,color:#000
    style H2 fill:#f59e0b,color:#000
    style H3 fill:#f59e0b,color:#000
    style H4 fill:#f59e0b,color:#000
    style H5 fill:#f59e0b,color:#000
```

### The Human Always Has Final Say

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TB
    subgraph AI_PROCESS["AI Processing Pipeline"]
        A1["Transcribe"] --> A2["Analyze"] --> A3["Themes"] --> A4["Arc"]
    end
    
    subgraph GATE["Human Gatekeeper"]
        H1["Review Interface"]
        H2["Approve / Reject / Reorder"]
    end
    
    subgraph OUTPUT["Output"]
        O1["EDL / FCPXML"]
    end
    
    AI_PROCESS --> H1 --> H2 --> O1
    
    style H1 fill:#f59e0b,color:#000
    style H2 fill:#f59e0b,color:#000
```

**Key principle:** The AI proposes, the human decides. Every segment must pass through your review before reaching the final timeline.

---

## 3. Quality Improvements

### What Plotline Measures (That Traditional Editing Can't)

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TB
    subgraph METRICS["Delivery Metrics"]
        M1["RMS Energy<br/><i>Volume/intensity</i>"]
        M2["Pitch Variation<br/><i>Vocal expressiveness</i>"]
        M3["Speech Rate<br/><i>Words per minute</i>"]
        M4["Pause Patterns<br/><i>Timing and pacing</i>"]
        M5["Spectral Features<br/><i>Voice quality</i>"]
    end
    
    subgraph SCORE["Composite Score"]
        S1["0.0 - 1.0<br/>Delivery quality"]
    end
    
    M1 --> S1
    M2 --> S1
    M3 --> S1
    M4 --> S1
    M5 --> S1
    
    style S1 fill:#10b981,color:#fff
```

| Metric | What It Measures | Why It Matters |
|--------|------------------|----------------|
| **Energy** | RMS amplitude | Engaging speakers vary volume |
| **Pitch Variation** | Standard deviation of pitch | Monotone = boring |
| **Speech Rate** | Words per minute | Too fast/slow loses audience |
| **Pauses** | Silence before/after | Natural pacing, breathing room |
| **Spectral** | Voice brightness/texture | Audio quality, clarity |

### Brief Alignment

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    subgraph INPUT
        B1["Creative Brief<br/>Key Messages"]
        S1["Selected Segments"]
    end
    
    subgraph ALIGNMENT["Coverage Analysis"]
        C1["Match segments<br/>to messages"]
        C2["Score alignment<br/>Strong/Weak/Gap"]
    end
    
    subgraph OUTPUT
        O1["Coverage Matrix"]
        O2["Gap Report"]
    end
    
    B1 --> C1
    S1 --> C1
    C1 --> C2 --> O1
    C2 --> O2
```

**Traditional approach:** Manually check if each message is covered. Easy to miss gaps.

**Plotline approach:** Automatic coverage matrix shows exactly which segments support which messages, and where you have gaps.

### Cross-Interview Synthesis

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TB
    subgraph INTERVIEWS
        I1["Interview A<br/>Themes: X, Y, Z"]
        I2["Interview B<br/>Themes: X, W"]
        I3["Interview C<br/>Themes: Y, Z, W"]
    end
    
    subgraph SYNTHESIS["Cross-Interview Synthesis"]
        S1["Unify themes<br/>across interviews"]
        S2["Find best takes<br/>for shared topics"]
        S3["Compare delivery<br/>scores globally"]
    end
    
    subgraph OUTPUT
        O1["Unified Themes<br/>X, Y, Z, W"]
        O2["Best Takes<br/>Highest scoring<br/>per topic"]
    end
    
    I1 --> S1
    I2 --> S1
    I3 --> S1
    S1 --> S2 --> S3 --> O1
    S3 --> O2
```

**Traditional approach:** Watch each interview separately, try to remember who said what best.

**Plotline approach:** AI identifies shared topics across all interviews, normalizes delivery scores globally, and ranks candidates so you can compare takes side-by-side.

---

## 4. Data Flow Architecture

### Pipeline Stages

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TB
    subgraph INPUT["Input"]
        V1["Video Files<br/>MOV, MP4, MXF"]
        V2["Creative Brief<br/>Optional"]
    end
    
    subgraph STAGE1["Stage 1: Extract"]
        S1["FFmpeg<br/>16kHz audio"]
    end
    
    subgraph STAGE2["Stage 2: Transcribe"]
        S2["Whisper<br/>Word timestamps"]
    end
    
    subgraph STAGE3["Stage 3: Analyze"]
        S3["Librosa<br/>Delivery metrics"]
    end
    
    subgraph STAGE4["Stage 4: Enrich"]
        S4["Merge<br/>Transcript + Delivery"]
    end
    
    subgraph STAGE5["Stage 5: LLM"]
        S5a["Themes"]
        S5b["Synthesize"]
        S5c["Arc"]
        S5a --> S5b --> S5c
    end
    
    subgraph STAGE6["Stage 6: Export"]
        S6["EDL / FCPXML"]
    end
    
    subgraph OUTPUT["Output Files"]
        O1["transcripts/*.json"]
        O2["delivery/*.json"]
        O3["segments/*.json"]
        O4["synthesis.json"]
        O5["selections.json"]
        O6["export/*.edl"]
    end
    
    V1 --> S1 --> S2 --> S3 --> S4
    V2 -.-> S5a
    S4 --> S5a
    S5c --> S6 --> O6
    
    S2 -.-> O1
    S3 -.-> O2
    S4 -.-> O3
    S5b -.-> O4
    S5c -.-> O5
```

### Data Transformations

| Stage | Input | Output | Tool |
|-------|-------|--------|------|
| **Extract** | Video files | 16kHz WAV + full-rate WAV | FFmpeg |
| **Transcribe** | Audio | Segments with word timestamps | Whisper |
| **Analyze** | Audio + segments | Delivery metrics per segment | Librosa |
| **Enrich** | Transcript + delivery | Unified segment data | Merge |
| **Themes** | Enriched segments | Per-interview themes | LLM |
| **Synthesize** | All themes | Unified cross-interview themes | LLM |
| **Arc** | Synthesis + brief | Narrative arc + selections | LLM |
| **Export** | Selections + approvals | EDL/FCPXML | Generator |

### File Structure

```
my-project/
├── plotline.yaml          # Configuration
├── interviews.json        # Manifest + stage status
├── brief.json             # Parsed creative brief
├── approvals.json         # Review approvals
├── source/                # Extracted audio
│   └── interview_001/
│       ├── audio_16k.wav  # For transcription
│       └── audio_full.wav # For delivery analysis
├── data/
│   ├── transcripts/       # Whisper output
│   ├── delivery/          # Librosa analysis
│   ├── segments/          # Enriched segments
│   ├── themes/            # Per-interview themes
│   ├── synthesis.json     # Cross-interview synthesis
│   └── selections.json    # Arc selections
├── reports/               # HTML reports
└── export/                # EDL/FCPXML files
```

---

## ASCII Reference (No Mermaid)

### Traditional Workflow

```
Watch all footage (hours/day)
        ↓
Transcribe (manual or $$$)
        ↓
Identify themes (mental)
        ↓
Select & assemble (subjective)
        ↓
Iterate & refine (many cycles)
        ↓
Export

TIME: ████████████████████ 100%
```

### Plotline Workflow

```
Add footage (5 min)
        ↓
plotline run
   ├── Extract audio
   ├── Transcribe (Whisper)
   ├── Analyze delivery
   ├── Extract themes
   ├── Synthesize cross-interview
   └── Build narrative arc
        ↓
plotline review
   ├── Listen to segment
   ├── Approve (A) or Reject (X)
   ├── Drag to reorder
   └── Add notes
        ↓
plotline export → Import to NLE

TIME: ███░░░░░░░░░░░░░░░ ~20%
```

### AI vs Human

```
┌─────────────────────────────────────────────────────┐
│  HUMAN          │  AI AUTOMATED                     │
├─────────────────┼───────────────────────────────────┤
│  Add footage    │  Extract audio                    │
│                 │  Transcribe (Whisper)             │
│                 │  Analyze delivery                 │
│                 │  Extract themes                   │
│                 │  Synthesize cross-interview       │
│                 │  Build narrative arc              │
│  Review         │                                   │
│  Approve/Reject │                                   │
│  Reorder        │                                   │
│  Add notes      │                                   │
│                 │  Generate EDL/FCPXML              │
│  Final export   │                                   │
└─────────────────┴───────────────────────────────────┘
```

### Data Flow

```
Video ──▶ Audio ──▶ Transcript ──▶ Delivery ──▶ Enriched
                                                      │
                                                      ▼
                                              Themes (per-interview)
                                                      │
                                                      ▼
                                              Synthesis (cross-interview)
                                                      │
                                                      ▼
                                              Narrative Arc
                                                      │
                                                      ▼
                                              Selections ──▶ EDL/FCPXML
```

---

## See Also

- **[Workflow Guide](workflow-guide.md)** — Step-by-step tutorial
- **[Export Guide](export-guide.md)** — NLE import workflows
- **[Reports Guide](reports-guide.md)** — HTML reports reference

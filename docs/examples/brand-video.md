# Example: Brand Video

## Project Overview

**"TechCorp Impact"** is a 3-minute brand video for an enterprise software company featuring interviews with three executives about platform, security, and customer success.

**Project type:** Brand Video
**Profile:** `brand`
**Target duration:** 3 minutes
**Interviews:** 3 (1.5 hours raw footage)

---

## Project Setup

```bash
plotline init techcorp-impact --profile brand
cd techcorp-impact
```

The brand profile emphasizes message clarity, energy, and alignment with key messages.

### Configuration

```yaml
project_name: techcorp-impact
project_profile: brand
target_duration_seconds: 180
```

### Creative Brief

A detailed brief guides the LLM toward key messages:

```markdown
# Key Messages

- Platform reduces operational costs by 40%
- Customers see ROI within 90 days
- Enterprise-grade security with SOC 2 Type II

# Audience

VPs of Engineering and CTOs at Fortune 500 companies.

# Tone

Confident, technical, trustworthy.

# Must Include

- Specific ROI number
- Security certification mention
- Customer success example

# Avoid

- Competitor names
- Pricing specifics
- "AI-powered" or "revolutionary"
```

### Adding Videos

```bash
plotline add ~/Footage/CEO_interview.mov
plotline add ~/Footage/CTO_interview.mov
plotline add ~/Footage/Customer_Success_Director.mov
```

### Running the Pipeline

```bash
plotline run
```

Processed all three interviews in approximately 25 minutes.

---

## Results

### Interview Statistics

| Interview | Duration | Segments | Avg Score |
|-----------|----------|----------|-----------|
| CEO | 32 min | 58 | 0.69 |
| CTO | 28 min | 51 | 0.72 |
| Customer Success Director | 24 min | 44 | 0.65 |

### Theme Extraction

8 unified themes identified:

1. **Cost Reduction** — 18 segments
2. **ROI Proof** — 14 segments
3. **Security Trust** — 12 segments
4. **Support Excellence** — 16 segments
5. **Innovation Culture** — 9 segments
6. **Customer Partnership** — 11 segments
7. **Technical Excellence** — 8 segments
8. **Scalability** — 7 segments

### Narrative Arc

18 segments totaling 2:58.

| Role | Count | Duration |
|------|-------|----------|
| Opening | 2 | 0:28 |
| Deepening | 6 | 1:12 |
| Turning Point | 3 | 0:34 |
| Climax | 3 | 0:32 |
| Resolution | 4 | 0:22 |

### Coverage Analysis

All three key messages had strong coverage.

---

## Review Process

### Editorial Decisions

Review took approximately 45 minutes:

1. Listened to all 18 proposed segments
2. Rejected 2 segments for being too technical
3. Moved "Security" section earlier
4. Replaced 1 rejected segment with alternate
5. Added editorial notes to 3 segments

### Using the Compare Report

Essential for selecting best takes across speakers:

- **Cost Reduction** — CEO more authoritative, CTO had better numbers
- **Security** — CTO's technical explanation was stronger
- **Support** — Customer Success Director was natural choice

### Using the Coverage Report

Shared with stakeholders for approval. Marketing team approved based on coverage report alone.

---

## Export

```bash
plotline export --format edl --handle 12
```

16 approved segments, 2:58 duration.

---

## Lessons Learned

### What Worked Well

1. Creative brief kept LLM focused on key messages
2. Coverage report essential for stakeholder approval
3. Compare report critical for best takes
4. Brand profile prioritized confident delivery

### Challenges

1. Some segments too technical
2. CEO initially dominated — had to include other voices
3. 3 minutes tight for 3 messages

### Recommendations

1. Write detailed brief — essential for alignment
2. Use compare report early
3. Check speaker balance
4. Allow time for stakeholder review

---

## Related Examples

- **[Documentary Project](documentary.md)**
- **[Commercial Documentary](commercial-doc.md)**

## Related Documentation

- **[Workflow Guide](../workflow-guide.md)**
- **[Export Guide](../export-guide.md)**
- **[Reports Guide](../reports-guide.md)**

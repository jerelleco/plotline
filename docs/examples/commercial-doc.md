# Example: Commercial Documentary

## Project Overview

**"Homes4Hope"** is a 5-minute branded documentary for a nonprofit housing initiative showcasing affordable housing impact in rural communities.

**Project type:** Commercial Documentary
**Profile:** `commercial-doc`
**Target duration:** 5 minutes
**Interviews:** 6 (4 hours raw footage)

---

## Project Setup

```bash
plotline init homes4hope --profile commercial-doc
cd homes4hope
```

The commercial-doc profile balances documentary authenticity with brand alignment and enables cultural sensitivity flagging by default.

### Configuration

```yaml
project_name: homes4hope
project_profile: commercial-doc
target_duration_seconds: 300
cultural_flags: true
```

### Creative Brief

```markdown
# Key Messages

- Affordable housing creates economic opportunity
- Community partnerships drive sustainable change
- Everyone deserves a safe, stable home

# Tone

Authentic, hopeful, grounded in real stories.

# Must Include

- At least 3 community member voices
- Local economic data
- Visual evidence of community investment

# Avoid

- Overly produced feel
- Corporate executives (keep it grassroots)
```

### Adding Videos

```bash
plotline add ~/Footage/executive_director.mov
plotline add ~/Footage/community_liaison.mov
plotline add ~/Footage/homeowner_maria.mov
plotline add ~/Footage/homeowner_james.mov
plotline add ~/Footage/local_business_owner.mov
plotline add ~/Footage/tribal_elder.mov
```

---

## Results

### Interview Statistics

| Interview | Duration | Segments | Avg Score |
|-----------|----------|----------|-----------|
| Executive Director | 38 min | 71 | 0.66 |
| Community Liaison | 42 min | 78 | 0.68 |
| Homeowner Maria | 24 min | 45 | 0.72 |
| Homeowner James | 28 min | 52 | 0.69 |
| Local Business Owner | 31 min | 58 | 0.64 |
| Tribal Elder | 35 min | 65 | 0.71 |

### Theme Extraction

10 unified themes including Economic Opportunity (28 segments), Community Partnership (24 segments), and Stable Housing (22 segments).

### Narrative Arc

22 segments totaling 5:12 with strong coverage on all key messages.

---

## Cultural Sensitivity Review

The cultural flags pass identified 3 segments for community consultation:

1. **Tribal Elder, Segment 18** — Indigenous ceremony reference
2. **Community Liaison, Segment 24** — Historical displacement context
3. **Homeowner Maria, Segment 31** — Spiritual practice reference

All three were approved after consultation with community liaisons.

---

## Review Process

### Balancing Voices

| Speaker Type | Initial | Final |
|--------------|---------|-------|
| Staff | 8 | 5 |
| Community | 14 | 17 |

The compare report helped identify authentic community voices over polished staff takes.

---

## Export

```bash
plotline export --format edl --handle 12
```

22 approved segments, 5:12 duration.

---

## Lessons Learned

### What Worked

1. Cultural flags caught sensitive content early
2. Compare report prioritized authentic voices
3. Commercial-doc profile balanced authenticity with messaging

### Challenges

1. Cultural review required extra time
2. Voice balance needed rebalancing
3. 5 minutes felt tight

### Recommendations

1. Enable cultural flags for community projects
2. Budget time for cultural review
3. Prioritize community voices
4. Share with community before finalizing

---

## Related Examples

- **[Documentary Project](documentary.md)**
- **[Brand Video](brand-video.md)**

## Related Documentation

- **[Workflow Guide](../workflow-guide.md)**
- **[Export Guide](../export-guide.md)**
- **[Reports Guide](../reports-guide.md)**

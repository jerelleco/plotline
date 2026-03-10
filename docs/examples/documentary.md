# Example: Documentary Project

## Project Overview

**"The River Keepers"** is a 12-minute documentary about Indigenous water stewardship in the Pacific Northwest. The film features interviews with five Elders and community members about their relationship with the river, traditional ecological knowledge, and efforts to protect waterways for future generations.

**Project type:** Documentary
**Profile:** `documentary`
**Target duration:** 12 minutes
**Interviews:** 5 (3.5 hours raw footage)

---

## Project Setup

```bash
plotline init river-keepers --profile documentary
cd river-keepers
```

The documentary profile emphasizes emotional authenticity, natural pauses, and emergent narrative structure.

### Configuration

```yaml
project_name: river-keepers
project_profile: documentary
target_duration_seconds: 720
```

### Creative Brief

A simple brief guides the LLM toward the story's core themes:

```markdown
# Key Messages

- Water is a living relative, not a resource
- Indigenous knowledge spans generations
- Community action creates change

# Tone

Reverent, contemplative. Let subjects tell their own stories.
```

### Adding Videos

```bash
plotline add ~/Footage/elder_margaret.mov
plotline add ~/Footage/elder_thomas.mov
plotline add ~/Footage/community_youth.mov
plotline add ~/Footage/waterkeeper_director.mov
plotline add ~/Footage/tribal_historian.mov
```

### Running the Pipeline

```bash
plotline run
```

Processed all five interviews in approximately 45 minutes.

---

## Results

### Interview Statistics

| Interview | Duration | Segments | Avg Score |
|-----------|----------|----------|-----------|
| Elder Margaret | 47 min | 89 | 0.68 |
| Elder Thomas | 52 min | 94 | 0.71 |
| Community Youth | 23 min | 42 | 0.58 |
| Waterkeeper Director | 31 min | 56 | 0.64 |
| Tribal Historian | 38 min | 71 | 0.69 |

### Theme Extraction

The LLM identified 12 unified themes. Strongest:

1. **River as Teacher** — 34 segments across 4 interviews
2. **Intergenerational Knowledge** — 28 segments across 5 interviews
3. **Ceremony and Respect** — 19 segments across 3 interviews
4. **Community Action** — 24 segments across 4 interviews
5. **Loss and Memory** — 15 segments across 3 interviews

### Narrative Arc

23 segments totaling 11:40.

| Role | Count | Duration |
|------|-------|----------|
| Opening | 3 | 1:42 |
| Deepening | 8 | 4:31 |
| Turning Point | 4 | 2:18 |
| Climax | 3 | 1:56 |
| Resolution | 5 | 1:33 |

### Coverage Analysis

| Message | Coverage | Segments |
|---------|----------|----------|
| Water as living relative | Strong | 12 |
| Indigenous knowledge | Strong | 18 |
| Community action | Moderate | 8 |

---

## Review Process

### Editorial Decisions

Review took approximately 2 hours:

1. Listened to all 23 proposed segments
2. Rejected 3 segments for redundancy
3. Moved 2 segments for better narrative flow
4. Replaced 1 rejected segment with an alternate
5. Added editorial notes to 5 segments

### Cultural Sensitivity

The cultural flags pass identified 2 segments for review:

1. **Elder Margaret, segment 14** — References specific ceremony by name
   - Resolution: Approved with note to verify naming conventions
2. **Elder Thomas, segment 22** — Mentions sacred location
   - Resolution: Approved after consultation with Tribal Historian

---

## Export

```bash
plotline export --format edl --handle 12
```

Final EDL: 20 approved segments, 11:42 duration, 12-frame handles.

### Import to DaVinci Resolve

Timeline imported cleanly with all media linked. Editorial notes appeared as clip markers.

---

## Lessons Learned

### What Worked Well

1. Theme extraction identified core ideas without prompting
2. Delivery scoring prioritized emotionally resonant segments
3. Cultural flags caught sensitive content before export
4. Alternates provided good backup options

### Challenges

1. Multiple speakers covered same themes — compare report was essential
2. Some Whisper segments split mid-sentence
3. "Community action" message needed strengthening

### Recommendations

1. Attach a brief early — helps focus LLM on core themes
2. Use compare report for multi-interview projects
3. Review cultural flags carefully — human judgment still required
4. Plan for gaps — additional interviews if coverage is weak

---

## Related Examples

- **[Brand Video](brand-video.md)**
- **[Commercial Documentary](commercial-doc.md)**

## Related Documentation

- **[Workflow Guide](../workflow-guide.md)**
- **[Export Guide](../export-guide.md)**
- **[Reports Guide](../reports-guide.md)**

# Data Architecture & Pipeline Patterns

**Domain:** Single-user scholarly research platform (philosophy PhD)
**Researched:** 2026-02-28
**Overall confidence:** HIGH (directory patterns, tool choices) / MEDIUM (Obsidian integration, lifecycle policies)

---

## Executive Summary

The Dionysus workstation has three storage tiers (/home at 343GB, /scratch at 92GB, /data at 1.8TB) but currently uses them inconsistently. The /data tier has empty placeholder directories (corpora/, embeddings/, models/, experiments/) while actual university data is split between /home/workspace/university/ and /data/university/ with no clear separation logic. The /scratch tier has an existing lecture-processing structure (incoming/models/output/processing/temp) that demonstrates the right pattern but was never generalized.

The recommended architecture uses a **canonical scholarly data directory** at `/data/scholarly/` with clear separation of raw inputs, processed outputs, embeddings, and working state. Processing happens on /scratch (temp, disposable), final outputs land on /data (permanent), and /home stays exclusively for code and active development. Symlinks from /home/workspace/ into /data/ make data discoverable without duplicating it on the space-constrained /home partition.

For pipeline automation, **systemd path units** are the right foundation for routine file-watch triggers (audio appears, transcription starts) because they integrate with the systemd service infrastructure already recommended in the service deployment research. Python `watchdog` is overkill for simple triggers. For multi-step pipeline orchestration, **`just` (justfile)** is the right fit: lighter than Prefect/Celery, more structured than shell scripts, with built-in listing, documentation, and error handling. Prefect is enterprise tooling that a single researcher does not need.

For embedding storage, **sqlite-vec** is the right choice for experimentation because each experiment gets its own .db file, there is no server to manage, files are portable and deletable, and the philo-rag-simple project already uses it. pgvector (already running) serves as the "graduated" home for embeddings that prove their worth in production services. FAISS stays as an in-memory option for notebooks and one-off exploration.

Obsidian can serve as an **access interface** to the scholarly data layer, but should NOT be the data store itself. The pattern is: processing pipelines write markdown files and metadata into a designated area, and an Obsidian vault includes that area (directly or via symlink) for reading and annotating. The vault is a view over the data, not the source of truth.

---

## 1. Directory Structure for Scholarly Data

### Current State (Problems)

The existing layout has several issues:

- `/data/corpora/`, `/data/embeddings/`, `/data/models/`, `/data/experiments/` all exist but are empty (4K each)
- University data is split: `/home/workspace/university/` (4.1GB, SyncThing-managed) and `/data/university/` (2.7GB)
- `/scratch/lecture-processing/` has a good pattern (incoming/models/output/processing/temp) but is the only pipeline with structure
- HuggingFace models (30GB) live in `~/.cache/huggingface/` instead of a managed location
- No convention distinguishes "raw input that must be preserved" from "generated output that can be regenerated"

### Recommended Layout

```
/data/scholarly/                    # Canonical scholarly data root
  raw/                              # Immutable inputs (never modified after ingest)
    pdfs/                           # Scholarly PDFs, organized by source
      calibre-exports/              # PDFs from Calibre library
      zlibrary/                     # Downloaded via zlibrary-mcp
      scans/                        # Scanned documents
      course-readings/              # Assigned readings
    epubs/                          # EPUB files
    audio/                          # Lecture recordings, seminars, interviews
      recordings/                   # Raw recordings from phone/microphone
      downloaded/                   # Podcasts, downloaded lectures
    handwritten/                    # Scanned handwritten notes, photos of whiteboard
    misc/                           # Other raw inputs

  processed/                        # Generated outputs (can be regenerated from raw/)
    transcripts/                    # Audio -> text (Whisper output)
      YYYY-MM-DD_source-desc/       # Each transcription job gets a dated folder
        transcript.md               # Markdown transcript
        transcript.json             # Structured output with timestamps
        metadata.json               # Processing params, model, duration, quality score
    ocr/                            # Scans -> text (PaddleOCR/scholardoc output)
      YYYY-MM-DD_source-desc/
        text.md
        structured.json             # ScholarDocument format
        metadata.json
    structured/                     # PDFs/EPUBs -> structured text (scholardoc output)
      by-work/                      # Keyed by work identifier
        hegel-phenomenology/
          scholardoc.json           # Full ScholarDocument
          chapters/                 # Chapter-level extracts
          metadata.json
    audio-generated/                # Text -> audiobooks (audiobookify output)
      by-work/

  embeddings/                       # Vector indexes and embedding data
    experiments/                    # Experimental embedding runs
      YYYY-MM-DD_desc/              # Each experiment is self-contained
        index.db                    # sqlite-vec database
        config.json                 # Model, chunk size, parameters
        eval.json                   # Quality metrics if evaluated
    production/                     # Graduated embeddings (used by running services)
      philo-rag/                    # philo-rag-simple's index
      philograph/                   # philograph-mcp's data

  knowledge/                        # Higher-order derived data
    graphs/                         # Knowledge graph exports
    connections/                    # Cross-reference data
    annotations/                   # User annotations, marginalia

  vault/                            # Obsidian-accessible layer (see section 3)
    notes/                          # User-authored notes
    transcripts/                    # Symlink -> processed/transcripts/ (read-only view)
    readings/                       # Note-per-work with links to processed/

/data/models/                       # ML models (shared across projects)
  huggingface/                      # HuggingFace hub cache (move from ~/.cache)
  whisper/                          # Whisper model weights
  sentence-transformers/            # Embedding models

/scratch/                           # Temp processing (cleaned weekly by cron)
  pipeline/                         # Active pipeline working directories
    {job-id}/                       # Each job gets a UUID directory
      input/                        # Copied/linked input files
      working/                      # Intermediate outputs
      output/                       # Final outputs (moved to /data on completion)
  downloads/                        # Staging area for incoming files
  notebooks/                        # Throwaway Jupyter exploration

/home/rookslog/workspace/
  projects/                         # Code only (no large data files)
  university/                       # SyncThing-managed coursework (keep as-is)
  data -> /data/scholarly            # Symlink for convenience
```

### Tier Assignment Logic

| Tier | What Goes Here | Why | Lifecycle |
|------|---------------|-----|-----------|
| `/data/scholarly/raw/` | Original inputs: PDFs, recordings, scans | Immutable, irreplaceable, 1.4TB free | Permanent |
| `/data/scholarly/processed/` | Generated outputs: transcripts, OCR, structured text | Reproducible but expensive to regenerate | Permanent (with metadata) |
| `/data/scholarly/embeddings/` | Vector indexes, sqlite-vec databases | Cheap to regenerate, but annoying | Permanent for production, 90-day for experiments |
| `/data/models/` | ML model weights | Large, slow to download, shared across projects | Permanent |
| `/scratch/pipeline/` | Active processing jobs | Temporary, disposable | Auto-cleaned weekly |
| `/scratch/downloads/` | Incoming files before classification | Staging area | Auto-cleaned weekly |
| `/home/workspace/` | Source code, configs, docs | Active development | Git-managed |

### Naming Conventions

**Processed output directories:**
```
YYYY-MM-DD_source-description/
  2026-02-28_hegel-phenomenology-ch4/
  2026-03-01_lecture-kant-cpr-session12/
  2026-03-05_reading-group-deleuze/
```

**Embedding experiment directories:**
```
YYYY-MM-DD_model-chunksize-description/
  2026-02-28_minilm-512-hegel-corpus/
  2026-03-01_bge-large-256-all-philosophy/
```

**Metadata files:** Every generated output directory MUST contain a `metadata.json` with:
```json
{
  "created": "2026-02-28T14:30:00-05:00",
  "source": "/data/scholarly/raw/audio/recordings/2026-02-28_lecture.m4a",
  "pipeline": "transcribe",
  "pipeline_version": "1.2.0",
  "tool": "faster-whisper",
  "tool_version": "1.0.0",
  "model": "large-v3",
  "params": { "language": "en", "beam_size": 5 },
  "duration_seconds": 142,
  "input_hash": "sha256:abc123...",
  "regenerable": true
}
```

This metadata is what prevents data sprawl. When you find a mystery directory six months later, the metadata tells you exactly what it is, where it came from, and whether you can safely delete it.

**Confidence:** HIGH. Directory patterns derived from academic research data management best practices (Imperial College, Duke, Oregon State guidelines) combined with direct observation of this workstation's existing patterns.

---

## 2. File-Watch Pipeline Patterns

### Recommendation: systemd Path Units

For the primary use case -- "audio file appears in a directory, transcription runs automatically" -- **systemd path units** are the right tool. They use the Linux kernel's inotify API, require zero running daemons, integrate with journald for logging, and restart automatically on failure.

**Why not the alternatives:**

| Tool | Verdict | Reason |
|------|---------|--------|
| **systemd path units** | USE THIS | Zero-daemon, kernel-level, integrates with existing systemd service infrastructure |
| Python watchdog | Overkill | Requires a running Python process; use only if path units can't express the trigger |
| inotifywait (shell) | Too fragile | No auto-restart, no logging integration, easy to miss events during processing |
| Celery | Way overkill | Enterprise message queue; single user does not need Redis/RabbitMQ broker |
| Prefect | Overkill | Cloud-oriented workflow engine; adds complexity without proportional value for single-user |

### Implementation Pattern

A file-watch pipeline needs three files:

**1. Path unit** (`~/.config/systemd/user/transcribe-incoming.path`):
```ini
[Unit]
Description=Watch for new audio files to transcribe

[Path]
DirectoryNotEmpty=/data/scholarly/raw/audio/recordings/incoming/
MakeDirectory=yes

[Install]
WantedBy=default.target
```

**2. Service unit** (`~/.config/systemd/user/transcribe-incoming.service`):
```ini
[Unit]
Description=Transcribe incoming audio files

[Service]
Type=oneshot
ExecStart=/home/rookslog/scripts/pipelines/transcribe.sh
StandardOutput=journal
StandardError=journal

# Prevent overlapping runs
ExecStartPre=/usr/bin/flock -n /tmp/transcribe.lock echo "Lock acquired"
```

**3. Pipeline script** (`~/scripts/pipelines/transcribe.sh`):
```bash
#!/bin/bash
set -euo pipefail

INCOMING="/data/scholarly/raw/audio/recordings/incoming"
SCRATCH="/scratch/pipeline/transcribe-$(date +%s)"
OUTPUT="/data/scholarly/processed/transcripts"

mkdir -p "$SCRATCH"

for file in "$INCOMING"/*.{m4a,mp3,wav,ogg}; do
    [ -f "$file" ] || continue

    name=$(basename "$file" | sed 's/\.[^.]*$//')
    outdir="$OUTPUT/$(date +%Y-%m-%d)_$name"
    mkdir -p "$outdir"

    # Process on /scratch (fast SSD, disposable)
    cp "$file" "$SCRATCH/"

    # Run transcription (faster-whisper)
    python3 -c "
from faster_whisper import WhisperModel
import json, sys
model = WhisperModel('large-v3', device='cuda', compute_type='float16')
segments, info = model.transcribe('$SCRATCH/$(basename "$file")')
# ... write transcript.md, transcript.json, metadata.json to $outdir
"

    # Move original from incoming to permanent raw storage
    mv "$file" "/data/scholarly/raw/audio/recordings/"

    echo "Transcribed: $name -> $outdir"
done

# Cleanup scratch
rm -rf "$SCRATCH"
```

### When to Use Which Trigger

| Pattern | Trigger | Example |
|---------|---------|---------|
| **File appears** | systemd PathUnit (DirectoryNotEmpty) | Audio recording synced from phone |
| **Manual run** | `just transcribe FILE` | Process a specific file on demand |
| **Scheduled batch** | systemd timer | Nightly batch of queued PDFs |
| **Complex multi-step** | `just pipeline-name ARGS` | Full pipeline: record -> transcribe -> embed -> notify |

**Confidence:** HIGH. systemd path units are stable, documented in official freedesktop.org docs, and already the recommended service management approach from the parallel service-deployment research.

---

## 3. Obsidian Vault as Data Integration Point

### Verdict: YES, but as a View Layer, NOT the Data Store

Obsidian can serve as the human interface to the scholarly data layer, but with important constraints.

### What Works

**The pattern:** Obsidian vault at `/data/scholarly/vault/` contains:
- User-authored notes (the vault's native content)
- Markdown files generated by pipelines (transcripts, reading summaries)
- Links to processed documents via relative paths or custom URI schemes

**Why this works for a philosophy researcher:**
- Notes are plain markdown files -- accessible from any editor, CLI, or script
- Wikilinks (`[[concept]]`) create the knowledge web naturally
- Frontmatter (YAML) stores structured metadata that scripts can read/write
- Community plugins extend functionality (Dataview for queries, Templater for automation)
- The vault syncs naturally via SyncThing to Apollo for mobile reading/writing

### What Does NOT Work

**Symlinks are unreliable.** Obsidian nominally supports symlinks since v0.11.1 but officially does not recommend them. Reported issues include:
- App hangs when vault contains symlink structures
- Vault indexing failures on mobile
- Cross-drive symlinks break drag-and-drop
- Sync conflicts when symlink targets are managed by other tools

**Large binary files in the vault are wasteful.** PDFs, audio files, and model weights should NOT be in the vault. Link to them instead.

### Recommended Architecture

```
/data/scholarly/vault/              # Obsidian vault root
  .obsidian/                        # Obsidian config
  notes/                            # User-authored notes
    daily/                          # Daily notes
    concepts/                       # Philosophy concepts
    readings/                       # One note per text being read
    projects/                       # Research project notes
  generated/                        # Pipeline-generated markdown (written by scripts)
    transcripts/                    # Markdown transcripts from audio
    summaries/                      # Auto-generated reading summaries
    extracts/                       # Key passages extracted by scholardoc
  templates/                        # Obsidian templates
  attachments/                      # Small images, diagrams only
```

**Key principle:** Pipelines write INTO `vault/generated/`. They do NOT read from or depend on the vault. The vault is a downstream consumer of processed data, not an upstream source.

**Linking to external files from vault notes:**
```markdown
---
source_pdf: "/data/scholarly/raw/pdfs/calibre-exports/hegel-phenomenology.pdf"
scholardoc: "/data/scholarly/processed/structured/by-work/hegel-phenomenology/"
embedding_index: "/data/scholarly/embeddings/production/philo-rag/index.db"
---

# Hegel - Phenomenology of Spirit

## Reading Notes
...

## Key Passages
![[generated/extracts/hegel-phenomenology/ch4-lordship-bondage.md]]
```

The frontmatter contains absolute paths to data files. Obsidian won't follow these natively, but scripts and MCP servers can read the frontmatter to locate associated data. The Dataview plugin can query frontmatter across all notes.

### SyncThing Integration

The vault at `/data/scholarly/vault/` syncs to Apollo via SyncThing. The `generated/` subdirectory syncs too (it's just markdown). Large processed data stays on Dionysus. This means:
- On the Mac: read notes, write notes, browse transcripts, search concepts
- On Dionysus: run pipelines that populate `generated/`, manage full data layer

**Confidence:** MEDIUM. The architecture is sound in principle, but Obsidian's symlink handling has known issues. The recommendation to avoid symlinks and instead use direct file placement in the vault is based on community reports of problems. The Obsidian-as-view-layer pattern needs testing with actual vault size and SyncThing interaction.

---

## 4. Embedding Storage

### Recommendation: sqlite-vec for Experiments, pgvector for Production

The user already uses both sqlite-vec (philo-rag-simple) and has pgvector infrastructure (mcp-vector-database docker-compose). The right pattern is to formalize their roles.

### Storage Strategy

| Stage | Storage | Why |
|-------|---------|-----|
| **Exploration** (Jupyter, one-offs) | FAISS in-memory | Zero setup, fast iteration, throw away when done |
| **Experiments** (trying models, chunk sizes) | sqlite-vec (.db files) | Self-contained, portable, deletable, no server needed |
| **Production** (running services) | pgvector (PostgreSQL) | Concurrent access, SQL queries, joins with metadata |

### Why sqlite-vec for Experimentation

1. **Each experiment is a single .db file.** Copy it, delete it, compare two experiments by loading both files. No database migrations, no schema conflicts.
2. **Already in use.** philo-rag-simple has a working `SQLiteVecStore` class. The pattern is proven in this codebase.
3. **No server overhead.** PostgreSQL is running for production services. Experiments should not touch production infrastructure.
4. **Portable.** Move a .db file to /scratch for fast access, copy to /data for preservation. Try a new embedding model: create a new .db, keep the old one for comparison.

### Experiment Lifecycle

```
/data/scholarly/embeddings/
  experiments/
    2026-02-28_minilm-512-hegel/
      index.db                 # sqlite-vec database
      config.json              # {"model": "paraphrase-multilingual-MiniLM-L12-v2",
                               #  "chunk_size": 512, "overlap": 64,
                               #  "corpus": "/data/scholarly/processed/structured/by-work/hegel*"}
      eval.json                # {"mrr@10": 0.72, "recall@5": 0.85, "notes": "Good for short queries"}
    2026-03-01_bge-large-256-hegel/
      index.db
      config.json
      eval.json                # Compare with previous: {"mrr@10": 0.78, "recall@5": 0.91}
  production/
    philo-rag/
      index.db                 # The "winner" from experiments, used by running service
      config.json
```

### When to Graduate to pgvector

Move an embedding index to pgvector when:
- It serves a persistent, always-on service (e.g., philograph-mcp)
- Multiple services need to query the same embeddings concurrently
- You need SQL JOINs between embeddings and structured metadata
- The dataset exceeds what sqlite-vec handles comfortably (~1M vectors)

### Current Embedding Models on This Machine

Found in `~/.cache/huggingface/hub/`:
- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (384 dims) -- used by philo-rag-simple
- `sentence-transformers/all-MiniLM-L6-v2` (384 dims) -- general purpose
- `Systran/faster-whisper-large-v3` -- for transcription, not embeddings
- `Systran/faster-whisper-medium` -- smaller transcription model

For philosophy text specifically, the multilingual MiniLM is a reasonable default. For experimentation, try `BAAI/bge-large-en-v1.5` (1024 dims, better for long passages) or `nomic-ai/nomic-embed-text-v1.5` (768 dims, Matryoshka dimensions). Both fit on the GTX 1080 Ti.

**Confidence:** HIGH. Based on direct observation of existing code (philo-rag-simple's vector_store.py uses both FAISS and sqlite-vec), existing infrastructure (mcp-vector-database's pgvector docker-compose), and well-documented capabilities of each tool.

---

## 5. Data Lifecycle & Preventing Sprawl

### The Core Problem

A single researcher who experiments generates:
- Multiple transcription attempts with different models/params
- Embedding indexes from different models and chunk sizes
- OCR outputs from evolving pipelines (scholardoc is actively developed)
- Intermediate files from abandoned experiments
- Downloaded papers and recordings that never get processed

Without discipline, /data fills up with mystery directories. The metadata.json convention (section 1) is the first defense. The lifecycle policy is the second.

### Lifecycle Policies

| Data Category | Retention | Action at Expiry |
|---------------|-----------|------------------|
| Raw inputs (`raw/`) | Permanent | Never auto-delete |
| Production processed (`processed/`) | Permanent | Manual review annually |
| Experiment embeddings (`embeddings/experiments/`) | 90 days | Auto-flag for review (not auto-delete) |
| Scratch pipeline jobs (`/scratch/pipeline/`) | 7 days | Auto-delete (already in cron) |
| Scratch downloads (`/scratch/downloads/`) | 7 days | Auto-delete |
| Production embeddings (`embeddings/production/`) | Permanent | Replaced only by explicit promotion |
| Vault generated content (`vault/generated/`) | Tied to source | Regenerate if source reprocessed |

### Automated Maintenance Script

`~/scripts/audit-scholarly-data.sh` (run weekly alongside existing audit scripts):

```bash
#!/bin/bash
# Audit scholarly data: flag stale experiments, check metadata, report sizes

SCHOLARLY="/data/scholarly"
REPORT="/home/rookslog/docs/scholarly-data-audit.md"

echo "# Scholarly Data Audit - $(date +%Y-%m-%d)" > "$REPORT"
echo "" >> "$REPORT"

# Size report
echo "## Storage Usage" >> "$REPORT"
du -sh "$SCHOLARLY"/*/ 2>/dev/null >> "$REPORT"
echo "" >> "$REPORT"

# Flag experiments older than 90 days without eval.json
echo "## Stale Experiments (>90 days, no evaluation)" >> "$REPORT"
find "$SCHOLARLY/embeddings/experiments" -maxdepth 1 -type d -mtime +90 | while read dir; do
    if [ ! -f "$dir/eval.json" ]; then
        echo "- $dir ($(du -sh "$dir" | cut -f1))" >> "$REPORT"
    fi
done
echo "" >> "$REPORT"

# Flag processed outputs without metadata.json
echo "## Missing Metadata" >> "$REPORT"
find "$SCHOLARLY/processed" -maxdepth 2 -type d | while read dir; do
    if [ "$(ls -A "$dir" 2>/dev/null)" ] && [ ! -f "$dir/metadata.json" ]; then
        echo "- $dir" >> "$REPORT"
    fi
done
echo "" >> "$REPORT"

# Total counts
echo "## Counts" >> "$REPORT"
echo "- Raw PDFs: $(find "$SCHOLARLY/raw/pdfs" -name "*.pdf" 2>/dev/null | wc -l)" >> "$REPORT"
echo "- Raw audio: $(find "$SCHOLARLY/raw/audio" -type f 2>/dev/null | wc -l)" >> "$REPORT"
echo "- Transcripts: $(find "$SCHOLARLY/processed/transcripts" -maxdepth 1 -type d 2>/dev/null | wc -l)" >> "$REPORT"
echo "- Embedding experiments: $(find "$SCHOLARLY/embeddings/experiments" -maxdepth 1 -type d 2>/dev/null | wc -l)" >> "$REPORT"
echo "- Production indexes: $(find "$SCHOLARLY/embeddings/production" -maxdepth 1 -type d 2>/dev/null | wc -l)" >> "$REPORT"
```

### Naming Discipline

**Rule: Every directory in `processed/` and `embeddings/experiments/` MUST have:**
1. A date prefix: `YYYY-MM-DD_`
2. A descriptive slug: `source-description` (lowercase, hyphens)
3. A `metadata.json` file

**The audit script flags violations.** This is enforcement through visibility, not restrictions. The weekly audit report shows what's missing, and the user fixes it.

### Dealing with the Existing Sprawl

Before the new structure can work, existing data needs migration:

| Current Location | Destination | Action |
|-----------------|-------------|--------|
| `/data/university/recordings/` (2.7GB) | `/data/scholarly/raw/audio/recordings/` | Move |
| `/data/university/transcripts/` | `/data/scholarly/processed/transcripts/` | Move |
| `/home/workspace/university/philosophy-notes/` (78MB) | `/data/scholarly/vault/notes/` | Move, set up SyncThing |
| `~/.cache/huggingface/` (30GB) | `/data/models/huggingface/` | Move, symlink back |
| `/data/corpora/` (empty) | Remove | Delete empty placeholder |
| `/data/embeddings/` (empty) | Remove (replaced by `/data/scholarly/embeddings/`) | Delete empty placeholder |
| `/data/experiments/` (empty) | Remove | Delete empty placeholder |
| `/data/datasets/` (empty) | Remove | Delete empty placeholder |

**Confidence:** HIGH for the policies and structure. MEDIUM for the migration plan (SyncThing interactions need careful handling).

---

## 6. Pipeline Orchestration

### Recommendation: `just` (Justfile) + systemd Path Units

The pipeline orchestration has two layers:

1. **Triggers** (when to run): systemd path units for file-watch, systemd timers for scheduled, `just` for manual
2. **Execution** (what to run): `just` recipes that call pipeline scripts

### Why `just`

| Feature | `just` | Makefile | Shell scripts | Prefect |
|---------|--------|----------|---------------|---------|
| Learning curve | Low | Medium (tab sensitivity, .PHONY) | Low | High |
| Command listing | `just --list` built-in | Requires grep hack | Manual | Web UI |
| Error handling | Configurable per-recipe | Silent failures common | `set -e` | Retries, backoff |
| Cross-platform | Yes (Rust binary) | Mostly | Bash-only | Yes |
| Dependency tracking | No (by design) | Yes | No | Yes |
| Server required | No | No | No | Yes (Prefect server) |
| Documentation | Inline comments | .PHONY targets | Comments | Decorators |

`just` is explicitly a **command runner**, not a build system. This is exactly right for pipelines that are "run this sequence of steps" rather than "rebuild only what changed."

### Justfile Structure

```just
# ~/scripts/pipelines/justfile

# List available pipelines
default:
    @just --list

# === TRANSCRIPTION ===

# Transcribe a single audio file
transcribe FILE:
    #!/bin/bash
    set -euo pipefail
    source ~/.env
    name=$(basename "{{FILE}}" | sed 's/\.[^.]*$//')
    outdir="/data/scholarly/processed/transcripts/$(date +%Y-%m-%d)_${name}"
    mkdir -p "$outdir"
    echo "Transcribing {{FILE}} -> $outdir"
    conda run -n whisper python ~/scripts/pipelines/transcribe.py \
        --input "{{FILE}}" \
        --output "$outdir" \
        --model large-v3
    echo "Done: $outdir"

# Transcribe all files in incoming directory
transcribe-incoming:
    #!/bin/bash
    set -euo pipefail
    for f in /data/scholarly/raw/audio/recordings/incoming/*.{m4a,mp3,wav,ogg}; do
        [ -f "$f" ] || continue
        just transcribe "$f"
        mv "$f" /data/scholarly/raw/audio/recordings/
    done

# === OCR & DOCUMENT PROCESSING ===

# Process a PDF through scholardoc
process-pdf FILE:
    #!/bin/bash
    set -euo pipefail
    cd ~/workspace/projects/scholardoc
    uv run python -m scholardoc process "{{FILE}}" \
        --output "/data/scholarly/processed/structured/by-work/"

# OCR a scanned document via PaddleOCR
ocr-scan FILE:
    #!/bin/bash
    set -euo pipefail
    curl -X POST http://localhost:8765/ocr \
        -F "file=@{{FILE}}" \
        -o "/data/scholarly/processed/ocr/$(date +%Y-%m-%d)_$(basename '{{FILE}}' | sed 's/\.[^.]*$//').json"

# === EMBEDDINGS ===

# Create embedding experiment
embed CORPUS MODEL="paraphrase-multilingual-MiniLM-L12-v2" CHUNK_SIZE="512":
    #!/bin/bash
    set -euo pipefail
    desc=$(basename "{{CORPUS}}")
    model_short=$(echo "{{MODEL}}" | sed 's/.*\///' | tr '[:upper:]' '[:lower:]')
    outdir="/data/scholarly/embeddings/experiments/$(date +%Y-%m-%d)_${model_short}-{{CHUNK_SIZE}}-${desc}"
    mkdir -p "$outdir"
    python ~/scripts/pipelines/embed.py \
        --corpus "{{CORPUS}}" \
        --model "{{MODEL}}" \
        --chunk-size "{{CHUNK_SIZE}}" \
        --output "$outdir"

# Promote experiment to production
embed-promote EXPERIMENT SERVICE:
    #!/bin/bash
    set -euo pipefail
    src="/data/scholarly/embeddings/experiments/{{EXPERIMENT}}"
    dst="/data/scholarly/embeddings/production/{{SERVICE}}"
    [ -d "$src" ] || { echo "Experiment not found: $src"; exit 1; }
    [ -f "$src/eval.json" ] || { echo "WARNING: No eval.json in experiment. Promote anyway? (y/n)"; read -r confirm; [ "$confirm" = "y" ] || exit 1; }
    mkdir -p "$(dirname "$dst")"
    rm -rf "$dst"
    cp -r "$src" "$dst"
    echo "Promoted $src -> $dst"

# === FULL PIPELINES ===

# Record -> Transcribe -> Embed (full pipeline for a lecture recording)
lecture-pipeline FILE:
    #!/bin/bash
    set -euo pipefail
    echo "=== Step 1: Transcribe ==="
    just transcribe "{{FILE}}"

    transcript_dir=$(ls -td /data/scholarly/processed/transcripts/$(date +%Y-%m-%d)_* | head -1)
    echo "=== Step 2: Embed transcript ==="
    just embed "$transcript_dir" "paraphrase-multilingual-MiniLM-L12-v2" "512"

    echo "=== Step 3: Generate vault note ==="
    python ~/scripts/pipelines/generate-vault-note.py \
        --transcript "$transcript_dir" \
        --output "/data/scholarly/vault/generated/transcripts/"

    echo "=== Complete ==="
    echo "Transcript: $transcript_dir"
    echo "Vault note generated"

# === MAINTENANCE ===

# Audit scholarly data
audit:
    ~/scripts/audit-scholarly-data.sh

# Show experiment comparison
compare-experiments EXP1 EXP2:
    #!/bin/bash
    echo "=== {{EXP1}} ==="
    cat "/data/scholarly/embeddings/experiments/{{EXP1}}/eval.json" 2>/dev/null || echo "No eval.json"
    echo ""
    echo "=== {{EXP2}} ==="
    cat "/data/scholarly/embeddings/experiments/{{EXP2}}/eval.json" 2>/dev/null || echo "No eval.json"
```

### How Triggers Connect to `just`

```
[systemd path unit] --triggers--> [systemd service] --runs--> just transcribe-incoming
[systemd timer]     --triggers--> [systemd service] --runs--> just audit
[user CLI]          --runs------> just transcribe FILE
[user CLI]          --runs------> just lecture-pipeline FILE
```

The systemd units handle "when" and "reliability" (restart on failure, logging to journald). `just` handles "what" (the actual pipeline steps, argument passing, documentation).

### Failure Handling

`just` recipes use `set -euo pipefail` so any step failure stops the pipeline. For systemd-triggered runs, failures appear in `journalctl --user -u transcribe-incoming.service`. For manual runs, failures print to the terminal.

For notification on failure (optional enhancement):
```bash
# In the systemd service unit:
ExecStopPost=/bin/bash -c 'if [ "$SERVICE_RESULT" != "success" ]; then echo "Pipeline failed: transcribe-incoming" | mail -s "Pipeline failure" logan@example.com; fi'
```

Or simpler: write failures to a log file that the weekly audit script checks.

**Confidence:** HIGH for `just` as the command runner. It is a mature, well-documented tool that matches the single-researcher use case exactly. MEDIUM for the specific justfile recipes (they need testing with actual tools like faster-whisper, scholardoc).

---

## 7. Implementation Priorities

### Phase 1: Create Directory Structure

1. Create `/data/scholarly/` with the full directory tree
2. Create `/data/models/`
3. Move existing data to new locations (see migration table in section 5)
4. Move HuggingFace cache: `mv ~/.cache/huggingface /data/models/huggingface && ln -s /data/models/huggingface ~/.cache/huggingface`
5. Create convenience symlink: `ln -s /data/scholarly /home/rookslog/workspace/data`
6. Clean up empty /data placeholders

### Phase 2: Install Tools & First Pipeline

1. Install `just`: `curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/bin`
2. Create `~/scripts/pipelines/justfile` with transcription recipe
3. Install faster-whisper in a conda env (GPU support via existing CUDA 11.8)
4. Test: drop an audio file, run `just transcribe file.m4a`, verify output in `/data/scholarly/processed/transcripts/`

### Phase 3: Automate with systemd Path Units

1. Create path unit for incoming audio
2. Create corresponding service unit
3. Enable and test end-to-end: phone recording syncs to incoming/ -> transcription runs -> output in processed/

### Phase 4: Obsidian Integration

1. Create vault at `/data/scholarly/vault/`
2. Set up SyncThing to sync vault to Apollo
3. Create vault note template with frontmatter linking to data paths
4. Add `generate-vault-note.py` script to create notes from processed outputs

### Phase 5: Embedding Experimentation Framework

1. Formalize experiment directory pattern
2. Create `just embed` and `just embed-promote` recipes
3. Write comparison tooling
4. Migrate philo-rag-simple's index to `/data/scholarly/embeddings/production/philo-rag/`

---

## Key Sources

- [Imperial College London - Naming files and folders](https://www.imperial.ac.uk/research-and-innovation/support-for-staff/scholarly-communication/research-data-management/organising-and-describing-data/naming-files-and-folders/)
- [Duke University - Organization and File Names](https://guides.library.duke.edu/c.php?g=633433&p=4429283)
- [systemd.path - freedesktop.org](https://www.freedesktop.org/software/systemd/man/latest/systemd.path.html)
- [Putorius - Using systemd Path Units](https://www.putorius.net/systemd-path-units.html)
- [sqlite-vec GitHub](https://github.com/asg017/sqlite-vec)
- [sqlite-vec stable release announcement](https://alexgarcia.xyz/blog/2024/sqlite-vec-stable-release/index.html)
- [Obsidian Forum - Managing Large Files and External Resources](https://forum.obsidian.md/t/managing-large-files-and-external-resources-in-obsidian-vaults/93829)
- [Obsidian Forum - Science Research Vault for Academics](https://forum.obsidian.md/t/science-research-vault-a-structured-workflow-for-academics/95589)
- [just GitHub - Task runner](https://github.com/casey/just)
- [faster-whisper GitHub](https://github.com/SYSTRAN/faster-whisper)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [Instaclustr pgvector 2026 guide](https://www.instaclustr.com/education/vector-database/pgvector-key-features-tutorial-and-pros-and-cons-2026-guide/)
- [FAISS vs pgvector comparison](https://zilliz.com/comparison/faiss-vs-pgvector)

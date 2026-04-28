---
slice: 4 (Artifact lifecycle + extension surfaces + migration tooling + distribution + light contribution-culture probe)
date: 2026-04-28
agent: codex GPT-5.5 high
status: complete
---

# Slice 4 output — Artifact lifecycle + extension surfaces + migration tooling + distribution + light contribution-culture probe

## (i) What I read

### Slice inputs

- Dispatch preamble: `.planning/gsd-2-uplift/orchestration/preamble.md`.
- Slice spec: `.planning/gsd-2-uplift/orchestration/slice-04-artifact-lifecycle.md`.

### gsd-2 README and project docs

- `README.md:1-80`, package identity, install framing, and extension-framework claims.
- `README.md:260-275`, migration claims for old GSD `.planning` projects.
- `README.md:620-625`, debug and deprecated agent-instruction surfaces.
- `CONTRIBUTING.md:1-220`, contribution process, PR requirements, extension contribution guidance, and review protocol.
- `CONTRIBUTING.md:400-428`, local development and security reporting.
- `docs/extension-sdk/README.md:1-110`, extension SDK overview, extension layout, allowed imports, and discovery locations.
- `docs/extension-sdk/manifest-spec.md:1-181`, extension manifest fields, tiers, validation, registry behavior, and startup flow.
- `docs/extension-sdk/building-extensions.md:11-40`, `129-140`, `746-756`, extension registration examples and tool-surface management.
- `docs/user-docs/migration.md:1-48`, user-facing migration command and supported v1-to-v2 migration shape.
- `src/resources/GSD-WORKFLOW.md:42-66`, `.gsd` artifact layout.
- `src/resources/GSD-WORKFLOW.md:72-120`, milestone roadmap schema.
- `src/resources/GSD-WORKFLOW.md:172-210`, task plan and state-file schema.
- `src/resources/GSD-WORKFLOW.md:271-359`, context, research, planning, and execution artifact lifecycle.
- `src/resources/GSD-WORKFLOW.md:383-407`, verification and summary artifact examples.
- `src/resources/GSD-WORKFLOW.md:459-533`, completion update protocol, `continue.md`, and state-cache semantics.

### gsd-2 source: artifacts and lifecycle

- `src/resources/extensions/gsd/paths.ts:1-9`, current vs legacy path conventions.
- `src/resources/extensions/gsd/paths.ts:145-215`, milestone/slice/task filename and resolver behavior.
- `src/resources/extensions/gsd/paths.ts:259-303`, root `.gsd` file names and `.gsd` root resolution.
- `src/resources/extensions/gsd/paths.ts:344-405`, `.gsd` probing and runtime-file resolution.
- `src/resources/extensions/gsd/init-wizard.ts:1-7`, init wizard purpose.
- `src/resources/extensions/gsd/init-wizard.ts:265-340`, bootstrap writes `.gsd`, preferences, database, gitignore, codebase, state, and workflow MCP setup.
- `src/resources/extensions/gsd/init-wizard.ts:347-380`, migration offer from detected `.planning`.
- `src/resources/extensions/gsd/init-wizard.ts:516-535`, initial directory creation and optional `.gsd/CONTEXT.md`.
- `src/resources/extensions/gsd/repo-identity.ts:1-7`, external repo-state model.
- `src/resources/extensions/gsd/repo-identity.ts:37-79`, `repo-meta.json` creation.
- `src/resources/extensions/gsd/migrate-external.ts:1-7`, in-project `.gsd` to external-state migration purpose.
- `src/resources/extensions/gsd/migrate-external.ts:22-35`, external-state migration algorithm summary.
- `src/resources/extensions/gsd/migrate-external.ts:36-84`, migration skip/fail conditions.
- `src/resources/extensions/gsd/migrate-external.ts:90-173`, copy, symlink, verification, cleanup, and nonfatal untracking behavior.
- `src/resources/extensions/gsd/migrate-external.ts:176-210`, rollback and recovery behavior.
- `packages/pi-coding-agent/src/core/artifact-manager.ts:1-15`, session artifact storage purpose and ID behavior.
- `packages/pi-coding-agent/src/core/artifact-manager.ts:22-28`, artifact directory derivation from session file path.
- `packages/pi-coding-agent/src/core/artifact-manager.ts:38-64`, lazy directory creation and ID scan.
- `packages/pi-coding-agent/src/core/artifact-manager.ts:75-124`, artifact log write/list/get behavior.
- `src/resources/extensions/gsd/debug-logger.ts:2-5`, debug logging purpose.
- `src/resources/extensions/gsd/debug-logger.ts:36-50`, debug log file setup and pruning.

### gsd-2 source: extension surfaces

- `src/extension-registry.ts:1-7`, enabled-by-default registry semantics and manifestless extension loading.
- `src/extension-registry.ts:15-48`, manifest and registry-entry interfaces.
- `src/extension-registry.ts:71-112`, registry path, persistence, and default-enabled lookup.
- `src/extension-registry.ts:131-155`, disable behavior and core-extension protection.
- `src/extension-registry.ts:159-221`, manifest read/discovery and registry entry population.
- `src/extension-discovery.ts:9-17`, extension entry resolution from `package.json` `pi.extensions` or entry-file fallback.
- `src/extension-discovery.ts:61-119`, directory scanning and installed-extension shadowing of bundled extensions.
- `src/resource-loader.ts:20-31`, resource-directory resolution.
- `src/resource-loader.ts:54-58`, extension-key derivation.
- `src/resource-loader.ts:78-112`, managed-resource manifest schema.
- `src/resource-loader.ts:541-580`, sync of bundled resources to `~/.gsd/agent` and resource initialization.
- `src/resource-loader.ts:615-707`, legacy skill migration to `~/.agents/skills`.
- `src/resource-loader.ts:746-800`, resource-loader extension discovery, registry filtering, and sorting.
- `src/loader.ts:109-163`, loader environment variables and bundled extension path serialization.
- `src/loader.ts:174-215`, workspace package linking.
- `packages/pi-coding-agent/src/core/extensions/types.ts:1-9`, high-level extension capability description.
- `packages/pi-coding-agent/src/core/extensions/types.ts:1288-1350`, event-subscription surface.
- `packages/pi-coding-agent/src/core/extensions/types.ts:1356-1427`, event emission, tool, command, lifecycle hook, shortcut, flag, and renderer registration.
- `packages/pi-coding-agent/src/core/extensions/types.ts:1433-1484`, message, retry, exec, and tool-management APIs.
- `packages/pi-coding-agent/src/core/extensions/types.ts:1490-1573`, model, provider, and event-bus APIs.
- `packages/pi-coding-agent/src/core/extensions/loader.ts:402-440`, extension runtime creation.
- `packages/pi-coding-agent/src/core/extensions/loader.ts:448-608`, API binding to commands, tools, hooks, shortcuts, flags, renderers, exec, and provider registration.
- `packages/pi-coding-agent/src/core/extensions/loader.ts:823-888`, module loading and failure diagnostics.
- `packages/pi-coding-agent/src/core/extensions/loader.ts:907-935`, sequential extension loading.
- `packages/pi-coding-agent/src/core/extensions/loader.ts:1078-1128`, project/global/installed/configured extension loading and sorting.
- `packages/pi-coding-agent/src/core/extensions/extension-sort.ts:17-137`, dependency-first topological sort and warning behavior.
- `src/resources/extensions/gsd/index.ts:18-36`, core `gsd` extension command registration.
- `src/resources/extensions/gsd/bootstrap/register-extension.ts:70-138`, GSD extension registration and non-critical registration failure handling.
- `src/resources/extensions/gsd/commands-bootstrap.ts:3-49`, `/gsd` subcommand list.
- `src/resources/extensions/gsd/commands-bootstrap.ts:213-220`, autocomplete entries for `/gsd extensions`.
- `src/resources/extensions/gsd/commands-extensions.ts:1-7`, extension command purpose.
- `src/resources/extensions/gsd/commands-extensions.ts:57-155`, extension command paths and locked registry transactions.
- `src/resources/extensions/gsd/commands-extensions.ts:183-255`, extension package validation and manifest discovery.
- `src/resources/extensions/gsd/commands-extensions.ts:400-497`, registry entry write and uninstall.
- `src/resources/extensions/gsd/commands-extensions.ts:520-651`, extension update behavior.
- `src/resources/extensions/gsd/commands-extensions.ts:658-786`, npm/git/local extension install paths.
- `src/resources/extensions/gsd/commands-extensions.ts:798-841`, extension subcommand dispatch.

### gsd-2 source: migration tooling

- `src/resources/extensions/gsd/migrate/command.ts:1-9`, migration command scope and pipeline.
- `src/resources/extensions/gsd/migrate/command.ts:80-129`, source-path handling and validation output.
- `src/resources/extensions/gsd/migrate/command.ts:131-189`, parse/transform/preview/confirm/write flow.
- `src/resources/extensions/gsd/migrate/command.ts:191-219`, optional post-write review.
- `src/resources/extensions/gsd/migrate/validator.ts:14-54`, fatal vs warning validation.
- `src/resources/extensions/gsd/migrate/parser.ts:58-139`, phase-directory parsing.
- `src/resources/extensions/gsd/migrate/parser.ts:142-177`, quick-task parsing.
- `src/resources/extensions/gsd/migrate/parser.ts:180-237`, milestone and research parsing.
- `src/resources/extensions/gsd/migrate/parser.ts:241-323`, top-level parse orchestration and missing-file behavior.
- `src/resources/extensions/gsd/migrate/transformer.ts:60-91`, research consolidation and task mapping.
- `src/resources/extensions/gsd/migrate/transformer.ts:104-180`, summary and slice mapping.
- `src/resources/extensions/gsd/migrate/transformer.ts:185-254`, duplicate phase, milestone, and requirement mapping.
- `src/resources/extensions/gsd/migrate/transformer.ts:294-345`, roadmap/flat/filesystem migration modes.
- `src/resources/extensions/gsd/migrate/writer.ts:20-35`, migration writer result counts.
- `src/resources/extensions/gsd/migrate/writer.ts:112-184`, roadmap and plan formatting.
- `src/resources/extensions/gsd/migrate/writer.ts:190-300`, summary and task-plan formatting.
- `src/resources/extensions/gsd/migrate/writer.ts:309-409`, requirements, decisions, context, and state formatting.
- `src/resources/extensions/gsd/migrate/writer.ts:421-573`, write behavior for roots, milestones, slices, and tasks.

### gsd-2 source: install, update, version, distribution

- `package.json:2-45`, package name/version, repository, workspaces, bins, files, config, and engine.
- `package.json:46-101`, package manager and scripts.
- `package.json:103-135`, runtime dependencies.
- `package-lock.json:1-10`, lockfile version and root package metadata.
- `package-lock.json:17-76`, dependency, bin, and optional-dependency metadata.
- `.npmrc:1`, `engine-strict=true`.
- `.npmignore:2-9`, npm package inclusion comment.
- `scripts/install.js:3-13`, install script purpose.
- `scripts/install.js:46-81`, version/help behavior.
- `scripts/install.js:148-199`, skip flags, RTK version, and global install.
- `scripts/install.js:201-260`, local install and Chromium install.
- `scripts/install.js:270-407`, RTK asset selection, download, checksum, extraction, and validation.
- `scripts/install.js:425-449`, workspace-package linking.
- `scripts/install.js:465-524`, install verification and postinstall/npx behavior.
- `scripts/bump-version.mjs:3-76`, version bump and package-lock synchronization.
- `.github/workflows/prod-release.yml:1-36`, manual release workflow and environment.
- `.github/workflows/prod-release.yml:57-90`, changelog, version bump, commit, and tag.
- `.github/workflows/prod-release.yml:92-125`, npm publish, dist-tag behavior, git push, and GitHub Release.
- `.github/workflows/prod-release.yml:138-176`, GHCR images and back-merge PR.
- `src/update-check.ts:8-12`, update-check cache and npm-registry target.
- `src/update-check.ts:58-75`, latest-version fetch.
- `src/update-check.ts:99-153`, install-command resolution, cache, and banner behavior.
- `src/update-cmd.ts:6-40`, `/gsd update` implementation.
- `native/Cargo.toml:1-17`, Rust workspace metadata.
- `native/npm/linux-x64-gnu/package.json:1-20`, platform native engine package metadata.
- `packages/native/package.json:1-17`, `@gsd/native` package metadata.

### Contribution-culture probe: raw `gh` output

Command:

```bash
gh repo view gsd-build/gsd-2 --json description,homepageUrl,createdAt,pushedAt,stargazerCount,forkCount,openIssuesCount
```

Raw output:

```text
Unknown JSON field: "openIssuesCount"
Available fields:
  assignableUsers
  codeOfConduct
  contactLinks
  createdAt
  defaultBranchRef
  deleteBranchOnMerge
  description
  diskUsage
  forkCount
  fundingLinks
  hasDiscussionsEnabled
  hasIssuesEnabled
  hasProjectsEnabled
  hasWikiEnabled
  homepageUrl
  id
  isArchived
  isBlankIssuesEnabled
  isEmpty
  isFork
  isInOrganization
  isMirror
  isPrivate
  isSecurityPolicyEnabled
  isTemplate
  isUserConfigurationRepository
  issueTemplates
  issues
  labels
  languages
  latestRelease
  licenseInfo
  mentionableUsers
  mergeCommitAllowed
  milestones
  mirrorUrl
  name
  nameWithOwner
  openGraphImageUrl
  owner
  parent
  primaryLanguage
  projects
  pullRequestTemplates
  pullRequests
  pushedAt
  rebaseMergeAllowed
  repositoryTopics
  securityPolicyUrl
  squashMergeAllowed
  sshUrl
  stargazerCount
  templateRepository
  updatedAt
  url
  usesCustomOpenGraphImage
  viewerCanAdminister
  viewerDefaultCommitEmail
  viewerDefaultMergeMethod
  viewerHasStarred
  viewerPermission
  viewerPossibleCommitEmails
  viewerSubscription
  visibility
  watchers
```

Command:

```bash
gh pr list --repo gsd-build/gsd-2 --state all --limit 20 --json number,title,state,createdAt,closedAt,mergedAt,author
```

Raw output:

```text
error connecting to api.github.com
check your internet connection or https://githubstatus.com
```

Command:

```bash
gh issue list --repo gsd-build/gsd-2 --state all --limit 20 --json number,title,state,createdAt,closedAt,author
```

Raw output:

```text
error connecting to api.github.com
check your internet connection or https://githubstatus.com
```

### Contribution-culture probe: local fallback evidence

- `CONTRIBUTING.md` exists and was read at `CONTRIBUTING.md:1-220` and `CONTRIBUTING.md:400-428`.
- Local `git log --oneline -20` showed merge-commit references to PR numbers `#5080`, `#5062`, `#5060`, `#5055`, `#5058`, and `#5053`; this fallback did not provide PR states, issue counts, or created/closed/merged timestamps.

## (ii) Calibrated findings

### Q1: What artifacts does gsd-2 produce?

**Finding 1.1 — Project artifacts are centered on `.gsd/`, with a documented milestone/slice/task hierarchy.** [high]

The workflow documentation lists a project-local `.gsd/` tree containing root files (`STATE.md`, `DECISIONS.md`, `CODEBASE.md`), milestone directories, slice directories, task directories, and optional context/research/summary/UAT/continuation files (`src/resources/GSD-WORKFLOW.md:42-66`). The path implementation uses bare directory IDs such as `M001/` and `S01/`, while files carry the ID prefix plus suffix such as `M001-ROADMAP.md`, `S01-PLAN.md`, and `T03-SUMMARY.md` (`src/resources/extensions/gsd/paths.ts:1-9`, `145-163`).

**Finding 1.2 — `.gsd` may be project-local or a symlink into external per-repo state.** [high]

The path resolver probes project-local `.gsd`, a worktree guard, the git-root `.gsd`, parent directories, and then falls back to a base `.gsd` path (`src/resources/extensions/gsd/paths.ts:292-303`, `344-397`). A separate repo-identity module describes "external state directory primitives" that compute a stable per-repo identity and manage a `<project>/.gsd -> external` symlink (`src/resources/extensions/gsd/repo-identity.ts:1-7`). That external state writes `repo-meta.json` with fields including `version`, `hash`, `gitRoot`, `remoteUrl`, and `createdAt` (`src/resources/extensions/gsd/repo-identity.ts:37-79`).

**Finding 1.3 — Root `.gsd` files are partly source-of-truth artifacts and partly derived cache.** [high]

The root file helpers name `PROJECT.md`, `DECISIONS.md`, `QUEUE.md`, `STATE.md`, `REQUIREMENTS.md`, `OVERRIDES.md`, `KNOWLEDGE.md`, and `CODEBASE.md` (`src/resources/extensions/gsd/paths.ts:259-268`). `STATE.md` is explicitly documented as a derived cache: the source of truth is roadmap, plan, task/slice/milestone summaries, and `STATE.md` should be regenerated or updated after significant actions (`src/resources/GSD-WORKFLOW.md:519-533`). The documented `STATE.md` schema includes current milestone/slice/task, last updated timestamp, and status lines (`src/resources/GSD-WORKFLOW.md:194-210`).

**Finding 1.4 — Init creates long-lived project artifacts and runtime support artifacts.** [high]

The init wizard bootstraps `.gsd`, writes project preferences, initializes SQLite state through `ensureDbOpen`, ensures `.gitignore` handling, generates `CODEBASE.md`, writes an initial `STATE.md`, and prepares workflow MCP for the project (`src/resources/extensions/gsd/init-wizard.ts:265-340`). The directory bootstrap creates `.gsd/milestones` and `.gsd/runtime`, and may seed `.gsd/CONTEXT.md` from project detection (`src/resources/extensions/gsd/init-wizard.ts:516-535`).

**Finding 1.5 — Milestone, slice, and task artifacts have markdown schemas but not all schemas are equally enforced by code.** [medium]

The documentation defines milestone roadmaps with title, vision, success criteria, and slice checklist entries whose `[x]`/`[ ]` status and inline tags are parse-significant (`src/resources/GSD-WORKFLOW.md:72-97`). It also documents a `Boundary Map` section (`src/resources/GSD-WORKFLOW.md:99-120`). The migration writer formats roadmap title, vision, success criteria, and slice checklist, but explicitly skips writing the boundary map "per D004" (`src/resources/extensions/gsd/migrate/writer.ts:112-143`). This suggests at least one documented section is not universally emitted by tooling.

**Finding 1.6 — Task plans and summaries are long-lived workflow artifacts; `continue.md` is explicitly ephemeral.** [high]

Task plans are documented as carrying `Artifacts` and `Key Links` sections for verification (`src/resources/GSD-WORKFLOW.md:172-192`). Completion protocol says task completion should mark the task done in its plan, write slice summaries and UAT artifacts, mark slices done in the roadmap, update `STATE.md`, and update milestone summaries (`src/resources/GSD-WORKFLOW.md:459-472`). `continue.md` is documented as a resumability artifact written on interruption and deleted after being consumed (`src/resources/GSD-WORKFLOW.md:476-513`).

**Finding 1.7 — Separate session artifacts store large/truncated tool outputs adjacent to session JSONL files.** [high]

The artifact manager describes "session-scoped artifact storage for truncated tool outputs" using `artifact://` URLs (`packages/pi-coding-agent/src/core/artifact-manager.ts:1-6`). It derives the artifact directory from the session `.jsonl` path by removing the suffix (`packages/pi-coding-agent/src/core/artifact-manager.ts:22-28`), lazily creates that directory, scans existing `N.<tool>.log` files for ID continuation (`packages/pi-coding-agent/src/core/artifact-manager.ts:38-64`), and writes artifact files named `${id}.${toolType}.log` (`packages/pi-coding-agent/src/core/artifact-manager.ts:75-90`).

**Finding 1.8 — Extension/distribution artifacts include an extension registry and managed-resource manifest.** [high]

The extension registry persists at `~/.gsd/extensions/registry.json` and uses tmp-write plus rename (`src/extension-registry.ts:71-99`). Registry entries include extension ID, enabled flag, source, disable metadata, version, installed origin, and install type (`src/extension-registry.ts:34-48`). Managed resource sync records `gsdVersion`, `syncedAt`, content hash, installed extensions, root files, and directories (`src/resource-loader.ts:78-112`), and copies bundled resources into `~/.gsd/agent`, including extensions and `GSD-WORKFLOW.md` (`src/resource-loader.ts:541-557`).

### Q2: Are there extension surfaces?

**Finding 2.1 — gsd-2 appears to expose a substantive extension system rather than only expecting monolithic forks.** [high]

The extension SDK states that extensions can add tools, commands, event hooks, UI components, and custom behaviors without modifying core (`docs/extension-sdk/README.md:1-5`). The PI extension type definition similarly says extensions can subscribe to lifecycle events and register LLM tools, commands, keyboard shortcuts, CLI flags, and UI components (`packages/pi-coding-agent/src/core/extensions/types.ts:1-9`). The source implements registration functions for tools, commands, lifecycle hooks, shortcuts, flags, renderers, model/provider controls, and event-bus access (`packages/pi-coding-agent/src/core/extensions/types.ts:1356-1573`; `packages/pi-coding-agent/src/core/extensions/loader.ts:448-608`).

**Finding 2.2 — The primary extension shape is: manifest metadata plus an entry module exporting an activation function that receives `ExtensionAPI`.** [high]

The quick-start extension layout includes an `extension-manifest.json` and `index.ts`, where the default export receives `ExtensionAPI` and calls `pi.registerTool` (`docs/extension-sdk/README.md:19-72`). The SDK structure section says the manifest is required and `index.ts` has a default export receiving `ExtensionAPI` (`docs/extension-sdk/README.md:76-87`). The manifest spec defines fields such as `id`, `name`, `version`, `tier`, `requires`, `provides`, and `dependencies` (`docs/extension-sdk/manifest-spec.md:25-34`), while source manifests and registry entries mirror that shape (`src/extension-registry.ts:15-48`).

**Finding 2.3 — Manifest metadata and runtime registration are related but not the same pipeline.** [high]

The manifest spec says `provides.tools`, `provides.commands`, `provides.hooks`, and `provides.shortcuts` are informational registry/dependency metadata and that actual registration still occurs during extension activation (`docs/extension-sdk/manifest-spec.md:95-115`). Source supports that separation: manifest discovery populates/updates registry entries (`src/extension-registry.ts:159-221`), while runtime activation calls extension modules and binds `registerTool`, `registerCommand`, `on`, and other methods into the active API (`packages/pi-coding-agent/src/core/extensions/loader.ts:823-935`, `448-608`).

**Finding 2.4 — Discovery has multiple roots and shadowing rules.** [high]

The SDK docs list global `~/.gsd/agent/extensions/`, project-local `.gsd/extensions/`, and bundled `src/resources/extensions/` as discovery locations (`docs/extension-sdk/README.md:102-110`). Source discovery resolves entry paths from package `pi.extensions`, falls back to `index.ts`/`index.js`, scans extension directories, and lets installed extensions with the same manifest ID shadow bundled extensions (`src/extension-discovery.ts:9-17`, `61-119`). The loader also reads global agent extensions, installed `~/.gsd/extensions`, explicitly configured paths, and trusted project-local `.pi/extensions` (`packages/pi-coding-agent/src/core/extensions/loader.ts:1078-1128`). The `.gsd/extensions` vs `.pi/extensions` project-local path difference is an open question below.

**Finding 2.5 — Loading order is dependency-aware and registry-filtered.** [high]

The manifest spec says registry/discovery uses manifests for enable/disable, dependency/load order, and compatibility, and that manifestless extensions still load but cannot be registry-managed (`docs/extension-sdk/manifest-spec.md:4-7`). Source registry lookup defaults missing entries to enabled (`src/extension-registry.ts:107-112`), prevents disabling core extensions (`src/extension-registry.ts:131-155`), filters extension paths by registry before loading (`src/resource-loader.ts:746-800`), and sorts extensions topologically while warning for missing dependencies and cycles (`packages/pi-coding-agent/src/core/extensions/extension-sort.ts:17-137`).

**Finding 2.6 — `/gsd extensions` is a lifecycle-management surface for extension packages.** [high]

The extension command validates packages for `package.json`, `gsd.extension: true`, `pi.extensions`, existing entry paths, and `@gsd/*` peer-dependency placement (`src/resources/extensions/gsd/commands-extensions.ts:183-234`). It supports npm, git, and local installs with staging/validation/rename behavior (`src/resources/extensions/gsd/commands-extensions.ts:658-786`), uninstall with dependency warnings (`src/resources/extensions/gsd/commands-extensions.ts:441-497`), and updates where npm extensions can update automatically while git/local extensions are skipped or require reinstall hints (`src/resources/extensions/gsd/commands-extensions.ts:520-651`). Dispatch supports `list`, `enable`, `disable`, `info`, `install`, `uninstall`, `update`, and `validate` (`src/resources/extensions/gsd/commands-extensions.ts:798-841`).

**Finding 2.7 — Core GSD itself is implemented as an extension, which is directionally important for extension-target thinking.** [high]

The bundled GSD extension registers `/gsd` first and then attempts the fuller setup, preserving the core command if platform-specific setup fails (`src/resources/extensions/gsd/index.ts:18-36`). Its bootstrap registers worktree commands, exit handling, hook emission, tools, shortcuts, events, and ecosystem loaders, with non-critical registrations wrapped so a failure warns but does not fail the whole bootstrap (`src/resources/extensions/gsd/bootstrap/register-extension.ts:70-138`). This suggests the extension system is not just for third-party extras; it is part of the product's own composition.

**Finding 2.8 — There are several extension-adjacent mechanisms, but they are not a single declarative plugin manifest.** [medium-high]

The unifying runtime mechanism appears to be extension entry loading plus imperative `ExtensionAPI` registration (`packages/pi-coding-agent/src/core/extensions/loader.ts:823-935`, `448-608`). The registry/manifest controls discovery, enablement, install metadata, and ordering (`src/extension-registry.ts:15-48`, `71-112`). Resource sync copies bundled extension code into an inspectable managed directory (`src/resource-loader.ts:541-580`). `/gsd extensions` manages user-installed packages (`src/resources/extensions/gsd/commands-extensions.ts:658-841`). These compose, but they are distinct subsystems with different artifacts and lifecycles rather than one declarative "extension manifest defines everything" pipeline.

### Q3: What migration tooling exists?

**Finding 3.1 — gsd-2 includes a user-facing `.planning` to `.gsd` migration command.** [high]

The user docs describe `/gsd migrate` as migrating existing `.planning` projects from original GSD v1 into `.gsd` (`docs/user-docs/migration.md:1-13`). The command source calls it a "one-shot migration command" from old `.planning` to new `.gsd`, with a pipeline of validate, parse, transform, preview, and write, plus optional post-write review (`src/resources/extensions/gsd/migrate/command.ts:1-9`, `131-219`).

**Finding 3.2 — Validation is permissive except for the source directory itself.** [high]

The validator has severities `fatal` and `warning`; migration is valid if there are no fatal findings (`src/resources/extensions/gsd/migrate/validator.ts:14-19`, `53-54`). Missing or non-directory `.planning` is fatal (`src/resources/extensions/gsd/migrate/validator.ts:20-27`). Missing `ROADMAP.md`, `PROJECT.md`, `REQUIREMENTS.md`, `STATE.md`, or phase directories are warnings, with text indicating migration can proceed with reduced data or no phase data (`src/resources/extensions/gsd/migrate/validator.ts:29-51`).

**Finding 3.3 — The parser reads more old-project material than the writer appears to preserve directly.** [medium-high]

The parser scans phase directories for plans, summaries, research, verification, and extra files (`src/resources/extensions/gsd/migrate/parser.ts:58-139`), parses quick-task directories (`src/resources/extensions/gsd/migrate/parser.ts:142-177`), scans milestone and research directories (`src/resources/extensions/gsd/migrate/parser.ts:180-237`), and reads top-level `PROJECT.md`, `ROADMAP.md`, `REQUIREMENTS.md`, `STATE.md`, and `config.json` (`src/resources/extensions/gsd/migrate/parser.ts:241-323`). The writer emits root project/decisions/state/requirements files, milestone roadmaps/context/research/summaries, slice plans/research/summaries, task plans, and task summaries (`src/resources/extensions/gsd/migrate/writer.ts:421-573`). I did not see writer emission for parsed verification files, arbitrary `extraFiles`, quick tasks as a first-class quick-task construct, old `config.json`, or old `STATE.md` content; these appear either dropped, transformed indirectly, or not written by this path.

**Finding 3.4 — Phase-to-slice migration intentionally normalizes and infers some fields.** [high]

Task mapping derives done status from matching summaries, extracts files and must-haves from summary frontmatter when present, and otherwise creates minimal task structures (`src/resources/extensions/gsd/migrate/transformer.ts:79-91`). Phase-to-slice mapping hardcodes `risk: medium`, gives each non-first slice a dependency on the previous slice, and attaches phase research and summaries where available (`src/resources/extensions/gsd/migrate/transformer.ts:150-180`). Requirements are normalized into `active`, `validated`, or `deferred`; `complete` aliases become `validated`, and unknown statuses become `active` (`src/resources/extensions/gsd/migrate/transformer.ts:231-239`). Requirement records are assigned class `core-capability`, source `inferred`, and `primarySlice` `"none yet"` (`src/resources/extensions/gsd/migrate/transformer.ts:241-254`).

**Finding 3.5 — The migrator has roadmap, flat-phase, and filesystem-fallback modes.** [high]

The transformer can derive milestones from the old roadmap, fall back to a flat milestone from parsed phases, or build from filesystem phase directories (`src/resources/extensions/gsd/migrate/transformer.ts:294-345`). The user docs align with this: they say migration is best when `ROADMAP.md` exists, and if there is no roadmap it creates a default milestone inferred from phase folders (`docs/user-docs/migration.md:26-38`).

**Finding 3.6 — There is also migration tooling for in-project `.gsd` state to external state, separate from v1 `.planning` conversion.** [high]

The external-state migrator migrates an in-project `.gsd/` into `~/.gsd/projects/<hash>/` and replaces the original `.gsd` with a symlink (`src/resources/extensions/gsd/migrate-external.ts:1-7`). It skips missing/symlink cases, refuses non-directory `.gsd`, skips git-tracked `.gsd`, and skips active `.gsd/worktrees` (`src/resources/extensions/gsd/migrate-external.ts:36-84`). It copies contents while skipping `worktrees/`, creates and verifies the symlink, tries nonfatal `git rm --cached .gsd`, removes backup, and has rollback/recovery paths (`src/resources/extensions/gsd/migrate-external.ts:90-210`).

### Q4: How does gsd-2 install / update / version?

**Finding 4.1 — The public package appears to be the npm package `gsd-pi`, currently version `2.78.1` in the inspected clone.** [high]

The root `package.json` names the package `gsd-pi`, version `2.78.1`, and points repository/homepage/bugs to `gsd-build/gsd-2` (`package.json:2-13`). It declares bins `gsd` and `gsd-cli` to `dist/loader.js`, plus `gsd-pi` to `scripts/install.js` (`package.json:20-24`). The package manager is `npm@10.9.3`, the engine is Node `>=22.0.0`, and `.npmrc` enforces engines (`package.json:39-46`; `.npmrc:1`).

**Finding 4.2 — Package inclusion is managed by npm `files`, with workspaces and lockfile v3.** [high]

The root package includes `dist`, `packages`, `pkg`, `src/resources`, scripts, package metadata, and README through the `files` list (`package.json:25-38`). `.npmignore` states that the `files` field controls publish contents and prevents `.gitignore` from interfering with npm packaging (`.npmignore:2-9`). `package-lock.json` is lockfile version 3 and records root version `2.78.1` with an install script (`package-lock.json:1-10`).

**Finding 4.3 — Install-time behavior includes npm global/local install, Playwright Chromium, RTK binary download, and workspace package linking.** [high]

The install script presents itself as the entry point for `npx gsd-pi` and postinstall (`scripts/install.js:3-13`). It supports version/help behavior and skip flags/envs for Chromium and RTK (`scripts/install.js:46-81`, `148-164`). Global install runs `npm install -g gsd-pi@<version>`, local install runs `npm install gsd-pi@<version>` in the current directory, Chromium install runs through Playwright unless skipped, and RTK install downloads a GitHub release asset, verifies checksum, extracts, copies to a managed bin directory, and validates the binary (`scripts/install.js:168-407`). Postinstall links workspace packages and performs Chromium/RTK setup, while npx full install also verifies `gsd --version` (`scripts/install.js:425-524`).

**Finding 4.4 — Runtime/update behavior checks npm registry and updates through npm/bun global install commands.** [high]

The update checker caches state at `~/.gsd/.update-check`, queries `https://registry.npmjs.org/gsd-pi/latest`, and uses a 24-hour check interval (`src/update-check.ts:8-12`). It fetches latest version from npm registry (`src/update-check.ts:58-75`) and resolves an install command using bun global install if the current install appears bun-based, otherwise npm global install (`src/update-check.ts:99-108`). `/gsd update` checks the registry, compares current/latest, and runs the resolved install command for `gsd-pi@latest` when newer (`src/update-cmd.ts:6-40`).

**Finding 4.5 — Version bumping is script-driven and synchronizes workspace/native package versions.** [high]

`scripts/bump-version.mjs` requires a semver `X.Y.Z`, updates root `package.json`, updates non-private workspace package versions and internal dependency ranges, syncs platform/package metadata, and regenerates package locks (`scripts/bump-version.mjs:3-76`). The root scripts include `sync-versions`, `validate-pack`, `release:patch/minor/major`, `prepublishOnly`, and build/typecheck/test steps around release packaging (`package.json:47-101`).

**Finding 4.6 — Release artifacts include npm, GitHub Releases, and GHCR Docker images.** [high]

The production release workflow is manually dispatched, uses a production environment, installs Node, generates changelog and bumps version, commits/tags, builds, publishes to npm, promotes the npm dist-tag if already published, pushes the release commit/tag, and creates a GitHub Release (`.github/workflows/prod-release.yml:1-125`). The same workflow builds and pushes GHCR Docker images and opens a main-to-next back-merge PR if needed (`.github/workflows/prod-release.yml:138-176`).

**Finding 4.7 — Native engine packages are present as optional/runtime-adjacent package surfaces.** [medium-high]

The root lockfile includes optional native engine packages and platform-specific dependencies (`package-lock.json:67-76`). The Rust workspace exists under `native/` (`native/Cargo.toml:1-17`), a platform package such as `@gsd-build/engine-linux-x64-gnu` carries version `2.78.1` and packages `gsd_engine.node` (`native/npm/linux-x64-gnu/package.json:1-20`), and `@gsd/native` is a workspace package with GSD linkable metadata (`packages/native/package.json:1-17`).

### Q5: Light contribution-culture probe

**Status: incomplete (gh probe failed).** [high]

The required `gh repo view` command failed before contacting the API because this local `gh` does not recognize the requested JSON field `openIssuesCount`. The required `gh pr list` and `gh issue list` commands then failed with `error connecting to api.github.com` and a network/status suggestion. Raw outputs are included in section (i). Because of those failures, PR counts, PR close/merge timestamps, issue counts, stargazer count, and fork count were not available from the requested `gh` probe.

**Local fallback observation — `CONTRIBUTING.md` exists and has explicit structural contribution requirements.** [high]

`CONTRIBUTING.md` section headers observed include `# Contributing to GSD`, `## Before you start`, `## First-time contributors: open an issue first`, `## Branches and commits`, `## Pull request description format`, `## Requirements before requesting review`, `## AI-assisted contributions`, `## Architecture guidelines`, `## Extension-specific guidelines`, `## Promoting a community extension to bundled`, `## Where contributions are most useful`, `## Review process`, `## Reviewer checklist`, `## Local development setup`, and `## Security` (`CONTRIBUTING.md:1-220`, `400-428`). Structural requirements include checking existing issues, claiming issues, creating an issue before new features, requiring RFC/issue approval before architectural changes, ADRs for significant decisions, first-time contributors opening an issue before PR, dedicated branches, conventional commits, one concern per PR, CI and `npm run verify:pr`, explicit disclosure for breaking public API/CLI/config/file-structure changes, and extension PR requirements including manifest, tests for tools/commands/hooks, state reconstruction, accurate `provides`, and use of `@gsd` packages (`CONTRIBUTING.md:7-18`, `20-36`, `101-164`).

**Local fallback observation — local git history shows recent merge commits with PR numbers, but no PR-state timestamps.** [medium]

Local `git log --oneline -20` showed merge-commit references to PR numbers `#5080`, `#5062`, `#5060`, `#5055`, `#5058`, and `#5053`. This is weaker than the required `gh` data because it does not include PR open/closed/merged timestamps, issue state, star count, fork count, or author metadata.

## (iii) What I deliberately did NOT read

- I did not read the forbidden dispatching-project files named in the common preamble: the wave-5 exemplar harvest, archive audit materials, initiative and decision-space files, orchestration files outside this slice spec and preamble, Gemini deep research, or deliberation logs.
- I did not read the slice-specific forbidden prior outputs: `01-mental-model-output.md`, `02-architecture-output.md`, or `03-workflow-surface-output.md`.
- I did not read external RTK or Pi SDK repositories. The slice's install/version and extension-surface questions were answerable from local gsd-2 source and docs, and reading external docs risked widening the slice.
- I did not modify the gsd-2 source tree.
- I did not inspect contribution culture qualitatively beyond the requested raw `gh` attempt and local `CONTRIBUTING.md` fallback evidence.

## (iv) Open questions surfaced

- **Project-local extension path discrepancy.** The SDK docs say project-local extensions live in `.gsd/extensions/` (`docs/extension-sdk/README.md:102-110`), while the PI extension loader reads trusted project-local extensions from `.pi/extensions` (`packages/pi-coding-agent/src/core/extensions/loader.ts:1078-1080`). It is unclear from this slice whether both are intended, one is legacy, or another layer maps `.gsd/extensions` into `.pi/extensions`.
- **Extension command completion appears narrower than command implementation.** The README advertises lifecycle commands including install/update/uninstall/list/info/validate (`README.md:52-53`), and command dispatch implements those plus enable/disable (`src/resources/extensions/gsd/commands-extensions.ts:798-841`). Autocomplete for `/gsd extensions`, however, only lists `list`, `enable`, `disable`, and `info` (`src/resources/extensions/gsd/commands-bootstrap.ts:213-220`). This may be a completion-only gap rather than a functional absence.
- **Compatibility enforcement needs deeper tracing.** The manifest spec says `requires.platform` is checked against running GSD version (`docs/extension-sdk/manifest-spec.md:83-92`). This slice verified manifest validation and registry population but did not trace semver compatibility enforcement end-to-end in the loader.
- **Migrator preservation limits need confirmation before relying on it for high-value historical artifacts.** The migrator parses verification files, extra files, quick tasks, top-level config, and old state (`src/resources/extensions/gsd/migrate/parser.ts:58-323`), but the writer path I read does not appear to emit all of those as first-class migrated artifacts (`src/resources/extensions/gsd/migrate/writer.ts:421-573`). That may be intentional lossy migration, indirect transformation, or a gap.
- **Boundary-map status is unclear across docs and migrator output.** Workflow docs present a `Boundary Map` section in the milestone roadmap schema (`src/resources/GSD-WORKFLOW.md:99-120`), while the migration writer explicitly skips boundary maps (`src/resources/extensions/gsd/migrate/writer.ts:140`). A downstream synthesis should avoid assuming every roadmap emitted by tooling contains that section.
- **Watchlist: telemetry/observability appears central enough to integrate across slices.** Debug logging is documented in README (`README.md:623-625`) and implemented as structured JSONL with pruning (`src/resources/extensions/gsd/debug-logger.ts:2-5`, `36-50`). This slice also saw update cache, session artifacts, registry files, and release/workflow artifacts. I did not characterize the broader logging/metrics/forensics surface because it is outside slice 4's main questions.
- **Watchlist: security/trust boundary appears central for extensions.** Project-local extension loading is gated on a trust state in the loader (`packages/pi-coding-agent/src/core/extensions/loader.ts:1078-1090`), and extension installation validates package shape and dependency placement (`src/resources/extensions/gsd/commands-extensions.ts:183-234`). A full security-model slice would need to characterize what extension code can do once loaded, since the API includes `exec`, tool registration, providers, and event hooks (`packages/pi-coding-agent/src/core/extensions/types.ts:1433-1573`).
- **Watchlist: collaboration/contribution process is structurally present but not characterized here.** `CONTRIBUTING.md` references issue claiming, review process, 72-hour response policy, and extension promotion (`CONTRIBUTING.md:7-18`, `166-205`), but the requested `gh` probe failed, so I could not provide live PR/issue counts or timestamps.

## (v) Flags where README claims diverge from source observations

- **Partial UX-surface divergence: extension lifecycle commands.** README says the extension framework includes lifecycle commands "install / update / uninstall / list / info / validate" (`README.md:52-53`). Source dispatch does implement those commands, along with enable/disable (`src/resources/extensions/gsd/commands-extensions.ts:798-841`). However, `/gsd extensions` autocomplete only lists `list`, `enable`, `disable`, and `info` (`src/resources/extensions/gsd/commands-bootstrap.ts:213-220`). I would treat this as a completion/discoverability divergence, not evidence that README's command list is functionally false.
- **No direct README/source divergence observed for v1 migration claims in this slice.** README says `/gsd migrate` parses old projects, maps phases to slices and plans to tasks, preserves completion status, consolidates research, previews before writing, and optionally runs review (`README.md:260-275`). The local migration docs and source support those claims at the level inspected (`docs/user-docs/migration.md:15-24`; `src/resources/extensions/gsd/migrate/command.ts:131-219`; `src/resources/extensions/gsd/migrate/transformer.ts:60-180`).
- **Adjacent non-README doc/source tension: boundary maps.** Workflow docs show a `Boundary Map` section as part of milestone roadmap structure (`src/resources/GSD-WORKFLOW.md:99-120`), while the migration writer skips boundary map emission (`src/resources/extensions/gsd/migrate/writer.ts:140`). This is not a README divergence, but it is relevant to artifact-schema expectations.

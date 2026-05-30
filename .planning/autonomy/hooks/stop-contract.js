#!/usr/bin/env node
/**
 * Stop completion-contract hook — DETERMINISTIC starter. NOT wired by default.
 *
 * Enable ONLY for an autonomous run: add a `Stop` hook in .claude/settings.json
 * pointing at the live copy (.claude/hooks/stop-contract.js), and write
 * .planning/autonomy/active-contract.json. REMOVE both when the run ends — a Stop
 * hook left on will interfere with normal interactive turns.
 *
 * Behavior:
 *  - No .planning/autonomy/active-contract.json -> allow stop (exit 0). No-op.
 *  - Contract present -> BLOCK stop (exit 2) until every required deliverable's
 *    marker exists at .planning/autonomy/markers/<id>. The agent `touch`es a marker
 *    only after it has actually verified that deliverable (the forcing function).
 *    A deliverable may instead be dispositioned by a marker whose content is one of
 *    halt_for_human / blocked_external / deferred_with_seam (honest failure is
 *    first-class; a silent "done" is not).
 *
 * This is the mechanical floor. An LLM-evaluated variant (type: prompt/agent,
 * judging the transcript against the contract, per the /goal field pattern) is the
 * documented next step in AUTONOMOUS-LOOP-SPEC.md.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = process.cwd();
const contractPath = path.join(ROOT, '.planning/autonomy/active-contract.json');
if (!fs.existsSync(contractPath)) process.exit(0); // no active run -> allow stop

let contract;
try {
  contract = JSON.parse(fs.readFileSync(contractPath, 'utf8'));
} catch (e) {
  process.stderr.write('[stop-contract] active-contract.json unparseable (' + e.message + ') — allowing stop\n');
  process.exit(0);
}

const markersDir = path.join(ROOT, '.planning/autonomy/markers');
const DISPOSITIONS = new Set(['halt_for_human', 'blocked_external', 'deferred_with_seam']);

function satisfied(id) {
  const m = path.join(markersDir, id);
  if (!fs.existsSync(m)) return false;
  // A marker may be empty (verified) or contain an honest-failure disposition.
  try {
    const body = fs.readFileSync(m, 'utf8').trim();
    return body === '' || DISPOSITIONS.has(body.split(/\s/)[0]);
  } catch (_) { return true; }
}

const required = (contract.deliverables || []).filter(d => d.required);
const unmet = required.filter(d => !satisfied(d.id));

if (unmet.length) {
  const lines = unmet.map(d => `  - ${d.id}: ${d.check || '(no check)'}  [no marker .planning/autonomy/markers/${d.id}]`);
  process.stderr.write(
    `[stop-contract] BLOCK stop — contract "${contract.unit || '?'}" has ${unmet.length} unmet required deliverable(s):\n` +
    lines.join('\n') +
    `\nEither verify the deliverable and write its marker, or disposition it ` +
    `(halt_for_human / blocked_external / deferred_with_seam) with evidence.\n`
  );
  process.exit(2); // block stop
}
process.exit(0); // all required deliverables verified/dispositioned -> allow stop

# Meta-HCH-Bench: Capability-Decoupled Metacognition for Frontier LLMs

> Frontier LLMs exhibit five distinct metacognitive failure modes during dollar-valued task decompositions

Kaggle benchmark submission for the [Measuring Progress Toward AGI](https://www.kaggle.com/competitions/measuring-progress-toward-agi) hackathon (Metacognition track).

## Kaggle Benchmark

- **Kernel:** https://www.kaggle.com/code/manumasson/meta-hch-bench
- **Benchmark page:** https://www.kaggle.com/benchmarks/manumasson/meta-hch-bench

## What this measures

This benchmark tests whether frontier LLMs can plan and execute dollar-valued combinatorial optimization tasks (TSP, CJS, Steiner trees, graph coloring, MWIS, VE) under a self-imposed time budget. The scoring function is economic: `score = max(0, 100 − gap_pct) − 0.01 × wall_seconds`. Models must metacognitively decide when to stop — spending more time only pays if it improves the solution enough to offset the penalty.

## Repo structure

```
task.py              # Single-file Kaggle bundle (@kbench.task decorated, ~300KB)
questions.jsonl      # 7-row smoke set (6 classes + 1 portfolio)
harness/             # runner.py, scoring.py, prompt.py, render_nl.py, protocol.py
generators/          # One generator per problem class
verifiers/           # One verifier per problem class
eval_harness/        # LocalLLM adapter for local parity runs
kaggle/              # build_task.py (regenerates task.py), kernel-metadata.json
scripts/             # build_smoke_questions.py, verify_pipeline.py
gold/                # Gold solutions for smoke set
writeup-v2.md        # Competition paper draft
```

## Quickstart

### Push to Kaggle

```bash
# Requires KAGGLE_USERNAME + KAGGLE_KEY in environment or .env
kaggle kernels push -p kaggle/
```

### Regenerate task.py (after editing harness/generators/verifiers)

```bash
python kaggle/build_task.py
# Verify: kaggle/task.py should be ~300KB with @kbench.task(name="meta_hch_bench")
```

### Run local parity check

```bash
python eval_harness/run_local.py --questions questions.jsonl --out results/runs/
```

## Known gotchas

- **Do NOT add `from __future__ import annotations` to `kaggle/build_task.py`'s TASK_TEMPLATE** — kbench's Score type inference fails on stringified `-> float` return annotations (PEP 563 makes all annotations strings, breaking `_infer_result_type` inside the SDK).

## Attribution

Built by [Voicetree Lab](https://github.com/voicetreelab).

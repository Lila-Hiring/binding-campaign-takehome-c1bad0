# Binding campaign take-home

## The situation

You've joined a team building AI agents that plan and interpret experiments in an automated lab.

The current campaign is looking for small molecules that bind **K-17**, a 32 kDa soluble ligand-binding domain. The lab measures binding with a fluorescence polarization (FP) competition assay in 384-well plates. Surface plasmon resonance (SPR) is available as a slower, orthogonal assay.

Between March and June the lab ran three campaigns: about 370 dose-response curves on about 320 compounds from three chemical series, plus a reference-compound curve on every plate. A modeling team trained an affinity model on the reported results and wrapped it in a digital twin of the assays, so agents can practice cheaply before they touch the real lab.

Everything here (the target, compounds, data, and people) is fictional and simulated.

## What we're asking

There is no single right answer. We care about the decisions you make and why. In the follow-up interview we'll go through your work in detail and ask you to change parts of it.

1. **Build an environment and reward in which an AI agent learns to run binding campaigns against the twin.** The agent can be an LLM with tools, an RL policy, or anything else. Design it so that agents that score well are agents you would trust to choose and interpret real experiments. Include a simple baseline agent and a way to run an episode.
2. **Propose the next real-lab batch.** Use the budget and options in [LAB_SPEC.md](LAB_SPEC.md). Say what you would run, under what assay conditions, and what you expect to learn.
3. **Write a decision log** in [DECISIONS.md](DECISIONS.md), one page long. List the main choices you made, the alternatives you rejected, and what would change your mind.

## Ground rules

- Plan on 4–6 hours. Stop there and write down what you would do next.
- Use any tools you like, including AI assistants. Be ready to explain every choice and to modify your work live.
- Add your work to this repository and organize it however you like. Commit as you go; we read the history.
- If something is ambiguous, make a decision, note it in DECISIONS.md, and move on.
- Keep the repository private and don't share the exercise.

## What's in the repository

| Path | Contents |
|---|---|
| [LAB_SPEC.md](LAB_SPEC.md) | The assay, reagents, protocol history, and the budget and options for the next batch |
| [DATA.md](DATA.md) | What every data file contains |
| [TWIN.md](TWIN.md) | The modeling team's notes on their affinity model and digital twin |
| [DECISIONS.md](DECISIONS.md) | Template for your decision log |
| `data/` | Historical assay data, compound library, and model predictions |
| `twin/` | The digital twin and the team's standard curve fit |
| `examples/quickstart.py` | Loads the data, runs the twin, and fits a few curves |

## Setup

Python 3.10 or newer:

```bash
pip install -e .
python examples/quickstart.py
```

RDKit is optional but useful for working with structures: `pip install -e ".[chem]"`. Its wheels are most reliable on Python 3.10–3.12.

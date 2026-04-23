# EffectomeExplorer

A proximity biology research tool for mapping the **effectome** of any human protein target which is built with [General Proximity](https://www.generalproximity.bio)'s OmniTAC™ platform in mind.

## What it does

Enter a gene name (e.g. `KRAS`, `TP53`, `BRD4`) and EffectomeExplorer:

- **Maps the interactome** — pulls up to 30 protein-protein interactions from [STRING DB](https://string-db.org) and classifies each partner by effector class
- **Identifies proximity-relevant effectors** 0- E3 ubiquitin ligases, deubiquitylases (DUBs), kinases, and chaperones highlighted automatically
- **Scores proximity potential** — a weighted 0–100 score based on E3 ligase / DUB coverage and interaction confidence
- **Visualizes an interactive network** — force-directed graph, color-coded by effector class, click any node to explore that protein
- **Surfaces proximity medicine literature**- top PubMed papers on PROTACs, degraders, and molecular glues for that target

## Background

All biological processes are driven by proximity. Induced-proximity medicines includes PROTACs, molecular glues, and next-generation bifunctional molecules work by bringing a disease-driving protein into close contact with an effector (most commonly an E3 ligase) to trigger a therapeutic outcome: degradation, re-localization, refolding, or activation.

The **effectome** is the full set of effector proteins capable of modulating a given target through proximity events. Mapping it computationally is the first step before running an experimental screen like OmniTAC™.

## Effector classes

| Color | Class | Role in proximity biology |
|---|---|---|
| 🟡 Amber | E3 Ubiquitin Ligase | Tags target for proteasomal degradation (PROTACs) |
| 🟣 Purple | Deubiquitylase (DUB) | Reverses ubiquitination; target for DUBTACs |
| 🔵 Blue | Kinase | Phosphorylation-based proximity modulation |
| 🩷 Pink | Chaperone | Protein folding/refolding proximity events |
| ⚫ Gray | Other interactor | General PPI network context |

## Proximity Potential Score

A 0–100 composite score weighted by:
- Number of E3 ligases in the interactome (up to 35 pts)
- Number of DUBs (up to 20 pts)
- High-confidence interactions ≥0.7 STRING score (up to 25 pts)
- Chaperone coverage (up to 10 pts)
- Kinase coverage (up to 10 pts)

## Data sources

| Source | What's pulled |
|---|---|
| [STRING DB](https://string-db.org) | Protein-protein interactions (human, species 9606) |
| [UniProt](https://www.uniprot.org) | Protein name, function, disease associations |
| [PubMed / NCBI](https://pubmed.ncbi.nlm.nih.gov) | Proximity medicine literature |

All data is fetched live from public APIs — no database required.

## Running locally

```bash
git clone https://github.com/varungazala16/effectome-explorer.git
cd effectome-explorer
pip install -r requirements.txt
python app.py
```

Open [http://localhost:5050](http://localhost:5050).

## Tech stack

- **Backend** — Python, Flask, concurrent API calls via `ThreadPoolExecutor`
- **Frontend** — Vanilla JS, [vis.js](https://visjs.org) network graph, custom CSS
- **APIs** — STRING DB, UniProt REST, NCBI E-utilities (all public, no keys needed)

## Example targets to try

| Gene | Disease area | Why interesting |
|---|---|---|
| `KRAS` | Oncology | Long considered undruggable; active PROTAC research |
| `TP53` | Oncology | Most mutated gene in cancer; MDM2 proximity well-characterized |
| `BRD4` | Oncology | First PROTAC target validated clinically (dBET1) |
| `MYC` | Oncology | Transcription factor, no binding pocket — proximity-only |
| `BCL2` | Oncology | Anti-apoptotic; degrader programs active at AbbVie, others |
| `EGFR` | Oncology | RTK with active PROTAC degrader programs |

## About

Built as a prototype research tool aligned with the mission of [General Proximity](https://www.generalproximity.bio) — pioneering the next generation of induced-proximity medicines for undruggable targets.

> *"All biological processes are driven by proximity."* General Proximity

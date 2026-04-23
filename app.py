import json
import requests
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# ── Effector class definitions ────────────────────────────────────────────────

E3_LIGASES = {
    'VHL', 'CRBN', 'MDM2', 'XIAP', 'TRIM21', 'TRIM33', 'RNF4', 'RNF111',
    'STUB1', 'HERC2', 'UBR5', 'DCAF15', 'DCAF1', 'KEAP1', 'FBXW7', 'BTRC',
    'SKP2', 'SPOP', 'CUL1', 'CUL2', 'CUL3', 'CUL4A', 'CUL4B', 'CUL5',
    'TRIM25', 'TRIM27', 'TRIM32', 'RNF2', 'RNF8', 'RNF168', 'BRCA1',
    'SIAH1', 'SIAH2', 'HUWE1', 'NEDD4', 'NEDD4L', 'WWP1', 'WWP2', 'ITCH',
    'TRIP12', 'FBXL3', 'FBXL4', 'FBXO11', 'RBX1', 'RBX2', 'SMURF1',
    'SMURF2', 'PRPF19', 'RAD18', 'UBE3A', 'UBE3B', 'UBE3C', 'CBL',
    'CBLB', 'CBLC', 'MDM4', 'MARCH7', 'MARCHF7', 'UHRF1', 'UHRF2',
    'RNF114', 'DCAF11', 'DCAF16', 'DCAF7', 'ZER1', 'ZNRF3', 'RNF43',
    'CRL1', 'CRL2', 'CRL3', 'CRL4', 'FBXO4', 'FBXO6', 'FBXO22', 'FBXO31',
}

DUBS = {
    'USP7', 'USP14', 'USP28', 'USP47', 'USP10', 'USP15', 'USP18',
    'USP22', 'OTUD7B', 'OTUB1', 'BAP1', 'UCHL1', 'UCHL5', 'USP1',
    'USP2', 'USP3', 'USP4', 'USP5', 'USP6', 'USP8', 'USP9X', 'USP11',
    'USP12', 'USP13', 'USP16', 'USP19', 'USP20', 'USP21', 'USP24',
    'USP25', 'USP26', 'USP29', 'USP30', 'USP31', 'USP32', 'USP33',
    'USP34', 'USP35', 'USP36', 'USP37', 'USP38', 'USP39', 'USP40',
    'USP41', 'USP42', 'USP44', 'USP45', 'USP46', 'USP48', 'USP49',
    'USP50', 'USP51', 'USP52', 'CYLD', 'JOSD1', 'JOSD2', 'ATXN3',
    'ATXN3L', 'PSMD14', 'TNFAIP3', 'OTULIN', 'MYSM1', 'BRCC3',
}

KINASES = {
    'CDK1', 'CDK2', 'CDK4', 'CDK6', 'CDK7', 'CDK8', 'CDK9', 'CDK12',
    'EGFR', 'ERBB2', 'ERBB3', 'MET', 'ALK', 'RET', 'FGFR1', 'FGFR2',
    'FGFR3', 'ABL1', 'ABL2', 'SRC', 'YES1', 'FYN', 'LCK', 'ZAP70',
    'JAK1', 'JAK2', 'JAK3', 'TYK2', 'AKT1', 'AKT2', 'AKT3', 'PIK3CA',
    'BRAF', 'RAF1', 'MAP2K1', 'MAP2K2', 'MAPK1', 'MAPK3', 'MTOR',
    'ATM', 'ATR', 'CHEK1', 'CHEK2', 'PRKDC', 'GSK3B', 'GSK3A',
    'AURKA', 'AURKB', 'PLK1', 'PLK2', 'PLK3', 'DYRK1A', 'PRKCA',
    'PRKCB', 'PRKCD', 'PRKCE', 'PRKCG', 'ROCK1', 'ROCK2', 'PAK1',
    'PAK2', 'PAK3', 'VRK1', 'BRD4', 'TRAF2', 'RPS6KB1', 'RPS6KB2',
    'IKBKB', 'IKBKG', 'MAP3K1', 'MAP3K5', 'MAP3K7', 'STK11', 'AMPK',
    'PRKAA1', 'PRKAA2', 'WEE1', 'WEE2', 'TTK', 'BUB1', 'BUB1B',
}

CHAPERONES = {
    'HSP90AA1', 'HSP90AB1', 'HSP90B1', 'HSPA1A', 'HSPA1B', 'HSPA5',
    'HSPA8', 'HSPB1', 'HSPD1', 'HSPE1', 'DNAJB1', 'DNAJB6',
    'STUB1', 'FKBP51', 'FKBP52', 'CDC37', 'AHSA1', 'TRAP1',
    'CALR', 'CANX', 'PTGES3', 'HSPA4', 'HSPH1', 'BAG1', 'BAG2',
    'BAG3', 'BAG4', 'BAG5', 'CHIP', 'CCT2', 'CCT3', 'CCT4',
    'TCP1', 'MKKS', 'BBS10', 'BBS12',
}

EFFECTOR_CLASS_COLORS = {
    'E3 Ligase': '#f59e0b',
    'Deubiquitylase (DUB)': '#8b5cf6',
    'Kinase': '#3b82f6',
    'Chaperone': '#ec4899',
    'Other Interactor': '#4b5563',
}


def get_effector_class(gene_name: str) -> str:
    g = gene_name.upper()
    if g in E3_LIGASES:
        return 'E3 Ligase'
    if g in DUBS:
        return 'Deubiquitylase (DUB)'
    if g in KINASES:
        return 'Kinase'
    if g in CHAPERONES:
        return 'Chaperone'
    return 'Other Interactor'


# ── API helpers ───────────────────────────────────────────────────────────────

def fetch_string_interactions(gene: str, limit: int = 30) -> list:
    try:
        r = requests.get(
            'https://string-db.org/api/json/interaction_partners',
            params={
                'identifiers': gene,
                'species': 9606,
                'limit': limit,
                'caller_identity': 'effectome_explorer_gp',
            },
            timeout=12,
        )
        r.raise_for_status()
        return r.json()
    except Exception:
        return []


def fetch_uniprot_info(gene: str) -> dict | None:
    try:
        r = requests.get(
            'https://rest.uniprot.org/uniprotkb/search',
            params={
                'query': f'gene_exact:{gene} AND organism_id:9606 AND reviewed:true',
                'format': 'json',
                'size': 1,
                'fields': 'accession,gene_names,protein_name,cc_function,cc_disease,cc_subcellular_location,organism_name',
            },
            timeout=10,
        )
        r.raise_for_status()
        results = r.json().get('results', [])
        return results[0] if results else None
    except Exception:
        return None


def fetch_pubmed_papers(gene: str, max_results: int = 6) -> list:
    try:
        search = requests.get(
            'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi',
            params={
                'db': 'pubmed',
                'term': f'{gene} AND (proximity OR degrader OR PROTAC OR "molecular glue" OR "induced proximity" OR "bifunctional")',
                'retmax': max_results,
                'retmode': 'json',
                'sort': 'relevance',
            },
            timeout=10,
        )
        ids = search.json().get('esearchresult', {}).get('idlist', [])
        if not ids:
            return []

        summary = requests.get(
            'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi',
            params={'db': 'pubmed', 'id': ','.join(ids), 'retmode': 'json'},
            timeout=10,
        )
        result = summary.json().get('result', {})

        papers = []
        for pmid in ids:
            p = result.get(pmid, {})
            if not p:
                continue
            authors = [a.get('name', '') for a in p.get('authors', [])[:3]]
            papers.append({
                'pmid': pmid,
                'title': p.get('title', ''),
                'authors': ', '.join(authors) + (' et al.' if len(p.get('authors', [])) > 3 else ''),
                'journal': p.get('source', ''),
                'year': p.get('pubdate', '')[:4],
                'url': f'https://pubmed.ncbi.nlm.nih.gov/{pmid}/',
            })
        return papers
    except Exception:
        return []


# ── Scoring ───────────────────────────────────────────────────────────────────

def compute_proximity_score(interactions: list) -> tuple[int, dict]:
    if not interactions:
        return 0, {}

    counts = {'E3 Ligase': 0, 'Deubiquitylase (DUB)': 0, 'Kinase': 0, 'Chaperone': 0}
    high_conf = sum(1 for ix in interactions if ix.get('score', 0) >= 0.7)

    for ix in interactions:
        ec = get_effector_class(ix.get('preferredName_B', ''))
        if ec in counts:
            counts[ec] += 1

    score = (
        min(counts['E3 Ligase'] * 15, 35)
        + min(counts['Deubiquitylase (DUB)'] * 10, 20)
        + min(high_conf * 2, 25)
        + min(counts['Chaperone'] * 5, 10)
        + min(counts['Kinase'] * 2, 10)
    )

    breakdown = {**counts, 'high_confidence': high_conf}
    return min(score, 100), breakdown


def score_label(score: int) -> tuple[str, str]:
    if score >= 75:
        return 'Excellent', '#00d4ff'
    if score >= 50:
        return 'Good', '#10b981'
    if score >= 25:
        return 'Moderate', '#f59e0b'
    return 'Low', '#6b7280'


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/explore')
def explore():
    gene = request.args.get('gene', '').strip().upper()
    if not gene:
        return redirect(url_for('index'))
    return redirect(url_for('results', gene=gene))


@app.route('/explore/<gene>')
def results(gene: str):
    gene = gene.upper()

    with ThreadPoolExecutor(max_workers=3) as pool:
        f_interactions = pool.submit(fetch_string_interactions, gene)
        f_protein = pool.submit(fetch_uniprot_info, gene)
        f_papers = pool.submit(fetch_pubmed_papers, gene)
        interactions_raw = f_interactions.result()
        protein_info = f_protein.result()
        papers = f_papers.result()

    # Classify interactions
    interactions = []
    for ix in interactions_raw:
        partner = ix.get('preferredName_B', '')
        ec = get_effector_class(partner)
        interactions.append({
            'gene': partner,
            'score': ix.get('score', 0),
            'score_pct': int(ix.get('score', 0) * 100),
            'escore': round(ix.get('escore', 0), 3),
            'tscore': round(ix.get('tscore', 0), 3),
            'effector_class': ec,
            'color': EFFECTOR_CLASS_COLORS[ec],
        })
    interactions.sort(key=lambda x: x['score'], reverse=True)

    # Proximity score
    score, score_breakdown = compute_proximity_score(interactions_raw)
    s_label, s_color = score_label(score)

    # Effector counts for summary bar
    effector_counts = {k: 0 for k in EFFECTOR_CLASS_COLORS}
    for ix in interactions:
        effector_counts[ix['effector_class']] += 1

    # Parse UniProt
    protein_name, protein_function, uniprot_id, diseases = gene, '', '', []
    if protein_info:
        acc = protein_info.get('primaryAccession', '')
        uniprot_id = acc
        desc = protein_info.get('proteinDescription', {})
        rec = desc.get('recommendedName', {})
        protein_name = rec.get('fullName', {}).get('value', gene)
        for comment in protein_info.get('comments', []):
            ct = comment.get('commentType', '')
            if ct == 'FUNCTION' and not protein_function:
                texts = comment.get('texts', [])
                if texts:
                    protein_function = texts[0].get('value', '')[:500]
            elif ct == 'DISEASE':
                d = comment.get('disease', {})
                name = d.get('diseaseId', '') or d.get('description', '')
                if name and name not in diseases:
                    diseases.append(name)

    # Build vis.js network data
    node_list = [{'id': 0, 'label': gene, 'group': 'target', 'title': f'<b>{gene}</b><br>Query target', 'value': 40}]
    edge_list = []
    for i, ix in enumerate(interactions, 1):
        node_list.append({
            'id': i,
            'label': ix['gene'],
            'group': ix['effector_class'],
            'title': f"<b>{ix['gene']}</b><br>{ix['effector_class']}<br>Score: {ix['score_pct']}%",
            'value': 10 + ix['score'] * 20,
        })
        edge_list.append({'from': 0, 'to': i, 'value': ix['score'], 'title': f"STRING: {ix['score_pct']}%"})

    network_data = json.dumps({'nodes': node_list, 'edges': edge_list})

    not_found = not interactions_raw and not protein_info

    return render_template(
        'results.html',
        gene=gene,
        protein_name=protein_name,
        protein_function=protein_function,
        uniprot_id=uniprot_id,
        diseases=diseases[:6],
        interactions=interactions,
        papers=papers,
        score=score,
        score_label=s_label,
        score_color=s_color,
        score_breakdown=score_breakdown,
        effector_counts=effector_counts,
        network_data=network_data,
        effector_colors=EFFECTOR_CLASS_COLORS,
        not_found=not_found,
    )


if __name__ == '__main__':
    app.run(debug=True, port=5050, use_reloader=False)

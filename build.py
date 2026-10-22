#!/usr/bin/env python3
"""Write the KROMA API site."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

NAV = [
    ("index.html", "Overview"),
    ("cli.html", "CLI"),
    ("pipeline.html", "Matching run"),
    ("loaders.html", "Loaders"),
    ("query.html", "Query"),
    ("models.html", "Models"),
    ("retrieval.html", "Retrieval"),
    ("refinement.html", "Refinement"),
    ("metrics.html", "Metrics"),
]

FOOTER = (
    "KROMA API. Ontology matching with knowledge retrieval and large language models. "
    'Code: <a href="https://github.com/lamng3/kroma">github.com/lamng3/kroma</a>.'
)


def nav_html(current):
    links = ['<a class="brand-desk" href="index.html">kroma</a>']
    for href, label in NAV:
        current_attr = ' aria-current="page"' if href == current else ""
        links.append(f'<a href="{href}"{current_attr}>{label}</a>')
    return "".join(links)


HEADER = """<header class="site">
  <a class="logo" href="index.html"><span class="logo-mark">K</span><span>KROMA</span></a>
  <nav class="site">
    <a href="pipeline.html">Pipeline</a>
    <a href="query.html">Query</a>
    <a href="cli.html">CLI</a>
    <label class="nav-button" for="nav-toggle">Menu</label>
    <a href="https://github.com/lamng3/kroma" class="pill">GitHub ↗</a>
  </nav>
</header>"""

HEAD = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=TikTok+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">"""

HOME = """<section class="hero">
  <div>
    <h1>Ontology matching with knowledge retrieval and large language models</h1>
    <p class="lede">LEDE</p>
    <pre class="install"><span class="prompt">$ </span>git clone https://github.com/lamng3/kroma.git &amp;&amp; cd kroma
<span class="prompt">$ </span>./setup.sh &amp;&amp; source .venv/bin/activate
<span class="prompt">$ </span>kroma run --help</pre>
    <div class="actions">
      <a class="btn solid" href="pipeline.html">Matching run</a>
      <a class="btn" href="cli.html">CLI</a>
      <a class="btn" href="https://arxiv.org/abs/2507.14032">Paper</a>
    </div>
  </div>
  <div class="demo-card" id="demo">
    <div class="head"><h3>What KROMA asks the model</h3><span class="tag">real <b>prompts</b>, recorded <b>answers</b></span></div>
    <p class="try">Try it: Pick a pair to see the prompt KROMA sends for it, and how the recorded run answered.</p>
    <div class="tabs" id="tabs" role="tablist"></div>
    <pre class="prompt-box" id="prompt"></pre>
    <div class="verdict-row" id="verdict"></div>
    <p class="note">Mouse–Human anatomy pairs. The prompt is built by KROMA's own loader and <code>build_task_prompt</code> from the two ontologies. The answer is what the routed run in the <a href="https://lamng3.com/agentic-ontologist/">Agentic Ontologist</a> recorded for the pair, and the tier that settled it: an evidence-only answer never reached a model. The page asks no model.</p>
  </div>
</section>
<section class="block"><div class="prose-home">BODY</div></section>
<script src="demo.js"></script>"""


def home_page(title, description, lede, body):
    body = re.sub(r'<nav class="toc">.*?</nav>', "", body, flags=re.S)
    hero = HOME.replace("LEDE", lede).replace("BODY", body)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{HEAD}
<title>KROMA — ontology matching with knowledge retrieval and LLMs</title>
<meta name="description" content="{description}">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<input id="nav-toggle" class="nav-toggle" type="checkbox">
{HEADER}
<main class="wrap" id="content" style="max-width:1280px">
{hero}
</main>
<footer class="site">{FOOTER}</footer>
</body>
</html>
"""


def page(filename, title, description, kicker, lede, body):
    if filename == "index.html":
        (ROOT / filename).write_text(home_page(title, description, lede, body), encoding="utf-8")
        return
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — kroma</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=TikTok+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="site">
  <a class="logo" href="index.html"><span class="logo-mark">K</span><span>KROMA</span></a>
  <nav class="site">
    <a href="pipeline.html">Pipeline</a>
    <a href="query.html">Query</a>
    <a href="cli.html">CLI</a>
    <label class="nav-button" for="nav-toggle">Menu</label>
    <a href="https://github.com/lamng3/kroma" class="pill">GitHub ↗</a>
  </nav>
</header>
<input id="nav-toggle" class="nav-toggle" type="checkbox">
<div class="layout">
<nav class="nav">
{nav_html(filename)}
</nav>
<main id="content">
<p class="kicker">{kicker}</p>
<h1>{title}</h1>
<p class="lede">{lede}</p>
{body}
</main>
</div>
<footer class="site">{FOOTER}</footer>
</body>
</html>
"""
    (ROOT / filename).write_text(html, encoding="utf-8")


def main():
    page(
        "index.html",
        "Overview",
        "The KROMA Python API: the command line, the matching run, retrieval, models, and refinement.",
        "API",
        "KROMA matches concepts across two ontologies. These pages are the Python API: what you call, and what it returns.",
        """
<nav class="toc"><strong>On this page</strong><ol><li><a href="#the-pieces">The pieces</a></li><li><a href="#one-run">One run</a></li><li><a href="#install">Install</a></li></ol></nav>
<p>A run loads an alignment, retrieves local context for each concept, asks a language model whether the pair matches, and refines the joined graph. The command line is the usual entry. The same steps are available as functions.</p>
<h2 id="the-pieces">The pieces</h2>
<div class="cards">
<a class="card" href="cli.html"><strong>CLI</strong><span><code>kroma run</code> and the flags that select a config, a model, and a mode.</span></a>
<a class="card" href="pipeline.html"><strong>Matching run</strong><span><code>MatchingRun</code> prepares the task, scores pairs, and writes metrics.</span></a>
<a class="card" href="loaders.html"><strong>Loaders</strong><span>CSV alignments and an OWL class hierarchy.</span></a>
<a class="card" href="query.html"><strong>Query</strong><span>Parents, children, synonyms, and labels from a named source.</span></a>
<a class="card" href="models.html"><strong>Models</strong><span>OpenAI and Together chat models, and embedding backends.</span></a>
<a class="card" href="retrieval.html"><strong>Retrieval</strong><span>Cosine search over concatenated text and Node2Vec vectors.</span></a>
<a class="card" href="refinement.html"><strong>Refinement</strong><span>Online updates while scoring, and a final offline collapse.</span></a>
<a class="card" href="metrics.html"><strong>Metrics</strong><span>Precision, recall, and F1 for a binary alignment.</span></a>
</div>
<h2 id="one-run">One run</h2>
<ol>
<li><code>kroma run</code> parses flags and calls <code>MatchingRun.execute</code>.</li>
<li><code>prepare</code> reads the method JSONL and the dataset JSON, then builds vector stores.</li>
<li><code>score_pairs</code> retrieves context, calls <code>infer</code>, and records the prediction.</li>
<li><code>finish</code> runs <code>offline_refine</code> and writes a metrics JSON file.</li>
</ol>
<h2 id="install">Install</h2>
<pre><code>git clone https://github.com/lamng3/kroma.git
cd kroma
./setup.sh
source .venv/bin/activate
uv pip install ".[models]"</code></pre>
<p>Copy <code>.env.example</code> to <code>.env</code> and set <code>TOGETHERAI_API_KEY</code> or <code>OPENAI_API_KEY</code>. The paper is <a href="https://arxiv.org/abs/2507.14032">ISWC 2025</a>.</p>
""",
    )
    page(
        "cli.html",
        "CLI",
        "The kroma command and the flags for one matching experiment.",
        "kroma.cli",
        "kroma run starts one experiment. With no arguments, kroma prints help and exits.",
        """
<nav class="toc"><strong>On this page</strong><ol><li><a href="#command">Command</a></li><li><a href="#flags">Flags</a></li><li><a href="#from-python">From Python</a></li></ol></nav>
<h2 id="command">Command</h2>
<pre><code>kroma run \\
  --method_config kroma_scibert_envo_sweet \\
  --llm meta-llama/Llama-3.3-70B-Instruct-Turbo-Free \\
  --baseline</code></pre>
<p><code>--method_config</code> is the JSONL file name under <code>experiments/configs/method/&lt;llm&gt;/</code>. <code>--llm</code> is that directory name. Both are required.</p>
<p>Source: <a href="https://github.com/lamng3/kroma/blob/main/src/kroma/cli.py">cli.py</a>.</p>
<h2 id="flags">Flags</h2>
<table>
<tr><th>Flag</th><th>Meaning</th></tr>
<tr><td><code>--method_config</code></td><td>Required. Config name, without <code>.jsonl</code>.</td></tr>
<tr><td><code>--llm</code></td><td>Required. Model directory under <code>experiments/configs/method/</code>.</td></tr>
<tr><td><code>--size</code></td><td>Fraction of the alignment to score. Default <code>full</code>.</td></tr>
<tr><td><code>--baseline</code></td><td>Single-model baseline.</td></tr>
<tr><td><code>--debate</code></td><td>Several agents, several rounds. Omit it for one model.</td></tr>
<tr><td><code>--reasoning</code></td><td>Ask the model to reason before yes or no.</td></tr>
<tr><td><code>--active_learning</code></td><td>Hold low-confidence pairs for review.</td></tr>
<tr><td><code>--compare_models</code></td><td>Compare model settings from the config.</td></tr>
<tr><td><code>--bisim</code></td><td>Use the bisimulation context path.</td></tr>
</table>
<h2 id="from-python">From Python</h2>
<pre><code>RunCommand(args).execute() -&gt; None</code></pre>
<p><code>RunCommand</code> imports <code>MatchingRun</code> and runs it. If a model package is missing, it exits with the install line <code>uv pip install '.[models]'</code>.</p>
""",
    )
    page(
        "pipeline.html",
        "Matching run",
        "MatchingRun prepares a task, scores each pair, and writes precision, recall, and F1.",
        "kroma.pipeline",
        "MatchingRun is the template for one evaluation: prepare, score, then finish.",
        """
<nav class="toc"><strong>On this page</strong><ol><li><a href="#call">Call</a></li><li><a href="#methods">Methods</a></li><li><a href="#output">Output</a></li></ol></nav>
<h2 id="call">Call</h2>
<pre><code>MatchingRun(args, listener=None)
MatchingRun.execute() -&gt; dict</code></pre>
<p><code>execute</code> calls <code>prepare</code>, <code>score_pairs</code>, and <code>finish</code>. <code>listener</code> defaults to <code>MetricsListener</code>, which counts tokens and refinement time.</p>
<p>Source: <a href="https://github.com/lamng3/kroma/blob/main/src/kroma/pipeline.py">pipeline.py</a>.</p>
<h2 id="methods">Methods</h2>
<table>
<tr><th>Method</th><th>What it does</th></tr>
<tr><td><code>prepare()</code></td><td>Load the method JSONL and dataset JSON, open output files, build the task, and fill the vector stores.</td></tr>
<tr><td><code>score_pairs()</code></td><td>Judge each alignment. Skip a pair already stored. Refine on a fixed interval.</td></tr>
<tr><td><code>finish()</code></td><td>Run the final offline refinement and write the metrics JSON.</td></tr>
</table>
<h2 id="output">Output</h2>
<p>Accepted alignments go under <code>results/</code>. Pairs that need an expert go under <code>reviews/</code>. The metrics file sits next to the prediction file and ends in <code>.metrics.json</code>. It includes precision, recall, F1, token counts, and refinement timings.</p>
<p>The run log is <code>logs/kroma.log</code>.</p>
""",
    )
    page(
        "loaders.html",
        "Loaders",
        "CsvAlignmentLoader and OwlOntologyLoader, the two OntologyLoader implementations.",
        "kroma.tasks.loader",
        "A loader returns a source graph, a target graph, and a list of alignments.",
        """
<nav class="toc"><strong>On this page</strong><ol><li><a href="#base">OntologyLoader</a></li><li><a href="#csv">CSV alignments</a></li><li><a href="#owl">OWL</a></li></ol></nav>
<h2 id="base">OntologyLoader</h2>
<pre><code>load() -&gt; (source_graph, target_graph, alignments)</code></pre>
<p>An alignment is <code>(source, target, label)</code>. Each endpoint is a <code>(label, uri)</code> pair.</p>
<p>Source: <a href="https://github.com/lamng3/kroma/blob/main/src/kroma/tasks/loader.py">loader.py</a>.</p>
<h2 id="csv">CSV alignments</h2>
<pre><code>CsvAlignmentLoader(csv_paths, dataset="ncit-doid").load()</code></pre>
<p>For <code>ncit-doid</code>, rows use <code>src_code</code>, <code>src_ety</code>, <code>tgt_code</code>, <code>tgt_ety</code>, <code>tgt_cands</code>, and <code>score</code>. Other datasets use <code>source</code>, <code>source_uri</code>, <code>target</code>, <code>target_uri</code>, and <code>relation</code>.</p>
<h2 id="owl">OWL</h2>
<pre><code>OwlOntologyLoader(owl_path).load()</code></pre>
<p>This reads an OWL or RDF/XML file and builds the class hierarchy from <code>rdfs:subClassOf</code>, with synonyms from the annotation properties on each class.</p>
""",
    )
    page(
        "query.html",
        "Query",
        "query() merges parents, children, synonyms, and labels from dictionary, SPARQL, ontology, and ConceptNet sources.",
        "kroma.tasks.query_engine",
        "query asks each named strategy for local context and concatenates the results.",
        """
<nav class="toc"><strong>On this page</strong><ol><li><a href="#call">Call</a></li><li><a href="#strategies">Strategies</a></li></ol></nav>
<h2 id="call">Call</h2>
<pre><code>query(concept_code, pcmap, dictionary, options)
  -&gt; parents, children, synonyms, labels

register_query_strategy(name, strategy) -&gt; None</code></pre>
<p>Unknown option names are skipped. A strategy that raises is skipped, and the other options still return.</p>
<p>Source: <a href="https://github.com/lamng3/kroma/blob/main/src/kroma/tasks/query_engine.py">query_engine.py</a>.</p>
<h2 id="strategies">Strategies</h2>
<table>
<tr><th>Strategy</th><th>Option names</th></tr>
<tr><td><code>DictionaryStrategy</code></td><td><code>envo</code>, <code>sweet</code>, <code>mouse</code>, <code>human</code>, <code>yago</code>, <code>wikidata</code>, <code>mi</code>, <code>mi2</code>, <code>matonto</code>, <code>emmo</code>, <code>omim</code>, <code>ordo</code></td></tr>
<tr><td><code>SparqlStrategy</code></td><td><code>ncit</code>, <code>doid</code>, <code>dbpedia</code></td></tr>
<tr><td><code>OntologyStrategy</code></td><td><code>ontology</code></td></tr>
<tr><td><code>ConceptNetStrategy</code></td><td><code>conceptnet</code></td></tr>
</table>
<p>A custom source is any object with <code>fetch(code, pcmap, dictionary, topk)</code> registered under a name.</p>
""",
    )
    page(
        "models.html",
        "Models",
        "Chat and embedding factories, and the single-model and debate inference strategies.",
        "kroma.inference",
        "Chat providers adapt OpenAI and Together. Embedding providers adapt Hugging Face and sentence-transformers.",
        """
<nav class="toc"><strong>On this page</strong><ol><li><a href="#factories">Factories</a></li><li><a href="#inference">Inference</a></li></ol></nav>
<h2 id="factories">Factories</h2>
<pre><code>create_inference_model(backend, model_name) -&gt; BaseModel
create_embedding_model(backend, model_name) -&gt; BaseEmbeddingModel
register_chat_backend(name, provider_cls) -&gt; None
register_embedding_backend(name, provider_cls) -&gt; None</code></pre>
<p>Chat backends are <code>openai</code> and <code>togetherai</code>. The API key is <code>OPENAI_API_KEY</code> or <code>TOGETHERAI_API_KEY</code>. Embedding backends are <code>huggingface</code> and <code>sentence-transformers</code>.</p>
<p><code>BaseModel.generate</code> retries transient connection, timeout, and rate-limit errors.</p>
<p>Source: <a href="https://github.com/lamng3/kroma/blob/main/src/kroma/inference/factory.py">factory.py</a>.</p>
<h2 id="inference">Inference</h2>
<pre><code>infer(debate, backend, model_name, source_term, target_term, ...)
  -&gt; prediction, metrics, confidence, accept</code></pre>
<table>
<tr><th>Class</th><th>Role</th></tr>
<tr><td><code>SingleModelInference</code></td><td>One agent, one round.</td></tr>
<tr><td><code>DebateInference</code></td><td>One agent per config, for <code>n_rounds</code> rounds.</td></tr>
</table>
<p><code>expand_term</code> calls <code>query</code> and returns the concept code plus parents, children, synonyms, and labels.</p>
<p>Source: <a href="https://github.com/lamng3/kroma/blob/main/src/kroma/agents/inference.py">inference.py</a>.</p>
""",
    )
    page(
        "retrieval.html",
        "Retrieval",
        "VectorStore cosine search and compute_combined_embeddings.",
        "kroma.retrieval",
        "Retrieval ranks concepts by cosine similarity of a combined text and structure vector.",
        """
<nav class="toc"><strong>On this page</strong><ol><li><a href="#store">VectorStore</a></li><li><a href="#embeddings">Combined embeddings</a></li></ol></nav>
<h2 id="store">VectorStore</h2>
<pre><code>VectorStore.add(ext_ids, embeddings) -&gt; None
VectorStore.query(query_emb, top_k=5) -&gt; list[(id, score)]</code></pre>
<p><code>add</code> stacks embedding rows and keeps the external ids in the same order. <code>query</code> L2-normalizes the stored matrix and the query, then returns the top cosine scores. An empty store returns an empty list.</p>
<p>Source: <a href="https://github.com/lamng3/kroma/blob/main/src/kroma/retrieval/vector_store.py">vector_store.py</a>.</p>
<h2 id="embeddings">Combined embeddings</h2>
<pre><code>compute_combined_embeddings(
    adj_dict, node_keys, text_embs,
    n2v_kwargs=None, combine_method="concat", alpha=0.5,
)</code></pre>
<p>The default combine method is concatenation of the text embedding and the Node2Vec embedding. <code>alpha</code> applies when the method is a weighted mix rather than concatenation.</p>
<p>Source: <a href="https://github.com/lamng3/kroma/blob/main/src/kroma/algorithms/node2vec.py">node2vec.py</a>.</p>
""",
    )
    page(
        "refinement.html",
        "Refinement",
        "online_refine and offline_refine for the joined ontology graph.",
        "kroma.algorithms.refinement",
        "Refinement keeps the joined graph consistent while pairs are accepted, then collapses it at the end.",
        """
<nav class="toc"><strong>On this page</strong><ol><li><a href="#online">Online</a></li><li><a href="#offline">Offline</a></li></ol></nav>
<h2 id="online">Online</h2>
<pre><code>online_refine(full_graph, rank_attr, equiv_classes, delta_edges, pred)
  -&gt; (equiv_classes, expert_questions)</code></pre>
<p>New edges are added to the graph. The function returns the updated equivalence classes and the pairs that should go to an expert. <code>ReviewRepository</code> records those questions. <code>PredictionRepository</code> appends accepted rows.</p>
<h2 id="offline">Offline</h2>
<pre><code>offline_refine(adj, rank_attr) -&gt; dict</code></pre>
<p><code>compute_node_ranks</code> assigns each node its longest distance from a root. <code>offline_refine</code> partitions nodes by that rank, splits blocks that a higher node separates, and collapses each block.</p>
<p><code>MatchingRun.finish</code> calls this once after scoring.</p>
<p>Source: <a href="https://github.com/lamng3/kroma/blob/main/src/kroma/algorithms/refinement.py">refinement.py</a>.</p>
""",
    )
    page(
        "metrics.html",
        "Metrics",
        "calculate_metrics returns precision, recall, and F1.",
        "kroma.metrics.scoring",
        "Metrics are binary. A positive prediction that matches the label is a true positive.",
        """
<nav class="toc"><strong>On this page</strong><ol><li><a href="#call">Call</a></li><li><a href="#empty">Empty input</a></li></ol></nav>
<h2 id="call">Call</h2>
<pre><code>calculate_metrics(y_true, y_pred, positive_label=1)
  -&gt; (precision, recall, f1)</code></pre>
<p><code>y_true</code> and <code>y_pred</code> are sequences of labels, zipped in order. <code>positive_label</code> defaults to <code>1</code>.</p>
<p>Source: <a href="https://github.com/lamng3/kroma/blob/main/src/kroma/metrics/scoring.py">scoring.py</a>.</p>
<h2 id="empty">Empty input</h2>
<p>Precision is 0 when there are no positive predictions. Recall is 0 when there are no positive labels. F1 is 0 when precision and recall are both 0. The function does not raise on an empty pair of lists.</p>
""",
    )
    import normalize

    normalize.run(ROOT)


if __name__ == "__main__":
    main()

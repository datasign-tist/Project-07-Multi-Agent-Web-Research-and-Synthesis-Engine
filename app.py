import time
import streamlit as st

from pipeline import run_research_pipeline

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="MARA — Research Dossier",
    page_icon="📁",
    layout="wide",
)

# -----------------------------------------------------
# CSS — "Field Dossier" system
# -----------------------------------------------------
# Palette
#   --bg        #12100C  near-black, warm (case-file cover)
#   --paper     #1A1712  panel background
#   --paper-alt #211D16  raised panel background
#   --ink       #ECE4D3  cream text
#   --ink-dim   #A79C87  muted cream (secondary text)
#   --rule      #3A3327  hairline dividers
#   --stamp     #A9382A  rubber-stamp red (primary accent / actions)
#   --brass     #C9A227  brass accent (data, numerals, highlights)
# Type
#   Display: 'Fraunces'      — dossier headline, characterful serif
#   Body:    'Source Serif 4'— report copy
#   Mono:    'IBM Plex Mono' — labels, stamps, index numbers

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Source+Serif+4:ital,wght@0,400;0,600;1,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root{
    --bg:#0E1420;
    --paper:#182234;
    --paper-alt:#1F2C42;
    --ink:#F4F6FA;
    --ink-dim:#B7C1D6;
    --rule:#37455F;
    --stamp:#F04B4B;
    --brass:#F5B93F;
    --teal:#2FD6C4;
}

html, body, [class*="css"]{
    font-family:'Source Serif 4', Georgia, serif;
    color:var(--ink);
}

.stApp{
    background:var(--bg);
    background-image:
        repeating-linear-gradient(180deg, rgba(255,255,255,0.012) 0px, rgba(255,255,255,0.012) 1px, transparent 1px, transparent 3px);
}

.block-container{
    padding-top:2.2rem;
    padding-bottom:3rem;
    max-width:1180px;
}

h1,h2,h3{
    font-family:'Fraunces', Georgia, serif;
    color:var(--ink);
    letter-spacing:0.2px;
}

/* -------------------------------------------------
   MONO / LABEL UTILITIES
------------------------------------------------- */
.mono-label{
    font-family:'IBM Plex Mono', monospace;
    font-size:11.5px;
    letter-spacing:2.5px;
    text-transform:uppercase;
    color:var(--ink-dim);
}

.hairline{
    border:none;
    border-top:1px solid var(--rule);
    margin:22px 0;
}

/* -------------------------------------------------
   HERO — cover sheet
------------------------------------------------- */
.hero{
    position:relative;
    padding:38px 40px 32px 40px;
    border:1px solid var(--rule);
    border-radius:2px;
    background:var(--paper);
}

.hero::before, .hero::after{
    content:"";
    position:absolute;
    left:40px; right:40px;
    height:1px;
    background:var(--rule);
}
.hero::before{ top:14px; }
.hero::after{ bottom:14px; }

.hero-topline{
    display:flex;
    justify-content:space-between;
    align-items:baseline;
    margin-bottom:26px;
}

.file-stamp{
    display:inline-block;
    font-family:'IBM Plex Mono', monospace;
    font-size:11px;
    letter-spacing:2px;
    color:var(--stamp);
    border:1.5px solid var(--stamp);
    padding:5px 12px;
    border-radius:3px;
    transform:rotate(-2deg);
    text-transform:uppercase;
}

.hero-title{
    font-family:'Fraunces', Georgia, serif;
    font-size:46px;
    font-weight:600;
    line-height:1.08;
    margin:4px 0 10px 0;
    color:var(--ink);
}

.hero-sub{
    font-family:'IBM Plex Mono', monospace;
    font-size:12.5px;
    letter-spacing:1px;
    color:var(--ink-dim);
}

.hero-sub b{ color:var(--brass); font-weight:600; }

/* -------------------------------------------------
   INPUT CARD
------------------------------------------------- */
.field-tab{
    font-family:'IBM Plex Mono', monospace;
    font-size:11.5px;
    letter-spacing:2.5px;
    text-transform:uppercase;
    color:var(--bg);
    background:var(--brass);
    display:inline-block;
    padding:4px 12px;
    border-radius:2px 2px 0 0;
    margin-bottom:-1px;
    margin-top:18px;
}

.stTextArea textarea{
    background:var(--paper) !important;
    border:1px solid var(--rule) !important;
    border-radius:2px !important;
    color:var(--ink) !important;
    font-family:'Source Serif 4', Georgia, serif !important;
    font-size:16px !important;
}
.stTextArea textarea::placeholder{
    color:var(--ink-dim) !important;
    opacity:0.7;
}
.stTextArea label{ display:none; }

/* -------------------------------------------------
   BUTTON — stamped action
------------------------------------------------- */
.stButton>button{
    width:100%;
    height:54px;
    border-radius:2px;
    background:var(--stamp);
    color:#F4EEDF;
    font-family:'IBM Plex Mono', monospace;
    font-size:14px;
    font-weight:600;
    letter-spacing:2.5px;
    text-transform:uppercase;
    border:1px solid var(--stamp);
    transition:all 0.15s ease;
}
.stButton>button:hover{
    background:transparent;
    color:var(--stamp);
    border:1px solid var(--stamp);
}

/* -------------------------------------------------
   METRICS — exhibit strip
------------------------------------------------- */
div[data-testid="stMetric"]{
    background:var(--paper);
    border:1px solid var(--rule);
    border-radius:2px;
    padding:14px 10px;
    text-align:center;
}
div[data-testid="stMetricLabel"]{
    font-family:'IBM Plex Mono', monospace !important;
    font-size:10.5px !important;
    letter-spacing:2px;
    text-transform:uppercase;
    color:var(--ink-dim) !important;
    justify-content:center;
}
div[data-testid="stMetricValue"]{
    font-family:'Fraunces', Georgia, serif !important;
    color:var(--brass) !important;
    font-size:30px !important;
    justify-content:center;
}

/* -------------------------------------------------
   SECTION HEADERS
------------------------------------------------- */
.section-head{
    display:flex;
    align-items:baseline;
    gap:12px;
    margin:8px 0 16px 0;
}
.section-head .idx{
    font-family:'IBM Plex Mono', monospace;
    font-size:13px;
    color:var(--brass);
}
.section-head .title{
    font-family:'Fraunces', Georgia, serif;
    font-size:24px;
    font-weight:600;
    color:var(--ink);
}
.section-head .rule{
    flex:1;
    height:1px;
    background:var(--rule);
}

/* -------------------------------------------------
   AGENT LOG — folder tabs (expanders)
------------------------------------------------- */
div[data-testid="stExpander"]{
    background:var(--paper);
    border:1px solid var(--rule) !important;
    border-left:3px solid var(--brass) !important;
    border-radius:2px;
    margin-bottom:10px;
}
div[data-testid="stExpander"] summary{
    font-family:'IBM Plex Mono', monospace;
    letter-spacing:1px;
    color:var(--ink);
}
div[data-testid="stExpander"] p{
    color:var(--ink);
}

/* -------------------------------------------------
   REPORT PANEL
------------------------------------------------- */
.report-box{
    padding:36px 40px;
    background:var(--paper);
    border:1px solid var(--rule);
    border-top:3px solid var(--brass);
    border-radius:2px;
    font-family:'Source Serif 4', Georgia, serif;
    font-size:16.5px;
    line-height:1.7;
    color:var(--ink);
}

/* -------------------------------------------------
   REVIEWER MEMO
------------------------------------------------- */
.feedback-box{
    position:relative;
    padding:24px 28px;
    background:var(--paper-alt);
    border:1px dashed var(--teal);
    border-radius:2px;
    color:var(--ink);
    font-size:15.5px;
}

/* -------------------------------------------------
   SOURCES
------------------------------------------------- */
.source-line{
    font-family:'IBM Plex Mono', monospace;
    font-size:13px;
    color:var(--ink-dim);
    padding:6px 0;
    border-bottom:1px solid var(--rule);
}
.source-line b{ color:var(--brass); margin-right:8px; }
.source-line a{ color:var(--ink); text-decoration:none; }
.source-line a:hover{ color:var(--brass); }

/* -------------------------------------------------
   CASE TIMELINE — left-hand progress tracker
------------------------------------------------- */
.timeline-wrap{
    position:sticky;
    top:24px;
    padding:20px 18px;
    background:var(--paper);
    border:1px solid var(--rule);
    border-radius:2px;
}
.timeline-head{
    font-family:'IBM Plex Mono', monospace;
    font-size:11px;
    letter-spacing:2.5px;
    text-transform:uppercase;
    color:var(--brass);
    margin-bottom:18px;
    padding-bottom:10px;
    border-bottom:1px solid var(--rule);
}
.tl-step{ display:flex; align-items:flex-start; gap:11px; }
.tl-node-col{ display:flex; flex-direction:column; align-items:center; }
.tl-node{
    width:12px; height:12px;
    border-radius:50%;
    border:1.5px solid var(--rule);
    background:transparent;
    position:relative;
    flex-shrink:0;
    margin-top:2px;
}
.tl-connector{ width:1.5px; flex:1; min-height:22px; background:var(--rule); margin:2px 0; }
.tl-body{ padding-bottom:20px; }
.tl-label{
    font-family:'IBM Plex Mono', monospace;
    font-size:12px;
    letter-spacing:1px;
    text-transform:uppercase;
    color:var(--ink-dim);
    opacity:0.55;
}
.tl-note{
    font-family:'Source Serif 4', Georgia, serif;
    font-style:italic;
    font-size:12.5px;
    color:var(--ink-dim);
    opacity:0;
    max-height:0;
    overflow:hidden;
    transition:opacity 0.2s ease;
}

.tl-pending .tl-label{ opacity:0.6; }

.tl-active .tl-node{
    border-color:var(--teal);
    background:var(--teal);
    box-shadow:0 0 0 4px rgba(47,214,196,0.28);
    animation:tl-pulse 1.1s ease-in-out infinite;
}
.tl-active .tl-label{ color:var(--teal); opacity:1; }
.tl-active .tl-note{ opacity:1; max-height:40px; margin-top:2px; }
.tl-active .tl-connector{ background:var(--teal); }

.tl-done .tl-node{ border-color:var(--brass); background:var(--brass); }
.tl-done .tl-node::after{
    content:"";
    position:absolute; left:3px; top:2.5px;
    width:3px; height:5.5px;
    border:solid var(--bg);
    border-width:0 1.5px 1.5px 0;
    transform:rotate(40deg);
}
.tl-done .tl-label{ color:var(--ink); opacity:1; }
.tl-done .tl-connector{ background:var(--brass); }

.tl-skipped .tl-node{ border:1.5px dashed var(--rule); }
.tl-skipped .tl-label{ color:var(--ink-dim); opacity:0.5; text-decoration:line-through; }

@keyframes tl-pulse{
    0%{ box-shadow:0 0 0 0 rgba(47,214,196,0.45); }
    70%{ box-shadow:0 0 0 7px rgba(47,214,196,0); }
    100%{ box-shadow:0 0 0 0 rgba(47,214,196,0); }
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# CASE TIMELINE — stepper logic
# -----------------------------------------------------

TIMELINE_STAGES = [
    ("query",    "Query Logged",      "Question received into the case file."),
    ("dispatch", "Agents Dispatched", "Research, Planning, Analysis, Writer, Reviewer online."),
    ("research", "Research",          "Gathering sources and raw findings."),
    ("plan",     "Planning",          "Structuring the investigation."),
    ("analyze",  "Analysis",          "Weighing evidence and drawing conclusions."),
    ("write",    "Writing",           "Drafting the report narrative."),
    ("review",   "Review",            "Critiquing the draft for gaps and bias."),
    ("report",   "Report Compiled",   "Case file closed and ready to read."),
]

RESULT_KEY_BY_STAGE = {
    "research": "Researcher_Output",
    "plan":     "Planner_Output",
    "analyze":  "Analysis_Output",
    "write":    "Writer_Output",
    "review":   "Reviewer_Output",
}

def render_timeline(slot, states):
    """states: dict of stage_key -> 'pending' | 'active' | 'done' | 'skipped'
    NOTE: output must not contain lines indented 4+ spaces — Streamlit's
    markdown parser treats those as code blocks and prints raw HTML instead
    of rendering it. Every fragment here is built as a single unindented line.
    """
    rows = ['<div class="timeline-wrap"><div class="timeline-head">Case Timeline</div>']
    for i, (key, label, note) in enumerate(TIMELINE_STAGES):
        state = states.get(key, "pending")
        is_last = (i == len(TIMELINE_STAGES) - 1)
        connector = "" if is_last else f'<div class="tl-connector tl-{state}"></div>'
        step_html = (
            f'<div class="tl-step tl-{state}">'
            f'<div class="tl-node-col"><div class="tl-node"></div>{connector}</div>'
            f'<div class="tl-body"><div class="tl-label">{label}</div>'
            f'<div class="tl-note">{note}</div></div>'
            f'</div>'
        )
        rows.append(step_html)
    rows.append("</div>")
    slot.markdown("".join(rows), unsafe_allow_html=True)

if "results" not in st.session_state:
    st.session_state.results = None
    st.session_state.elapsed = None
    st.session_state.tl_states = {key: "pending" for key, _, _ in TIMELINE_STAGES}

# -----------------------------------------------------
# HEADER
# -----------------------------------------------------

st.markdown("""
<div class="hero">
    <div class="hero-topline">
        <span class="file-stamp">Dossier Open</span>
        <span class="mono-label">System · MARA v2</span>
    </div>
    <div class="hero-title">Multi-Agent Research Dossier</div>
    <div class="hero-sub">
        <b>Research</b> → <b>Plan</b> → <b>Analyze</b> → <b>Write</b> → <b>Review</b> — five agents,
        one case file, compiled autonomously.
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# -----------------------------------------------------
# LAYOUT — left: case timeline · right: query + results
# -----------------------------------------------------

left_col, right_col = st.columns([1, 2.6], gap="large")

with left_col:
    timeline_slot = st.empty()
    render_timeline(timeline_slot, st.session_state.tl_states)

with right_col:

    st.markdown('<span class="field-tab">Research Query</span>', unsafe_allow_html=True)

    topic = st.text_area(
        "Research Question",
        height=120,
        placeholder="Example:\nCompare OpenAI, Anthropic and Google Gemini enterprise strategy for 2026...",
        label_visibility="collapsed",
    )

    st.write("")

    run_clicked = st.button("Open the Case →")

if run_clicked:

    if not topic.strip():
        with right_col:
            st.warning("Please enter a research question.")
        st.stop()

    start = time.time()

    # ---- animate the tracker while the case is worked ----
    states = {key: "pending" for key, _, _ in TIMELINE_STAGES}

    states["query"] = "done"
    render_timeline(timeline_slot, states)
    time.sleep(0.2)

    states["dispatch"] = "done"
    states["research"] = "active"
    render_timeline(timeline_slot, states)

    with right_col:
        spinner_slot = st.empty()
        spinner_slot.info("🟢 Agents working the case...")

    results = run_research_pipeline(topic)

    elapsed = round(time.time() - start, 2)

    with right_col:
        spinner_slot.success("✅ Research Complete")

    # ---- resolve final stage states from what the pipeline actually returned ----
    for key, result_key in RESULT_KEY_BY_STAGE.items():
        states[key] = "done" if result_key in results else "skipped"
    states["report"] = "done" if results.get("Report") else "skipped"
    render_timeline(timeline_slot, states)

    st.session_state.results = results
    st.session_state.elapsed = elapsed
    st.session_state.tl_states = states

# -----------------------------------------------------
# RESULTS — persisted via session_state so the timeline
# and report survive reruns (e.g. clicking Download)
# -----------------------------------------------------

if st.session_state.results:

    results = st.session_state.results
    elapsed = st.session_state.elapsed

    with right_col:

        # -----------------------------------------------------
        # METRICS
        # -----------------------------------------------------

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Status","Closed")

        c2.metric("Runtime",f"{elapsed}s")

        c3.metric("Agents",
                  len(
                      [
                          k
                          for k in results.keys()
                          if "Output" in k
                      ]
                  ))

        c4.metric("Sources",
                  len(results.get("Sources",[])))

        st.markdown('<hr class="hairline"/>', unsafe_allow_html=True)

        # -----------------------------------------------------
        # PIPELINE
        # -----------------------------------------------------

        st.markdown(
            '<div class="section-head"><span class="idx">01</span>'
            '<span class="title">Agent Log</span><span class="rule"></span></div>',
            unsafe_allow_html=True
        )

        agent_order = [

            ("Research Agent","Researcher_Output"),

            ("Planning Agent","Planner_Output"),

            ("Analysis Agent","Analysis_Output"),

            ("Writer Agent","Writer_Output"),

            ("Reviewer Agent","Reviewer_Output"),

        ]

        shown=False

        for i,(title,key) in enumerate(agent_order,1):

            if key in results:

                shown=True

                with st.expander(f"FILE {i:02d} — {title.upper()}", expanded=False):

                    st.markdown(results[key])

        if not shown:

            st.info(
                "Pipeline currently returns only the final report. "
                "Expose intermediate agent outputs to see them here."
            )

        st.markdown('<hr class="hairline"/>', unsafe_allow_html=True)

        # -----------------------------------------------------
        # FINAL REPORT
        # -----------------------------------------------------

        st.markdown(
            '<div class="section-head"><span class="idx">02</span>'
            '<span class="title">Final Report</span><span class="rule"></span></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
<div class="report-box">

{results.get("Report","No report generated.")}

</div>
""",
            unsafe_allow_html=True
        )

        st.write("")

        st.download_button(

            "⬇ Download Report",

            results.get("Report",""),

            file_name="research_report.md"

        )

        st.markdown('<hr class="hairline"/>', unsafe_allow_html=True)

        # -----------------------------------------------------
        # CRITIC
        # -----------------------------------------------------

        st.markdown(
            '<div class="section-head"><span class="idx">03</span>'
            '<span class="title">Reviewer Notes</span><span class="rule"></span></div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
<div class="feedback-box">

{results.get("Feedback","No feedback available.")}

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown('<hr class="hairline"/>', unsafe_allow_html=True)

        # -----------------------------------------------------
        # SOURCES
        # -----------------------------------------------------

        st.markdown(
            '<div class="section-head"><span class="idx">04</span>'
            '<span class="title">Sources Cited</span><span class="rule"></span></div>',
            unsafe_allow_html=True
        )

        links = results.get("Sources", [])

        if links:

            unique = sorted(set(links))

            rows = "".join(
                f'<div class="source-line"><b>{i:02d}</b><a href="{link}" target="_blank">{link}</a></div>'
                for i,link in enumerate(unique,1)
            )

            st.markdown(rows, unsafe_allow_html=True)

        else:

            st.info("No sources returned.")
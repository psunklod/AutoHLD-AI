import sys
import base64
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# APPLICATION IMPORTS
# ============================================================

from backend.services.ingestion_service import IngestionService
from backend.services.architecture_service import ArchitectureService
from backend.services.pdf_service import extract_text_from_pdf
from backend.services.graph_service import GraphService
from backend.services.comparison_service import ComparisonService
from backend.services.impact_service import ImpactAnalysisService
from backend.rag.rag_service import RAGService
from backend.services.llm_service import LLMService


# ============================================================
# PATHS
# ============================================================

UPLOAD_DIR = (
    PROJECT_ROOT
    / "data"
    / "uploads"
)

ASSET_DIR = (
    PROJECT_ROOT
    / "frontend"
    / "assets"
)

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

ASSET_DIR.mkdir(
    parents=True,
    exist_ok=True
)

LOGO_PATH = (
    ASSET_DIR
    / "tata-technologies-logo.png"
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AutoHLD AI | Tata Technologies Case Study",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   GLOBAL
   ============================================================ */

.stApp {
    background:
        linear-gradient(
            180deg,
            #071a33 0%,
            #091827 28%,
            #0b111a 100%
        );
}

.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}


/* ============================================================
   BRAND HEADER
   ============================================================ */

.brand-header {
    padding: 1rem 1.35rem;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.10);

    background:
        linear-gradient(
            135deg,
            rgba(5,31,62,0.96),
            rgba(10,22,38,0.98)
        );

    margin-bottom: 1.1rem;
}

.brand-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.brand-logo {
    width: 210px;
    max-height: 58px;
    object-fit: contain;
    object-position: left center;
}

.brand-logo-fallback {
    font-size: 1rem;
    font-weight: 800;
    letter-spacing: 0.12em;
    white-space: nowrap;
}

.brand-logo-fallback span {
    display: block;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.04em;
    opacity: 0.65;
    margin-top: 0.15rem;
}

.prototype-badge {
    padding: 0.42rem 0.78rem;
    border-radius: 999px;
    border: 1px solid rgba(255,255,255,0.16);
    font-size: 0.76rem;
    opacity: 0.88;
    white-space: nowrap;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    padding: 2rem 2rem 2.15rem 2rem;
    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            rgba(9,45,88,0.96),
            rgba(10,27,47,0.98)
        );

    border: 1px solid rgba(255,255,255,0.09);
    margin-bottom: 1.25rem;
}

.hero-kicker {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    opacity: 0.70;
    margin-bottom: 0.65rem;
}

.hero-title {
    font-size: 2.7rem;
    line-height: 1.05;
    font-weight: 800;
    margin: 0;
}

.hero-subtitle {
    font-size: 1.15rem;
    margin-top: 0.65rem;
    opacity: 0.87;
}

.hero-description {
    max-width: 920px;
    margin-top: 0.9rem;
    font-size: 0.96rem;
    line-height: 1.65;
    opacity: 0.72;
}


/* ============================================================
   ENGINEERING NOTICE
   ============================================================ */

.engineering-notice {
    padding: 0.82rem 1rem;
    border-radius: 10px;

    border-left: 4px solid #4bb3fd;

    background:
        rgba(75,179,253,0.08);

    margin-bottom: 1.2rem;
    font-size: 0.86rem;
    line-height: 1.55;
}


/* ============================================================
   QUICK NAVIGATION
   ============================================================ */

.quick-nav {
    display: flex;
    gap: 0.55rem;
    flex-wrap: wrap;

    padding: 0.7rem;
    margin: 0.7rem 0 1.45rem 0;

    border-radius: 12px;

    background:
        rgba(255,255,255,0.035);

    border:
        1px solid rgba(255,255,255,0.07);
}

.quick-nav a {
    text-decoration: none;
    color: inherit;

    padding:
        0.52rem
        0.8rem;

    border-radius: 8px;

    background:
        rgba(255,255,255,0.035);

    border:
        1px solid rgba(255,255,255,0.07);

    font-size: 0.79rem;
    font-weight: 600;
}

.quick-nav a:hover {
    background:
        rgba(255,255,255,0.085);
}


/* ============================================================
   SECTION LABEL
   ============================================================ */

.section-kicker {
    font-size: 0.71rem;
    letter-spacing: 0.14em;
    font-weight: 700;
    opacity: 0.56;
    text-transform: uppercase;
    margin-bottom: -0.4rem;
}


/* ============================================================
   STATUS CARDS
   ============================================================ */

.info-card {
    padding: 1rem 1.05rem;

    min-height: 108px;

    border-radius: 14px;

    background:
        rgba(255,255,255,0.035);

    border:
        1px solid rgba(255,255,255,0.08);
}

.info-card-label {
    font-size: 0.70rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    opacity: 0.55;
}

.info-card-value {
    font-size: 1.18rem;
    font-weight: 750;
    margin-top: 0.4rem;
}

.info-card-small {
    font-size: 0.75rem;
    opacity: 0.52;
    margin-top: 0.25rem;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    margin-top: 2.4rem;
    padding-top: 1rem;

    border-top:
        1px solid rgba(255,255,255,0.09);

    text-align: center;

    font-size: 0.74rem;
    line-height: 1.7;

    opacity: 0.48;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_ARCHITECTURE = {
    "components": [],
    "interfaces": [],
    "ports": [],
    "signals": [],
    "dependencies": []
}


if "document_ready" not in st.session_state:
    st.session_state.document_ready = False

if "document_name" not in st.session_state:
    st.session_state.document_name = None

if "pages" not in st.session_state:
    st.session_state.pages = 0

if "chunks" not in st.session_state:
    st.session_state.chunks = 0

if "architecture" not in st.session_state:
    st.session_state.architecture = (
        DEFAULT_ARCHITECTURE.copy()
    )

if "comparison_result" not in st.session_state:
    st.session_state.comparison_result = None

if "impact_result" not in st.session_state:
    st.session_state.impact_result = None

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

if "last_question" not in st.session_state:
    st.session_state.last_question = None

if "last_sources" not in st.session_state:
    st.session_state.last_sources = []

if "last_context" not in st.session_state:
    st.session_state.last_context = None


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def save_uploaded_file(
    uploaded_file,
    filename: str
) -> Path:

    file_path = (
        UPLOAD_DIR
        / filename
    )

    with open(
        file_path,
        "wb"
    ) as file:

        file.write(
            uploaded_file.getbuffer()
        )

    return file_path


def extract_architecture(
    pdf_path: Path
) -> dict:

    pages = extract_text_from_pdf(
        str(pdf_path)
    )

    architecture_service = (
        ArchitectureService()
    )

    return architecture_service.extract(
        pages
    )


def get_change_counts(
    changes: dict
) -> tuple[int, int]:

    added = len(
        changes.get(
            "added",
            []
        )
    )

    removed = len(
        changes.get(
            "removed",
            []
        )
    )

    return added, removed


def display_changes(
    title: str,
    changes: dict
):

    st.subheader(title)

    added = changes.get(
        "added",
        []
    )

    removed = changes.get(
        "removed",
        []
    )

    unchanged = changes.get(
        "unchanged",
        []
    )

    if added:

        st.markdown(
            "**🟢 Added**"
        )

        for item in added:

            st.markdown(
                f"• `{item}`"
            )

    if removed:

        st.markdown(
            "**🔴 Removed**"
        )

        for item in removed:

            st.markdown(
                f"• `{item}`"
            )

    if unchanged:

        st.markdown(
            "**⚪ Unchanged**"
        )

        for item in unchanged:

            st.markdown(
                f"• `{item}`"
            )

    if (
        not added
        and not removed
        and not unchanged
    ):

        st.info(
            "No changes detected."
        )


def display_dependency_changes(
    changes: dict
):

    st.subheader(
        "Dependencies"
    )

    added = changes.get(
        "added",
        []
    )

    removed = changes.get(
        "removed",
        []
    )

    unchanged = changes.get(
        "unchanged",
        []
    )

    if added:

        st.markdown(
            "**🟢 Added**"
        )

        for source, target in added:

            st.markdown(
                f"• **{source}** → **{target}**"
            )

    if removed:

        st.markdown(
            "**🔴 Removed**"
        )

        for source, target in removed:

            st.markdown(
                f"• **{source}** → **{target}**"
            )

    if unchanged:

        st.markdown(
            "**⚪ Unchanged**"
        )

        for source, target in unchanged:

            st.markdown(
                f"• **{source}** → **{target}**"
            )

    if (
        not added
        and not removed
        and not unchanged
    ):

        st.info(
            "No dependency changes detected."
        )


def display_revision_summary(
    comparison: dict
):

    categories = {
        "Components": comparison["components"],
        "Interfaces": comparison["interfaces"],
        "Ports": comparison["ports"],
        "Signals": comparison["signals"],
        "Dependencies": comparison["dependencies"],
    }

    total_added = 0
    total_removed = 0

    for changes in categories.values():

        added, removed = (
            get_change_counts(
                changes
            )
        )

        total_added += added
        total_removed += removed

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Added",
        total_added
    )

    col2.metric(
        "Removed",
        total_removed
    )

    col3.metric(
        "Total Changes",
        total_added + total_removed
    )

    if (
        total_added == 0
        and total_removed == 0
    ):

        st.success(
            "No architecture changes detected."
        )

    else:

        st.info(
            f"{total_added} additions and "
            f"{total_removed} removals detected."
        )


def display_source_evidence():

    sources = (
        st.session_state.last_sources
    )

    if not sources:
        return

    st.subheader(
        "Source Evidence"
    )

    for index, source in enumerate(
        sources,
        start=1
    ):

        page = source["page"]

        section = (
            source.get("section")
            or "Unknown section"
        )

        text = source["text"]

        distance = source["distance"]

        with st.expander(
            f"📄 Page {page} · "
            f"{section} · Evidence {index}"
        ):

            st.caption(
                f"Retrieval distance: "
                f"{distance:.4f}"
            )

            st.code(
                text,
                language=None
            )


def display_impact_analysis(
    impact_result: dict
):

    if not impact_result:
        return

    impacts = impact_result.get(
        "impacts",
        []
    )

    st.subheader(
        "Potential Engineering Impact"
    )

    st.warning(
        "These are review suggestions only. "
        "They are not automatic engineering decisions."
    )

    if not impacts:

        st.success(
            "No potential review items were identified."
        )

        return

    for impact in impacts:

        with st.expander(
            f"⚠ {impact['type']}: "
            f"{impact['item']}"
        ):

            st.markdown(
                f"**Reason:** {impact['reason']}"
            )

            st.markdown(
                "**Suggested review areas:**"
            )

            for check in impact["checks"]:

                st.markdown(
                    f"• {check}"
                )


# ============================================================
# TATA TECHNOLOGIES HEADER
# ============================================================

if LOGO_PATH.exists():

    try:

        with open(LOGO_PATH, "rb") as logo_file:
            logo_base64 = base64.b64encode(
                logo_file.read()
            ).decode("utf-8")

        header_html = (
            '<div class="brand-header">'
            '<div class="brand-row">'
            f'<img class="brand-logo" '
            f'src="data:image/png;base64,{logo_base64}" '
            f'alt="Tata Technologies Logo">'
            '<div class="prototype-badge">'
            'Candidate Prototype'
            '</div>'
            '</div>'
            '</div>'
        )

        st.markdown(
            header_html,
            unsafe_allow_html=True
        )

    except Exception:

        st.markdown(
            (
                '<div class="brand-header">'
                '<div class="brand-row">'
                '<div class="brand-logo-fallback">'
                'TATA TECHNOLOGIES'
                '<span>'
                'Engineering a better world'
                '</span>'
                '</div>'
                '<div class="prototype-badge">'
                'Candidate Prototype'
                '</div>'
                '</div>'
                '</div>'
            ),
            unsafe_allow_html=True
        )

else:

    st.markdown(
        (
            '<div class="brand-header">'
            '<div class="brand-row">'
            '<div class="brand-logo-fallback">'
            'TATA TECHNOLOGIES'
            '<span>'
            'Engineering a better world'
            '</span>'
            '</div>'
            '<div class="prototype-badge">'
            'Candidate Prototype'
            '</div>'
            '</div>'
            '</div>'
        ),
        unsafe_allow_html=True
    )

# ============================================================
# HERO
# ============================================================

st.markdown(
    """<div class="hero">
<div class="hero-kicker">AUTOMOTIVE ENGINEERING AI · CASE STUDY PROTOTYPE</div>
<div class="hero-title">🚗 AutoHLD AI</div>
<div class="hero-subtitle">AUTOSAR Architecture Intelligence</div>
<div class="hero-description">
AI-assisted analysis of AUTOSAR High-Level Design documents
using architecture extraction, grounded retrieval,
dependency mapping, revision intelligence, and local AI.
</div>
</div>""",
    unsafe_allow_html=True
)


# ============================================================
# ENGINEERING NOTICE
# ============================================================

st.markdown(
    """<div class="engineering-notice">
🛡️ <strong>Engineering Review Required</strong><br>
AI-assisted analysis should be verified against the approved
HLD before engineering decisions are made.
</div>""",
    unsafe_allow_html=True
)


# ============================================================
# QUICK NAVIGATION
# ============================================================

st.markdown(
    """
    <div class="quick-nav">
        <a href="#hld-document">01 · Document</a>
        <a href="#architecture-overview">02 · Architecture</a>
        <a href="#ask-your-hld">03 · Ask HLD</a>
        <a href="#revision-intelligence">04 · Revisions</a>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# ANALYSIS STATUS
# ============================================================

if st.session_state.document_ready:

    st.markdown(
        """
        <div class="section-kicker">
            CURRENT ANALYSIS
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader(
        "Analysis Status"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Status",
            "Ready"
        )

    with col2:

        st.metric(
            "Pages",
            st.session_state.pages
        )

    with col3:

        st.metric(
            "Chunks",
            st.session_state.chunks
        )

    with col4:

        st.metric(
            "Components",
            len(
                st.session_state.architecture[
                    "components"
                ]
            )
        )

    st.caption(
        f"Active HLD: "
        f"{st.session_state.document_name}"
    )


# ============================================================
# 1. HLD DOCUMENT
# ============================================================

st.markdown(
    '<div id="hld-document"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-kicker">01 · DOCUMENT</div>',
    unsafe_allow_html=True
)

st.header(
    "HLD Document"
)

uploaded_file = st.file_uploader(
    "Upload an AUTOSAR HLD PDF",
    type=["pdf"],
    key="main_hld"
)


if uploaded_file is not None:

    if st.button(
        "⚙️ Process HLD",
        type="primary",
        use_container_width=True
    ):

        try:

            save_path = (
                save_uploaded_file(
                    uploaded_file,
                    uploaded_file.name
                )
            )

            with st.spinner(
                "Extracting and indexing HLD..."
            ):

                ingestion = (
                    IngestionService()
                )

                result = ingestion.process_pdf(
                    str(save_path)
                )

                architecture = (
                    extract_architecture(
                        save_path
                    )
                )

                st.session_state.document_ready = True

                st.session_state.document_name = (
                    uploaded_file.name
                )

                st.session_state.pages = (
                    result["pages"]
                )

                st.session_state.chunks = (
                    result["chunks"]
                )

                st.session_state.architecture = (
                    architecture
                )

                st.session_state.last_answer = None
                st.session_state.last_question = None
                st.session_state.last_sources = []
                st.session_state.last_context = None

                st.session_state.comparison_result = None
                st.session_state.impact_result = None

            st.success(
                "HLD processed successfully."
            )

        except Exception as error:

            st.error(
                f"Unable to process HLD: {error}"
            )


# ============================================================
# DOCUMENT STATUS CARDS
# ============================================================

if st.session_state.document_ready:

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="info-card">
                <div class="info-card-label">
                    Document
                </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
                <div class="info-card-value">
                    {st.session_state.document_name}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-label">
                    Pages
                </div>
                <div class="info-card-value">
                    {st.session_state.pages}
                </div>
                <div class="info-card-small">
                    Extracted pages
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-card-label">
                    Chunks
                </div>
                <div class="info-card-value">
                    {st.session_state.chunks}
                </div>
                <div class="info-card-small">
                    Searchable evidence units
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 2. ARCHITECTURE OVERVIEW
# ============================================================

if st.session_state.document_ready:

    st.markdown(
        '<div id="architecture-overview"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-kicker">02 · ARCHITECTURE</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Architecture Overview"
    )

    architecture = (
        st.session_state.architecture
    )

    components = architecture["components"]
    interfaces = architecture["interfaces"]
    ports = architecture["ports"]
    signals = architecture["signals"]
    dependencies = architecture["dependencies"]


    # --------------------------------------------------------
    # Counts
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Components",
        len(components)
    )

    col2.metric(
        "Interfaces",
        len(interfaces)
    )

    col3.metric(
        "Ports",
        len(ports)
    )

    col4.metric(
        "Signals",
        len(signals)
    )


    # --------------------------------------------------------
    # Components
    # --------------------------------------------------------

    with st.expander(
        "Software Components",
        expanded=True
    ):

        if components:

            for component in components:

                st.markdown(
                    f"• **{component}**"
                )

        else:

            st.info(
                "No software components detected."
            )


    # --------------------------------------------------------
    # Interfaces
    # --------------------------------------------------------

    with st.expander(
        "Interfaces"
    ):

        if interfaces:

            for interface in interfaces:

                st.markdown(
                    f"• **{interface}**"
                )

        else:

            st.info(
                "No interfaces detected."
            )


    # --------------------------------------------------------
    # Ports
    # --------------------------------------------------------

    with st.expander(
        "Ports"
    ):

        if ports:

            for port in ports:

                st.markdown(
                    f"• **{port}**"
                )

        else:

            st.info(
                "No ports detected."
            )


    # --------------------------------------------------------
    # Signals
    # --------------------------------------------------------

    with st.expander(
        "Signals"
    ):

        if signals:

            for signal in signals:

                st.markdown(
                    f"• **{signal}**"
                )

        else:

            st.info(
                "No signals detected."
            )


    # --------------------------------------------------------
    # Dependency Graph
    # --------------------------------------------------------

    st.subheader(
        "Dependency Graph"
    )

    if dependencies:

        try:

            graph_service = GraphService()

            graph = (
                graph_service.create_dependency_graph(
                    dependencies
                )
            )

            st.graphviz_chart(
                graph.source,
                use_container_width=True
            )

        except Exception as error:

            st.warning(
                f"Unable to render dependency graph: "
                f"{error}"
            )

    else:

        st.info(
            "No dependency graph available."
        )


# ============================================================
# 3. ASK YOUR HLD
# ============================================================

if st.session_state.document_ready:

    st.markdown(
        '<div id="ask-your-hld"></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-kicker">03 · INTELLIGENCE</div>',
        unsafe_allow_html=True
    )

    st.header(
        "Ask Your HLD"
    )

    question = st.text_input(
        "Engineering question",
        placeholder=(
            "What dependencies are defined?"
        )
    )


    if st.button(
        "🔎 Ask AI",
        type="primary",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            try:

                with st.spinner(
                    "Analyzing HLD evidence..."
                ):

                    rag = RAGService()

                    # One retrieval only
                    result = rag.prepare_question(
                        question,
                        top_k=3
                    )

                    llm = LLMService()

                    answer = llm.generate_answer(
                        question=result["question"],
                        context=result["context"]
                    )

                    # Save answer
                    st.session_state.last_question = (
                        result["question"]
                    )

                    st.session_state.last_answer = (
                        answer
                    )

                    st.session_state.last_context = (
                        result["context"]
                    )

                    # SAME retrieval result used
                    # for evidence display
                    st.session_state.last_sources = (
                        result["sources"]
                    )


            except Exception as error:

                st.error(
                    f"Unable to generate answer: "
                    f"{error}"
                )


    # --------------------------------------------------------
    # Answer + Evidence
    # --------------------------------------------------------

    if st.session_state.last_answer:

        st.subheader(
            "AI Answer"
        )

        st.info(
            st.session_state.last_answer
        )


        source_pages = sorted(
            {
                source["page"]
                for source
                in st.session_state.last_sources
            }
        )


        if source_pages:

            st.caption(
                "Sources: "
                + ", ".join(
                    f"Page {page}"
                    for page in source_pages
                )
            )


        display_source_evidence()


# ============================================================
# 4. REVISION INTELLIGENCE
# ============================================================

st.markdown(
    '<div id="revision-intelligence"></div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-kicker">04 · CHANGE ANALYSIS</div>',
    unsafe_allow_html=True
)

st.header(
    "Revision Intelligence"
)

st.write(
    "Compare two HLD revisions to identify architecture "
    "changes and potential engineering review areas."
)


col1, col2 = st.columns(2)


with col1:

    st.subheader(
        "Previous Revision"
    )

    old_file = st.file_uploader(
        "Upload previous HLD",
        type=["pdf"],
        key="old_hld"
    )


with col2:

    st.subheader(
        "New Revision"
    )

    new_file = st.file_uploader(
        "Upload new HLD",
        type=["pdf"],
        key="new_hld"
    )


if (
    old_file is not None
    and new_file is not None
):

    if st.button(
        "📊 Compare Revisions",
        type="primary",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "Comparing architecture revisions..."
            ):

                # ------------------------------------------------
                # Save revisions
                # ------------------------------------------------

                old_path = save_uploaded_file(
                    old_file,
                    f"old_{old_file.name}"
                )

                new_path = save_uploaded_file(
                    new_file,
                    f"new_{new_file.name}"
                )


                # ------------------------------------------------
                # Extract architecture
                # ------------------------------------------------

                old_architecture = (
                    extract_architecture(
                        old_path
                    )
                )

                new_architecture = (
                    extract_architecture(
                        new_path
                    )
                )


                # ------------------------------------------------
                # Compare revisions
                # ------------------------------------------------

                comparison_service = (
                    ComparisonService()
                )

                comparison = (
                    comparison_service.compare(
                        old_architecture,
                        new_architecture
                    )
                )


                # ------------------------------------------------
                # Impact analysis
                # ------------------------------------------------

                impact_service = (
                    ImpactAnalysisService()
                )

                impact = (
                    impact_service.analyze(
                        comparison
                    )
                )


                # ------------------------------------------------
                # Store results
                # ------------------------------------------------

                st.session_state.comparison_result = (
                    comparison
                )

                st.session_state.impact_result = (
                    impact
                )


            st.success(
                "Revision comparison completed."
            )


        except Exception as error:

            st.error(
                f"Unable to compare revisions: "
                f"{error}"
            )


# ============================================================
# REVISION RESULTS
# ============================================================

if st.session_state.comparison_result is not None:

    comparison = (
        st.session_state.comparison_result
    )


    st.divider()

    st.subheader(
        "Revision Summary"
    )

    display_revision_summary(
        comparison
    )


    with st.expander(
        "Component Changes"
    ):

        display_changes(
            "Software Components",
            comparison["components"]
        )


    with st.expander(
        "Interface Changes"
    ):

        display_changes(
            "Interfaces",
            comparison["interfaces"]
        )


    with st.expander(
        "Port Changes"
    ):

        display_changes(
            "Ports",
            comparison["ports"]
        )


    with st.expander(
        "Signal Changes"
    ):

        display_changes(
            "Signals",
            comparison["signals"]
        )


    with st.expander(
        "Dependency Changes"
    ):

        display_dependency_changes(
            comparison["dependencies"]
        )


    if st.session_state.impact_result:

        display_impact_analysis(
            st.session_state.impact_result
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Tata Technologies · Candidate Case Study Prototype<br>
        AutoHLD AI · AUTOSAR Architecture Intelligence<br>
        AI-assisted engineering analysis with human review
    </div>
    """,
    unsafe_allow_html=True
)
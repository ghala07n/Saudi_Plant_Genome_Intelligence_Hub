import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import spearmanr
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION & THEME
# ============================================================================

st.set_page_config(
    page_title="Saudi Plant Genome Intelligence Hub",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# MODERN DARK THEME CSS INJECTION
# ============================================================================

DARK_THEME_CSS = """
<style>
    /* Global color scheme */
    :root {
        --bg-dark: #0e1117;
        --bg-card: #161b22;
        --bg-hover: #21262d;
        --text-primary: #f0f6fc;
        --text-secondary: #8b949e;
        --accent-primary: #58a6ff;
        --accent-secondary: #79c0ff;
        --accent-danger: #f85149;
        --accent-success: #3fb950;
        --accent-warning: #d29922;
        --border-color: #30363d;
    }

    /* Main page background */
    .main {
        background-color: var(--bg-dark) !important;
    }

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: var(--bg-dark) !important;
    }

    /* Text colors */
    body, p, span, div, label {
        color: var(--text-primary) !important;
    }

    /* Header & title styling */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px;
    }

    /* Metric cards styling */
    [data-testid="metric-container"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 12px !important;
        padding: 24px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="metric-container"]:hover {
        background-color: var(--bg-hover) !important;
        border-color: var(--accent-primary) !important;
        box-shadow: 0 8px 32px rgba(88, 166, 255, 0.2) !important;
    }

    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
    }

    /* Button styling */
    .stButton > button {
        background-color: var(--accent-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background-color: var(--accent-secondary) !important;
        box-shadow: 0 4px 12px rgba(88, 166, 255, 0.3) !important;
    }

    /* Selectbox & input styling */
    .stSelectbox, .stTextInput, .stMultiSelect {
        background-color: var(--bg-card) !important;
    }

    .stSelectbox [data-testid="stSelectbox"] > div > div,
    .stTextInput input,
    .stMultiSelect [data-testid="stMultiSelect"] > div > div {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        color: var(--text-primary) !important;
    }

    .stSelectbox [data-testid="stSelectbox"] > div > div:hover,
    .stTextInput input:hover,
    .stMultiSelect [data-testid="stMultiSelect"] > div > div:hover {
        border-color: var(--accent-primary) !important;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid var(--border-color) !important;
    }

    .stTabs [role="tab"] {
        color: var(--text-secondary) !important;
        border: none !important;
    }

    .stTabs [role="tab"][aria-selected="true"] {
        color: var(--accent-primary) !important;
        border-bottom: 2px solid var(--accent-primary) !important;
    }

    /* Card containers */
    .metric-card {
        background: linear-gradient(135deg, var(--bg-card) 0%, rgba(88, 166, 255, 0.05) 100%);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        border-color: var(--accent-primary);
        box-shadow: 0 8px 32px rgba(88, 166, 255, 0.2);
        transform: translateY(-2px);
    }

    /* Hero banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(88, 166, 255, 0.1) 0%, rgba(79, 185, 240, 0.05) 100%);
        border: 1px solid var(--accent-primary);
        border-radius: 16px;
        padding: 48px 32px;
        text-align: center;
        box-shadow: 0 8px 32px rgba(88, 166, 255, 0.15);
        margin-bottom: 32px;
    }

    .hero-banner h1 {
        font-size: 2.5em;
        margin: 0 0 12px 0;
        background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-banner p {
        font-size: 1.1em;
        color: var(--text-secondary);
        margin: 0;
    }

    /* Badge styling */
    .badge {
        display: inline-block;
        background-color: rgba(88, 166, 255, 0.2);
        border: 1px solid var(--accent-primary);
        color: var(--accent-secondary);
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.9em;
        font-weight: 600;
        margin: 4px;
    }

    /* Info box styling */
    .stInfo, [data-testid="stAlert"] {
        background-color: rgba(88, 166, 255, 0.1) !important;
        border: 1px solid var(--accent-primary) !important;
        border-radius: 8px !important;
        padding: 16px !important;
    }

    /* Markdown styling */
    .stMarkdown p {
        line-height: 1.6;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-color), transparent);
        margin: 32px 0;
    }

    /* Plotly chart container */
    [data-testid="plotly-chart"] {
        background-color: var(--bg-card) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border-color) !important;
        padding: 16px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
    }

    /* Caption styling */
    .stCaption {
        color: var(--text-secondary) !important;
        font-size: 0.85em !important;
    }

    /* Spinner override */
    .stSpinner > div > div {
        border-top-color: var(--accent-primary) !important;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }

    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-primary);
    }
</style>
"""

st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

# ============================================================================
# DATA LOADING & CONSTANTS
# ============================================================================

DATA_DIR = "data"

# Validated constants (from verified CSV data)
VALIDATED_CONSTANTS = {
    "chromosomes": 18,
    "total_genes": 23679,
    "protein_coding": 20805,
    "protein_coding_pct": 87.86,
    "salinity_candidates": 1795,
    "genome_size_mb": 385.59,
    "gene_density": 61.41,
    "protein_coding_density": 53.96,
}

# Salinity category breakdown (from verified data)
SALINITY_CATEGORIES = {
    "Protein_Kinases": 1607,
    "Stress_Osmoprotectants": 80,
    "Ion_Transporters": 61,
    "Transcription_Factors": 27,
    "Other_Signaling_Metabolism": 20,
}

SPEARMAN_CORRELATIONS = {
    "gc_vs_gene_density": -0.4902,
    "gc_vs_protein_coding_density": -0.4778,
}

@st.cache_data
def load_datasets(data_dir=DATA_DIR):
    """Load CSV files from data directory with strict validation."""
    files = {
        "candidates": "salinity_candidates_categorized.csv",
        "gene_density": "chromosome_gene_density.csv",
        "gc_density": "chromosome_gc_gene_density_clean.csv",
        "genome_summary": "genome_annotation_summary.csv",
        "chr_summary": "chromosome_annotation_summary.csv",
        "protein_stats": "chromosome_protein_coding_stats.csv",
    }
    out = {}
    for key, fname in files.items():
        path = os.path.join(data_dir, fname)
        if os.path.exists(path):
            try:
                out[key] = pd.read_csv(path)
            except Exception as e:
                st.warning(f"⚠️ Error loading {fname}: {str(e)}")
                out[key] = None
        else:
            out[key] = None
    return out

data = load_datasets()
candidates_df = data.get("candidates")
gene_density_df = data.get("gene_density")
gc_density_df = data.get("gc_density")
genome_summary_df = data.get("genome_summary")
chr_summary_df = data.get("chr_summary")
protein_stats_df = data.get("protein_stats")

def df_ok(df):
    """Check if dataframe exists and is not empty."""
    return df is not None and isinstance(df, pd.DataFrame) and not df.empty

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_metric_card(label, value, unit="", icon="📊"):
    """Create styled metric card HTML."""
    return f"""
    <div class="metric-card">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <p style="margin: 0; color: #8b949e; font-size: 0.95em; font-weight: 500;">{label}</p>
                <p style="margin: 8px 0 0 0; font-size: 2em; font-weight: 700; color: #58a6ff;">
                    {value} <span style="font-size: 0.6em; color: #8b949e;">{unit}</span>
                </p>
            </div>
            <div style="font-size: 2.5em;">{icon}</div>
        </div>
    </div>
    """

def finalize_plotly_figure(fig, title="", height=500):
    """Apply consistent styling to Plotly figures."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#161b22",
        font=dict(family="Segoe UI, sans-serif", size=12, color="#f0f6fc"),
        title=dict(text=title, font=dict(size=16, color="#f0f6fc")),
        margin=dict(l=50, r=50, t=80, b=60),
        height=height,
        hovermode="closest",
        showlegend=True,
        legend=dict(
            bgcolor="rgba(22, 27, 34, 0.8)",
            bordercolor="#30363d",
            borderwidth=1,
            font=dict(size=11),
        ),
    )
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="#30363d",
        showline=True,
        linewidth=1,
        linecolor="#30363d",
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="#30363d",
        showline=True,
        linewidth=1,
        linecolor="#30363d",
    )
    return fig

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown("### 🧬 SPGIH Portal")
    st.markdown("---")
    
    nav_sections = {
        "🏠 Home": "home",
        "📊 Genome Overview": "genome_overview",
        "🗺️ Chromosome Explorer": "chromosome_explorer",
        "🔬 Salinity Candidates": "salinity_candidates",
        "🛠️ Tool Center": "tool_center",
        "🤖 AI Gene Analyst": "ai_analyst",
    }
    
    selected_nav = st.radio("Navigation", list(nav_sections.keys()), label_visibility="collapsed")
    current_page = nav_sections[selected_nav]
    
    st.markdown("---")
    
    # Data status
    st.markdown("### 📁 Data Status")
    data_status = {
        "Salinity Candidates": df_ok(candidates_df),
        "Gene Density": df_ok(gene_density_df),
        "GC Density": df_ok(gc_density_df),
        "Genome Summary": df_ok(genome_summary_df),
    }
    
    for name, status in data_status.items():
        status_icon = "✅" if status else "❌"
        st.caption(f"{status_icon} {name}")
    
    st.markdown("---")
    st.caption("Phoenix dactylifera · Salinity Genomics")

# ============================================================================
# PAGE: HOME
# ============================================================================

if current_page == "home":
    # Hero Banner
    st.markdown("""
    <div class="hero-banner">
        <h1>🧬 Saudi Plant Genome Intelligence Hub</h1>
        <p>Phoenix dactylifera — Advanced Genomic Analysis & Salinity Research Portal</p>
        <div style="margin-top: 20px;">
            <span class="badge">🌴 18 Chromosomes</span>
            <span class="badge">🔬 23,679 Genes</span>
            <span class="badge">⚡ 1,795 Salinity Candidates</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # KPI Grid
    st.markdown("### 📈 Genome Summary Metrics")
    
    kpi_cols = st.columns(5)
    
    with kpi_cols[0]:
        st.markdown(create_metric_card(
            "Chromosomes",
            VALIDATED_CONSTANTS["chromosomes"],
            icon="🗺️"
        ), unsafe_allow_html=True)
    
    with kpi_cols[1]:
        st.markdown(create_metric_card(
            "Total Genes",
            f"{VALIDATED_CONSTANTS['total_genes']:,}",
            icon="🧬"
        ), unsafe_allow_html=True)
    
    with kpi_cols[2]:
        st.markdown(create_metric_card(
            "Protein-Coding",
            f"{VALIDATED_CONSTANTS['protein_coding']:,}",
            icon="⚙️"
        ), unsafe_allow_html=True)
    
    with kpi_cols[3]:
        st.markdown(create_metric_card(
            "Salinity Candidates",
            f"{VALIDATED_CONSTANTS['salinity_candidates']}",
            icon="🌊"
        ), unsafe_allow_html=True)
    
    with kpi_cols[4]:
        st.markdown(create_metric_card(
            "Assembly Size",
            f"{VALIDATED_CONSTANTS['genome_size_mb']}",
            "Mb",
            icon="💾"
        ), unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin-top: 0;">🔬 Salinity Candidates</h3>
            <p style="color: #8b949e; line-height: 1.6;">
            Explore 1,795 functionally categorized genes involved in salt-stress response and tolerance mechanisms in date palm.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin-top: 0;">🗺️ Chromosome Analysis</h3>
            <p style="color: #8b949e; line-height: 1.6;">
            Analyze gene distribution, density patterns, and GC content across all 18 nuclear chromosomes with interactive visualizations.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3 style="margin-top: 0;">🤖 AI Gene Analysis</h3>
            <p style="color: #8b949e; line-height: 1.6;">
            Query the AI analyst layer to understand gene functions, predict salinity responses, and discover functional relationships.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick stats
    st.markdown("### 📊 Quick Statistics")
    
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    with stats_col1:
        st.metric("Protein-Coding %", f"{VALIDATED_CONSTANTS['protein_coding_pct']}%")
    
    with stats_col2:
        st.metric("Gene Density (avg)", f"{VALIDATED_CONSTANTS['gene_density']} genes/Mb")
    
    with stats_col3:
        st.metric("PC Gene Density (avg)", f"{VALIDATED_CONSTANTS['protein_coding_density']} genes/Mb")

# ============================================================================
# PAGE: GENOME OVERVIEW
# ============================================================================

elif current_page == "genome_overview":
    st.markdown("### 📊 Genome Overview")
    st.write("Interactive genome-wide analysis with dynamic data binding to CSV datasets.")
    
    if not df_ok(gene_density_df):
        st.info("📋 **Not available in current dataset** — chromosome_gene_density.csv missing or empty")
    else:
        # Chromosome lengths
        if "length_Mb" in gene_density_df.columns and "chromosome" in gene_density_df.columns:
            df_plot = gene_density_df.sort_values("length_Mb", ascending=True)
            fig = px.bar(
                df_plot,
                x="length_Mb",
                y="chromosome",
                orientation="h",
                labels={"length_Mb": "Length (Mb)", "chromosome": "Chromosome"},
                title="Chromosome Lengths (Mb)",
                color="length_Mb",
                color_continuous_scale="Viridis",
            )
            fig = finalize_plotly_figure(fig, height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # Gene counts per chromosome
        if "total_genes" in gene_density_df.columns and "chromosome" in gene_density_df.columns:
            df_genes = gene_density_df.sort_values("total_genes", ascending=True)
            fig = px.bar(
                df_genes,
                x="total_genes",
                y="chromosome",
                orientation="h",
                labels={"total_genes": "Total Genes", "chromosome": "Chromosome"},
                title="Total Genes per Chromosome",
                color="total_genes",
                color_continuous_scale="Blues",
            )
            fig = finalize_plotly_figure(fig, height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # Protein-coding genes
        if "protein_coding" in gene_density_df.columns:
            df_pc = gene_density_df.sort_values("protein_coding", ascending=True)
            fig = px.bar(
                df_pc,
                x="protein_coding",
                y="chromosome",
                orientation="h",
                labels={"protein_coding": "Protein-Coding Genes"},
                title="Protein-Coding Genes per Chromosome",
                color="protein_coding",
                color_continuous_scale="Greens",
            )
            fig = finalize_plotly_figure(fig, height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # Gene density
        if "gene_density_per_Mb" in gene_density_df.columns:
            df_density = gene_density_df.sort_values("gene_density_per_Mb", ascending=True)
            fig = px.bar(
                df_density,
                x="gene_density_per_Mb",
                y="chromosome",
                orientation="h",
                labels={"gene_density_per_Mb": "Genes per Mb"},
                title="Gene Density per Chromosome (genes/Mb)",
                color="gene_density_per_Mb",
                color_continuous_scale="Reds",
            )
            fig = finalize_plotly_figure(fig, height=500)
            st.plotly_chart(fig, use_container_width=True)
        
        # GC content analysis
        if df_ok(gc_density_df) and "GC_percent" in gc_density_df.columns:
            df_gc = gc_density_df.sort_values("GC_percent")
            fig = px.bar(
                df_gc,
                x="GC_percent",
                y="chromosome",
                orientation="h",
                labels={"GC_percent": "GC %"},
                title="GC Content per Chromosome (%)",
                color="GC_percent",
                color_continuous_scale="Plasma",
            )
            fig = finalize_plotly_figure(fig, height=500)
            st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.markdown("---")
    st.markdown("### 📋 Detailed Chromosome Data")
    if df_ok(gene_density_df):
        st.dataframe(gene_density_df, use_container_width=True, height=400)
    else:
        st.info("📋 **Not available in current dataset** — chromosome_gene_density.csv missing")

# ============================================================================
# PAGE: CHROMOSOME EXPLORER
# ============================================================================

elif current_page == "chromosome_explorer":
    st.markdown("### 🗺️ Chromosome Explorer")
    st.write("Select and analyze individual chromosomes in detail.")
    
    if not df_ok(gene_density_df):
        st.info("📋 **Not available in current dataset** — chromosome_gene_density.csv missing")
    else:
        chr_list = sorted(gene_density_df["chromosome"].astype(str).unique().tolist())
        selected_chr = st.selectbox("Select Chromosome", options=chr_list)
        
        chr_data = gene_density_df[gene_density_df["chromosome"].astype(str) == str(selected_chr)].iloc[0]
        
        # Chromosome metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Length (Mb)", f"{chr_data.get('length_Mb', 'N/A')}")
        with col2:
            st.metric("Total Genes", f"{chr_data.get('total_genes', 'N/A')}")
        with col3:
            st.metric("Protein-Coding", f"{chr_data.get('protein_coding', 'N/A')}")
        with col4:
            st.metric("Gene Density", f"{chr_data.get('gene_density_per_Mb', 'N/A')} genes/Mb")
        
        st.markdown("---")
        
        # Position visualization
        if "length_bp" in chr_data.index or "length_Mb" in chr_data.index:
            try:
                if "length_bp" in chr_data.index:
                    chr_len = float(chr_data["length_bp"])
                else:
                    chr_len = float(chr_data["length_Mb"]) * 1e6
                
                # Create chromosome ideogram
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=[chr_len],
                    y=[selected_chr],
                    orientation="h",
                    marker=dict(color="#58a6ff", line=dict(color="#30363d", width=2)),
                    showlegend=False,
                    text=f"{chr_len/1e6:.2f} Mb",
                    textposition="outside",
                ))
                fig.update_layout(
                    title=f"Chromosome {selected_chr} Ideogram",
                    xaxis_title="Base Pairs (bp)",
                    yaxis_title="",
                    height=200,
                    template="plotly_dark",
                    paper_bgcolor="#0e1117",
                    plot_bgcolor="#161b22",
                    margin=dict(l=50, r=50, t=60, b=50),
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception:
                st.info("Position visualization not available for this chromosome")
        
        st.markdown("---")
        
        # Compare to genome average
        if "gene_density_per_Mb" in gene_density_df.columns:
            avg_density = float(gene_density_df["gene_density_per_Mb"].astype(float).mean())
            chr_density = float(chr_data.get("gene_density_per_Mb", 0))
            deviation = chr_density - avg_density
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Genome Avg Density", f"{avg_density:.2f} genes/Mb")
            with col2:
                st.metric("This Chr Density", f"{chr_density:.2f} genes/Mb")
            with col3:
                status = "🟢 Above" if deviation > 0 else "🔴 Below"
                st.metric(status, f"{abs(deviation):.2f} genes/Mb")

# ============================================================================
# PAGE: SALINITY CANDIDATES
# ============================================================================

elif current_page == "salinity_candidates":
    st.markdown("### 🔬 Salinity Candidate Explorer")
    st.write("Browse and filter 1,795 functionally categorized genes involved in salt-stress response.")
    
    if not df_ok(candidates_df):
        st.info("📋 **Not available in current dataset** — salinity_candidates_categorized.csv missing")
    else:
        # Category breakdown
        st.markdown("#### 📊 Category Distribution")
        
        if "functional_category" in candidates_df.columns:
            cat_counts = candidates_df["functional_category"].value_counts()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.pie(
                    values=cat_counts.values,
                    names=cat_counts.index,
                    title="Salinity Candidate Categories",
                    color_discrete_sequence=px.colors.qualitative.Set2,
                )
                fig = finalize_plotly_figure(fig, height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("**Category Counts:**")
                for cat, count in cat_counts.items():
                    st.caption(f"• {cat}: {count}")
        
        st.markdown("---")
        
        # Filters
        st.markdown("#### 🔍 Filter & Search")
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            cats = ["All"] + sorted(candidates_df["functional_category"].fillna("Unknown").unique().tolist())
            selected_cat = st.selectbox("Functional Category", options=cats)
        
        with filter_col2:
            chrs = ["All"] + sorted(candidates_df["chromosome"].astype(str).unique().tolist())
            selected_chr = st.selectbox("Chromosome", options=chrs)
        
        with filter_col3:
            search_term = st.text_input("Search (Gene ID or Description)", placeholder="LOC103723720...")
        
        # Apply filters
        filtered = candidates_df.copy()
        
        if selected_cat != "All":
            filtered = filtered[filtered["functional_category"] == selected_cat]
        
        if selected_chr != "All":
            filtered = filtered[filtered["chromosome"].astype(str) == str(selected_chr)]
        
        if search_term:
            mask = pd.Series([False] * len(filtered), index=filtered.index)
            if "gene_id" in filtered.columns:
                mask = mask | filtered["gene_id"].astype(str).str.contains(search_term, case=False, na=False)
            if "product_description" in filtered.columns:
                mask = mask | filtered["product_description"].astype(str).str.contains(search_term, case=False, na=False)
            filtered = filtered[mask]
        
        # Results
        st.markdown(f"### 📋 Results: {len(filtered):,} genes")
        
        if filtered.empty:
            st.warning("⚠️ No genes match your filters")
        else:
            st.dataframe(filtered, use_container_width=True, height=500)
            
            # Download button
            try:
                csv = filtered.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Filtered Results (CSV)",
                    data=csv,
                    file_name="salinity_candidates_filtered.csv",
                    mime="text/csv"
                )
            except Exception:
                st.warning("Unable to prepare download")

# ============================================================================
# PAGE: TOOL CENTER
# ============================================================================

elif current_page == "tool_center":
    st.markdown("### 🛠️ Tool Center")
    st.write("Advanced analytical tools for genome analysis.")
    
    tool_tabs = st.tabs(["GC vs Gene Density", "Chromosome Comparison", "Gene Statistics", "Correlation Matrix"])
    
    # Tab 1: GC vs Gene Density
    with tool_tabs[0]:
        st.markdown("#### 📈 GC Content vs Gene Density Analysis")
        
        if not df_ok(gc_density_df):
            st.info("📋 **Not available in current dataset** — chromosome_gc_gene_density_clean.csv missing")
        else:
            if "GC_percent" in gc_density_df.columns and "gene_density_per_Mb" in gc_density_df.columns:
                df_gc = gc_density_df.dropna(subset=["GC_percent", "gene_density_per_Mb"])
                
                # Scatter plot with trendline
                fig = px.scatter(
                    df_gc,
                    x="GC_percent",
                    y="gene_density_per_Mb",
                    hover_name="chromosome",
                    labels={"GC_percent": "GC Content (%)", "gene_density_per_Mb": "Gene Density (genes/Mb)"},
                    title="GC Content vs Gene Density",
                    size_max=15,
                    color="gene_density_per_Mb",
                    color_continuous_scale="Viridis",
                )
                
                # Add trendline
                try:
                    x = df_gc["GC_percent"].astype(float).values
                    y = df_gc["gene_density_per_Mb"].astype(float).values
                    z = np.polyfit(x, y, 1)
                    p = np.poly1d(z)
                    x_trend = np.linspace(x.min(), x.max(), 100)
                    fig.add_trace(go.Scatter(
                        x=x_trend,
                        y=p(x_trend),
                        mode="lines",
                        name="Trend",
                        line=dict(color="#f85149", width=2, dash="dash"),
                    ))
                except Exception:
                    pass
                
                fig = finalize_plotly_figure(fig)
                st.plotly_chart(fig, use_container_width=True)
                
                # Correlation display
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Spearman ρ (GC vs Gene Density)", f"{SPEARMAN_CORRELATIONS['gc_vs_gene_density']:.4f}")
                with col2:
                    st.metric("Spearman ρ (GC vs PC Density)", f"{SPEARMAN_CORRELATIONS['gc_vs_protein_coding_density']:.4f}")
    
    # Tab 2: Chromosome Comparison
    with tool_tabs[1]:
        st.markdown("#### 🗺️ Multi-Chromosome Comparison")
        
        if not df_ok(gene_density_df):
            st.info("📋 **Not available in current dataset**")
        else:
            if "gene_density_per_Mb" in gene_density_df.columns and "protein_coding_density_per_Mb" in gene_density_df.columns:
                fig = px.scatter(
                    gene_density_df,
                    x="gene_density_per_Mb",
                    y="protein_coding_density_per_Mb",
                    hover_name="chromosome",
                    size="length_Mb" if "length_Mb" in gene_density_df.columns else None,
                    labels={"gene_density_per_Mb": "Gene Density (genes/Mb)", "protein_coding_density_per_Mb": "PC Density (genes/Mb)"},
                    title="Gene Density vs Protein-Coding Density",
                    size_max=20,
                )
                fig = finalize_plotly_figure(fig)
                st.plotly_chart(fig, use_container_width=True)
    
    # Tab 3: Gene Statistics
    with tool_tabs[2]:
        st.markdown("#### 📊 Gene Statistics")
        
        if not df_ok(protein_stats_df):
            st.info("📋 **Not available in current dataset** — chromosome_protein_coding_stats.csv missing")
        else:
            st.dataframe(protein_stats_df, use_container_width=True)
            
            if "mean_length" in protein_stats_df.columns:
                fig = px.bar(
                    protein_stats_df.sort_values("mean_length"),
                    x="mean_length",
                    y="chromosome",
                    orientation="h",
                    labels={"mean_length": "Mean Gene Length (bp)"},
                    title="Average Protein-Coding Gene Length per Chromosome",
                    color="mean_length",
                    color_continuous_scale="Turbo",
                )
                fig = finalize_plotly_figure(fig)
                st.plotly_chart(fig, use_container_width=True)
    
    # Tab 4: Correlation Matrix
    with tool_tabs[3]:
        st.markdown("#### 🔗 Correlation Analysis")
        
        if not df_ok(gc_density_df):
            st.info("📋 **Not available in current dataset**")
        else:
            numeric_cols = gc_density_df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                corr_matrix = gc_density_df[numeric_cols].corr(method="spearman")
                
                fig = px.imshow(
                    corr_matrix,
                    labels=dict(color="Spearman ρ"),
                    title="Spearman Correlation Matrix",
                    color_continuous_scale="RdBu_r",
                    color_continuous_midpoint=0,
                    zmin=-1,
                    zmax=1,
                )
                fig = finalize_plotly_figure(fig, height=600)
                st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# PAGE: AI GENE ANALYST
# ============================================================================

elif current_page == "ai_analyst":
    st.markdown("### 🤖 AI Gene Analyst")
    st.write("Query individual genes and explore their functional properties, predictions, and relationships.")
    
    if not df_ok(candidates_df):
        st.info("📋 **Not available in current dataset** — salinity_candidates_categorized.csv missing")
    else:
        if "gene_id" in candidates_df.columns:
            gene_ids = sorted(candidates_df["gene_id"].astype(str).unique().tolist())
            
            selected_gene = st.selectbox(
                "Select Gene for Analysis",
                options=[""] + gene_ids,
                label_visibility="collapsed"
            )
            
            if selected_gene:
                gene_row = candidates_df[candidates_df["gene_id"].astype(str) == str(selected_gene)].iloc[0]
                
                # Gene header
                st.markdown(f"### 🧬 {selected_gene}")
                
                # Gene properties
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    st.markdown("#### 📝 Gene Properties")
                    st.markdown(f"**Product Description:** {gene_row.get('product_description', 'Not available in current dataset')}")
                    st.markdown(f"**Functional Category:** `{gene_row.get('functional_category', 'N/A')}`")
                    st.markdown(f"**Chromosome:** `{gene_row.get('chromosome', 'N/A')}`")
                    st.markdown(f"**Position:** {gene_row.get('start', 'N/A')} - {gene_row.get('end', 'N/A')}")
                    st.markdown(f"**Strand:** `{gene_row.get('strand', 'N/A')}`")
                
                with col2:
                    st.markdown("#### 🎯 Category Info")
                    category = gene_row.get('functional_category', 'Unknown')
                    if category in SALINITY_CATEGORIES:
                        count = SALINITY_CATEGORIES[category]
                        st.metric(f"{category}", f"{count} genes")
                
                st.markdown("---")
                
                # Chromosome context
                if df_ok(gene_density_df):
                    chr_data = gene_density_df[gene_density_df["chromosome"].astype(str) == str(gene_row.get('chromosome'))].iloc[0] if gene_row.get('chromosome') else None
                    
                    if chr_data is not None:
                        st.markdown("#### 🗺️ Chromosome Context")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Chr Length", f"{chr_data.get('length_Mb', 'N/A')} Mb")
                        with col2:
                            st.metric("Chr Total Genes", f"{chr_data.get('total_genes', 'N/A')}")
                        with col3:
                            st.metric("Gene Density", f"{chr_data.get('gene_density_per_Mb', 'N/A')} g/Mb")
                        with col4:
                            st.metric("PC Density", f"{chr_data.get('protein_coding_density_per_Mb', 'N/A')} g/Mb")
                
                st.markdown("---")
                
                # Functional insights
                st.markdown("#### 💡 Functional Insights")
                
                insights = []
                
                if gene_row.get('functional_category') == 'Protein_Kinases':
                    insights.append("🔬 **Protein Kinase**: This gene encodes a signaling enzyme involved in phosphorylation-based signal transduction. Often central to stress-response pathways.")
                
                elif gene_row.get('functional_category') == 'Ion_Transporters':
                    insights.append("⚡ **Ion Transporter**: This gene encodes a membrane protein involved in ion homeostasis. Critical for maintaining cellular osmotic balance under saline conditions.")
                
                elif gene_row.get('functional_category') == 'Transcription_Factors':
                    insights.append("📖 **Transcription Factor**: This gene encodes a DNA-binding regulatory protein. Controls expression of downstream genes under stress conditions.")
                
                elif gene_row.get('functional_category') == 'Stress_Osmoprotectants':
                    insights.append("🛡️ **Stress/Osmoprotectant**: This gene is involved in osmotic protection and cellular adaptation to high salt concentrations.")
                
                elif gene_row.get('functional_category') == 'Other_Signaling_Metabolism':
                    insights.append("⚙️ **Other Signaling/Metabolism**: This gene participates in metabolic or signaling processes relevant to salinity stress response.")
                
                if insights:
                    for insight in insights:
                        st.markdown(insight)
                else:
                    st.info("Not available in current dataset")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #8b949e; font-size: 0.9em;">
    <p>🧬 <strong>Saudi Plant Genome Intelligence Hub (SPGIH)</strong><br>
    Phoenix dactylifera · Salinity Genomics · Data-Driven Discovery<br>
    <em>Powered by modern bioinformatics and deep data integration</em></p>
</div>
""", unsafe_allow_html=True)

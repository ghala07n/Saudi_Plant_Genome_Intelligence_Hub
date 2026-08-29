import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Saudi Plant Genome Intelligence Hub (SPGIH)", layout="wide", initial_sidebar_state="expanded")

# --- Translations ---
TRANSLATIONS = {
    "English": {
        "app_title": "Saudi Plant Genome Intelligence Hub (SPGIH)",
        "app_subtitle": "Phoenix dactylifera — Salinity Stress Candidate Genes & Genomic Explorer",
        "nav_overview": "Home / Overview",
        "nav_genome": "Genome Overview",
        "nav_chr_explorer": "Chromosome Explorer",
        "nav_candidates": "Salinity Candidate Explorer",
        "nav_gene": "Gene Detail",
        "nav_insights": "Genomic Insights",
        "nav_salinity_research": "Salinity Research",
        "nav_methods": "Data & Methods",
        "nav_downloads": "Download Data",
        "settings": "Settings",
        "language_label": "Language / اللغة",
        "kpi_chromosomes": "Chromosomes",
        "kpi_total_genes": "Total Nuclear Genes",
        "kpi_protein_coding": "Protein-Coding Genes",
        "kpi_salinity_candidates": "Salinity Candidate Genes",
        "kpi_genome_size": "Total Assembly (Mb)",
        "search_placeholder": "Search gene ID or description...",
        "filter_category": "Filter by functional category",
        "filter_chr": "Filter by chromosome",
        "download_csv": "Download CSV",
        "no_data": "Data not available — check the data/ directory.",
        "insights_header": "Data-driven Insights",
        "insights_spearman": "Spearman rho GC vs gene density",
        "table_no_matches": "No matching records found.",
        "showing_results": "Showing",
        "results_count": "results",
        "reset_filters": "Reset filters",
    },
    "العربية": {
        "app_title": "مركز ذكاء جينوم النباتات السعودي (SPGIH)",
        "app_subtitle": "Phoenix dactylifera — الجينات المرشحة لتحمل الملوحة ومستكشف الجينوم",
        "nav_overview": "الصفحة الرئيسية / نظرة عامة",
        "nav_genome": "نظرة عامة على الجينوم",
        "nav_chr_explorer": "مستكشف الكروموسومات",
        "nav_candidates": "مستكشف المرشحين للملوحة",
        "nav_gene": "تفاصيل الجين",
        "nav_insights": "ملاحظات جينومية",
        "nav_salinity_research": "أبحاث الملوحة",
        "nav_methods": "البيانات والطريقة",
        "nav_downloads": "تحميل البيانات",
        "settings": "الإعدادات",
        "language_label": "اللغة / Language",
        "kpi_chromosomes": "الكروموسومات",
        "kpi_total_genes": "إجمالي الجينات النووية",
        "kpi_protein_coding": "الجينات المرمّزة للبروتين",
        "kpi_salinity_candidates": "جينات مرشحة للملوحة",
        "kpi_genome_size": "إجمالي التجميع (Mb)",
        "search_placeholder": "ابحث برقم الجين أو الوصف...",
        "filter_category": "التصفية بحسب التصنيف الوظيفي",
        "filter_chr": "التصفية بحسب الكروموسوم",
        "download_csv": "تحميل CSV",
        "no_data": "البيانات غير متاحة — تحقق من مجلد data/.",
        "insights_header": "ملاحظات مدفوعة بالبيانات",
        "insights_spearman": "Spearman rho محتوى GC مقابل كثافة الجينات",
        "table_no_matches": "لا توجد سجلات مطابقة.",
        "showing_results": "عرض",
        "results_count": "نتائج",
        "reset_filters": "إعادة تعيين المرشحات",
    }
}

DATA_DIR = "data"

# Fallback (validated) constants to keep the app stable when files are missing
FALLBACKS = {
    "chromosomes": 18,
    "total_genes": 23679,
    "protein_coding": 20805,
    "salinity_candidates": 1795,
    "genome_size_mb": 385.59,
}

@st.cache_data
def load_datasets(data_dir=DATA_DIR):
    """Load CSV files from the data directory. Return dict with DataFrames or None on failure.
    This function is cached to improve interactive performance.
    """
    files = {
        "candidates": "salinity_candidates_categorized.csv",
        "gene_density": "chromosome_gene_density.csv",
        "gc_density": "chromosome_gc_gene_density_clean.csv",
        "genome_summary": "genome_annotation_summary.csv",
        "chr_summary": "chromosome_annotation_summary.csv",
    }
    out = {}
    for key, fname in files.items():
        path = os.path.join(data_dir, fname)
        if os.path.exists(path):
            try:
                out[key] = pd.read_csv(path)
            except Exception:
                out[key] = None
        else:
            out[key] = None
    return out

# Load datasets (cached)
data = load_datasets()

candidates_df = data.get("candidates")
gene_density_df = data.get("gene_density")
gc_density_df = data.get("gc_density")
genome_summary_df = data.get("genome_summary")
chr_summary_df = data.get("chr_summary")

# Helper: safe dataframe check
def df_ok(df):
    return df is not None and isinstance(df, pd.DataFrame) and not df.empty

# Sidebar: language and navigation
with st.sidebar:
    # safe spacer instead of empty image
    st.markdown("<br>", unsafe_allow_html=True)
    selected_lang = st.selectbox(TRANSLATIONS["English"]["language_label"], options=["English", "العربية"], index=0)
    t = TRANSLATIONS.get(selected_lang, TRANSLATIONS["English"])
    st.markdown("---")
    nav_options = [
        t["nav_overview"],
        t["nav_genome"],
        t["nav_chr_explorer"],
        t["nav_candidates"],
        t["nav_gene"],
        t["nav_insights"],
        t["nav_salinity_research"],
        t["nav_methods"],
        t["nav_downloads"],
    ]
    nav = st.radio("", nav_options)
    st.markdown("---")
    st.caption("Saudi Plant Genome Intelligence Hub — SPGIH")

# Page header (hero) — clean, no broken HTML
st.markdown(f"### 🧬 {t['app_title']}")
st.write(t["app_subtitle"])
st.markdown("---")

# Compute KPIs from data with safe fallbacks
if df_ok(genome_summary_df):
    try:
        total_genes = int(genome_summary_df['count'].sum())
    except Exception:
        total_genes = FALLBACKS['total_genes']
else:
    total_genes = FALLBACKS['total_genes']

if df_ok(genome_summary_df):
    try:
        protein_coding = int(genome_summary_df.loc[genome_summary_df['gene_type'].str.contains('protein_coding', na=False), 'count'].sum())
        # If the filtered sum is zero, fallback
        if protein_coding == 0:
            protein_coding = FALLBACKS['protein_coding']
    except Exception:
        protein_coding = FALLBACKS['protein_coding']
else:
    protein_coding = FALLBACKS['protein_coding']

if df_ok(gene_density_df):
    try:
        # Prefer length_Mb when available, else try length_bp
        if 'length_Mb' in gene_density_df.columns:
            genome_size_mb = round(float(gene_density_df['length_Mb'].astype(float).sum()), 2)
        elif 'length_bp' in gene_density_df.columns:
            genome_size_mb = round(float(gene_density_df['length_bp'].astype(float).sum()) / 1e6, 2)
        else:
            genome_size_mb = FALLBACKS['genome_size_mb']
    except Exception:
        genome_size_mb = FALLBACKS['genome_size_mb']
else:
    genome_size_mb = FALLBACKS['genome_size_mb']

salinity_count = int(candidates_df.shape[0]) if df_ok(candidates_df) else FALLBACKS['salinity_candidates']
chromosome_count = int(gene_density_df['chromosome'].nunique()) if df_ok(gene_density_df) and 'chromosome' in gene_density_df.columns else FALLBACKS['chromosomes']

# KPI cards - equal width columns
cols = st.columns(5)
with cols[0]:
    st.metric(label=t['kpi_chromosomes'], value=f"{chromosome_count}")
with cols[1]:
    st.metric(label=t['kpi_total_genes'], value=f"{total_genes:,}")
with cols[2]:
    st.metric(label=t['kpi_protein_coding'], value=f"{protein_coding:,}")
with cols[3]:
    st.metric(label=t['kpi_salinity_candidates'], value=f"{salinity_count:,}")
with cols[4]:
    st.metric(label=t['kpi_genome_size'], value=f"{genome_size_mb} Mb")

st.markdown("---")

# Utility: common layout for Plotly figures to avoid tick overlap and keep consistent style
def finalize_figure(fig, title=None, rotate_xticks=True):
    fig.update_layout(template='plotly_white', title=title or '', margin=dict(l=40, r=40, t=60, b=90))
    if rotate_xticks:
        fig.update_layout(xaxis_tickangle=-45, xaxis_automargin=True)
    return fig

# NAVIGATION HANDLERS
if nav == t['nav_overview']:
    st.header(t['nav_overview'])
    st.write(t['app_subtitle'])

    # Chromosome lengths
    if df_ok(gene_density_df) and 'length_Mb' in gene_density_df.columns and 'chromosome' in gene_density_df.columns:
        df_plot = gene_density_df.sort_values('length_Mb', ascending=False)
        fig = px.bar(df_plot, x='chromosome', y='length_Mb', labels={'length_Mb': 'Length (Mb)', 'chromosome': 'Chromosome'}, title='Chromosome lengths')
        finalize_figure(fig, rotate_xticks=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(t['no_data'])

    # GC vs gene density scatter with trendline (calculated from available columns)
    if df_ok(gc_density_df) and {'GC_percent', 'gene_density_per_Mb', 'chromosome'}.issubset(gc_density_df.columns):
        df_gc = gc_density_df.dropna(subset=['GC_percent', 'gene_density_per_Mb'])
        fig2 = px.scatter(df_gc, x='GC_percent', y='gene_density_per_Mb', text='chromosome', labels={'GC_percent': 'GC %', 'gene_density_per_Mb': 'Gene density (genes/Mb)'}, title='GC % vs gene density per chromosome')
        # add linear trendline computed with numpy
        try:
            x = df_gc['GC_percent'].astype(float)
            y = df_gc['gene_density_per_Mb'].astype(float)
            coeffs = np.polyfit(x, y, 1)
            x_line = np.linspace(x.min(), x.max(), 100)
            y_line = coeffs[0] * x_line + coeffs[1]
            fig2.add_trace(go.Scatter(x=x_line, y=y_line, mode='lines', name='Trend', line=dict(color='firebrick')))
        except Exception:
            pass
        finalize_figure(fig2, rotate_xticks=False)
        st.plotly_chart(fig2, use_container_width=True)

elif nav == t['nav_genome']:
    st.header(t['nav_genome'])
    st.write("Interactive genome-wide charts with tooltips. Hover to inspect chromosome-level values.")
    if not df_ok(gene_density_df):
        st.info(t['no_data'])
    else:
        # Chromosome length bar
        if 'length_Mb' in gene_density_df.columns and 'chromosome' in gene_density_df.columns:
            df_len = gene_density_df.sort_values('length_Mb')
            fig_len = px.bar(df_len, x='chromosome', y='length_Mb', labels={'length_Mb': 'Length (Mb)'}, title='Chromosome lengths (Mb)', hover_data=[col for col in ['total_genes','protein_coding'] if col in gene_density_df.columns])
            finalize_figure(fig_len)
            st.plotly_chart(fig_len, use_container_width=True)

        # gene counts
        if 'total_genes' in gene_density_df.columns and 'chromosome' in gene_density_df.columns:
            df_genes = gene_density_df.sort_values('total_genes')
            fig_genes = px.bar(df_genes, x='chromosome', y='total_genes', labels={'total_genes': 'Total genes'}, title='Total genes per chromosome', hover_data=[col for col in ['length_Mb','gene_density_per_Mb'] if col in gene_density_df.columns])
            finalize_figure(fig_genes)
            st.plotly_chart(fig_genes, use_container_width=True)

        # protein-coding genes
        if 'protein_coding' in gene_density_df.columns and 'chromosome' in gene_density_df.columns:
            df_pc = gene_density_df.sort_values('protein_coding')
            fig_pc = px.bar(df_pc, x='chromosome', y='protein_coding', labels={'protein_coding': 'Protein-coding genes'}, title='Protein-coding genes per chromosome', hover_data=[col for col in ['protein_coding_density_per_Mb'] if col in gene_density_df.columns])
            finalize_figure(fig_pc)
            st.plotly_chart(fig_pc, use_container_width=True)

        # gene density
        if 'gene_density_per_Mb' in gene_density_df.columns and 'chromosome' in gene_density_df.columns:
            df_gd = gene_density_df.sort_values('gene_density_per_Mb')
            fig_gd = px.bar(df_gd, x='chromosome', y='gene_density_per_Mb', labels={'gene_density_per_Mb':'Gene density (genes/Mb)'}, title='Gene density per chromosome', hover_data=[col for col in ['protein_coding_density_per_Mb'] if col in gene_density_df.columns])
            finalize_figure(fig_gd)
            st.plotly_chart(fig_gd, use_container_width=True)

        # GC percent
        if df_ok(gc_density_df) and 'GC_percent' in gc_density_df.columns and 'chromosome' in gc_density_df.columns:
            df_gcplot = gc_density_df.sort_values('GC_percent')
            fig_gc = px.bar(df_gcplot, x='chromosome', y='GC_percent', labels={'GC_percent':'GC %'}, title='GC % per chromosome', hover_data=[col for col in ['gene_density_per_Mb'] if col in gc_density_df.columns])
            finalize_figure(fig_gc)
            st.plotly_chart(fig_gc, use_container_width=True)

elif nav == t['nav_chr_explorer']:
    st.header(t['nav_chr_explorer'])
    if not df_ok(gene_density_df):
        st.info(t['no_data'])
    else:
        chr_list = gene_density_df['chromosome'].astype(str).tolist() if 'chromosome' in gene_density_df.columns else []
        sel_chr = st.selectbox(t['filter_chr'], options=['All'] + chr_list)
        if sel_chr == 'All':
            st.dataframe(gene_density_df.set_index('chromosome') if 'chromosome' in gene_density_df.columns else gene_density_df, use_container_width=True)
        else:
            row = gene_density_df[gene_density_df['chromosome'].astype(str) == str(sel_chr)].iloc[0]
            st.markdown(f"### {sel_chr}")
            cols = st.columns(2)
            with cols[0]:
                st.write(f"Length (Mb): {row.get('length_Mb', 'N/A')}")
                st.write(f"Total genes: {row.get('total_genes', 'N/A')}")
                st.write(f"Protein-coding: {row.get('protein_coding', 'N/A')}")
            with cols[1]:
                st.write(f"Gene density (genes/Mb): {row.get('gene_density_per_Mb', 'N/A')}")
                st.write(f"Protein-coding density (genes/Mb): {row.get('protein_coding_density_per_Mb', 'N/A')}")
                # deviation from genome average
                try:
                    avg_density = float(gene_density_df['gene_density_per_Mb'].astype(float).mean()) if 'gene_density_per_Mb' in gene_density_df.columns else None
                    deviation = float(row.get('gene_density_per_Mb', 0)) - avg_density if avg_density is not None else None
                    if deviation is not None:
                        st.write(f"Deviation from genome average gene density: {deviation:.2f} genes/Mb")
                except Exception:
                    pass

        # Comparison chart
        if {'gene_density_per_Mb','protein_coding_density_per_Mb','chromosome','length_Mb'}.intersection(gene_density_df.columns):
            fig_cmp = px.scatter(gene_density_df, x='gene_density_per_Mb', y='protein_coding_density_per_Mb', color='chromosome' if 'chromosome' in gene_density_df.columns else None, hover_name='chromosome' if 'chromosome' in gene_density_df.columns else None, size='length_Mb' if 'length_Mb' in gene_density_df.columns else None, labels={'gene_density_per_Mb':'Gene density (genes/Mb)','protein_coding_density_per_Mb':'Protein-coding density (genes/Mb)'} )
            finalize_figure(fig_cmp, rotate_xticks=False)
            st.plotly_chart(fig_cmp, use_container_width=True)

elif nav == t['nav_candidates']:
    st.header(t['nav_candidates'])
    if not df_ok(candidates_df):
        st.info(t['no_data'])
    else:
        # filters
        cats = ['All'] + sorted(candidates_df['functional_category'].fillna('Unknown').unique().tolist()) if 'functional_category' in candidates_df.columns else ['All']
        selected_cat = st.selectbox(t['filter_category'], options=cats)
        chr_options = ['All'] + sorted(candidates_df['chromosome'].astype(str).unique().tolist()) if 'chromosome' in candidates_df.columns else ['All']
        selected_chr = st.selectbox(t['filter_chr'], options=chr_options)
        search = st.text_input('', placeholder=t['search_placeholder'])

        filtered = candidates_df.copy()
        if selected_cat != 'All' and 'functional_category' in filtered.columns:
            filtered = filtered[filtered['functional_category'] == selected_cat]
        if selected_chr != 'All' and 'chromosome' in filtered.columns:
            filtered = filtered[filtered['chromosome'].astype(str) == str(selected_chr)]
        if search and any(col in filtered.columns for col in ['gene_id','product_description']):
            mask = pd.Series([False] * len(filtered), index=filtered.index)
            if 'gene_id' in filtered.columns:
                mask = mask | filtered['gene_id'].astype(str).str.contains(search, case=False, na=False)
            if 'product_description' in filtered.columns:
                mask = mask | filtered['product_description'].astype(str).str.contains(search, case=False, na=False)
            filtered = filtered[mask]

        st.write(f"{t['showing_results']} **{len(filtered):,}** {t['results_count']}")
        if filtered.empty:
            st.info(t['table_no_matches'])
        else:
            st.dataframe(filtered, use_container_width=True)
            try:
                csv = filtered.to_csv(index=False).encode('utf-8')
                st.download_button(label=t['download_csv'], data=csv, file_name='filtered_salinity_candidates.csv', mime='text/csv')
            except Exception:
                st.warning("Unable to prepare CSV for download.")

elif nav == t['nav_gene']:
    st.header(t['nav_gene'])
    if not df_ok(candidates_df):
        st.info(t['no_data'])
    else:
        gene_ids = candidates_df['gene_id'].astype(str).tolist() if 'gene_id' in candidates_df.columns else []
        selected_gene = st.selectbox('Select gene', options=[''] + gene_ids)
        if selected_gene:
            gene_row = candidates_df[candidates_df['gene_id'].astype(str) == str(selected_gene)].iloc[0]
            st.subheader(f"{selected_gene}")
            cols = st.columns([2,3])
            with cols[0]:
                st.markdown(f"**Product description:** {gene_row.get('product_description', 'N/A')}")
                st.markdown(f"**Functional category:** {gene_row.get('functional_category', 'N/A')}")
                st.markdown(f"**Chromosome:** {gene_row.get('chromosome', 'N/A')}")
                st.markdown(f"**Start - End:** {gene_row.get('start', 'N/A')} - {gene_row.get('end', 'N/A')}")
                st.markdown(f"**Strand:** {gene_row.get('strand', 'N/A')}")
            with cols[1]:
                # simple chromosome position visualization
                try:
                    if df_ok(gene_density_df) and 'chromosome' in gene_density_df.columns:
                        chr_len_row = gene_density_df[gene_density_df['chromosome'].astype(str) == str(gene_row.get('chromosome'))].iloc[0]
                        if 'length_bp' in chr_len_row.index:
                            chr_len = float(chr_len_row['length_bp'])
                        elif 'length_Mb' in chr_len_row.index:
                            chr_len = float(chr_len_row['length_Mb']) * 1e6
                        else:
                            raise ValueError('Chromosome length not available')

                        start = float(gene_row.get('start', 0))
                        end = float(gene_row.get('end', 0))
                        # ensure sensible coordinates
                        start, end = max(0, min(start, end)), max(start, end)

                        fig = go.Figure()
                        fig.add_trace(go.Bar(x=[chr_len], y=[1], orientation='h', marker_color='#e6eef6', showlegend=False))
                        fig.add_trace(go.Bar(x=[end - start], y=[1], orientation='h', marker_color='#0f62fe', base=[start], name=selected_gene))
                        fig.update_layout(height=120, xaxis_title='bp', yaxis={'visible':False}, template='plotly_white', margin=dict(l=10,r=10,t=10,b=10))
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info('Position visualization not available.')
                except Exception:
                    st.info('Position visualization not available.')

elif nav == t['nav_insights']:
    st.header(t['nav_insights'])
    st.subheader(t['insights_header'])
    insights = []
    if df_ok(gene_density_df) and 'gene_density_per_Mb' in gene_density_df.columns:
        try:
            hi = gene_density_df.loc[gene_density_df['gene_density_per_Mb'].astype(float).idxmax()]
            lo = gene_density_df.loc[gene_density_df['gene_density_per_Mb'].astype(float).idxmin()]
            insights.append(f"Highest gene-density chromosome: {hi['chromosome']} ({hi['gene_density_per_Mb']} genes/Mb)")
            insights.append(f"Lowest gene-density chromosome: {lo['chromosome']} ({lo['gene_density_per_Mb']} genes/Mb)")
            most_genes = gene_density_df.loc[gene_density_df['total_genes'].astype(int).idxmax()] if 'total_genes' in gene_density_df.columns else None
            if most_genes is not None:
                insights.append(f"Chromosome with most genes: {most_genes['chromosome']} ({most_genes['total_genes']} genes)")
            most_pc = gene_density_df.loc[gene_density_df['protein_coding'].astype(int).idxmax()] if 'protein_coding' in gene_density_df.columns else None
            if most_pc is not None:
                insights.append(f"Chromosome with most protein-coding genes: {most_pc['chromosome']} ({most_pc['protein_coding']} genes)")
            pct_pc = (protein_coding / total_genes) * 100 if total_genes else None
            if pct_pc is not None:
                insights.append(f"Percentage of genes that are protein-coding: {pct_pc:.2f}%")
        except Exception:
            pass

    if df_ok(gc_density_df) and {'GC_percent','gene_density_per_Mb'}.issubset(gc_density_df.columns):
        try:
            rho = gc_density_df['GC_percent'].astype(float).corr(gc_density_df['gene_density_per_Mb'].astype(float), method='spearman')
            insights.append(f"{t['insights_spearman']}: {rho:.4f}")
        except Exception:
            insights.append(f"{t['insights_spearman']}: (calculation failed)")

    if not insights:
        st.info(t['no_data'])
    else:
        for s in insights:
            st.markdown(f"- {s}")

elif nav == t['nav_salinity_research']:
    st.header(t['nav_salinity_research'])
    st.markdown("This section explains the salinity candidate functional categories. Descriptions are concise and avoid overstating gene function. They reflect the categories present in the dataset.")
    st.markdown("- Protein Kinases: signaling enzymes that phosphorylate target proteins and are often involved in stress-response pathways.")
    st.markdown("- Ion Transporters: membrane proteins involved in ion homeostasis and transport, frequently implicated in salinity tolerance.")
    st.markdown("- Transcription Factors: DNA-binding proteins that regulate gene expression under stress.")
    st.markdown("- Stress / Osmoprotectants: genes involved in osmotic balance and protection against salt-induced dehydration.")
    st.markdown("- Other Signaling / Metabolism: assorted signaling or metabolic genes found among candidates.")

elif nav == t['nav_methods']:
    st.header(t['nav_methods'])
    st.markdown("## Data & Methods")
    st.markdown("- Genome assembly: nuclear assembly used for Phoenix dactylifera (18 chromosomes).\n- Annotation source: supplied annotation CSVs in the data/ directory.\n- Gene counting: derived from the genome_annotation_summary.csv file when available; otherwise fallbacks are used to preserve stability.")

elif nav == t['nav_downloads']:
    st.header(t['nav_downloads'])
    st.write("Download published datasets included with this project. These are the source CSVs used to generate the dashboard.")
    files_to_offer = [
        ("salinity_candidates_categorized.csv", os.path.join(DATA_DIR, "salinity_candidates_categorized.csv")),
        ("chromosome_gene_density.csv", os.path.join(DATA_DIR, "chromosome_gene_density.csv")),
        ("chromosome_gc_gene_density_clean.csv", os.path.join(DATA_DIR, "chromosome_gc_gene_density_clean.csv")),
        ("genome_annotation_summary.csv", os.path.join(DATA_DIR, "genome_annotation_summary.csv")),
        ("chromosome_annotation_summary.csv", os.path.join(DATA_DIR, "chromosome_annotation_summary.csv")),
    ]
    for label, path in files_to_offer:
        if os.path.exists(path):
            try:
                with open(path, 'rb') as f:
                    st.download_button(label=f"Download {label}", data=f, file_name=label, mime='text/csv')
            except Exception:
                st.write(f"{label}: unable to prepare download")
        else:
            st.write(f"{label}: not found")

# Footer: credits
st.markdown("---")
st.caption("SPGIH — Date Palm Genomics · Salinity Stress Research · Data-driven insights. English default; use the sidebar to switch to Arabic.")

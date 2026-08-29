import streamlit as st
import pandas as pd
import numpy as np
import os
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Saudi Plant Genome Intelligence Hub",
                   layout="wide",
                   initial_sidebar_state="expanded")

# --- Translations ---
TRANSLATIONS = {
    "English": {
        "app_title": "Saudi Plant Genome Intelligence Hub",
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
        "app_title": "مركز ذكاء جينوم النباتات السعودي",
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

@st.cache_data
def load_datasets(data_dir=DATA_DIR):
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
            except Exception as e:
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

# Sidebar: language and navigation
with st.sidebar:
    st.image("", width=1)  # spacing
    selected_lang = st.selectbox(TRANSLATIONS["English"]["language_label"], options=["English", "العربية"], index=0)
    t = TRANSLATIONS[selected_lang]
    st.markdown("---")
    nav = st.radio("", (t["nav_overview"], t["nav_genome"], t["nav_chr_explorer"], t["nav_candidates"], t["nav_gene"], t["nav_insights"], t["nav_salinity_research"], t["nav_methods"], t["nav_downloads"]))
    st.markdown("---")
    st.caption("Saudi Plant Genome Intelligence Hub — SPGIH")

# Page header (hero)
st.markdown(
    f"<div style='display:flex;align-items:center;gap:16px'>"
    f"<div style='flex:1'>"
    f"<h1 style='margin:0'>{t['app_title']}</h1>"
    f"<p style='margin:0;color:#666'>{t['app_subtitle']}</p>"
    f"</div>"
    f"<div style='width:220px;text-align:right'>"
    f"<img src='data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'200\' height=\'80\' viewBox=\'0 0 200 80\'><rect rx=\'8\' width=\'200\' height=\'80\' fill=\'%230f1724\'/><text x=\'10\' y=\'52\' fill=\'%23a7f3d0\' font-size=\'12\' font-family=\'Arial\'>SPGIH</text></svg>' alt='logo' style='max-width:220px'/>"
    f"</div>"
    f"</div>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Helper: safe dataframe check
def df_ok(df):
    return df is not None and not df.empty

# Compute KPIs from data (do not hard-code)
if df_ok(genome_summary_df):
    total_genes = int(genome_summary_df['count'].sum())
else:
    # fallback to known validated number
    total_genes = 23679

if df_ok(genome_summary_df):
    protein_coding = int(genome_summary_df.loc[genome_summary_df['gene_type'] == 'protein_coding', 'count'].values[0])
else:
    protein_coding = 20805

if df_ok(gene_density_df):
    genome_size_mb = round(float(gene_density_df['length_Mb'].sum()), 2)
else:
    genome_size_mb = 385.59

salinity_count = len(candidates_df) if df_ok(candidates_df) else 1795
chromosome_count = len(gene_density_df) if df_ok(gene_density_df) else 18

# KPI cards
k1, k2, k3, k4, k5 = st.columns([1.2,1.2,1.2,1.2,1.2])
with k1:
    st.metric(label=t['kpi_chromosomes'], value=f"{chromosome_count}")
with k2:
    st.metric(label=t['kpi_total_genes'], value=f"{total_genes:,}")
with k3:
    st.metric(label=t['kpi_protein_coding'], value=f"{protein_coding:,}")
with k4:
    st.metric(label=t['kpi_salinity_candidates'], value=f"{salinity_count:,}")
with k5:
    st.metric(label=t['kpi_genome_size'], value=f"{genome_size_mb} Mb")

st.markdown("---")

# NAVIGATION HANDLERS
if nav == t['nav_overview']:
    st.header(t['nav_overview'])
    st.write("A bilingual Streamlit platform for exploration of the date palm nuclear genome and salinity stress candidate genes. Use the left navigation to explore genome-wide summaries, chromosome-level detail, and candidate gene annotations.")
    # Small summary cards and plots
    if df_ok(gene_density_df):
        fig = px.bar(gene_density_df.sort_values('length_Mb', ascending=False), x='chromosome', y='length_Mb',
                     labels={'length_Mb':'Length (Mb)','chromosome':'Chromosome'},
                     title='Chromosome lengths')
        fig.update_layout(margin=dict(l=10,r=10,t=40,b=10), template='plotly_white')
        st.plotly_chart(fig, use_container_width=True)

    if df_ok(gc_density_df):
        fig2 = px.scatter(gc_density_df, x='GC_percent', y='gene_density_per_Mb', text='chromosome',
                          labels={'GC_percent':'GC %','gene_density_per_Mb':'Gene density (genes/Mb)'},
                          title='GC % vs gene density per chromosome')
        # add trendline using numpy polyfit on ranks (Spearman-like)
        coeffs = np.polyfit(gc_density_df['GC_percent'], gc_density_df['gene_density_per_Mb'], 1)
        x_line = np.linspace(gc_density_df['GC_percent'].min(), gc_density_df['GC_percent'].max(), 100)
        y_line = coeffs[0] * x_line + coeffs[1]
        fig2.add_traces(go.Line(x=x_line, y=y_line, name='Trend'))
        fig2.update_traces(marker=dict(size=10), selector=dict(mode='markers'))
        fig2.update_layout(margin=dict(l=10,r=10,t=40,b=10), template='plotly_white')
        st.plotly_chart(fig2, use_container_width=True)

elif nav == t['nav_genome']:
    st.header(t['nav_genome'])
    st.write("Interactive genome-wide charts with tooltips. Hover to inspect chromosome-level values.")
    if not df_ok(gene_density_df):
        st.info(t['no_data'])
    else:
        # Chromosome length bar
        fig_len = px.bar(gene_density_df.sort_values('length_Mb'), x='chromosome', y='length_Mb',
                         labels={'length_Mb':'Length (Mb)'}, title='Chromosome lengths (Mb)',
                         hover_data=['total_genes','protein_coding'])
        fig_len.update_layout(template='plotly_white')
        st.plotly_chart(fig_len, use_container_width=True)

        # gene counts
        fig_genes = px.bar(gene_density_df.sort_values('total_genes'), x='chromosome', y='total_genes',
                          labels={'total_genes':'Total genes'}, title='Total genes per chromosome',
                          hover_data=['length_Mb','gene_density_per_Mb'])
        fig_genes.update_layout(template='plotly_white')
        st.plotly_chart(fig_genes, use_container_width=True)

        # protein-coding genes
        fig_pc = px.bar(gene_density_df.sort_values('protein_coding'), x='chromosome', y='protein_coding',
                       labels={'protein_coding':'Protein-coding genes'}, title='Protein-coding genes per chromosome',
                       hover_data=['protein_coding_density_per_Mb'])
        fig_pc.update_layout(template='plotly_white')
        st.plotly_chart(fig_pc, use_container_width=True)

        # gene density
        fig_gd = px.bar(gene_density_df.sort_values('gene_density_per_Mb'), x='chromosome', y='gene_density_per_Mb',
                        labels={'gene_density_per_Mb':'Gene density (genes/Mb)'}, title='Gene density per chromosome',
                        hover_data=['protein_coding_density_per_Mb'])
        fig_gd.update_layout(template='plotly_white')
        st.plotly_chart(fig_gd, use_container_width=True)

        # GC percent
        if df_ok(gc_density_df):
            fig_gc = px.bar(gc_density_df.sort_values('GC_percent'), x='chromosome', y='GC_percent',
                            labels={'GC_percent':'GC %'}, title='GC % per chromosome', hover_data=['gene_density_per_Mb'])
            fig_gc.update_layout(template='plotly_white')
            st.plotly_chart(fig_gc, use_container_width=True)

elif nav == t['nav_chr_explorer']:
    st.header(t['nav_chr_explorer'])
    if not df_ok(gene_density_df):
        st.info(t['no_data'])
    else:
        chr_list = gene_density_df['chromosome'].tolist()
        sel_chr = st.selectbox(t['filter_chr'], options=['All'] + chr_list)
        if sel_chr == 'All':
            st.dataframe(gene_density_df.set_index('chromosome'), use_container_width=True)
        else:
            row = gene_density_df[gene_density_df['chromosome'] == sel_chr].iloc[0]
            st.markdown(f"### {sel_chr}")
            cols = st.columns(2)
            with cols[0]:
                st.write(f"Length (Mb): {row['length_Mb']}")
                st.write(f"Total genes: {row['total_genes']}")
                st.write(f"Protein-coding: {row['protein_coding']}")
            with cols[1]:
                st.write(f"Gene density (genes/Mb): {row['gene_density_per_Mb']}")
                st.write(f"Protein-coding density (genes/Mb): {row['protein_coding_density_per_Mb']}")
                # deviation from genome average
                avg_density = gene_density_df['gene_density_per_Mb'].mean()
                deviation = float(row['gene_density_per_Mb']) - float(avg_density)
                st.write(f"Deviation from genome average gene density: {deviation:.2f} genes/Mb")

        # Comparison chart
        st.markdown("#### Chromosome comparison: gene density vs protein-coding density")
        fig_cmp = px.scatter(gene_density_df, x='gene_density_per_Mb', y='protein_coding_density_per_Mb', color='chromosome',
                             hover_name='chromosome', size='length_Mb',
                             labels={'gene_density_per_Mb':'Gene density (genes/Mb)','protein_coding_density_per_Mb':'Protein-coding density (genes/Mb)'} )
        fig_cmp.update_layout(template='plotly_white')
        st.plotly_chart(fig_cmp, use_container_width=True)

elif nav == t['nav_candidates']:
    st.header(t['nav_candidates'])
    if not df_ok(candidates_df):
        st.info(t['no_data'])
    else:
        # filters
        cats = ['All'] + sorted(candidates_df['functional_category'].fillna('Unknown').unique().tolist())
        selected_cat = st.selectbox(t['filter_category'], options=cats)
        chr_options = ['All'] + sorted(candidates_df['chromosome'].unique().tolist())
        selected_chr = st.selectbox(t['filter_chr'], options=chr_options)
        search = st.text_input('', placeholder=t['search_placeholder'])

        filtered = candidates_df.copy()
        if selected_cat != 'All':
            filtered = filtered[filtered['functional_category'] == selected_cat]
        if selected_chr != 'All':
            filtered = filtered[filtered['chromosome'] == selected_chr]
        if search:
            mask = (filtered['gene_id'].str.contains(search, case=False, na=False)) | (filtered['product_description'].str.contains(search, case=False, na=False))
            filtered = filtered[mask]

        st.write(f"{t['showing_results']} **{len(filtered):,}** {t['results_count']}")
        if filtered.empty:
            st.info(t['table_no_matches'])
        else:
            st.dataframe(filtered, use_container_width=True)
            csv = filtered.to_csv(index=False).encode('utf-8')
            st.download_button(label=t['download_csv'], data=csv, file_name='filtered_salinity_candidates.csv', mime='text/csv')

elif nav == t['nav_gene']:
    st.header(t['nav_gene'])
    if not df_ok(candidates_df):
        st.info(t['no_data'])
    else:
        gene_ids = candidates_df['gene_id'].tolist()
        selected_gene = st.selectbox('Select gene', options=[''] + gene_ids)
        if selected_gene:
            gene_row = candidates_df[candidates_df['gene_id'] == selected_gene].iloc[0]
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
                    chr_len_row = gene_density_df[gene_density_df['chromosome'] == gene_row['chromosome']].iloc[0]
                    chr_len = float(chr_len_row['length_bp']) if 'length_bp' in chr_len_row.index else float(chr_len_row['length_Mb'] * 1e6)
                    start = float(gene_row.get('start', 0))
                    end = float(gene_row.get('end', 0))
                    center = (start + end) / 2
                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=[chr_len], y=[1], orientation='h', marker_color='#e6eef6', showlegend=False))
                    fig.add_trace(go.Bar(x=[end - start], y=[1], orientation='h', marker_color='#0f62fe', base=[start], name=selected_gene))
                    fig.update_layout(height=120, xaxis_title='bp', yaxis={'visible':False}, template='plotly_white', margin=dict(l=10,r=10,t=10,b=10))
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    st.info('Position visualization not available.')

elif nav == t['nav_insights']:
    st.header(t['nav_insights'])
    st.subheader(t['insights_header'])
    insights = []
    if df_ok(gene_density_df):
        # highest/lowest gene-density
        hi = gene_density_df.loc[gene_density_df['gene_density_per_Mb'].idxmax()]
        lo = gene_density_df.loc[gene_density_df['gene_density_per_Mb'].idxmin()]
        insights.append(f"Highest gene-density chromosome: {hi['chromosome']} ({hi['gene_density_per_Mb']} genes/Mb)")
        insights.append(f"Lowest gene-density chromosome: {lo['chromosome']} ({lo['gene_density_per_Mb']} genes/Mb)")
        most_genes = gene_density_df.loc[gene_density_df['total_genes'].idxmax()]
        insights.append(f"Chromosome with most genes: {most_genes['chromosome']} ({most_genes['total_genes']} genes)")
        most_pc = gene_density_df.loc[gene_density_df['protein_coding'].idxmax()]
        insights.append(f"Chromosome with most protein-coding genes: {most_pc['chromosome']} ({most_pc['protein_coding']} genes)")
        pct_pc = (protein_coding / total_genes) * 100 if total_genes else None
        if pct_pc is not None:
            insights.append(f"Percentage of genes that are protein-coding: {pct_pc:.2f}%")
    if df_ok(gc_density_df):
        # compute spearman correlation data-driven
        try:
            rho = gc_density_df['GC_percent'].corr(gc_density_df['gene_density_per_Mb'], method='spearman')
            insights.append(f"{t['insights_spearman']}: {rho:.4f}")
        except Exception:
            insights.append(f"{t['insights_spearman']}: (calculation failed)")
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
    st.markdown("- Genome assembly: nuclear assembly used for Phoenix dactylifera (18 chromosomes).\n- Annotation source: supplied annotation CSVs in the data/ directory.\n- Gene counting: derived from the genome_annotation_summary.csv and chromosome_annotation_summary.csv files.\n- Protein-coding classification: based on gene_type == 'protein_coding' in genome_annotation_summary.csv.\n- Chromosome lengths: taken from chromosome_gene_density.csv length_bp / length_Mb columns.\n- GC calculation: per-chromosome GC % provided in chromosome_gc_gene_density_clean.csv.\n- Gene density: genes per Mb calculated as total_genes / length_Mb and provided in chromosome_gene_density.csv.\n- Salinity candidate identification: provided in salinity_candidates_categorized.csv with functional_category assignments.\n")

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
            with open(path, 'rb') as f:
                st.download_button(label=f"Download {label}", data=f, file_name=label, mime='text/csv')
        else:
            st.write(f"{label}: not found")

# Footer: credits
st.markdown("---")
st.caption("SPGIH — Date Palm Genomics · Salinity Stress Research · Data-driven insights. English default; use the sidebar to switch to Arabic.")

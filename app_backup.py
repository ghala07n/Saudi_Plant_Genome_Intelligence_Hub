import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Saudi Plant Genome Intelligence Hub",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم والواجهة (Custom CSS)
st.markdown("""
    <style>
        /* خلفية عامة والخطوط */
        .main {
            background-color: #0e1117;
            color: #fafafa;
        }
        /* تصميم البطاقات الإحصائية */
        .metric-card {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            padding: 20px;
            border-radius: 12px;
            border: 1px solid #374151;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            text-align: center;
        }
        /* تخصيص العناوين */
        h1, h2, h3 {
            color: #10b981 !important;
            font-weight: 700;
        }
        /* تنسيق الجداول */
        dataframe {
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# قاموس الترجمة (عربي / إنجليزي)
TRANSLATIONS = {
    "English": {
        "title": "🌱 Saudi Plant Genome Intelligence Hub",
        "subtitle": "Date Palm (Phoenix dactylifera) — Salinity Stress Candidate Genes & Genomic Explorer",
        "total_genes": "Total Genes",
        "protein_coding": "Protein-Coding",
        "salinity_candidates": "Salinity Candidates",
        "chromosomes": "Chromosomes",
        "overview": "📊 Genomic Overview & Functional Distribution",
        "chr_explorer": "🧬 Chromosome Explorer",
        "select_chr": "Select Chromosome",
        "chr_stats": "Chromosome Detailed Statistics",
        "gene_details_title": "🔬 Individual Gene Deep-Dive & Details",
        "select_gene": "Select or Search Gene ID",
        "gene_card_header": "Detailed Gene Card",
        "tab1": "Functional Categories",
        "tab2": "Chromosome Gene Density",
        "tab3": "GC vs Gene Density",
        "tab4": "Genome Annotation Summary",
        "tab5": "Protein-Coding Stats",
        "explorer": "🔍 Salinity Candidate Explorer",
        "filter_header": "Filter Options",
        "select_cat": "Select Functional Category",
        "search_label": "Search Gene ID or Description",
        "download_btn": "📥 Download Filtered Data as CSV",
        "all": "All",
        "showing": "Showing",
        "matching": "matching genes out of",
        "total_cand": "total candidates."
    },
    "العربية": {
        "title": "🌱 مركز ذكاء جينوم النباتات السعودي",
        "subtitle": "نخيل التمر (Phoenix dactylifera) — مستكشف الجينات المرشحة لتحمل الملوحة والبيانات الجينومية",
        "total_genes": "إجمالي الجينات",
        "protein_coding": "المرمز للبروتين",
        "salinity_candidates": "مرشحو الملوحة",
        "chromosomes": "الكروموسومات",
        "overview": "📊 نظرة عامة والتوزيع الوظيفي للجينوم",
        "chr_explorer": "🧬 مستكشف الكروموسومات",
        "select_chr": "اختر الكروموسوم",
        "chr_stats": "إحصائيات الكروموسوم التفصيلية",
        "gene_details_title": "🔬 استعراض وتفاصيل الجين الفردي",
        "select_gene": "اختر أو ابحث برقم الجين",
        "gene_card_header": "بطاقة الجين التفصيلية",
        "tab1": "التصنيفات الوظيفية",
        "tab2": "كثافة الجينات حسب الكروموسوم",
        "tab3": "العلاقة بين محتوى GC وكثافة الجينات",
        "tab4": "ملخص تعليقات الجينوم",
        "tab5": "إحصائيات التشفير البروتيني",
        "explorer": "🔍 مستكشف جينات الملوحة",
        "filter_header": "خيارات التصفية",
        "select_cat": "اختر التصنيف الوظيفي",
        "search_label": "بحث برقم الجين أو الوصف",
        "download_btn": "📥 تحميل البيانات المفلترة كملف CSV",
        "all": "الكل",
        "showing": "عرض",
        "matching": "جين مطابق من أصل",
        "total_cand": "مرشح إجمالي."
    }
}

DATA_DIR = "data"

@st.cache_data
def load_data():
    try:
        candidates_df = pd.read_csv(os.path.join(DATA_DIR, "salinity_candidates_categorized.csv"))
        gene_density_df = pd.read_csv(os.path.join(DATA_DIR, "chromosome_gene_density.csv"))
        gc_density_df = pd.read_csv(os.path.join(DATA_DIR, "chromosome_gc_gene_density_clean.csv"))
        genome_summary_df = pd.read_csv(os.path.join(DATA_DIR, "genome_annotation_summary.csv"))
        chr_summary_df = pd.read_csv(os.path.join(DATA_DIR, "chromosome_annotation_summary.csv"))
        protein_coding_df = pd.read_csv(os.path.join(DATA_DIR, "chromosome_protein_coding_stats.csv"))
        return candidates_df, gene_density_df, gc_density_df, genome_summary_df, chr_summary_df, protein_coding_df
    except Exception as e:
        return None, None, None, None, None, None

candidates_df, gene_density_df, gc_density_df, genome_summary_df, chr_summary_df, protein_coding_df = load_data()

# اختيار اللغة من الشريط الجانبي
st.sidebar.markdown("### 🌐 Language / اللغة")
selected_lang = st.sidebar.selectbox("Choose Language", ["English", "العربية"])
t = TRANSLATIONS[selected_lang]

# العناوين الرئيسية
st.title(t["title"])
st.subheader(t["subtitle"])
st.markdown("---")

if candidates_df is not None:
    # البطاقات الإحصائية بتصميم مميز
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(t["total_genes"], "23,679", "100% Genome" if selected_lang=="English" else "100% الجينوم")
    col2.metric(t["protein_coding"], "20,805", "87.86%")
    col3.metric(t["salinity_candidates"], f"{len(candidates_df):,}", "Target Traits" if selected_lang=="English" else "السمات المستهدفة")
    col4.metric(t["chromosomes"], "18", "Complete Assembly" if selected_lang=="English" else "الجمع التام")

    st.markdown("---")

    # 1. مستكشف الكروموسومات
    st.markdown(f"### {t['chr_explorer']}")
    if gene_density_df is not None and not gene_density_df.empty:
        chr_col = [c for c in gene_density_df.columns if 'chr' in c.lower()][0]
        selected_chr = st.selectbox(t["select_chr"], gene_density_df[chr_col].unique())
        
        chr_data = gene_density_df[gene_density_df[chr_col] == selected_chr]
        st.markdown(f"#### {t['chr_stats']} ({selected_chr})")
        st.dataframe(chr_data, use_container_width=True)
        
        if chr_summary_df is not None and not chr_summary_df.empty:
            chr_sum_col = [c for c in chr_summary_df.columns if 'chr' in c.lower()][0]
            if selected_chr in chr_summary_df[chr_sum_col].values:
                st.dataframe(chr_summary_df[chr_summary_df[chr_sum_col] == selected_chr], use_container_width=True)
    else:
        st.info("Chromosome data not available.")

    st.markdown("---")

    # 2. تفاصيل الجين الفردي
    st.markdown(f"### {t['gene_details_title']}")
    if "gene_id" in candidates_df.columns:
        gene_list = candidates_df["gene_id"].tolist()
        selected_gene = st.selectbox(t["select_gene"], gene_list)
        
        gene_row = candidates_df[candidates_df["gene_id"] == selected_gene].iloc[0]
        
        st.markdown(f"#### {t['gene_card_header']}: `{selected_gene}`")
        gcol1, gcol2 = st.columns(2)
        
        with gcol1:
            st.info(f"**Functional Category / التصنيف الوظيفي:** {gene_row.get('functional_category', 'N/A')}")
            st.write(f"**Chromosome / الكروموسوم:** {gene_row.get('chromosome', gene_row.get('chrom', 'N/A'))}")
            st.write(f"**Start / البداية:** {gene_row.get('start', 'N/A')}")
            st.write(f"**End / النهاية:** {gene_row.get('end', 'N/A')}")
            
        with gcol2:
            st.write(f"**Strand / الاتجاه:** {gene_row.get('strand', 'N/A')}")
            st.success(f"**Product Description / وصف المنتج:** {gene_row.get('product_description', gene_row.get('description', 'N/A'))}")
    else:
        st.warning("Gene ID column not found.")

    st.markdown("---")

    # 3. الرسوم البيانية الإحصائية الشاملة
    st.markdown(f"### {t['overview']}")
    tab1, tab2, tab3, tab4, tab5 = st.tabs([t["tab1"], t["tab2"], t["tab3"], t["tab4"], t["tab5"]])
    
    with tab1:
        st.markdown(f"#### {t['tab1']}")
        cat_counts = candidates_df["functional_category"].value_counts()
        st.bar_chart(cat_counts)
        
    with tab2:
        st.markdown(f"#### {t['tab2']}")
        if gene_density_df is not None and not gene_density_df.empty:
            col_candidates = [c for c in gene_density_df.columns if 'dens' in c.lower() or 'count' in c.lower() or 'gene' in c.lower()]
            target_col = col_candidates[1] if len(col_candidates) > 1 else (col_candidates[0] if col_candidates else gene_density_df.columns[1])
            st.bar_chart(gene_density_df.set_index(chr_col)[target_col])
        else:
            st.info("Data not available.")
            
    with tab3:
        st.markdown(f"#### {t['tab3']}")
        if gc_density_df is not None and not gc_density_df.empty:
            cols = gc_density_df.columns
            st.scatter_chart(gc_density_df, x=cols[1], y=cols[2] if len(cols) > 2 else cols[1])
        else:
            st.info("Data not available.")

    with tab4:
        st.markdown(f"#### {t['tab4']}")
        if genome_summary_df is not None and not genome_summary_df.empty:
            st.dataframe(genome_summary_df, use_container_width=True)
        else:
            st.info("Genome summary data not available.")

    with tab5:
        st.markdown(f"#### {t['tab5']}")
        if protein_coding_df is not None and not protein_coding_df.empty:
            st.dataframe(protein_coding_df, use_container_width=True)
        else:
            st.info("Protein coding statistics data not available.")

    st.markdown("---")

    # مستكشف جينات الملوحة
    st.markdown(f"### {t['explorer']}")
    
    st.sidebar.markdown("---")
    st.sidebar.header(t["filter_header"])
    
    cat_options = [t["all"]] + list(candidates_df["functional_category"].unique())
    selected_cat = st.sidebar.selectbox(t["select_cat"], cat_options)
    search_query = st.sidebar.text_input(t["search_label"], "")

    filtered_df = candidates_df.copy()
    if selected_cat != t["all"]:
        filtered_df = filtered_df[filtered_df["functional_category"] == selected_cat]
    if search_query:
        filtered_df = filtered_df[
            filtered_df["gene_id"].str.contains(search_query, case=False, na=False) |
            filtered_df["product_description"].str.contains(search_query, case=False, na=False)
        ]

    st.write(f"{t['showing']} **{len(filtered_df):,}** {t['matching']} **{len(candidates_df):,}** {t['total_cand']}")
    st.dataframe(filtered_df, use_container_width=True)

    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=t["download_btn"],
        data=csv_data,
        file_name="filtered_salinity_candidates.csv",
        mime="text/csv",
    )
else:
    st.error("⚠️ Dataset files not found in `data/` directory.")

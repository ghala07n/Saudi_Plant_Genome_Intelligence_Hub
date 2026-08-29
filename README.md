
[![GitHub stars](https://img.shields.io/github/stars/ghala07n/Saudi_Plant_Genome_Intelligence_Hub?style=social)](https://github.com/ghala07n/Saudi_Plant_Genome_Intelligence_Hub/stargazers)
[![Platform](https://img.shields.io/badge/BioSense-Platform-2ea043.svg)](https://github.com/ghala07n/Saudi_Plant_Genome_Intelligence_Hub)

A professional, bilingual (English/Arabic) bioinformatics web application built with Streamlit to explore, analyze, and visualize the nuclear genome assembly and salinity stress candidate genes of the Saudi Date Palm (*Phoenix dactylifera*).

---

## 📖 نظرة عامة على المشروع (Project Overview)

يهدف هذا المشروع إلى توثيق واستعراض منصة **BioSense** الذكية التي تربط بين علم الجينوم المتقدم والزراعة الدقيقة لتحسين استدامة النخيل في المملكة العربية السعودية.

| المرحلة | الوصف | الصورة التوضيحية |
| :--- | :--- | :--- |
| **1. الحقل الذكي** | جمع البيانات الجينومية والظاهرية من مزارع النخيل السعودية. | ![مزرعة النخيل الذكية](https://replicate.delivery/xpbkg/Wf04f5r8z9YpYt8v4j7k1u3l7o0t4c0t3e6u2v9h4b0i5s8A/out-0.png) |
| **2. التحليل الحيوي** | تحليل بيانات الجينوم (23,679 جيناً) باستخدام بايثون. | ![مركز التحليل الجينومي](https://replicate.delivery/xpbkg/f5O6O6E7a7c4W2V8k0v1c1Y8n2q9u5a4d8e3w1q7n8l6A/out-0.png) |
| **3. منصة BioSense** | تطبيق ويب تفاعلي لاستكشاف الجينات وتصنيف المرشحين. | ![لوحة تحكم BioSense التفاعلية](https://replicate.delivery/xpbkg/K8c7i8y7e8c7i8v4h0v1c1Y8n2q9u5a4d8e3w1q7n8l6A/out-0.png) |
| **4. التطبيق الحقلي** | دعم اتخاذ القرار في الزراعة الدقيقة وتحسين إدارة النخيل. | ![تطبيق المنصة في الحقل الذكي](https://replicate.delivery/xpbkg/T6b9x9c9w6g7e7j1e0v1c1Y8n2q9u5a4d8e3w1q7n8l6A/out-0.png) |

---

## 📊 Core Genomic Statistics
* **Nuclear Chromosomes:** 18 complete assemblies
* **Total Nuclear Genes:** 23,679
* **Protein-Coding Genes:** 20,805 (87.86%)
* **Salinity Stress Candidates:** 1,795 genes
* **Total Assembly Length:** 385.59 Mb
* **Mean Gene Density:** 61.41 genes/Mb

---

## 🔍 Functional Categorization of Salinity Candidates
* **Protein Kinases:** 1,607
* **Stress Osmoprotectants:** 80
* **Ion Transporters:** 61
* **Transcription Factors:** 27
* **Other Signaling/Metabolism:** 20

---

## 🚀 Key Platform Features
1. **Bilingual User Interface:** Instant toggle between English and Arabic.
2. **Genomic Overview & Interactive Charts:** Visualizing gene density, functional distributions, and GC content vs. gene density relationships (Spearman correlation: $-0.49$).
3. **Chromosome Explorer:** Deep-dive statistics for each of the 18 chromosomes.
4. **Individual Gene Deep-Dive:** Dedicated gene cards displaying precise coordinates, strand orientation, and functional descriptions.
5. **Salinity Candidate Explorer:** Advanced filtering, keyword search, and CSV data export.

---

## ⚙️ Installation & Usage

1. **Activate the Conda Environment:**
   ```bash
   conda activate datepalm

# Índice de Referências — docs/refs/

Leia o arquivo específico antes de escrever células markdown que citem o paper. Cada seção analítica deve incluir ao menos uma citação no formato `(Autor, Ano)`.

## Papers de Alta Prioridade (usar em todos os notebooks de modelagem)

| Arquivo | cite_as | Fato principal |
|---------|---------|----------------|
| [shi2022_code_dkt.md](shi2022_code_dkt.md) | Shi et al. (2022) | Code-DKT: AUC ~74.3% em A1 no CSEDM Release/Test; KC=ProblemID (footnote 1 do paper); sequências truncadas em 50 |
| [pankiewicz2025_srcml_dkt.md](pankiewicz2025_srcml_dkt.md) | Pankiewicz, Shi & Baker (2025) | srcML-DKT: extensão do Code-DKT com srcML; inclui Compile.Error como correct=0; dataset RunCode (≠CSEDM) |
| [progsnap2.md](progsnap2.md) | Price et al. (2020) | Especificação ProgSnap2 v6: formato do CSEDM; Run.Program com Score; sem EventType=Submit |

## Papers de Prioridade Média (usar em seções de background/metodologia)

| Arquivo | cite_as | Fato principal |
|---------|---------|----------------|
| [kt_survey.md](kt_survey.md) | Abdelrahman et al. (2022) | Survey KT: BKT (4 parâmetros) → DKT (LSTM) → Attention (SAKT, AKT); métrica padrão = AUC |
| [kalita2025_edm_review.md](kalita2025_edm_review.md) | Kalita et al. (2025) | Revisão EDM 2013–2023 PRISMA; 4 fases EDM: Problem Definition → Data Prep → Modelling → Deployment |
| [lin2024_dl_edm_survey.md](lin2024_dl_edm_survey.md) | Lin et al. (2024) | Survey DL em EDM; KT, behavior detection, performance prediction, recomendação; DL supera baselines em 67% |

## Papers de Baixa Prioridade (background geral / trabalhos futuros)

| Arquivo | cite_as | Fato principal |
|---------|---------|----------------|
| [duan2025_automatedkc.md](duan2025_automatedkc.md) | Duan et al. (2025) | KCGen-KT: geração automática de KCs por LLM (GPT-4o) para programação; supera KCs humanos |
| [pan2026_edm_ars.md](pan2026_edm_ars.md) | Pan et al. (2026) | EDM-ARS: sistema multi-agente para pesquisa EDM automatizada — referência arquitetural para harness |
| [yagci2022_edm_prediction.md](yagci2022_edm_prediction.md) | Yağcı (2022) | Performance prediction (≠KT): RF/LR com 70–75% acurácia em notas finais universitárias |
| [lopezmeneses2025_ai_edm.md](lopezmeneses2025_ai_edm.md) | López-Meneses et al. (2025) | Revisão AI+EDM+HITL-ML; 370 artigos 2006–2024; ética e equidade em algoritmos educacionais |
| [busropan2024_thesis.md](busropan2024_thesis.md) | Busropan (2024) | Tese TU Delft: LLMs para learning analytics e intervenções em programação — relevante para TCC 2 |

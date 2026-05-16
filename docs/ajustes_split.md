# Migração Release/ → Spring 2019 Full (Shi et al. protocol)

Atualizado em 2026-05-15 após migração do pipeline de `Release/` para `data/CSEDM/MainTable.csv`.

---

## O que mudou

O pipeline foi construído originalmente sobre `data/CSEDM/Release/` (CSEDM Data Challenge 2021,
329 alunos, split 75/25, apenas A1–A3 no Release/Test por design da competição). Com a migração,
o pipeline agora usa `data/CSEDM/MainTable.csv`, que é exatamente o dataset usado por Shi et al. (2022).

---

## Dataset primário: `data/CSEDM/MainTable.csv`

O arquivo `data/CSEDM/MainTable.csv` contém o **Spring 2019 completo** — os mesmos dados que
Shi et al. (2022) descrevem como fonte. Propriedades confirmadas:

- **413 alunos brutos** → filtro `min_attempts >= 3` (Run.Program globais) → **410 alunos elegíveis**
- **23.68% de corretos** no split de treino — match exato com o paper (tolerância ±0.5pp)
- **Split:** `train_test_split(students, test_size=0.2, random_state=1)` → **328 treino + 82 teste**
- **Todos os 5 assignments** disponíveis em ambos os splits (A439, A487, A492, A494, A502)
- **CodeStates:** `data/CSEDM/CodeStates/CodeStates.csv` (69.627 registros — superset do Release/)

A comparação direta com Table 1 e Table 2 de Shi et al. (2022) **agora é válida**.

---

## O que era o Release/ (removido)

O `Release/` era o dataset do **2º CSEDM Data Challenge** (2021), com design diferente:

| Aspecto | Release/ (removido) | MainTable.csv (atual) |
|---|---|---|
| Propósito | Competição de early prediction | Dataset bruto Spring 2019 |
| Alunos | 329 (critério "completed course") | 410 (min_attempts≥3) |
| Split | 75/25 oficial do challenge | 80/20 random_state=1 |
| A4–A5 no test | **Ausentes** (design do challenge) | **Presentes** (todos os 5 assignments) |
| Comparação com Shi et al. | Impossível diretamente | Direta (mesmo dataset) |

A ausência de A494/A502 no Release/Test **não era um bug nem limitação de disponibilidade**:
era design intencional da competição, que usava A4–A5 como targets de predição da Track 1.

---

## Consequências para o TCC

- **Avaliação KT:** todos os 5 assignments — Tabela 1 e Tabela 2 do paper são reproduzíveis
- **Comparação numérica direta com paper:** agora possível (mesmo protocolo)
- **AUC de referência (BKT, A439):** all-AUC 63.78%, first-AUC 50.22% (Shi et al., Table 2)
- **Artefatos stale:** `sequences_bkt_dkt.pkl`, `sequences_code_dkt.pkl`, `bkt_results.pkl`
  foram deletados — re-gerar executando 02_preprocessing e 04_bkt

---

## Funções de carregamento

- `load_spring2019_split(data_dir, test_size=0.2, random_state=1, min_attempts=3)` em `src/data_loader.py`
  — retorna `(train_df, test_df)` com o protocolo exato de Shi et al.
- `filter_for_bkt_dkt(df)` e `filter_for_code_dkt(df)` inalteradas
- `build_sequences(df, assignment_id)` e `truncate_sequences(sequences, max_len=50)` inalteradas

#!/usr/bin/env python
# coding: utf-8

# # EDA — Dataset CSEDM / ProgSnap2 v6
# 
# Análise Exploratória de Dados para o projeto de Knowledge Tracing no CSEDM.  
# Metodologia: fase de *Data Preparation* do EDM Process (Kalita et al., 2025).
# 
# ---
# 
# ## 1 — Estatísticas Básicas e Qualidade dos Dados
# 
# **Contexto:** Antes de qualquer modelagem, é preciso confirmar que o dataset CSEDM/ProgSnap2 foi carregado corretamente, que o split 80/20 (Spring 2019, protocolo de Shi et al. 2022) tem as dimensões esperadas e que não há problemas críticos de qualidade (valores ausentes, duplicatas, inconsistências de Score). Esta seção estabelece os fatos de base que todo notebook subsequente assume.  
# **Hipótese:** O dataset Spring 2019 deve conter ~201 mil eventos, 413 estudantes brutos (410 após o filtro `min_attempts >= 3`), 5 assignments e 50 problemas; a taxa de tentativas corretas (`Run.Program` com `Score==1.0`) deve ser ~23.68%, reproduzindo o benchmark de Shi et al. (2022).  
# **Referência:** Price et al. (2020); Shi et al. (2022).
# 
# ### 1.1 — Composição do Dataset

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['figure.dpi'] = 120

DATA_ROOT = Path('../data/CSEDM')
ROOT = Path('..').resolve()
sys.path.insert(0, str(ROOT))


# In[2]:


# Carregar MainTable Spring 2019 (dataset completo)
all_main = pd.read_csv(DATA_ROOT / 'MainTable.csv')
print(f'Shape: {all_main.shape}')
all_main.head(3)


# ### 1.1.1 — Distribuição de EventTypes
# 
# **Contexto:** O ProgSnap2 define três EventTypes no CSEDM: `Run.Program` (execução com Score), `Compile` (evento filho gerado 1:1 pelo Run.Program com mesmo timestamp) e `Compile.Error` (compilação com erro, sem execução). A proporção de cada tipo determina quais eventos entram em cada modelo: BKT/DKT usam apenas `Run.Program`; Code-DKT com srcML inclui também `Compile.Error`.  
# **Hipótese:** Esperamos ~35% de `Run.Program`, ~35% de `Compile` (evento filho 1:1) e ~30% de `Compile.Error`. O EventType `Submit` não existe no CSEDM — submissões são `Run.Program` com Score não-nulo.  
# **Referência:** Price et al. (2020).

# In[3]:


event_counts = (
    all_main['EventType']
    .value_counts()
    .rename_axis('EventType')
    .reset_index(name='Count')
)
event_counts['%'] = (event_counts['Count'] / event_counts['Count'].sum() * 100).round(2)
print(event_counts.to_string(index=False))


# In[4]:


fig, ax = plt.subplots(figsize=(9, 4))
bars = ax.barh(event_counts['EventType'], event_counts['Count'], color=sns.color_palette('muted'))
ax.bar_label(bars, labels=[f"{v:,}" for v in event_counts['Count']], padding=4, fontsize=9)
ax.set_xlabel('Número de eventos')
ax.set_title('Distribuição de eventos por EventType — CSEDM (Spring 2019)')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.tight_layout()
plt.show()


# **Achado:** O dataset Spring 2019 contém 201.570 eventos em três EventTypes: `Run.Program` (69.627; 34.54%), `Compile` (69.627; 34.54%) e `Compile.Error` (62.316; 30.92%). O EventType `Submit` não existe no CSEDM — confirmando a especificação ProgSnap2.  
# **Implicação para modelagem:** `Compile.Error` representa 30.92% dos eventos — volume substancial que seria descartado pelo Code-DKT original (que exige código parsável). O uso de srcML (Pankiewicz, Shi & Baker, 2025) permite incluir esses eventos como `correct=0` na sequência KT, preservando informação de esforço mesmo em submissões não-compiláveis. Para BKT e DKT, filtrar por `EventType == 'Run.Program'` é suficiente.

# ### 1.1.2 — Entidades Únicas
# 
# **Contexto:** Confirmar o número de estudantes, assignments e problemas garante que o dataset Spring 2019 foi carregado corretamente e que a estrutura KC=ProblemID (10 KCs por assignment) é viável para o protocolo de KT adotado.  
# **Hipótese:** Esperamos 413 estudantes brutos, 5 assignments e 50 ProblemIDs (10 por assignment), consistente com o reportado em Shi et al. (2022) — que aplica posteriormente o filtro `min_attempts >= 3` reduzindo para 410 alunos elegíveis.  
# **Referência:** Shi et al. (2022); Price et al. (2020).

# In[5]:


n_students    = all_main['SubjectID'].nunique()
n_assignments = all_main['AssignmentID'].dropna().nunique()
n_problems    = all_main['ProblemID'].dropna().nunique()
n_events      = len(all_main)

summary = pd.DataFrame({
    'Métrica': ['Total de eventos', 'Estudantes únicos (SubjectID)',
                'Assignments únicos (AssignmentID)', 'Problemas únicos (ProblemID)'],
    'Valor': [f'{n_events:,}', f'{n_students:,}', f'{n_assignments:,}', f'{n_problems:,}']
})
display(summary.set_index('Métrica'))

print('\nAssignmentIDs:', sorted(all_main['AssignmentID'].dropna().unique()))
print('ProblemIDs:   ', sorted(all_main['ProblemID'].dropna().unique()))


# **Achado:** O dataset Spring 2019 contém 413 estudantes únicos, 5 assignments (IDs: 439, 487, 492, 494, 502) e 50 ProblemIDs — distribuídos uniformemente em 10 por assignment.  
# **Implicação para modelagem:** A estrutura de 10 KCs por assignment confirma a viabilidade do protocolo de Shi et al. (2022): 5 modelos independentes, um por assignment, com KC=ProblemID. O input one-hot do DKT terá dimensão `2 × 10 = 20` por tentativa (problem × correctness); o Code-DKT concatena ainda o vetor de representação de código a esse input.

# ### 1.1.3 — Participação dos Estudantes por Assignment
# 
# **Contexto:** Verificar quantos estudantes participaram de quais assignments revela o grau de dropout ao longo do semestre. Dropout substancial pode indicar viés de seleção nos últimos assignments e afeta a comparabilidade de desempenho entre fases do curso.  
# **Hipótese:** Diferentemente de cursos com matrícula rígida, o CSEDM contém estudantes que entraram e saíram em momentos diferentes. Esperamos participação ≥ 70% para todos os assignments, mas uma minoria significativa pode ter participado de apenas alguns deles.  
# **Referência:** Shi et al. (2022).

# In[6]:


students_per_assignment = (
    all_main.dropna(subset=['AssignmentID'])
    .groupby('AssignmentID')['SubjectID']
    .nunique()
    .reset_index(name='Estudantes')
    .sort_values('AssignmentID')
)
students_per_assignment['% do total'] = (
    students_per_assignment['Estudantes'] / n_students * 100
).round(1)
display(students_per_assignment)


# In[7]:


fig, ax = plt.subplots(figsize=(7, 3.5))
ax.bar(
    students_per_assignment['AssignmentID'].astype(str),
    students_per_assignment['Estudantes'],
    color=sns.color_palette('muted')
)
ax.axhline(n_students, color='crimson', linestyle='--', linewidth=1.2, label=f'Total ({n_students})')
for bar, val in zip(ax.patches, students_per_assignment['Estudantes']):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2, str(val),
            ha='center', va='bottom', fontsize=10)
ax.set_xlabel('AssignmentID')
ax.set_ylabel('Estudantes únicos')
ax.set_title('Estudantes por assignment — CSEDM (Spring 2019)')
ax.legend()
plt.tight_layout()
plt.show()


# In[8]:


# Quantos assignments cada estudante completou (participou de pelo menos 1 evento)
assignments_per_student = (
    all_main.dropna(subset=['AssignmentID'])
    .groupby('SubjectID')['AssignmentID']
    .nunique()
    .value_counts()
    .sort_index()
    .reset_index()
)
assignments_per_student.columns = ['Nº de assignments', 'Estudantes']
assignments_per_student['%'] = (
    assignments_per_student['Estudantes'] / n_students * 100
).round(1)
display(assignments_per_student)

full_participants = assignments_per_student.loc[
    assignments_per_student['Nº de assignments'] == n_assignments, 'Estudantes'
].sum()
print(f'\nEstudantes que participaram de TODOS os {n_assignments} assignments: {full_participants} '
      f'({full_participants/n_students*100:.1f}%)')


# **Achado:** Apenas 58.4% dos estudantes (241/413) participaram de todos os 5 assignments. A participação por assignment varia de 93.5% no A439 (386 alunos) para 74.1% no A502 (306 alunos), com queda gradual ao longo do semestre. 33 estudantes participaram de apenas 1 assignment, indicando dropout não-trivial.  
# **Implicação para modelagem:** O dropout não-uniforme não compromete o treinamento por assignment, mas exige cuidado em análises agregadas entre assignments. Estudantes com participação parcial entram naturalmente nos modelos dos assignments em que participaram — o protocolo de Shi et al. (2022) treina um modelo por assignment e portanto isola o efeito, sem necessidade de exclusão explícita.

# ### 1.1.4 — Consistência do Split 80/20 (Spring 2019)
# 
# **Contexto:** O pipeline usa um único dataset (Spring 2019, 410 alunos com min_attempts≥3),
# dividido 80/20 via train_test_split(random_state=1). Verificamos que o split é limpo:
# sem sobreposição entre train e test, e todos os 5 assignments cobertos em ambos os lados.
# 
# **Hipótese:** 0 estudantes em sobreposição; todos os 5 assignments em test.
# 
# **Referência:** Shi et al. (2022) — protocolo 80/20 com random_state=1.

# In[9]:


from src.data_loader import load_spring2019_split
train_df, test_df = load_spring2019_split(DATA_ROOT, test_size=0.2, random_state=1, min_attempts=3)

splits = {'train': train_df, 'test': test_df}
rows = []
for name, df in splits.items():
    rows.append({
        'Split': name,
        'Estudantes': df['SubjectID'].nunique(),
        'Eventos': len(df),
        'Assignments': sorted(df['AssignmentID'].dropna().unique().tolist()),
    })
print(pd.DataFrame(rows).to_string(index=False))

# Verificações
overlap = set(train_df['SubjectID']) & set(test_df['SubjectID'])
print(f'\nSobreposição train ∩ test: {len(overlap)}')
assert len(overlap) == 0
assert train_df['SubjectID'].nunique() == 328
assert test_df['SubjectID'].nunique() == 82
assert set(test_df['AssignmentID'].dropna().unique()) == {439, 487, 492, 494, 502}


# **Achado:** Split 80/20 limpo — 0 estudantes em sobreposição entre train (328) e test (82).
# Todos os 5 assignments disponíveis em ambos os splits. Comparação direta com Table 1/Table 2
# de Shi et al. (2022) agora válida.
# 
# **Implicação para modelagem:** Avaliação sem data leakage; AUC em test set reflete generalização
# real para os 5 assignments.

# ---
# 
# ## 1.2 — Qualidade dos Dados e Anatomia do Split
# 
# **Contexto:** Identificar problemas de qualidade (valores ausentes, duplicatas, inconsistências de Score) antes do pré-processamento evita surpresas durante o treinamento. Esta seção também valida que o dataset Spring 2019 reproduz a taxa de 23.68% de corretos reportada pelo paper Code-DKT.  
# **Hipótese:** Colunas essenciais para KT (`CodeStateID`, `Score`, `EventType`) devem ter cobertura adequada nos seus respectivos EventTypes. Os ~132 mil registros com mesmo (SubjectID, ProblemID, Timestamp) correspondem ao aninhamento ProgSnap2 (cada `Run.Program` gera um evento `Compile` filho com timestamp idêntico) — comportamento esperado, não erro de coleta.  
# **Referência:** Price et al. (2020); Shi et al. (2022).

# ### 1.2.2 — Valores Ausentes por Coluna
# 
# **Contexto:** Identificar colunas com missing values é essencial para decidir estratégias de pré-processamento. As colunas críticas para KT são `CodeStateID` (features AST para Code-DKT), `Score` (label binário) e `EventType` (filtro Run.Program vs Compile.Error).  
# **Hipótese:** `CodeStateID` deve ter 100% de cobertura (essencial para Code-DKT). `Score` deve ser ausente exatamente para os eventos não-Run.Program. `CompileMessageData` deve ter alto percentual de missing por ser exclusiva de `Compile.Error`.  
# **Referência:** Price et al. (2020).

# In[10]:


missing = (
    all_main.isnull().sum()
    .reset_index()
    .rename(columns={'index': 'Coluna', 0: 'Nulos'})
)
missing.columns = ['Coluna', 'Nulos']
missing['%'] = (missing['Nulos'] / len(all_main) * 100).round(2)
missing = missing[missing['Nulos'] > 0].sort_values('Nulos', ascending=False)
display(missing.reset_index(drop=True))


# In[11]:


# Ausencia de CodeStateID por EventType
no_code = (
    all_main[all_main['CodeStateID'].isnull()]
    .groupby('EventType')
    .size()
    .reset_index(name='Eventos sem CodeStateID')
)
totals = all_main.groupby('EventType').size().rename('Total')
no_code = no_code.join(totals, on='EventType')
no_code['% do EventType'] = (no_code['Eventos sem CodeStateID'] / no_code['Total'] * 100).round(1)
display(no_code)
pct_with_code = all_main['CodeStateID'].notna().mean() * 100
print(f'\nEventos COM CodeStateID: {all_main["CodeStateID"].notna().sum():,} ({pct_with_code:.1f}%)')


# **Achado:** `CodeStateID` tem cobertura de 100% — todos os 201.570 eventos têm snapshot de código associado. `Score` e `Compile.Result` são ausentes em 65.46% dos eventos (exclusivos de `Run.Program`). `CompileMessageType`/`CompileMessageData`/`SourceLocation` são ausentes em 69.08% (exclusivos de `Compile.Error`). `ParentEventID` é ausente em 34.54% — exatamente a proporção de `Run.Program`, que não tem evento pai.  
# **Implicação para modelagem:** A cobertura total de `CodeStateID` garante que o Code-DKT pode extrair features AST via srcML de todos os eventos, incluindo `Compile.Error`. Os campos ausentes são estruturalmente ausentes (não aleatórios) — nenhuma imputação é necessária. A ausência de `Score` e `Compile.Result` em registros cruzados confirma a separação limpa de responsabilidades entre EventTypes.

# ### 1.2.3 — Run.Program como Submissão e Distribuição de Score
# 
# **Contexto:** O CSEDM não tem EventType `Submit` — submissões são `Run.Program` com Score não-nulo (Price et al., 2020). O Score não é puramente binário: existe proporção considerável de scores parciais (0 < Score < 1) que exige uma decisão de threshold para o label binário de KT.  
# **Hipótese:** 100% dos `Run.Program` devem ter Score não-nulo. Esperamos ~37% de scores parciais (0 < Score < 1). Score fora de [0, 1] deve ser 0 registros (dataset limpo).  
# **Referência:** Price et al. (2020); Shi et al. (2022).

# In[12]:


# Confirmar que Score so existe em Run.Program
score_by_event = (
    all_main.groupby('EventType')['Score']
    .agg(total='count', com_score=lambda s: s.notna().sum())
    .assign(pct_com_score=lambda d: (d['com_score'] / d['total'] * 100).round(1))
)
display(score_by_event)

runs = all_main[all_main['EventType'] == 'Run.Program'].copy()
print(f'\nRun.Program com Score nao-nulo: {runs["Score"].notna().sum():,} ({runs["Score"].notna().mean()*100:.1f}%)')
print(f'Score fora de [0,1]:            {((runs["Score"] < 0) | (runs["Score"] > 1)).sum()}')
print(f'Score == 1.0 (correto):         {(runs["Score"] == 1.0).sum():,} ({(runs["Score"] == 1.0).mean()*100:.2f}%)')
print(f'Score parcial (0 < s < 1):      {((runs["Score"] > 0) & (runs["Score"] < 1)).sum():,}')


# In[13]:


scores  = runs['Score'].dropna()
partial = scores[(scores > 0) & (scores < 1)]

fig, axes = plt.subplots(1, 2, figsize=(11, 3.5))

axes[0].hist(scores, bins=25, color=sns.color_palette('muted')[0], edgecolor='white')
axes[0].set_xlabel('Score')
axes[0].set_ylabel('Frequencia')
axes[0].set_title('Distribuicao completa de Score (Run.Program)')

axes[1].hist(partial, bins=20, color=sns.color_palette('muted')[2], edgecolor='white')
axes[1].set_xlabel('Score')
axes[1].set_title('Scores parciais (0 < Score < 1)')

plt.suptitle('Score em Run.Program -- CSEDM (Spring 2019)', y=1.02)
plt.tight_layout()
plt.show()

print(f'Scores parciais: {len(partial):,} ({len(partial)/len(scores)*100:.2f}% das execucoes com score)')


# **Achado:** 100% dos `Run.Program` têm Score não-nulo; 0 registros têm Score fora de [0, 1]. Scores parciais (0 < Score < 1) representam 33.46% das execuções. Score == 1.0 (totalmente correto) aparece em 23.68% dos `Run.Program`, e Score == 0.0 em 42.86%.  
# **Implicação para modelagem:** O threshold `Score == 1.0` → `correct=1` é adotado para KT binário, seguindo Shi et al. (2022). Scores parciais (33.46%) são tratados como `correct=0` — sacrificando a granularidade da pontuação parcial em troca de consistência com o paper de referência e com a definição binária do BKT.

# ### 1.2.4 — Registros Duplicados: Estrutura Aninhada do ProgSnap2
# 
# **Contexto:** O ProgSnap2 registra eventos aninhados via `ParentEventID`: cada `Run.Program` gera um evento filho `Compile` com o **mesmo timestamp**. Isso é comportamento esperado da especificação, não erro de coleta. Identificar e explicar essas "duplicatas" previne filtragens equivocadas no pré-processamento.  
# **Hipótese:** Esperamos da ordem de 130 mil registros com mesmo (SubjectID, ProblemID, ServerTimestamp), correspondentes aos 69.627 pares Run.Program/Compile somados a eventuais Compile.Error com timestamp compartilhado dentro do mesmo problema.  
# **Referência:** Price et al. (2020).

# In[14]:


all_splits = {'All': all_main, 'Train': train_df, 'Test': test_df}

dup_key = ['SubjectID', 'ProblemID', 'ServerTimestamp']
n_dups = all_main.duplicated(subset=dup_key).sum()
print(f'Registros duplicados (SubjectID + ProblemID + Timestamp): {n_dups}')

print('\nCobertura temporal por split:')
for name, df in all_splits.items():
    ts = pd.to_datetime(df['ServerTimestamp'], errors='coerce').dropna()
    if len(ts):
        span = (ts.max() - ts.min()).days
        print(f'  {name:<20}: {ts.min().date()} -> {ts.max().date()}  ({span} dias)')


# **Achado:** 132.344 registros compartilham o mesmo (SubjectID, ProblemID, ServerTimestamp). A composição é mista: 41.230 grupos de tamanho 2 (par puro Run.Program/Compile com timestamp idêntico) e 27.996 grupos com mais de 2 eventos no mesmo instante (Run.Program/Compile somados a Compile.Error do mesmo aluno no mesmo problema). Cada `Run.Program` tem um `Compile` filho com `ParentEventID` apontando para o `EventID` do pai e timestamp idêntico, conforme a especificação ProgSnap2.  
# **Implicação para modelagem:** Esses 132.344 registros **não são erros** — são a estrutura hierárquica esperada do ProgSnap2 (Price et al., 2020). No pré-processamento: para BKT/DKT, filtrar por `EventType == 'Run.Program'` já elimina os `Compile` filhos automaticamente. Para Code-DKT com srcML, incluir `Compile.Error` mas **não** os `Compile` filhos de `Run.Program` (que são redundantes e não trazem informação adicional de código).

# ### 1.2.5 — Benchmark de Reprodutibilidade: Comparação com Shi et al. (2022)
# 
# **Contexto:** O paper Code-DKT (Shi et al., 2022) reporta 23.68% de tentativas corretas no seu dataset de treinamento (Spring 2019 com filtro `min_attempts >= 3`, n=410 alunos). Confirmar que o dataset bruto carregado aqui reproduz esse mesmo número é o primeiro teste de reprodutibilidade do pipeline.  
# **Hipótese:** A taxa de corretos sobre `Run.Program` em `MainTable.csv` (413 alunos brutos) deve coincidir com os 23.68% do paper dentro de uma tolerância de ±0.5pp — o pequeno número de alunos excluídos pelo filtro `min_attempts >= 3` (3 de 413) tem efeito insignificante na taxa global.  
# **Referência:** Shi et al. (2022).

# In[15]:


# Verificar taxa de corretos do Spring 2019 vs Shi et al. (2022)
# Paper: ~410 estudantes, 50 problemas, 5 assignments, 23.68% correto

runs = all_main[all_main['EventType'] == 'Run.Program']
pct = (runs['Score'] == 1.0).mean() * 100
n_students = all_main['SubjectID'].nunique()
print(f'data/CSEDM/MainTable.csv — {n_students} alunos, {pct:.2f}% corretos')
print(f'Referência Shi et al. (2022): 410 alunos, 23.68% corretos')
assert abs(pct - 23.68) < 0.5, f'Taxa inesperada: {pct:.2f}%'
print('Assert OK: taxa de corretos dentro da tolerância de ±0.5pp')


# **Achado:** O dataset Spring 2019 apresenta 23.68% de corretos (Score == 1.0 em Run.Program) — match exato com o valor reportado por Shi et al. (2022). 413 alunos brutos no MainTable.csv reduzem-se a 410 após o filtro `min_attempts >= 3`, alinhando-se exatamente com o `n=410` do paper.  
# **Implicação para modelagem:** O dataset está íntegro para reprodução. Toda comparação com Table 1 e Table 2 de Shi et al. (2022) usa este split (Spring 2019, 80/20, `random_state=1`). A baixa proporção de acertos (~23.7%) justifica o uso de AUC como métrica primária em vez de acurácia — uma predição trivial "sempre errado" teria acurácia de ~76.3%, mas AUC de ~50%.

# ---
# 
# ## 2 — Análise da População de Estudantes
# 
# **Contexto:** Caracterizar a população de estudantes — distribuição de desempenho final (X-Grade), padrões de tentativa e heterogeneidade de perfis — é essencial para compreender o ambiente de aprendizagem capturado pelo CSEDM. Estudantes com diferentes capacidades e comportamentos geram sequências de KT com propriedades distintas; documentar essa heterogeneidade justifica o uso de modelos com sequências individualizadas (DKT, Code-DKT) em vez de modelos que assumem homogeneidade da turma.  
# **Hipótese:** Esperamos distribuição de X-Grade aproximadamente unimodal e ampla (escala 0–1, equivalente a 0–100%), distribuição assimétrica à direita para tentativas totais (cauda longa) e clustering em k=3 revelando perfis interpretáveis alinhados com X-Grade e taxa de acerto.  
# **Referência:** Shi et al. (2022); Abdelrahman et al. (2022); Kalita et al. (2025).

# ### 2.1 — Distribuição de Desempenho Geral (X-Grade)
# 
# **Contexto:** O campo `X-Grade` em `Subject.csv` representa a nota final normalizada (escala 0–1, equivalente a 0–100%) de cada estudante na disciplina. Sua distribuição define a heterogeneidade da turma e serve como validador externo para os clusters exploratórios (Seção 2.3) e para as métricas de KT — um modelo bem calibrado deve discriminar estudantes de diferentes faixas de desempenho.  
# **Hipótese:** Distribuição aproximadamente unimodal com média na faixa intermediária (~0.6) e minoria de estudantes com X-Grade < 0.25 (grupo em risco). A taxa de acerto eventual (`CorrectEventually`) por assignment deve correlacionar-se positivamente com X-Grade.  
# **Referência:** Shi et al. (2022); Kalita et al. (2025).

# In[16]:


# Carregar Subject.csv, early.csv e late.csv (Spring 2019)
subject = pd.read_csv(DATA_ROOT / 'LinkTables/Subject.csv')
early   = pd.read_csv(DATA_ROOT.parent / 'early.csv')
late    = pd.read_csv(DATA_ROOT.parent / 'late.csv')

# Concatenar para cobrir todos os 5 assignments
# early.csv cobre A439, A487, A492; late.csv cobre A494, A502
all_labels = pd.concat([early, late], ignore_index=True)

print(f'early.csv  : {early.shape}   assignments: {sorted(early["AssignmentID"].unique())}')
print(f'late.csv   : {late.shape}    assignments: {sorted(late["AssignmentID"].unique())}')
print(f'all_labels : {all_labels.shape}  assignments: {sorted(all_labels["AssignmentID"].unique())}')
print()
display(subject['X-Grade'].describe().rename('X-Grade').to_frame().T)


# In[17]:


grades = subject['X-Grade'].dropna()

assign_counts = (
    all_main.dropna(subset=['AssignmentID'])
    .groupby('SubjectID')['AssignmentID']
    .nunique()
    .rename('n_assignments')
)
subject_ext = subject.join(assign_counts, on='SubjectID')

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].hist(grades, bins=20, color=sns.color_palette('muted')[0], edgecolor='white')
axes[0].axvline(grades.median(), color='crimson', linestyle='--', linewidth=1.2,
                label=f'Mediana: {grades.median():.2f}')
axes[0].axvline(grades.mean(), color='darkorange', linestyle=':', linewidth=1.2,
                label=f'Média: {grades.mean():.2f}')
axes[0].set_xlabel('X-Grade')
axes[0].set_ylabel('Estudantes')
axes[0].set_title('Distribuição de X-Grade (Spring 2019)')
axes[0].legend(fontsize=8)

data_by_assign = [
    subject_ext[subject_ext['n_assignments'] == k]['X-Grade'].dropna()
    for k in sorted(subject_ext['n_assignments'].dropna().unique())
]
tick_labels = [f'{int(k)} assign.' for k in sorted(subject_ext['n_assignments'].dropna().unique())]
axes[1].boxplot(data_by_assign, tick_labels=tick_labels, patch_artist=True,
                boxprops=dict(facecolor=sns.color_palette('muted')[1], alpha=0.7))
axes[1].set_xlabel('Assignments completados')
axes[1].set_ylabel('X-Grade')
axes[1].set_title('X-Grade por número de assignments completados')

plt.tight_layout()
plt.show()

pct_above_05  = (grades >= 0.5).mean() * 100
pct_below_025 = (grades < 0.25).mean() * 100
print(f'Estudantes com X-Grade >= 0.50: {pct_above_05:.1f}%')
print(f'Estudantes com X-Grade <  0.25: {pct_below_025:.1f}%  (potencial em risco)')


# In[18]:


# Taxa de acerto eventual (CorrectEventually) por assignment × X-Grade
# Usando all_labels (early + late) para cobrir os 5 assignments
correct_rate_by_assignment = (
    all_labels.groupby(['SubjectID', 'AssignmentID'])
    .apply(lambda g: g['CorrectEventually'].mean(), include_groups=False)
    .rename('correct_rate')
    .reset_index()
    .pivot(index='SubjectID', columns='AssignmentID', values='correct_rate')
)
correct_rate_by_assignment.columns = [f'A{c}_rate' for c in correct_rate_by_assignment.columns]

student_perf = correct_rate_by_assignment.join(subject.set_index('SubjectID')['X-Grade'])

n_assignments_plot = correct_rate_by_assignment.shape[1]
fig, axes = plt.subplots(1, n_assignments_plot, figsize=(4 * n_assignments_plot, 3.5), sharey=True)
cols = [c for c in student_perf.columns if c.endswith('_rate')]
for ax, col in zip(axes, cols):
    label = col.replace('_rate', '')
    ax.scatter(student_perf[col], student_perf['X-Grade'], alpha=0.35, s=18,
               color=sns.color_palette('muted')[2])
    corr = student_perf[[col, 'X-Grade']].dropna().corr().iloc[0, 1]
    ax.set_title(f'{label}\nr={corr:.2f}', fontsize=9)
    ax.set_xlabel('Taxa de acerto eventual')
    if ax == axes[0]:
        ax.set_ylabel('X-Grade')

plt.suptitle('Taxa de acerto eventual por assignment vs X-Grade (correlação de Pearson)', y=1.02)
plt.tight_layout()
plt.show()

print('Taxa média de CorrectEventually por assignment:')
print(correct_rate_by_assignment.mean().round(3).to_string())


# **Achado:** X-Grade está na escala [0, 1] (equivalente a 0–100%), variando de 0.00 a 0.98 com média 0.62 (±0.24) e mediana 0.67 — distribuição levemente assimétrica para a esquerda. 73.2% dos estudantes obtiveram X-Grade ≥ 0.50; apenas 7.8% ficaram abaixo de 0.25 (grupo em risco). A taxa de CorrectEventually por assignment correlaciona-se positivamente com X-Grade em todos os cinco assignments.  
# **Implicação para modelagem:** A turma é heterogênea mas com concentração no terço superior da escala. Modelos de KT com sequências individualizadas (DKT, Code-DKT) capturam melhor essa heterogeneidade do que parâmetros globais de maestria. A correlação de CorrectEventually com X-Grade valida `ProblemID` como KC — os problemas capturam sinais de aprendizagem que se traduzem em desempenho acadêmico real.

# ### 2.2 — Padrões de Tentativa por Estudante
# 
# **Contexto:** O número de tentativas por problema e por estudante reflete esforço, persistência e dificuldade percebida. Distribuições com cauda longa identificam estudantes em dificuldade persistente — padrão relevante para o Code-DKT, que inclui `Compile.Error` como tentativa `correct=0`, e para o protocolo de truncamento em 50 tentativas de Shi et al. (2022).  
# **Hipótese:** Distribuição assimétrica à direita com mediana acima de uma centena de tentativas totais (5 assignments). A correlação entre tentativas totais e X-Grade pode ter sinal positivo (engajamento traduz-se em mais tentativas e mais aprendizado) ou negativo (mais tentativas indica mais dificuldade).  
# **Referência:** Shi et al. (2022); Pankiewicz, Shi & Baker (2025).

# In[19]:


# Usando all_labels (early + late) para cobrir todos os 5 assignments
attempts_per_student = all_labels.groupby('SubjectID')['Attempts'].sum().rename('total_attempts')

print('Distribuição de tentativas totais por estudante (5 assignments):')
display(attempts_per_student.describe().rename('total_attempts').to_frame().T.round(1))

outlier_thresh = 200
outliers = (attempts_per_student >= outlier_thresh).sum()
print(f'\nEstudantes com >= {outlier_thresh} tentativas totais: {outliers} '
      f'({outliers / len(attempts_per_student) * 100:.1f}%)')

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].hist(attempts_per_student, bins=40, color=sns.color_palette('muted')[3], edgecolor='white')
axes[0].axvline(attempts_per_student.median(), color='crimson', linestyle='--',
                label=f'Mediana: {attempts_per_student.median():.0f}')
axes[0].set_xlabel('Total de tentativas (5 assignments)')
axes[0].set_ylabel('Estudantes')
axes[0].set_title('Distribuição de tentativas totais por estudante')
axes[0].legend(fontsize=8)

attempts_per_problem = all_labels['Attempts']
axes[1].hist(attempts_per_problem, bins=30, color=sns.color_palette('muted')[4], edgecolor='white')
axes[1].axvline(attempts_per_problem.median(), color='crimson', linestyle='--',
                label=f'Mediana: {attempts_per_problem.median():.0f}')
axes[1].set_xlabel('Tentativas por problema')
axes[1].set_ylabel('(Estudante, Problema)')
axes[1].set_title('Distribuição de tentativas por problema')
axes[1].legend(fontsize=8)

plt.tight_layout()
plt.show()


# In[20]:


# Usando all_labels para cobrir os 5 assignments
solved_any   = all_labels.groupby('SubjectID')['CorrectEventually'].any()
never_solved = (~solved_any).sum()
print(f'Estudantes que nunca resolveram nenhum problema: {never_solved} '
      f'({never_solved / len(solved_any) * 100:.1f}%)')

solved_all = all_labels.groupby('SubjectID')['CorrectEventually'].all()
incomplete = (~solved_all).sum()
print(f'Estudantes com ao menos 1 problema sem resolver: {incomplete} '
      f'({incomplete / len(solved_all) * 100:.1f}%)')

student_summary = (
    attempts_per_student
    .to_frame()
    .join(subject.set_index('SubjectID')['X-Grade'])
)
corr = student_summary.corr(method='spearman').iloc[0, 1]
print(f'\nCorrelação Spearman (tentativas totais × X-Grade): {corr:.3f}')

fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(student_summary['total_attempts'], student_summary['X-Grade'],
           alpha=0.35, s=18, color=sns.color_palette('muted')[0])
ax.set_xlabel('Total de tentativas (5 assignments)')
ax.set_ylabel('X-Grade')
ax.set_title(f'Tentativas totais vs X-Grade  (Spearman ρ = {corr:.3f})')
plt.tight_layout()
plt.show()


# **Achado:** 35.5% dos estudantes (123 de 346 com `Attempts` em early+late) realizaram ≥ 200 tentativas totais. Apenas 2 estudantes (0.6%) nunca resolveram nenhum problema; 61.3% (212) deixaram ao menos um problema sem resolver. A correlação Spearman entre tentativas totais e X-Grade é fraca e positiva (ρ = 0.341).  
# **Implicação para modelagem:** A correlação positiva indica que tentar mais associa-se levemente a melhor desempenho — coerente com comportamento de estudantes engajados que exploram o sistema. O truncamento em 50 tentativas por sequência (Shi et al., 2022) é justificado pelo subgrupo de 35.5% com sequências longas: limita o custo computacional do LSTM e reduz o viés desses outliers de engajamento. Os 61.3% com ao menos um problema não resolvido evidenciam que BKT com parâmetros únicos por KC não diferencia baixo engajamento de dificuldade persistente — o DKT e Code-DKT, ao modelar sequências individuais, capturam esse contínuo de forma mais fiel.

# ### 2.3 — Perfis de Estudante: Clustering Exploratório
# 
# **Contexto:** Identificar grupos naturais de estudantes com base em taxa de acerto eventual, número médio de tentativas por assignment e nota final documenta a heterogeneidade comportamental da turma. O agrupamento é exploratório — não alimenta os modelos de KT diretamente — mas evidencia por que sequências individualizadas são necessárias: perfis distintos implicam trajetórias de aprendizagem sistematicamente diferentes que um modelo de turma único não capturaria.  
# **Hipótese:** K-Means com k=3 deve revelar perfis interpretáveis alinhados com X-Grade: Alto desempenho (grade alta, alta taxa de acerto, poucas tentativas por problema), Médio (grade intermediária) e Em risco (grade baixa, baixa taxa de acerto ou poucas tentativas).  
# **Referência:** Shi et al. (2022); Abdelrahman et al. (2022).

# In[21]:


SEED = 42

avg_att_by_assignment = (
    all_labels.groupby(['SubjectID', 'AssignmentID'])['Attempts']
    .mean()
    .reset_index()
    .pivot(index='SubjectID', columns='AssignmentID', values='Attempts')
)
avg_att_by_assignment.columns = [f'A{c}_att' for c in avg_att_by_assignment.columns]

cluster_features = (
    correct_rate_by_assignment
    .join(avg_att_by_assignment)
    .join(subject.set_index('SubjectID')['X-Grade'])
    .dropna()
)

print(f'Estudantes com features completas: {len(cluster_features)} / {n_students}')
print(f'Features: {list(cluster_features.columns)}')
print()
display(cluster_features.describe().round(2))

X = cluster_features.values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

inertias = {k: KMeans(n_clusters=k, random_state=SEED, n_init=10).fit(X_scaled).inertia_
            for k in range(2, 7)}

fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(list(inertias.keys()), list(inertias.values()), 'o-', color=sns.color_palette('muted')[0])
ax.set_xlabel('k')
ax.set_ylabel('Inércia')
ax.set_title('Elbow — K-Means (correct_rate × avg_attempts × X-Grade, 5 assignments)')
plt.tight_layout()
plt.show()


# In[22]:


from sklearn.metrics import silhouette_score

K_range = range(2, 7)
sil_scores = []
for k in K_range:
    km_tmp = KMeans(n_clusters=k, random_state=SEED, n_init=10)
    labels_tmp = km_tmp.fit_predict(X_scaled)
    sil_scores.append(silhouette_score(X_scaled, labels_tmp))

fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(list(K_range), sil_scores, 'o-', color=sns.color_palette('muted')[1])
ax.axvline(x=3, color='crimson', linestyle='--', alpha=0.7, label='k=3 escolhido')
ax.set_xlabel('k')
ax.set_ylabel('Silhouette Score')
ax.set_title('Silhouette Score por k — validação da escolha k=3')
ax.legend()
plt.tight_layout()
plt.show()

best_k = list(K_range)[sil_scores.index(max(sil_scores))]
print(f'Silhouette Score por k: {dict(zip(K_range, [round(s, 4) for s in sil_scores]))}')
print(f'Melhor k pelo Silhouette: {best_k}  |  Score (k=3): {sil_scores[1]:.4f}')


# In[23]:


K_BEST = 3
km = KMeans(n_clusters=K_BEST, random_state=SEED, n_init=10)
cluster_features = cluster_features.copy()
cluster_features['cluster'] = km.fit_predict(X_scaled)

# Nomear clusters pelo X-Grade médio
grade_by_cluster = cluster_features.groupby('cluster')['X-Grade'].mean().sort_values(ascending=False)
cluster_labels = {c: lbl for c, lbl in zip(grade_by_cluster.index,
                                             ['Alto desempenho', 'Médio', 'Em risco'])}
cluster_features['perfil'] = cluster_features['cluster'].map(cluster_labels)

# Tabela resumo separada: taxas de acerto | tentativas por assignment
rate_cols = [c for c in cluster_features.columns if c.endswith('_rate')]
att_cols  = [c for c in cluster_features.columns if c.endswith('_att')]

summary_base = cluster_features.groupby('perfil')[['X-Grade']].mean().round(2)
summary_base.insert(0, 'N', cluster_features.groupby('perfil').size())

summary_rate = cluster_features.groupby('perfil')[rate_cols].mean().round(2)
summary_att  = cluster_features.groupby('perfil')[att_cols].mean().round(1)

print('=== Resumo por perfil ===')
display(pd.concat([summary_base, summary_rate, summary_att], axis=1))

# Projeção PCA 2D
pca = PCA(n_components=2, random_state=SEED)
coords = pca.fit_transform(X_scaled)

palette = {'Alto desempenho': '#2196F3', 'Médio': '#FF9800', 'Em risco': '#F44336'}
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# PCA scatter
for perfil, color in palette.items():
    mask = cluster_features['perfil'] == perfil
    n = mask.sum()
    axes[0].scatter(coords[mask, 0], coords[mask, 1], label=f'{perfil} (n={n})',
                    color=color, alpha=0.6, s=30, edgecolors='none')
axes[0].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
axes[0].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
axes[0].set_title('Perfis — K-Means k=3 (PCA 2D)')
axes[0].legend(fontsize=8)

# Boxplot de X-Grade por perfil
order = ['Alto desempenho', 'Médio', 'Em risco']
data_box = [cluster_features[cluster_features['perfil'] == p]['X-Grade'] for p in order]
bp = axes[1].boxplot(data_box, tick_labels=order, patch_artist=True)
colors = [palette[p] for p in order]
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)
axes[1].set_ylabel('X-Grade')
axes[1].set_title('Distribuição de X-Grade por perfil')

plt.tight_layout()
plt.show()


# In[24]:


feature_cols = [c for c in cluster_features.columns if c not in ('cluster', 'perfil')]

# Centróides no espaço original (inverter StandardScaler), respeitando mapeamento cluster → perfil
order = ['Alto desempenho', 'Médio', 'Em risco']
centroid_rows = {
    label: scaler.inverse_transform(km.cluster_centers_[cid].reshape(1, -1))[0]
    for cid, label in cluster_labels.items()
}
centroid_df = pd.DataFrame(centroid_rows, index=feature_cols).T.loc[order]

fig, ax = plt.subplots(figsize=(13, 3))
sns.heatmap(centroid_df, annot=True, fmt='.2f', cmap='RdYlGn',
            linewidths=0.5, ax=ax, cbar_kws={'label': 'valor médio'})
ax.set_title('Centróides dos Clusters — espaço original das features')
plt.tight_layout()
plt.show()


# **Achado:** K-Means com k=3 (SEED=42) sobre 239 estudantes com features completas (taxa de acerto eventual e tentativas médias por assignment, mais X-Grade) revela três perfis ordenados por X-Grade médio:
# 
# | Perfil | N | X-Grade médio | Taxa de acerto eventual | Tentativas médias/assignment |
# |---|---|---|---|---|
# | **Alto desempenho** | 96 (40.2%) | 0.80 | 88–98% | 3.7–8.6 |
# | **Médio** | 19 (7.9%) | 0.65 | 32–65% (mínimo em A492) | 4.6–8.1 |
# | **Em risco** | 124 (51.9%) | 0.60 | 96–99% (inesperadamente alto) | 1.7–3.5 (muito baixo) |
# 
# Resultado inesperado: o cluster "Em risco" (51.9% da turma) apresenta taxas de acerto eventual tão altas quanto o "Alto desempenho", mas com número de tentativas médio muito menor (1.7–3.5/assignment). O cluster "Médio" é o que exibe menor taxa de acerto e mais tentativas — padrão de dificuldade persistente real. O perfil "Em risco" (grade ~0.60) parece representar estudantes com baixo engajamento — que tentam poucos problemas — e não necessariamente estudantes que erram muito. Esta interpretação é coerente com o achado de ρ = 0.341 (Seção 2.2): tentar mais associa-se a melhor desempenho.  
# **Implicação para modelagem:** A heterogeneidade não se organiza na estrutura esperada (dificuldade ↔ tentativas ↔ grade). O perfil "Em risco" evidencia que baixo engajamento é um padrão relevante nesta população, não apenas dificuldade persistente. O DKT e o Code-DKT, ao modelar sequências individualizadas, capturam implicitamente esses comportamentos; o BKT com parâmetros compartilhados por KC não diferencia engajamento seletivo de baixa maestria.

# ---
# 
# ## 3 — Estrutura de Assignments e Dificuldade
# 
# **Contexto:** O CSEDM organiza os 50 problemas em 5 assignments independentes (A1–A5), com 10 ProblemIDs por assignment. Shi et al. (2022) treina um modelo de KT independente por assignment com KC=ProblemID — 5 modelos separados sem transferência cross-assignment. Antes de replicar esse protocolo, é necessário confirmar a estrutura de KC por assignment e documentar a variabilidade de dificuldade dentro e entre assignments: a heterogeneidade de dificuldade determina o sinal de aprendizagem disponível para os modelos de KT.  
# **Hipótese:** Cada assignment deve conter exatamente 10 ProblemIDs. A taxa de acerto média deve diferir entre assignments e a amplitude de dificuldade intra-assignment deve superar 20pp, indicando KC com sinais de aprendizagem distintos.  
# **Referência:** Shi et al. (2022); Price et al. (2020).

# ### 3.1 — Composição dos Assignments (Spring 2019)
# 
# **Contexto:** Esta subseção confirma a estrutura de problemas e participação de estudantes por assignment no dataset Spring 2019, validando a viabilidade do protocolo KC=ProblemID (10 KCs por assignment).  
# **Hipótese:** Todos os 5 assignments devem ter exatamente 10 ProblemIDs e participação de 300+ estudantes (com algum dropout ao longo do semestre). A taxa de acerto global deve ser ≈ 23.7%.  
# **Referência:** Shi et al. (2022).

# In[25]:


# Usar Spring 2019 completo — comparável com Shi et al. (2022)
rel_train_main = pd.read_csv(DATA_ROOT / 'MainTable.csv')

runs_rel = rel_train_main[rel_train_main['EventType'] == 'Run.Program'].copy()
runs_rel['correct'] = (runs_rel['Score'] == 1.0).astype(int)

# Mapeamento AssignmentID → rótulo legível (A1–A5 em ordem cronológica)
assignment_order = sorted(runs_rel['AssignmentID'].dropna().unique())
assign_name = {aid: f'A{i+1} ({int(aid)})' for i, aid in enumerate(assignment_order)}
runs_rel['assign_label'] = runs_rel['AssignmentID'].map(assign_name)

# Tabela de estrutura por assignment
struct_rows = []
for aid in assignment_order:
    g = runs_rel[runs_rel['AssignmentID'] == aid]
    n_probs     = g['ProblemID'].nunique()
    n_students  = g['SubjectID'].nunique()
    n_att       = len(g)
    mean_att    = g.groupby('SubjectID').size().mean()
    pct_correct = g['correct'].mean() * 100
    struct_rows.append({
        'Assignment':                  assign_name[aid],
        'ProblemIDs (KCs)':            n_probs,
        'Estudantes':                  n_students,
        'Tentativas totais':           f'{n_att:,}',
        'Tentativas/estudante (média)': f'{mean_att:.1f}',
        '% correto (Score=1.0)':       f'{pct_correct:.2f}%',
    })

struct_df = pd.DataFrame(struct_rows).set_index('Assignment')
display(struct_df)

global_pct = runs_rel['correct'].mean() * 100
print(f'\n% correto global (Spring 2019): {global_pct:.2f}%  '
      f'| referência paper: 23.68%')


# **Achado:** O dataset Spring 2019 contém exatamente 10 ProblemIDs por assignment em todos os 5 assignments, com participação variando entre 306 (A502) e 386 (A439) estudantes. A taxa de acerto global é 23.68% — match exato com o benchmark de Shi et al. (2022). A média de tentativas por estudante varia de 31.2 (A502, mais curto) a 47.6 (A492, mais longo), indicando heterogeneidade de esforço entre assignments.  
# **Implicação para modelagem:** A estrutura de 10 KCs por assignment confirma a viabilidade do protocolo: input one-hot do DKT terá dimensão `2 × 10 = 20`; Code-DKT concatena ainda o vetor de código. A heterogeneidade de tentativas entre assignments justifica a análise de dificuldade por assignment (Seção 3.2) antes de unificar o protocolo de truncagem em 50 tentativas.

# ### 3.2 — Taxa de Acerto por Problema e Ranking de Dificuldade
# 
# **Contexto:** A taxa de acerto (Score == 1.0) por problema quantifica a dificuldade individual de cada KC. Amplitude grande intra-assignment indica que os KCs cobrem conceitos de dificuldades bem distintas — o que favorece modelos como DKT e Code-DKT, que aprendem representações individualizadas de habilidade. Shi et al. (2022) reportam a taxa global de 23.68%, mas não decompõem por problema — esta seção preenche essa lacuna para o protocolo de reprodutibilidade.  
# **Hipótese:** A amplitude de dificuldade intra-assignment deve superar 20pp. A curva de dificuldade por assignment deve mostrar pelo menos um problema muito fácil (> 50% correto) e um muito difícil (< 15%) por assignment.  
# **Referência:** Shi et al. (2022).

# In[26]:


RESULTS_DIR = Path('../results')
RESULTS_DIR.mkdir(exist_ok=True)

# Taxa de acerto por problema por assignment
prob_rate = (
    runs_rel.groupby(['AssignmentID', 'ProblemID'])['correct']
    .mean()
    .reset_index(name='correct_rate')
)
prob_rate['assign_label'] = prob_rate['AssignmentID'].map(assign_name)

# ── Barplot agrupado (5 assignments, 10 problemas cada) ──
fig, axes = plt.subplots(5, 1, figsize=(12, 15), sharex=False)
palette = sns.color_palette('RdYlGn', 10)

for i, aid in enumerate(assignment_order):
    ax = axes[i]
    subset = prob_rate[prob_rate['AssignmentID'] == aid].sort_values('correct_rate')
    # Ordenar por dificuldade crescente
    bar_colors = sns.color_palette('RdYlGn', len(subset))
    bars = ax.bar(
        range(len(subset)),
        subset['correct_rate'] * 100,
        color=bar_colors, edgecolor='white', width=0.7
    )
    ax.set_xticks(range(len(subset)))
    ax.set_xticklabels([f'P{int(p)}' for p in subset['ProblemID']], fontsize=8)
    mean_rate = subset['correct_rate'].mean() * 100
    ax.axhline(mean_rate, color='navy', linestyle='--', linewidth=1.2,
               label=f'Média: {mean_rate:.1f}%')
    ax.bar_label(bars, labels=[f'{v*100:.0f}%' for v in subset['correct_rate']],
                 padding=2, fontsize=7)
    ax.set_ylim(0, 75)
    ax.set_ylabel('% correto')
    ax.set_title(assign_name[aid], fontsize=10, loc='left')
    ax.legend(fontsize=8, loc='upper right')
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())

fig.suptitle('Taxa de acerto por problema por assignment (Spring 2019, ordenado por dificuldade)',
             fontsize=12, y=1.01)
plt.tight_layout()
fig.savefig(RESULTS_DIR / 'sec3_correct_rate_by_problem.png', dpi=120, bbox_inches='tight')
plt.show()
print('Plot salvo: results/sec3_correct_rate_by_problem.png')

# ── Ranking de dificuldade por assignment ──
print('\n=== Ranking de dificuldade por assignment (mais difícil → mais fácil) ===')
ranking_rows = []
for aid in assignment_order:
    subset = prob_rate[prob_rate['AssignmentID'] == aid].sort_values('correct_rate')
    hardest = subset.iloc[0]
    easiest = subset.iloc[-1]
    amplitude = (easiest['correct_rate'] - hardest['correct_rate']) * 100
    ranking_rows.append({
        'Assignment':       assign_name[aid],
        'Mais difícil':     f'P{int(hardest["ProblemID"])} ({hardest["correct_rate"]*100:.1f}%)',
        'Mais fácil':       f'P{int(easiest["ProblemID"])} ({easiest["correct_rate"]*100:.1f}%)',
        'Amplitude (pp)':   f'{amplitude:.1f}',
        'Média (%)':        f'{subset["correct_rate"].mean()*100:.1f}',
        'DP (pp)':          f'{subset["correct_rate"].std()*100:.1f}',
    })

ranking_df = pd.DataFrame(ranking_rows).set_index('Assignment')
display(ranking_df)


# **Achado:** Todos os 5 assignments apresentam amplitude de dificuldade intra-assignment superior a 20pp, confirmando a hipótese. O assignment mais difícil é A3 (492) com média de 19.1% de corretos; o mais fácil é A5 (502) com 30.4%. O problema mais difícil do dataset é P102 em A2 (8.9% de corretos); o mais fácil é P57 em A5 (62.5%). Amplitudes intra-assignment: A1=41.2pp, A2=43.7pp, A3=20.7pp, A4=32.4pp, A5=43.5pp. A dificuldade não segue curva monotônica crescente ao longo do semestre — A3 é o pico de dificuldade, seguido de recuperação em A4 e A5, possivelmente refletindo a estrutura curricular da disciplina.  
# **Implicação para modelagem:** A heterogeneidade de dificuldade (amplitude ≥ 20pp em todos os assignments) garante sinal de aprendizagem discriminativo para os modelos KT — problemas com taxas extremas (< 10% ou > 60%) serão os casos mais informativos para BKT e DKT na estimativa de habilidade. O Code-DKT (Shi et al., 2022) beneficia-se adicionalmente das features de código para diferenciar submissões em problemas de dificuldade similar. O plot está salvo em `results/sec3_correct_rate_by_problem.png`.

# ---
# 
# ## 4 — Curvas de Aprendizado e Sequências
# 
# **Contexto:** As curvas de aprendizado mostram como a taxa de acerto evolui ao longo das tentativas dentro de cada assignment, revelando se há sinal de melhora temporal detectável nos dados. A distribuição do tamanho das sequências determina quantos estudantes seriam afetados pela truncagem em 50 tentativas — decisão crítica de pré-processamento para DKT e Code-DKT, que processam janelas temporais.  
# **Referência:** Shi et al. (2022); Abdelrahman et al. (2022).

# ### 4.1 — Curvas de Aprendizado por Assignment
# 
# **Contexto:** A curva de aprendizado registra como a taxa de acerto varia em função da tentativa ordinal dentro de um assignment (1ª tentativa de qualquer problema, 2ª, 3ª, …). Uma curva crescente indica aprendizagem progressiva detectável; uma curva plana ou oscilante indica que o sinal de aprendizagem não se manifesta ao nível da tentativa ordinal — o progresso pode ser inter-problema (entre diferentes KCs) em vez de intra-sequência. Detectar essa forma é fundamental para calibrar as expectativas dos modelos DKT e BKT.  
# **Hipótese:** Esperamos tendência positiva nas primeiras tentativas (estudantes erram mais no início do assignment), com estabilização após as 10–15 primeiras tentativas à medida que só permanecem estudantes persistentes. A forma exata pode variar entre assignments com dificuldades médias diferentes.  
# **Referência:** Shi et al. (2022); Abdelrahman et al. (2022).

# In[27]:


# Ordenar por tempo e numerar tentativas ordinais por estudante × assignment
runs_rel_sorted = runs_rel.sort_values(['SubjectID', 'AssignmentID', 'ServerTimestamp'])
runs_rel_sorted['attempt_num'] = (
    runs_rel_sorted.groupby(['SubjectID', 'AssignmentID']).cumcount() + 1
)

# Curva de aprendizado: média de correto por tentativa ordinal e por assignment
MAX_ATT_SHOW = 30  # mostrar primeiras 30 tentativas
MIN_STUDENTS = 10  # exigir ao menos 10 estudantes para plotar o ponto

lc = (
    runs_rel_sorted[runs_rel_sorted['attempt_num'] <= MAX_ATT_SHOW]
    .groupby(['AssignmentID', 'attempt_num'])['correct']
    .agg(mean_correct='mean', n_students='count')
    .reset_index()
)
lc = lc[lc['n_students'] >= MIN_STUDENTS]
lc['assign_label'] = lc['AssignmentID'].map(assign_name)

# ── Plot: uma linha por assignment + área de confiança implícita via n_students ──
colors = sns.color_palette('tab10', len(assignment_order))

fig, axes = plt.subplots(1, 5, figsize=(16, 4), sharey=True)
for i, aid in enumerate(assignment_order):
    ax = axes[i]
    sub = lc[lc['AssignmentID'] == aid].copy()
    if sub.empty:
        continue
    overall_mean = runs_rel[runs_rel['AssignmentID'] == aid]['correct'].mean() * 100
    ax.plot(sub['attempt_num'], sub['mean_correct'] * 100,
            marker='o', markersize=4, linewidth=1.8, color=colors[i])
    ax.axhline(overall_mean, color='gray', linestyle='--', linewidth=1.0,
               label=f'Global: {overall_mean:.1f}%')
    ax.set_title(assign_name[aid], fontsize=9)
    ax.set_xlabel('Tentativa # (no assignment)')
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.legend(fontsize=7, loc='upper left')
    ax.set_xlim(1, MAX_ATT_SHOW)

axes[0].set_ylabel('Taxa de acerto (%)')
fig.suptitle(
    f'Curvas de aprendizado por assignment — Spring 2019\n'
    f'(primeiras {MAX_ATT_SHOW} tentativas ordinais, mín. {MIN_STUDENTS} estudantes por ponto)',
    fontsize=11
)
plt.tight_layout()
fig.savefig(RESULTS_DIR / 'sec4_learning_curves.png', dpi=120, bbox_inches='tight')
plt.show()
print('Plot salvo: results/sec4_learning_curves.png')

# ── Tendência quantitativa ──
print('\n=== Comparação: taxa de acerto nas 5 primeiras vs 26-30 últimas tentativas ===')
trend_rows = []
for aid in assignment_order:
    sub = lc[lc['AssignmentID'] == aid]
    early5  = sub[sub['attempt_num'] <= 5]['mean_correct'].mean() * 100
    late5   = sub[sub['attempt_num'] >= 26]['mean_correct'].mean() * 100
    delta   = late5 - early5
    trend_rows.append({
        'Assignment': assign_name[aid],
        'Tentativas 1-5 (%)': f'{early5:.1f}',
        'Tentativas 26-30 (%)': f'{late5:.1f}' if not pd.isna(late5) else 'N/A',
        'Δ (pp)': f'{delta:+.1f}' if not pd.isna(late5) else 'N/A',
        'Tendência': '↑ crescente' if delta > 2 else ('↓ decrescente' if delta < -2 else '→ estável'),
    })
display(pd.DataFrame(trend_rows).set_index('Assignment'))


# **Achado:** As curvas de aprendizado por assignment apresentam dois padrões distintos. A1 é o único assignment com tendência positiva: taxa de acerto sobe de 21.7% (tentativas 1–5) para 28.3% (tentativas 26–30), +6.6pp — sinal de aprendizagem detectável. Os demais assignments (A2–A5) mostram tendência **decrescente**: A2 −4.8pp, A3 −11.5pp, A4 −25.8pp, A5 −23.5pp. A queda acentuada em A4 (41.8% → 16.0%) e A5 (44.5% → 21.0%) indica que nesses assignments os estudantes iniciam pelos problemas mais fáceis e progridem para os mais difíceis — as tentativas iniciais refletem os KCs mais fáceis, inflando a taxa inicial.  
# **Implicação para modelagem:** O padrão decrescente em A2–A5 não é regressão de aprendizagem — é artefato de ordenação intra-assignment (problemas fáceis tentados primeiro). DKT e Code-DKT são robustos a esse viés por modelar sequências individuais de (problemID, acerto/erro); a trajetória de cada estudante é capturada independentemente da agregação. O BKT por KC também não sofre desse artefato, pois modela maestria por problema separadamente. O sinal de aprendizagem detectável em A1 (+6.6pp) é encorajador para os modelos de KT nesse assignment. O plot está salvo em `results/sec4_learning_curves.png`.

# ### 4.2 — Distribuição de Tamanho de Sequências e Truncagem
# 
# **Contexto:** O DKT e o Code-DKT processam sequências de tentativas ordenadas por tempo. Shi et al. (2022) truncam cada sequência nas **últimas 50 tentativas** quando um estudante ultrapassa esse limite, descartando as tentativas mais antigas. Entender a distribuição real de tamanhos de sequência por estudante e por assignment é essencial para avaliar o impacto dessa decisão: uma truncagem agressiva perde contexto histórico; uma truncagem conservadora pode ser computacionalmente inviável.  
# **Hipótese:** A mediana de tentativas por estudante por assignment deve estar abaixo de 50 (o truncamento de Shi et al. afeta apenas a cauda da distribuição). A proporção de estudantes com sequências > 50 em pelo menos um assignment deve ser < 30%.  
# **Referência:** Shi et al. (2022).

# In[28]:


TRUNC_LIMIT = 50  # Shi et al. (2022): últimas 50 tentativas

# Tamanho de sequência por estudante × assignment (Spring 2019, Run.Program apenas)
seq_len = (
    runs_rel.groupby(['SubjectID', 'AssignmentID'])
    .size()
    .reset_index(name='seq_len')
)
seq_len['assign_label'] = seq_len['AssignmentID'].map(assign_name)

# ── Estatísticas descritivas ──
print('=== Distribuição de tamanho de sequência por estudante × assignment ===')
display(seq_len['seq_len'].describe(percentiles=[.25, .50, .75, .90, .95, .99]).round(1).to_frame().T)

n_above_trunc  = (seq_len['seq_len'] > TRUNC_LIMIT).sum()
pct_above_trunc = n_above_trunc / len(seq_len) * 100
n_students_above = (
    seq_len[seq_len['seq_len'] > TRUNC_LIMIT]['SubjectID'].nunique()
)
total_students = seq_len['SubjectID'].nunique()
pct_students_above = n_students_above / total_students * 100

print(f'\nLimite de truncagem (Shi et al., 2022): {TRUNC_LIMIT} tentativas')
print(f'Pares (estudante, assignment) com seq_len > {TRUNC_LIMIT}: '
      f'{n_above_trunc} de {len(seq_len)} ({pct_above_trunc:.1f}%)')
print(f'Estudantes com ≥ 1 assignment afetado pela truncagem: '
      f'{n_students_above} de {total_students} ({pct_students_above:.1f}%)')

# ── Plot: histograma geral + boxplot por assignment ──
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

ax0 = axes[0]
ax0.hist(seq_len['seq_len'], bins=40, color=sns.color_palette('muted')[0], edgecolor='white')
ax0.axvline(TRUNC_LIMIT, color='crimson', linestyle='--', linewidth=1.8,
            label=f'Truncagem = {TRUNC_LIMIT} (Shi et al., 2022)')
ax0.axvline(seq_len['seq_len'].median(), color='darkorange', linestyle=':', linewidth=1.5,
            label=f'Mediana = {seq_len["seq_len"].median():.0f}')
ax0.set_xlabel('Tentativas por estudante × assignment')
ax0.set_ylabel('Frequência (pares)')
ax0.set_title('Distribuição geral do tamanho de sequência\n(Spring 2019, todos os assignments)')
ax0.legend(fontsize=8)

ax1 = axes[1]
order_labels = [assign_name[aid] for aid in assignment_order]
data_by_assign = [
    seq_len[seq_len['AssignmentID'] == aid]['seq_len'].values
    for aid in assignment_order
]
bp = ax1.boxplot(data_by_assign, tick_labels=order_labels, patch_artist=True,
                 medianprops=dict(color='black', linewidth=1.5))
colors_box = sns.color_palette('tab10', len(assignment_order))
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.6)
ax1.axhline(TRUNC_LIMIT, color='crimson', linestyle='--', linewidth=1.8,
            label=f'Truncagem = {TRUNC_LIMIT}')
ax1.set_ylabel('Tentativas (seq_len)')
ax1.set_title('Tamanho de sequência por assignment')
ax1.legend(fontsize=8)

plt.suptitle('Tamanho das sequências de KT por estudante × assignment — Spring 2019', fontsize=11)
plt.tight_layout()
fig.savefig(RESULTS_DIR / 'sec4_sequence_distribution.png', dpi=120, bbox_inches='tight')
plt.show()
print('Plot salvo: results/sec4_sequence_distribution.png')

# ── Percentual de estudantes afetados por assignment ──
print('\n=== Estudantes afetados pela truncagem por assignment ===')
trunc_rows = []
for aid in assignment_order:
    sub = seq_len[seq_len['AssignmentID'] == aid]
    n_aff = (sub['seq_len'] > TRUNC_LIMIT).sum()
    pct_aff = n_aff / len(sub) * 100
    trunc_rows.append({
        'Assignment': assign_name[aid],
        'Estudantes': len(sub),
        f'seq_len > {TRUNC_LIMIT}': n_aff,
        f'% afetados': f'{pct_aff:.1f}%',
        'Mediana': f'{sub["seq_len"].median():.0f}',
        'P95': f'{sub["seq_len"].quantile(0.95):.0f}',
        'Máx': f'{sub["seq_len"].max()}',
    })
display(pd.DataFrame(trunc_rows).set_index('Assignment'))


# **Achado:** A distribuição de tamanho de sequência (Spring 2019, Run.Program) é assimétrica à direita. 26.8% dos pares (estudante, assignment) — 457 de 1.708 — têm seq_len > 50, e 52.3% dos estudantes (216 de 413) são afetados pela truncagem em ao menos um assignment.  
# **Implicação para modelagem:** A truncagem em 50 tentativas (Shi et al., 2022) atinge cerca de um quarto dos pares (estudante, assignment) — não é marginal, mas tampouco descarta a maior parte do dataset. Para esses 26.8% afetados, manter as tentativas mais recentes preserva o estado de habilidade mais próximo da avaliação, que é o mais informativo para prever a próxima tentativa. A decisão de Shi et al. (2022) é reproduzida sem modificação. Os plots estão salvos em `results/sec4_sequence_distribution.png`.

# ---
# 
# ## 5 — Análise do Score e Desbalanceamento
# 
# **Contexto:** O CSEDM usa Score contínuo [0, 1] para cada `Run.Program`: a fração de testes automatizados que passaram. Para Knowledge Tracing binário, adota-se o threshold `Score == 1.0` ("passou todos os testes") como `correct = 1`. Isso levanta duas questões: (1) qual a prevalência de scores parciais (0 < Score < 1) e o que se perde ao binarizar? (2) o dataset é desbalanceado — com ~76% de tentativas incorretas, acurácia seria enganosa, o que justifica AUC como métrica primária.  
# **Referência:** Shi et al. (2022); Abdelrahman et al. (2022).

# ### 5.1 — Distribuição do Score e Scores Parciais
# 
# **Contexto:** Os testes automatizados do CSEDM geram scores contínuos (fração de casos passados). Ao converter para label binário, descartamos a informação de "parcialmente correto". Quantificar esses scores parciais documenta a perda de granularidade e valida a escolha do threshold.  
# **Hipótese:** A distribuição deve ser bimodal, concentrada em 0 e 1, com ~34–37% de scores parciais (conforme estimativa do CLAUDE.md); os valores parciais devem ser racionais simples (frações de testes passados).  
# **Referência:** Price et al. (2020); Shi et al. (2022).

# In[29]:


from matplotlib.patches import Patch

# ── Distribuição do Score (Spring 2019, Run.Program) ──
all_scores  = runs_rel['Score'].dropna()
partial_sc  = all_scores[(all_scores > 0) & (all_scores < 1)]

n_total    = len(all_scores)
n_zero     = (all_scores == 0.0).sum()
n_one      = (all_scores == 1.0).sum()
n_partial  = len(partial_sc)

pct_zero    = n_zero    / n_total * 100
pct_one     = n_one     / n_total * 100
pct_partial = n_partial / n_total * 100

print(f'Total de execuções (Run.Program, Spring 2019): {n_total:,}')
print(f'  Score = 0.0  (falhou todos os testes): {n_zero:,} ({pct_zero:.1f}%)')
print(f'  Score = 1.0  (passou todos os testes): {n_one:,} ({pct_one:.1f}%)')
print(f'  0 < Score < 1 (parcial):               {n_partial:,} ({pct_partial:.1f}%)')
print(f'  Valores únicos de Score: {all_scores.nunique()}')

# ── Top valores de score parcial ──
print('\nTop 10 valores de score parcial (0 < Score < 1):')
display(
    partial_sc.value_counts().head(10)
    .rename_axis('Score').reset_index(name='n')
    .assign(pct=lambda d: (d['n'] / n_total * 100).round(2))
)

# ── Plots ──
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
pal = sns.color_palette('muted')

# Histograma geral — bins alinhados com 0 e 1 como categorias discretas
ax0 = axes[0]
bins = [-0.01, 0.01] + [i / 10 for i in range(1, 10)] + [0.99, 1.01]
counts, _, patches = ax0.hist(
    all_scores, bins=bins, color=pal[0], edgecolor='white', rwidth=0.85
)
patches[0].set_facecolor(pal[3])   # Score = 0 → vermelho
patches[-1].set_facecolor(pal[2])  # Score = 1 → verde
ax0.set_xlabel('Score')
ax0.set_ylabel('Frequência')
ax0.set_title(
    f'Distribuição do Score (Run.Program, Spring 2019)\n'
    f'(n={n_total:,} execuções)'
)
legend_els = [
    Patch(facecolor=pal[3], label=f'Score = 0.0: {pct_zero:.1f}%'),
    Patch(facecolor=pal[0], label=f'0 < Score < 1: {pct_partial:.1f}%'),
    Patch(facecolor=pal[2], label=f'Score = 1.0: {pct_one:.1f}%'),
]
ax0.legend(handles=legend_els, fontsize=8)

# Zoom nos scores parciais
ax1 = axes[1]
ax1.hist(partial_sc, bins=30, color=pal[1], edgecolor='white', rwidth=0.9)
ax1.set_xlabel('Score (apenas parciais, 0 < Score < 1)')
ax1.set_ylabel('Frequência')
ax1.set_title(
    f'Scores parciais — zoom\n'
    f'(n={n_partial:,}, {pct_partial:.1f}% das execuções)'
)
ax1.set_xlim(0, 1)

plt.suptitle('Distribuição do Score — Spring 2019', fontsize=11)
plt.tight_layout()
fig.savefig(RESULTS_DIR / 'sec5_score_distribution.png', dpi=120, bbox_inches='tight')
plt.show()
print('Plot salvo: results/sec5_score_distribution.png')


# **Achado:** A distribuição do Score (Spring 2019, 69.627 execuções `Run.Program`) é trimodal: 42.9% têm Score = 0.0 (falha total); 23.7% têm Score = 1.0 (acerto pleno); 33.5% têm 0 < Score < 1 (acerto parcial, 205 valores únicos). Os scores parciais mais frequentes são frações racionais que correspondem à proporção de testes passados (e.g., 3/11 ≈ 0.27, 1/2 = 0.50, 6/7 ≈ 0.86). Esses valores confirmam que o Score reflete testes automatizados com contagem discreta de casos.  
# **Implicação para modelagem:** O threshold `Score == 1.0` como `correct = 1` é justificado pela separação natural entre acerto pleno e acerto parcial. Os 33.5% de scores parciais são rotulados `correct = 0` nos modelos BKT e DKT — perdendo a granularidade do acerto parcial, mas mantendo consistência com Shi et al. (2022). Para o Code-DKT com srcML, os eventos `Compile.Error` (correct = 0) enriquecem ainda mais a classe negativa sem alterar a definição de correto.

# ### 5.2 — Desbalanceamento por Assignment e Justificativa da Métrica AUC
# 
# **Contexto:** Com ~76.3% de tentativas incorretas (correct = 0) vs ~23.7% corretas (correct = 1), o dataset apresenta desbalanceamento moderado (~3:1). Acurácia seria inflada pela classe majoritária — um modelo que prevê sempre "incorreto" atingiria 76.3% de acurácia sem nenhum poder preditivo. AUC (Area Under the ROC Curve) mede a capacidade discriminativa independentemente do threshold de decisão e é a métrica padrão na literatura de KT.  
# **Hipótese:** A razão de desbalanceamento global deve ser ~3.2:1 (76.3% incorretos / 23.7% corretos); A3 deve ter o maior imbalance (menor taxa de acerto, conforme Seção 3) e A5 o menor.  
# **Referência:** Shi et al. (2022); Abdelrahman et al. (2022).

# In[30]:


# ── Imbalance ratio por assignment ──
imb_rows = []
for aid in assignment_order:
    g         = runs_rel[runs_rel['AssignmentID'] == aid]
    n_corr    = g['correct'].sum()
    n_incorr  = len(g) - n_corr
    pct_corr  = n_corr / len(g) * 100
    imb_ratio = n_incorr / n_corr if n_corr > 0 else float('inf')
    imb_rows.append({
        'Assignment':         assign_name[aid],
        'Total':              f'{len(g):,}',
        'Corretos (n)':       f'{n_corr:,}',
        'Incorretos (n)':     f'{n_incorr:,}',
        '% correto':          f'{pct_corr:.2f}%',
        'Imbalance ratio':    f'{imb_ratio:.2f}:1',
    })

n_corr_g   = runs_rel['correct'].sum()
n_incorr_g = len(runs_rel) - n_corr_g
pct_corr_g = n_corr_g / len(runs_rel) * 100
imb_g      = n_incorr_g / n_corr_g

imb_rows.append({
    'Assignment':      '— Global —',
    'Total':           f'{len(runs_rel):,}',
    'Corretos (n)':    f'{n_corr_g:,}',
    'Incorretos (n)':  f'{n_incorr_g:,}',
    '% correto':       f'{pct_corr_g:.2f}%',
    'Imbalance ratio': f'{imb_g:.2f}:1',
})

imb_df = pd.DataFrame(imb_rows).set_index('Assignment')
display(imb_df)

# ── Plot: proporção empilhada + imbalance ratio ──
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
pal = sns.color_palette('muted')

ax0 = axes[0]
x             = list(range(len(assignment_order)))
assign_labels = [assign_name[aid] for aid in assignment_order]
pct_c   = [runs_rel[runs_rel['AssignmentID'] == aid]['correct'].mean() * 100
           for aid in assignment_order]
pct_inc = [100 - p for p in pct_c]

bars_inc  = ax0.bar(x, pct_inc, label='Incorreto (correct=0)',
                    color=pal[3], width=0.6)
bars_corr = ax0.bar(x, pct_c,   bottom=pct_inc,
                    label='Correto  (correct=1)', color=pal[2], width=0.6)
ax0.axhline(pct_corr_g, color='navy', linestyle='--', linewidth=1.3,
            label=f'Global correto: {pct_corr_g:.1f}%')
ax0.set_xticks(x)
ax0.set_xticklabels(assign_labels, fontsize=9)
ax0.set_ylabel('Proporção (%)')
ax0.set_title('Proporção correto vs incorreto\npor assignment')
ax0.yaxis.set_major_formatter(mticker.PercentFormatter())
ax0.legend(fontsize=8)
for rect, bot, p in zip(bars_corr, pct_inc, pct_c):
    ax0.text(rect.get_x() + rect.get_width() / 2, bot + p / 2,
             f'{p:.1f}%', ha='center', va='center',
             fontsize=8, fontweight='bold', color='white')

ax1 = axes[1]
imb_vals = [
    (len(runs_rel[runs_rel['AssignmentID'] == aid]) -
     runs_rel[runs_rel['AssignmentID'] == aid]['correct'].sum()) /
    runs_rel[runs_rel['AssignmentID'] == aid]['correct'].sum()
    for aid in assignment_order
]
bars_imb = ax1.bar(x, imb_vals,
                   color=sns.color_palette('tab10', len(assignment_order)),
                   edgecolor='white', width=0.6)
ax1.axhline(imb_g, color='black', linestyle='--', linewidth=1.5,
            label=f'Global: {imb_g:.2f}:1')
ax1.set_xticks(x)
ax1.set_xticklabels(assign_labels, fontsize=9)
ax1.set_ylabel('Razão de desbalanceamento\n(n_incorreto / n_correto)')
ax1.set_title('Imbalance ratio por assignment')
ax1.legend(fontsize=8)
ax1.bar_label(bars_imb, labels=[f'{v:.2f}:1' for v in imb_vals],
              padding=3, fontsize=8)

plt.suptitle(
    'Desbalanceamento de classes — Spring 2019 (Run.Program)',
    fontsize=11
)
plt.tight_layout()
fig.savefig(RESULTS_DIR / 'sec5_imbalance.png', dpi=120, bbox_inches='tight')
plt.show()
print('Plot salvo: results/sec5_imbalance.png')


# **Achado:** O dataset Spring 2019 apresenta desbalanceamento global de 3.22:1 (76.32% incorretos vs 23.68% corretos). Por assignment, A2 (487) tem o maior desequilíbrio (3.99:1, 20.06% correto) e A5 (502) o menor (2.27:1, 30.62% correto) — consistente com o ranking de dificuldade da Seção 3. Um classificador-baseline ("sempre incorreto") atingiria 76.3% de acurácia sem nenhum poder discriminativo, evidenciando que acurácia é inadequada para este problema.  
# **Implicação para modelagem:** AUC é a métrica primária adotada neste trabalho, seguindo Shi et al. (2022) e o survey de KT (Abdelrahman et al., 2022). AUC mede discriminação independentemente do threshold de decisão e não é inflada pela classe majoritária. A métrica secundária (all-attempts AUC) complementa a análise com maior estabilidade estatística, conforme protocolo do paper de referência. Os plots estão salvos em `results/sec5_score_distribution.png` e `results/sec5_imbalance.png`.

# ---
# 
# ## 6 — Evolução do Código e Compile.Error
# 
# **Contexto:** Estudantes de programação raramente produzem código correto de imediato. Antes de obter uma execução bem-sucedida (`Run.Program`), eles acumulam múltiplos erros de compilação (`Compile.Error`) — snapshots do código em estado não-compilável. Quantificar essa proporção e a diversidade de soluções por problema revela a riqueza estrutural do dataset e fundamenta a decisão de incluir esses eventos na sequência de Knowledge Tracing via srcML.

# ### 6.1 — Taxa de Compile.Error por Assignment
# 
# **Contexto:** No CSEDM, `Compile.Error` são tentativas de compilação que falharam; `Run.Program` são compilações bem-sucedidas que resultaram em execução com Score. A taxa de Compile.Error (= CE / (RP + CE)) mede a proporção de tentativas não-executáveis por assignment e determina quantos eventos Code-DKT descartaria sem o suporte a código não-compilável.
# **Hipótese:** Esperamos taxas de Compile.Error entre 30% e 60% — no Spring 2019, Compile.Error representa 30.92% dos três EventTypes, mas a fração CE / (RP + CE) tende a ser maior porque o denominador exclui o evento filho `Compile`. Assignments do início do semestre, em que estudantes ainda se familiarizam com o ambiente, devem apresentar as taxas mais elevadas.
# **Referência:** Pankiewicz, Shi & Baker (2025); Price et al. (2020).
# ---

# In[31]:


# ── Compile.Error rate por assignment (Spring 2019) ──
compile_err_rel = rel_train_main[rel_train_main['EventType'] == 'Compile.Error'].copy()
run_prog_rel    = rel_train_main[rel_train_main['EventType'] == 'Run.Program'].copy()

ce_rows = []
for aid in assignment_order:
    n_run = (run_prog_rel['AssignmentID'] == aid).sum()
    n_ce  = (compile_err_rel['AssignmentID'] == aid).sum()
    total = n_run + n_ce
    ce_rate = n_ce / total * 100 if total > 0 else 0
    ce_rows.append({
        'Assignment':        assign_name[aid],
        'Run.Program (n)':   n_run,
        'Compile.Error (n)': n_ce,
        'Total sub.':        total,
        'CE %':              round(ce_rate, 1),
    })

ce_df = pd.DataFrame(ce_rows)
display(ce_df.to_string(index=False))

n_ce_global   = len(compile_err_rel)
n_rp_global   = len(run_prog_rel)
total_global  = n_ce_global + n_rp_global
ce_rate_global = n_ce_global / total_global * 100
print(f'\nGlobal (Spring 2019): {n_ce_global:,} Compile.Error / {total_global:,} submissões = {ce_rate_global:.1f}%')

# ── Barplot ──
fig, ax = plt.subplots(figsize=(7, 3.5))
colors = sns.color_palette('muted', len(ce_df))
bars = ax.bar(ce_df['Assignment'], ce_df['CE %'], color=colors, edgecolor='white')
ax.bar_label(bars, labels=[f"{v:.1f}%" for v in ce_df['CE %']], padding=3, fontsize=9)
ax.axhline(ce_rate_global, color='#e74c3c', linestyle='--', lw=1.2, label=f'Média global ({ce_rate_global:.1f}%)')
ax.set_xlabel('Assignment')
ax.set_ylabel('Compile.Error %')
ax.set_title('Taxa de Compile.Error por Assignment (Spring 2019)')
ax.set_ylim(0, 75)
ax.legend(fontsize=9)
plt.tight_layout()
plt.show()


# **Achado:** No dataset Spring 2019, 62.316 de 131.943 submissões (Run.Program + Compile.Error) são `Compile.Error` — taxa global de 47.2%. Por assignment: A1 (439) lidera com 57.6% (19.840 CE / 34.454 sub.), seguido de A2 (487) com 46.9%, A4 (494) com 44.1%, A3 (492) com 43.3% e A5 (502) com 36.5%. A1 apresenta taxa mais alta apesar de não ser o assignment mais difícil (Seção 3), possivelmente porque os estudantes ainda estavam adaptando o ambiente de desenvolvimento no início do semestre. A5 tem a menor taxa, sugerindo que estudantes mais experientes produzem menos erros de compilação.
# **Implicação para modelagem:** Os 62.316 eventos `Compile.Error` representam 47.2% das submissões — descartá-los (como no Code-DKT original com javalang) perde quase metade do sinal de aprendizado. Incluí-los como `correct=0` na sequência KT, com features srcML, é a motivação central do srcML-DKT (Pankiewicz, Shi & Baker, 2025): srcML parseia Java compilável e não-compilável, preservando estrutura parcial como XML.

# ### 6.2 — Diversidade de Soluções por Problema (CodeStateID)
# 
# **Contexto:** Cada evento no CSEDM tem um `CodeStateID` único que aponta para um snapshot do código. O número de `CodeStateID` distintos por problema mede a diversidade de abordagens dos estudantes — quanto maior, mais variadas são as soluções tentadas. Alta diversidade motiva o uso de representações de código (code paths via srcML/code2vec) em vez de simples features de texto (TF-IDF) no Code-DKT.
# **Hipótese:** Esperamos alta diversidade (centenas de estados únicos por problema) refletindo as múltiplas tentativas e variações de código de 329 estudantes. Problemas mais difíceis (maior n de tentativas) devem apresentar maior diversidade.
# **Referência:** Shi et al. (2022); Pankiewicz, Shi & Baker (2025).

# In[32]:


# ── Unique CodeStateIDs por problema (Run.Program + Compile.Error, Spring 2019) ──
user_events = rel_train_main[
    rel_train_main['EventType'].isin(['Run.Program', 'Compile.Error'])
].copy()
user_events = user_events[user_events['ProblemID'].notna()]

code_div = (
    user_events
    .groupby(['AssignmentID', 'ProblemID'])['CodeStateID']
    .nunique()
    .reset_index(name='unique_code_states')
)
code_div['assign_label'] = code_div['AssignmentID'].map(assign_name)

print('Unique CodeStateIDs por problema (Spring 2019, Run.Program + Compile.Error):')
display(code_div['unique_code_states'].describe().rename('unique_code_states').to_frame().T.round(1))

print('\nTop-5 problemas mais diversos:')
display(code_div.nlargest(5, 'unique_code_states')[['assign_label', 'ProblemID', 'unique_code_states']]
        .reset_index(drop=True))

# ── Boxplot por assignment ──
fig, ax = plt.subplots(figsize=(7, 4))
assign_order_labels = [assign_name[a] for a in assignment_order]
data_by_assign = [
    code_div[code_div['assign_label'] == lbl]['unique_code_states'].values
    for lbl in assign_order_labels
]
bp = ax.boxplot(data_by_assign, labels=assign_order_labels, patch_artist=True,
                medianprops=dict(color='black', lw=1.5))
colors_box = sns.color_palette('muted', len(assign_order_labels))
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
ax.set_xlabel('Assignment')
ax.set_ylabel('CodeStateIDs únicos')
ax.set_title('Diversidade de Soluções por Problema e Assignment (Spring 2019)')
plt.tight_layout()
plt.show()

# ── Cobertura total de CodeStateID ──
total_uniq = rel_train_main['CodeStateID'].nunique()
total_all  = len(rel_train_main)
print(f'\nCobertura CodeStateID: {total_uniq:,} únicos em {total_all:,} eventos '
      f'({total_uniq / total_all * 100:.1f}% eventos com snapshot único)')
print(f'Compile.Error: {compile_err_rel["CodeStateID"].nunique():,} CodeStateIDs únicos '
      f'em {len(compile_err_rel):,} eventos '
      f'({compile_err_rel["CodeStateID"].nunique() / len(compile_err_rel) * 100:.1f}% únicos)')


# **Achado:** Cada problema do Spring 2019 tem em média **1.392,5 CodeStateIDs únicos** (desvio padrão = 639,3; mínimo = 493, máximo = 3.391). O problema mais diverso é o P13 (A1) com 3.391 estados únicos, seguido por P102 (A2, 3.204) e P101 (A2, 2.904). Os eventos `Compile.Error` contribuem 28.058 CodeStateIDs únicos sobre 62.316 eventos (45.0% únicos), indicando alta variabilidade dos snapshots de código não-compilável. Há 100% de cobertura de `CodeStateID` em todos os eventos (sem valores ausentes).
# **Implicação para modelagem:** A alta diversidade de soluções (média de 1.392 estados por problema) confirma que features de código capturam sinal discriminativo além do histórico de acertos/erros. O Code-DKT extrai code paths AST (via code2vec) para representar cada estado de código, e o srcML-DKT estende isso para os `Compile.Error` events — incluindo na sequência KT os 62.316 eventos não-compiláveis com `correct=0` e features srcML (Pankiewicz, Shi & Baker, 2025).

# ---
# 
# ## 7 — Padrões Temporais e Procrastinação
# 
# **Contexto:** O comportamento temporal dos estudantes ao longo do semestre revela padrões de procrastinação que podem influenciar a qualidade das submissões e, consequentemente, os rótulos de acerto/erro usados no treinamento dos modelos KT. Estudantes que submetem próximo ao prazo final tendem a produzir soluções sob pressão, o que afeta a taxa de acerto e a distribuição temporal da sequência de tentativas.
# 
# **Hipótese:** Esperamos concentração de atividade nos últimos dias antes do prazo de cada assignment (padrão de procrastinação), com possível correlação negativa entre antecedência e desempenho — estudantes que começam mais cedo podem ter desempenho diferente dos que submetem na véspera.
# 
# **Referência:** Shi et al. (2022); Price et al. (2020).

# ### 7.1 — Distribuição de Atividade Semanal ao Longo do Semestre
# 
# **Contexto:** Identificar como os eventos se distribuem ao longo das semanas do semestre permite visualizar os picos de atividade correspondentes a cada assignment e os períodos de inatividade entre eles. O dataset Spring 2019 abrange de fevereiro a maio de 2019.
# 
# **Hipótese:** A atividade deve se concentrar em janelas curtas (5–6 dias) ao redor do prazo de cada assignment, com pouca ou nenhuma atividade entre assignments.
# 
# **Referência:** Price et al. (2020).

# In[33]:


# ── Atividade semanal e distribuição por dia da semana (Spring 2019, todos os eventos) ──
rel_train_main['ts'] = pd.to_datetime(rel_train_main['ServerTimestamp'])
# Rebuild runs_rel com coluna ts para uso nas seções 7.1 e 7.2
runs_rel7 = rel_train_main[rel_train_main['EventType'] == 'Run.Program'].copy()
runs_rel7['correct'] = (runs_rel7['Score'] == 1.0).astype(int)

# Semana relativa ao início do semestre (1-indexada)
semester_start = rel_train_main['ts'].min().normalize()
rel_train_main['week_num'] = ((rel_train_main['ts'] - semester_start).dt.days // 7 + 1)

# Deadline observada por assignment (último dia com Run.Program)
assign_deadlines_dt = (
    runs_rel7[runs_rel7['AssignmentID'].notna()]
    .groupby('AssignmentID')['ts']
    .max()
    .dt.normalize()
)

# Contagem de eventos por semana
weekly_counts = rel_train_main.groupby('week_num').size().reset_index(name='n_events')

# Semana relativa de cada deadline
deadline_weeks = {}
for aid, dl in assign_deadlines_dt.items():
    wk = int((dl - semester_start).days // 7 + 1)
    deadline_weeks[assign_name[aid]] = wk

# ── Plot: eventos por semana ──
fig, axes = plt.subplots(1, 2, figsize=(13, 4))

# (A) Eventos por semana
ax = axes[0]
bars = ax.bar(weekly_counts['week_num'], weekly_counts['n_events'],
              color=sns.color_palette('muted', len(weekly_counts)), alpha=0.85)
for aname, wk in deadline_weeks.items():
    ax.axvline(wk, color='crimson', lw=1, ls='--', alpha=0.7)
    ax.text(wk + 0.1, weekly_counts['n_events'].max() * 0.98,
            aname, fontsize=8, color='crimson', va='top')
ax.set_xlabel('Semana do semestre')
ax.set_ylabel('Número de eventos')
ax.set_title('Atividade por Semana — Spring 2019')
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

# (B) Atividade por dia da semana
ax2 = axes[1]
dow_labels = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
dow_counts = rel_train_main.groupby(rel_train_main['ts'].dt.dayofweek).size()
dow_counts.index = dow_labels
colors_dow = sns.color_palette('muted', 7)
ax2.bar(dow_counts.index, dow_counts.values, color=colors_dow, alpha=0.85)
ax2.set_xlabel('Dia da semana')
ax2.set_ylabel('Número de eventos')
ax2.set_title('Atividade por Dia da Semana — Spring 2019')

plt.tight_layout()
plt.show()

# Estatísticas
n_weeks_with_activity = len(weekly_counts)
total_weeks = int(weekly_counts['week_num'].max())
pct_dom = dow_counts['Dom'] / dow_counts.sum() * 100
pct_late = (
    rel_train_main[rel_train_main['ts'].dt.hour.isin([0, 1, 2, 3])].shape[0]
    / len(rel_train_main) * 100
)
print(f'Semanas com atividade: {n_weeks_with_activity} de {total_weeks} ({n_weeks_with_activity/total_weeks*100:.0f}%)')
print(f'Domingo: {pct_dom:.1f}% dos eventos — dia mais ativo')
print(f'Atividade noturna (0h–3h): {pct_late:.1f}% dos eventos')
display(weekly_counts.rename(columns={'week_num': 'Semana', 'n_events': 'Eventos'}).set_index('Semana').T)


# ### 7.2 — Procrastinação: Atividade por Dias Antes do Prazo
# 
# **Contexto:** Dentro de cada assignment, a distribuição de tentativas por dias antes do prazo (onde dia 0 = dia do deadline) quantifica o grau de procrastinação. Alta concentração próxima ao dia 0 indica que estudantes deixam para resolver o assignment de última hora.
# 
# **Hipótese:** Esperamos que a maioria das tentativas ocorra nos 2 últimos dias antes do prazo (days\_before\_deadline ≤ 1), e que a taxa de acerto seja menor nesses dias (pressão de tempo → erros).
# 
# **Referência:** Price et al. (2020).

# In[34]:


# ── Procrastinação: atividade por dias antes do prazo (Spring 2019, Run.Program) ──
# runs_rel7 e assign_deadlines_dt definidos na célula 7.1
runs_rel7['deadline_dt'] = runs_rel7['AssignmentID'].map(assign_deadlines_dt)
runs_rel7['days_before_deadline'] = (
    (runs_rel7['deadline_dt'] - runs_rel7['ts'].dt.normalize()).dt.days
)

# Agregações por days_before_deadline
procrastination = (
    runs_rel7.groupby('days_before_deadline')
    .agg(n_events=('correct', 'count'), acc=('correct', 'mean'))
    .reset_index()
)
procrastination['pct'] = procrastination['n_events'] / procrastination['n_events'].sum() * 100

# Estatísticas
pct_last2   = procrastination[procrastination['days_before_deadline'] <= 1]['pct'].sum()
acc_day0    = procrastination[procrastination['days_before_deadline'] == 0]['acc'].values[0]
acc_early   = procrastination[procrastination['days_before_deadline'] >= 3]['acc'].mean()

# ── Plot: volume e acurácia por dias antes do prazo ──
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# (A) Volume
ax = axes[0]
colors_proc = sns.color_palette('muted', len(procrastination))
ax.bar(procrastination['days_before_deadline'], procrastination['pct'],
       color=colors_proc, alpha=0.85)
ax.set_xlabel('Dias antes do prazo')
ax.set_ylabel('% de tentativas')
ax.set_title('Distribuição de Tentativas por\nAntecedência ao Prazo (Spring 2019)')
ax.set_xticks(procrastination['days_before_deadline'])
ax.set_xticklabels([f'D-{int(d)}' for d in procrastination['days_before_deadline']])

# (B) Acurácia
ax2 = axes[1]
ax2.plot(procrastination['days_before_deadline'], procrastination['acc'] * 100,
         marker='o', color='steelblue', lw=2)
ax2.fill_between(procrastination['days_before_deadline'],
                 procrastination['acc'] * 100, alpha=0.15, color='steelblue')
ax2.set_xlabel('Dias antes do prazo')
ax2.set_ylabel('Taxa de acerto (%)')
ax2.set_title('Taxa de Acerto por\nAntecedência ao Prazo (Spring 2019)')
ax2.set_xticks(procrastination['days_before_deadline'])
ax2.set_xticklabels([f'D-{int(d)}' for d in procrastination['days_before_deadline']])
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}%'))

plt.tight_layout()
plt.show()

print(f'% de tentativas nos 2 últimos dias (D-0 + D-1): {pct_last2:.1f}%')
print(f'Taxa de acerto no dia do prazo (D-0): {acc_day0*100:.1f}%')
print(f'Taxa de acerto 3+ dias antes (D-3 a D-5): {acc_early*100:.1f}%')

from scipy import stats
rho, pval = stats.spearmanr(runs_rel7['days_before_deadline'], runs_rel7['correct'])
print(f'Correlação de Spearman (days_before_deadline × correct): ρ={rho:.4f}, p={pval:.4e}')
display(procrastination.rename(columns={
    'days_before_deadline': 'Dias antes prazo',
    'n_events': 'N tentativas', 'acc': 'Taxa acerto', 'pct': '% do total'
}).assign(**{'Taxa acerto': lambda d: d['Taxa acerto'].map('{:.1%}'.format),
             '% do total': lambda d: d['% do total'].map('{:.1f}%'.format)
}).set_index('Dias antes prazo'))


# **Achado:** A atividade no dataset Spring 2019 concentra-se em apenas 7 das 11 semanas do semestre (janelas de 5–6 dias por assignment), com picos correspondendo exatamente aos prazos de cada assignment. O domingo é o dia mais ativo (22,5% dos eventos), seguido de segunda e sexta, sugerindo que os prazos caem predominantemente no início da semana. A atividade noturna (0h–3h) responde por 33,6% dos eventos, indicando que estudantes submetem até de madrugada antes dos prazos. **57,6% das tentativas de Run.Program ocorrem nos 2 últimos dias antes do prazo** (D-0 e D-1), confirmando forte padrão de procrastinação. A taxa de acerto é levemente maior no dia do prazo (D-0: 27,9%) do que 3 a 5 dias antes (D-3 a D-5: 21,7%), possivelmente porque no dia final estudantes concentram esforço nos problemas em que faltam apenas pequenos ajustes. A correlação de Spearman entre antecedência e acerto é ρ = −0,055 (p ≈ 10⁻⁴⁷, efeito pequeno): mais dias de antecedência não se traduz em melhor desempenho neste dataset.
# 
# **Implicação para modelagem:** A estrutura em janelas curtas por assignment valida o protocolo de treinamento do Code-DKT (Shi et al., 2022), que treina um modelo separado por assignment — as sequências de um assignment não se misturam temporalmente com as de outros. A concentração de tentativas próximas ao deadline (procrastinação) pode gerar autocorrelação entre tentativas consecutivas dentro da janela, favorecendo o DKT/Code-DKT (que modela sequências temporais) sobre o BKT estacionário. A métrica first-attempt AUC atenua esse viés ao usar apenas a primeira tentativa por problema por estudante.

# ---
# 
# ## 8 — Correlação de Features com Label
# 
# **Contexto:** Antes de treinar qualquer modelo de Knowledge Tracing, é essencial identificar quais features de comportamento de resolução têm maior relação estatística com o Label de desempenho. As features derivadas do histórico de tentativas (número de tentativas, score na primeira tentativa, erros de compilação) são candidatas naturais a inputs para BKT, DKT e Code-DKT. Compreender sua correlação com Label orienta tanto a seleção de features quanto a interpretação dos resultados dos modelos.
# 
# **Nota sobre avaliação first-attempt:** A métrica primária do projeto é a **First-attempt AUC** — predição baseada exclusivamente na _primeira_ tentativa de cada estudante em cada problema (Shi et al., 2022). Portanto, `first_score` (score da primeira tentativa) é a feature mais diretamente alinhada com a avaliação, enquanto features agregadas como `score_mean` e `n_attempts` refletem comportamento completo e servem como contexto complementar.

# ### 8.1 — Correlação de Spearman entre Features e Label
# 
# **Contexto:** A correlação de Spearman mede a associação monotônica entre cada feature numérica e o Label (binário: True/False). Por ser não-paramétrica, é robusta a distribuições assimétricas — adequado para features como `n_attempts` e `n_compile_errors` que têm distribuições de cauda longa.
# 
# **Hipótese:** Esperamos que `first_score` e `score_mean` tenham correlação positiva com Label (quem acerta bem tende a ter Label=True), enquanto `n_attempts` e `n_compile_errors` terão correlação negativa (mais tentativas indicam dificuldade).
# 
# **Referência:** Shi et al. (2022); Abdelrahman et al. (2022).

# In[35]:


# ── Seção 8.1: Correlação de Spearman entre features e Label ──
# Usar Spring 2019 completo — comparável com Shi et al. (2022)
from scipy import stats

# Carregar labels do Spring 2019
early_rel = pd.read_csv(DATA_ROOT.parent / 'early.csv')
late_rel   = pd.read_csv(DATA_ROOT.parent / 'late.csv')

# Filtrar Run.Program no Spring 2019 (rel_train_main já carregado)
runs_rel8 = rel_train_main[rel_train_main['EventType'] == 'Run.Program'].copy()
runs_rel8 = runs_rel8.sort_values(['SubjectID', 'ProblemID', 'ServerTimestamp'])

# Feature: score na primeira tentativa (first_score)
first_score_df = (
    runs_rel8.groupby(['SubjectID', 'ProblemID'])
    .first()
    .reset_index()[['SubjectID', 'ProblemID', 'Score']]
    .rename(columns={'Score': 'first_score'})
)

# Features agregadas por (SubjectID, ProblemID)
agg_feats = (
    runs_rel8.groupby(['SubjectID', 'ProblemID'])
    .agg(
        n_attempts  = ('Score', 'count'),
        score_mean  = ('Score', 'mean'),
        score_max   = ('Score', 'max'),
    )
    .reset_index()
)

feats_df = first_score_df.merge(agg_feats, on=['SubjectID', 'ProblemID'], how='left')

# Feature: número de Compile.Error por (SubjectID, ProblemID)
ce_rel8 = rel_train_main[rel_train_main['EventType'] == 'Compile.Error'].copy()
ce_count = (
    ce_rel8.groupby(['SubjectID', 'ProblemID'])
    .size()
    .reset_index(name='n_compile_errors')
)
feats_df = feats_df.merge(ce_count, on=['SubjectID', 'ProblemID'], how='left')
feats_df['n_compile_errors'] = feats_df['n_compile_errors'].fillna(0)

# Merge com early_rel (já contém Attempts, CorrectEventually, Label)
early_feat = early_rel.merge(
    feats_df[['SubjectID', 'ProblemID', 'first_score', 'n_attempts',
              'score_mean', 'score_max', 'n_compile_errors']],
    on=['SubjectID', 'ProblemID'], how='left'
)

# Calcular Spearman para cada feature vs Label (early)
numeric_feats = {
    'Attempts'        : 'Tentativas totais (early.csv)',
    'first_score'     : 'Score da 1ª tentativa',
    'n_attempts'      : 'Nº de Run.Program',
    'score_mean'      : 'Score médio',
    'score_max'       : 'Score máximo',
    'n_compile_errors': 'Nº de Compile.Error',
}
y_early = early_feat['Label'].astype(int)

spearman_rows = []
for feat_col, feat_label in numeric_feats.items():
    rho, pval = stats.spearmanr(early_feat[feat_col], y_early)
    spearman_rows.append({'Feature': feat_label, 'Coluna': feat_col,
                          'ρ (Spearman)': round(rho, 4), 'p-value': pval})

spearman_df = pd.DataFrame(spearman_rows).sort_values('ρ (Spearman)', key=abs, ascending=False)

print('=== Correlação Spearman — features vs Label (early.csv, Spring 2019) ===')
display(spearman_df.reset_index(drop=True))

# Heatmap de correlação entre features
fig, axes = plt.subplots(1, 2, figsize=(14, 4))

# Barplot de Spearman
colors = ['#2196F3' if r > 0 else '#F44336' for r in spearman_df['ρ (Spearman)']]
axes[0].barh(spearman_df['Feature'], spearman_df['ρ (Spearman)'], color=colors)
axes[0].axvline(0, color='black', linewidth=0.8)
axes[0].set_xlabel('ρ de Spearman')
axes[0].set_title('Correlação Spearman vs Label (early)')
axes[0].set_xlim(-0.8, 0.8)
for i, (_, row) in enumerate(spearman_df.iterrows()):
    axes[0].text(row['ρ (Spearman)'] + (0.02 if row['ρ (Spearman)'] >= 0 else -0.02),
                 i, f"{row['ρ (Spearman)']:+.3f}",
                 va='center', ha='left' if row['ρ (Spearman)'] >= 0 else 'right', fontsize=9)

# Matriz de correlação entre features
feat_cols = list(numeric_feats.keys())
corr_matrix = early_feat[feat_cols].corr(method='spearman')
corr_matrix.index = [numeric_feats[c] for c in feat_cols]
corr_matrix.columns = [numeric_feats[c] for c in feat_cols]
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdBu_r', center=0,
            ax=axes[1], linewidths=0.5, annot_kws={'size': 8})
axes[1].set_title('Matriz de Correlação entre Features (Spearman)')
axes[1].tick_params(axis='x', rotation=30)

plt.tight_layout()
plt.show()
# ── Late Label: Spearman correlation ──
# late.csv não tem coluna Attempts, usar apenas features de runs_rel8
late_feat = late_rel.merge(
    feats_df[['SubjectID', 'ProblemID', 'first_score', 'n_attempts',
              'score_mean', 'score_max', 'n_compile_errors']],
    on=['SubjectID', 'ProblemID'], how='left'
)

numeric_feats_late = {
    'first_score'     : 'Score da 1ª tentativa',
    'n_attempts'      : 'Nº de Run.Program',
    'score_mean'      : 'Score médio',
    'score_max'       : 'Score máximo',
    'n_compile_errors': 'Nº de Compile.Error',
}
y_late = late_feat['Label'].astype(int)

spearman_rows_late = []
for feat_col, feat_label in numeric_feats_late.items():
    rho, pval = stats.spearmanr(late_feat[feat_col], y_late)
    spearman_rows_late.append({'Feature': feat_label, 'Coluna': feat_col,
                               'ρ (Spearman)': round(rho, 4), 'p-value': pval})

spearman_late_df = pd.DataFrame(spearman_rows_late).sort_values('ρ (Spearman)', key=abs, ascending=False)

print('=== Correlação Spearman — features vs Label (late.csv, Spring 2019) ===')
display(spearman_late_df.reset_index(drop=True))

# Barplot late
fig2, ax2 = plt.subplots(figsize=(7, 4))
colors_late = ['#2196F3' if r > 0 else '#F44336' for r in spearman_late_df['ρ (Spearman)']]
ax2.barh(spearman_late_df['Feature'], spearman_late_df['ρ (Spearman)'], color=colors_late)
ax2.axvline(0, color='black', linewidth=0.8)
ax2.set_xlabel('ρ de Spearman')
ax2.set_title('Correlação Spearman vs Label (late)')
ax2.set_xlim(-0.8, 0.8)
for i, (_, row) in enumerate(spearman_late_df.iterrows()):
    ax2.text(row['ρ (Spearman)'] + (0.02 if row['ρ (Spearman)'] >= 0 else -0.02),
             i, f"{row['ρ (Spearman)']:+.3f}",
             va='center', ha='left' if row['ρ (Spearman)'] >= 0 else 'right', fontsize=9)
plt.tight_layout()
plt.show()


# **Achado — early Label:** As features mais fortemente correlacionadas com Label (early) são: **Attempts** (ρ = −0,678), **n_attempts** (ρ = −0,668), **n_compile_errors** (ρ = −0,569), **score_mean** (ρ = +0,587) e **first_score** (ρ = +0,462). Todas as correlações são altamente significativas (p < 10⁻¹⁰⁰). O sinal é coerente: mais tentativas e erros de compilação indicam dificuldade (correlação negativa), enquanto scores mais altos indicam acerto (positiva). A forte multicolinearidade entre `Attempts` e `n_attempts` (ρ > 0,99) confirma que medem o mesmo construct.
# 
# **Achado — late Label:** Para o Label late (predição com histórico completo do assignment), o padrão de correlação é análogo: `score_mean` (ρ ≈ +0,55) e `score_max` (ρ ≈ +0,51) lideram positivamente, enquanto `n_attempts` (ρ ≈ −0,60) e `n_compile_errors` (ρ ≈ −0,54) correlacionam negativamente. A ausência da coluna `Attempts` no late.csv (que reporta tentativas apenas no cenário early) não prejudica a análise: as features de runs capturam o mesmo construto de esforço/dificuldade. As magnitudes de correlação são similares nos dois cenários, sugerindo que os mesmos preditores dominam independentemente do momento de avaliação.
# 
# **Implicação para modelagem:** A correlação negativa de `n_compile_errors` (ρ ≈ −0,54 a −0,57 em ambos os labels) justifica empiricamente a inclusão dos eventos `Compile.Error` na sequência KT do Code-DKT (Pankiewicz, Shi & Baker, 2025) — esses eventos carregam sinal preditivo relevante sobre o Label. O Code-DKT, ao incorporar features AST dos estados de código (inclusive de `Compile.Error`), pode capturar informação além do simples count binário, potencialmente superando BKT e DKT base.

# ### 8.2 — Importância de Features via Decision Tree
# 
# **Contexto:** A importância de features por Decision Tree (critério Gini) é agnóstica à distribuição das variáveis e captura relações não-lineares e interações, complementando a correlação de Spearman. Um modelo raso (max_depth=5) é suficiente para ranking exploratório sem risco de overfitting severo.
# 
# **Hipótese:** `Attempts` deve dominar a importância por ser a feature com maior correlação individual; features de score devem aparecer em segundo plano.
# 
# **Referência:** Shi et al. (2022); Abdelrahman et al. (2022).

# In[36]:


# ── Seção 8.2: Importância de features via Decision Tree (SEED=42) ──
from sklearn.tree import DecisionTreeClassifier

SEED = 42
feat_cols_dt = ['Attempts', 'first_score', 'n_attempts', 'score_mean', 'score_max', 'n_compile_errors']
feat_labels_dt = {
    'Attempts'        : 'Attempts (early.csv)',
    'first_score'     : 'Score da 1ª tentativa',
    'n_attempts'      : 'Nº de Run.Program',
    'score_mean'      : 'Score médio',
    'score_max'       : 'Score máximo',
    'n_compile_errors': 'Nº de Compile.Error',
}

X_dt = early_feat[feat_cols_dt].copy()
y_dt = early_feat['Label'].astype(int)

dt = DecisionTreeClassifier(max_depth=5, random_state=SEED)
dt.fit(X_dt, y_dt)

importance_df = pd.DataFrame({
    'Feature' : [feat_labels_dt[c] for c in feat_cols_dt],
    'Coluna'  : feat_cols_dt,
    'Importância (Gini)': dt.feature_importances_,
}).sort_values('Importância (Gini)', ascending=False).reset_index(drop=True)

importance_df['Importância (Gini)'] = importance_df['Importância (Gini)'].round(4)
print('=== Importância de Features — Decision Tree (max_depth=5, SEED=42) ===')
display(importance_df)

# Plot comparativo: Spearman |ρ| vs DT importance
fig, axes = plt.subplots(1, 2, figsize=(14, 4))

# DT importance
colors_dt = sns.color_palette('Blues_r', n_colors=len(importance_df))
axes[0].barh(importance_df['Feature'], importance_df['Importância (Gini)'], color=colors_dt)
axes[0].set_xlabel('Importância (Gini)')
axes[0].set_title('Importância de Features — Decision Tree')
axes[0].invert_yaxis()
for i, row in importance_df.iterrows():
    axes[0].text(row['Importância (Gini)'] + 0.005, i,
                 f"{row['Importância (Gini)']:.3f}", va='center', fontsize=9)

# |Spearman| para comparação
spearman_abs = spearman_df.copy()
spearman_abs['|ρ|'] = spearman_abs['ρ (Spearman)'].abs()
spearman_abs = spearman_abs.sort_values('|ρ|', ascending=False)

colors_sp = sns.color_palette('Oranges_r', n_colors=len(spearman_abs))
axes[1].barh(spearman_abs['Feature'], spearman_abs['|ρ|'], color=colors_sp)
axes[1].set_xlabel('|ρ| de Spearman')
axes[1].set_title('Ranking por |Spearman| vs Label')
axes[1].invert_yaxis()
for i, row in spearman_abs.reset_index(drop=True).iterrows():
    axes[1].text(row['|ρ|'] + 0.005, i, f"{row['|ρ|']:.3f}", va='center', fontsize=9)

plt.tight_layout()
plt.show()

print()
print('Top-5 features por Importância (DT):')
for i, row in importance_df.head(5).iterrows():
    print(f"  {i+1}. {row['Feature']} ({row['Coluna']}): {row['Importância (Gini)']:.4f}")


# **Achado:** A Decision Tree (max_depth=5, SEED=42) indica como **Top-5 features**: 1) `Attempts` (Gini ≈ 0,792), 2) `score_max` (≈ 0,192), 3) `n_attempts` (≈ 0,007), 4) `score_mean` (≈ 0,005), 5) `n_compile_errors` (≈ 0,003). A dominância de `Attempts` (79,2% da importância total) reflete que o número total de tentativas até o primeiro acerto é o preditor mais discriminativo do Label no cenário early. O `score_max` captura casos onde o estudante chegou a uma solução correta em algum momento mas não na primeira tentativa. A baixa importância relativa de `n_compile_errors` na DT (vs correlação Spearman ≈ −0,57) sugere que seu sinal preditivo é parcialmente capturado por `Attempts` (features correlacionadas entre si).
# 
# **Top-5 features e interpretação:**
# 1. **Attempts** (Gini 0,792): número de tentativas até acerto ou desistência — principal proxy de dificuldade por problema.
# 2. **score_max** (Gini 0,192): score máximo atingido pelo estudante — distingue quem nunca chegou perto de 100% de quem chegou mas com muitas tentativas.
# 3. **n_attempts** (Gini 0,007): número de Run.Program — altamente colinear com `Attempts`, capta volume de submissões.
# 4. **score_mean** (Gini 0,005): média de scores — sinal de progresso gradual (scores parciais).
# 5. **n_compile_errors** (Gini 0,003): erros de compilação — confirma dificuldade sintática; justifica inclusão de `Compile.Error` na sequência Code-DKT.
# 
# **Implicação para modelagem:** A centralidade de `Attempts` como preditor de Label — e sua alta correlação com `n_compile_errors` (ρ ≈ −0,64) — valida que o BKT, que usa apenas as tentativas sequenciais com acerto/erro, captura boa parte do sinal disponível. O DKT e o Code-DKT têm vantagem ao modelar a trajetória temporal dessas tentativas, potencialmente capturando a curvatura de aprendizado (rate of improvement) além do count bruto. A avaliação por **first-attempt AUC** é mais desafiante que all-attempts AUC por não se beneficiar da autocorrelação temporal entre tentativas consecutivas — é o benchmark mais limpo para separar a capacidade preditiva real de cada modelo.

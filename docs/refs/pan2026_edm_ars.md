---
source: docs/EDM_LLM.pdf
cite_as: Pan et al. (2026)
title: "EDM-ARS: A Domain-Specific Multi-Agent System for Automated Educational Data Mining Research"
venue: Technical Report, arXiv:2603.18273v1 [cs.AI], 18 Mar 2026. edmars.ai
---

## Resumo de uma linha
Sistema multi-agente (5 LLMs especializados) que automatiza o pipeline completo de pesquisa em EDM — da formulação de problema à escrita do manuscrito LaTeX com citações reais.

## Fatos críticos para este projeto
- **Relevância direta para o harness de agentes deste TCC**: EDM-ARS é a referência mais próxima do que estamos construindo
- 5 agentes: ProblemFormulator, DataEngineer, Analyst, Critic, Writer — coordenados por state-machine
- Problemas de sistemas genéricos em EDM: desconhecimento de convenções de dados (e.g., códigos sentinela negativos para missing data), temporal leakage — motivam sistemas domain-specific
- Dataset de referência atual: HSLS:09 (survey longitudinal, ~23.500 alunos, 9º ao ensino superior)
- Mecanismo de checkpoint-based recovery e sandboxed code execution

## Metodologia relevante
- 3-tier data registry: domain knowledge encoding + leakage prevention
- Inter-agent communication protocol com loops de revisão
- Limitações atuais: single-dataset scope, output formulaico — roadmap inclui causal inference e cross-dataset

## Relevância para este TCC
Referência arquitetural para o harness de agentes Generator + Evaluator. Confirma que domain-specific knowledge (como `docs/refs/`) é crítico para qualidade de sistemas automáticos em EDM.

## Citação BibTeX
```
@techreport{pan2026edmars,
  author    = {Chenguang Pan and Zhou Zhang and Weixuan Xiao and Chengyuan Yao},
  title     = {{EDM-ARS}: A Domain-Specific Multi-Agent System for Automated Educational Data Mining Research},
  institution = {edmars.ai / Columbia University},
  year      = {2026},
  note      = {arXiv:2603.18273v1}
}
```

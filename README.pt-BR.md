# Claude para Serviços Financeiros

> [English](./README.md) | **Português (Brasil)**

Agentes de referência, habilidades e conectores de dados para os fluxos de trabalho de serviços financeiros mais comuns — banco de investimento, pesquisa de ações, private equity e gestão de patrimônio.

Tudo aqui está disponível **de duas formas a partir de uma única fonte**: instale como um plugin do [Claude Cowork](https://claude.com/product/cowork) ou implante via [API de Agentes Gerenciados do Claude](https://docs.claude.com/en/api/managed-agents) no seu próprio motor de fluxo de trabalho. O mesmo prompt de sistema, as mesmas habilidades — você escolhe onde executar.

> [!IMPORTANT]
> Nada neste repositório constitui conselho de investimento, jurídico, fiscal ou contábil. Esses agentes elaboram produtos de trabalho de analista — modelos, memorandos, notas de pesquisa, reconciliações — para revisão por um profissional qualificado. Eles não fazem recomendações de investimento, executam transações, vinculam risco, lançam em um livro razão ou aprovam onboarding; toda saída é encaminhada para aprovação humana. Você é responsável por verificar os resultados e pela conformidade com as leis e regulamentos aplicáveis à sua empresa.

O que está no repositório:

- **[Agentes](#agentes)** — agentes de fluxo de trabalho nomeados e completos (Pitch Agent, Market Researcher, GL Reconciler, …). Cada um é distribuído como um plugin do Cowork **e** como um [template de Agente Gerenciado do Claude](./managed-agent-cookbooks) implantado via `/v1/agents`.
- **[Plugins verticais](#plugins-verticais)** — as habilidades subjacentes, comandos slash e conectores de dados, agrupados por vertical de FSI. Instale-os sozinhos se você só quiser `/comps`, `/dcf`, `/earnings` e os conectores sem um agente completo.

## Agentes

Cada agente é nomeado pelo fluxo de trabalho que executa. São pontos de partida: instale os que correspondem ao seu trabalho e ajuste os prompts, habilidades e conectores de acordo com como sua empresa opera.

Cada plugin de agente é **autossuficiente** — ele inclui as habilidades que usa, então instalar o agente é tudo que você precisa.

| Função | Agente | O que faz |
|---|---|---|
| **Cobertura e consultoria** | **[Pitch Agent](./plugins/agent-plugins/pitch-agent)** | Comps, precedentes, LBO → deck de pitch com marca, do início ao fim |
| | **[Meeting Prep Agent](./plugins/agent-plugins/meeting-prep-agent)** | Pacote de briefing antes de cada reunião com clientes |
| **Pesquisa e modelagem** | **[Market Researcher](./plugins/agent-plugins/market-researcher)** | Setor ou tema → visão geral da indústria, cenário competitivo, comps de pares, lista de ideias |
| | **[Earnings Reviewer](./plugins/agent-plugins/earnings-reviewer)** | Ligação de resultados + arquivamentos → atualização do modelo → rascunho de nota |
| | **[Model Builder](./plugins/agent-plugins/model-builder)** | DCF, LBO, 3-statement, comps — ao vivo no Excel |
| **Administração de fundos e operações financeiras** | **[Valuation Reviewer](./plugins/agent-plugins/valuation-reviewer)** | Ingere pacotes de GP, executa template de avaliação, prepara relatórios para LP |
| | **[GL Reconciler](./plugins/agent-plugins/gl-reconciler)** | Encontra divergências, rastreia a causa raiz, encaminha para aprovação |
| | **[Month-End Closer](./plugins/agent-plugins/month-end-closer)** | Acréscimos, roll-forwards, comentários de variância |
| | **[Statement Auditor](./plugins/agent-plugins/statement-auditor)** | Audita extratos de LP antes da distribuição |
| **Operações e onboarding** | **[KYC Screener](./plugins/agent-plugins/kyc-screener)** | Analisa documentos de onboarding, executa o mecanismo de regras, sinaliza lacunas |

Para implantação de Agente Gerenciado — `agent.yaml`, subagentes leaf-worker, exemplos de eventos de direcionamento e notas de segurança por agente — veja **[managed-agent-cookbooks/](./managed-agent-cookbooks)**.

## Estrutura do Repositório

```
plugins/
  agent-plugins/               # Agentes nomeados — um plugin autossuficiente cada
  vertical-plugins/            # Pacotes de habilidades e comandos por vertical de FSI, mais conectores MCP
  partner-built/               # Plugins desenvolvidos por parceiros (LSEG, S&P Global)
managed-agent-cookbooks/       # Cookbooks de Agentes Gerenciados do Claude — um diretório por agente
claude-for-msft-365-install/   # Ferramentas de administração para provisionar o suplemento Claude no Microsoft 365
scripts/                       # deploy-managed-agent.sh · check.py · validate.py · orchestrate.py · sync-agent-skills.py
```

## Primeiros Passos

### Cowork

No Cowork, abra **Configurações → Plugins → Adicionar plugin** e:

- **Cole a URL deste repositório** — `https://github.com/anthropics/claude-for-financial-services` — e escolha os agentes e verticais que deseja na lista do marketplace, ou
- **Faça upload de um zip** — compacte qualquer diretório em `plugins/` (ex.: `plugins/agent-plugins/pitch-agent/`) e faça o upload.

### Claude Code

```bash
# Adicionar o marketplace
claude plugin marketplace add anthropics/claude-for-financial-services

# Habilidades e conectores principais (instale primeiro)
claude plugin install financial-analysis@claude-for-financial-services

# Agentes nomeados — escolha os que quiser
claude plugin install pitch-agent@claude-for-financial-services
claude plugin install gl-reconciler@claude-for-financial-services
claude plugin install market-researcher@claude-for-financial-services

# Pacotes de habilidades verticais
claude plugin install investment-banking@claude-for-financial-services
claude plugin install equity-research@claude-for-financial-services
```

Após instalados, os agentes aparecem no dispatch do Cowork, as habilidades são ativadas automaticamente quando relevantes e os comandos slash ficam disponíveis na sessão (`/comps`, `/dcf`, `/earnings`, `/ic-memo`, …).

### Agentes Gerenciados do Claude

```bash
export ANTHROPIC_API_KEY=sk-ant-...
scripts/deploy-managed-agent.sh gl-reconciler
```

Cada template em [`managed-agent-cookbooks/`](./managed-agent-cookbooks) referencia o mesmo prompt de sistema e as mesmas habilidades que seu plugin equivalente. O script de implantação resolve referências de arquivos, faz upload de habilidades, cria subagentes leaf-worker e faz POST do orquestrador em `/v1/agents`. Veja [`scripts/orchestrate.py`](./scripts/orchestrate.py) para um loop de eventos de referência que roteia eventos `handoff_request` entre agentes via sua própria camada de orquestração.

> **Preview de Pesquisa:** delegação a subagentes (`callable_agents`) é uma capacidade em preview. Veja os READMEs por agente para orientações de segurança e handoff.

## Como se Encaixa

| | O que é | Onde fica |
|---|---|---|
| **Agentes** | Plugins autossuficientes que possuem um fluxo de trabalho de ponta a ponta — prompt de sistema mais as habilidades que utiliza. O Cowork e o wrapper de Agente Gerenciado referenciam o mesmo diretório. | `plugins/agent-plugins/<slug>/` |
| **Habilidades** | Expertise de domínio, convenções e métodos passo a passo que o Claude utiliza automaticamente quando relevante. Criadas uma vez nas verticais; cada agente inclui uma cópia sincronizada das que precisa. | `plugins/vertical-plugins/<vertical>/skills/` (fonte) · `plugins/agent-plugins/<slug>/skills/` (incluída) |
| **Comandos** | Ações slash que você dispara explicitamente (`/comps`, `/earnings`, `/ic-memo`). | `plugins/vertical-plugins/<vertical>/commands/` |
| **Conectores** | [Servidores MCP](https://modelcontextprotocol.io/) que conectam o Claude aos seus dados — terminais, plataformas de pesquisa, repositórios de documentos. | `plugins/vertical-plugins/financial-analysis/.mcp.json` |
| **Wrappers de agente gerenciado** | `agent.yaml` + subagentes depth-1 + exemplos de direcionamento para implantação headless. | `managed-agent-cookbooks/<slug>/` |

Tudo é baseado em arquivos — markdown e JSON, sem etapa de build.

## Plugins Verticais

Comece com **financial-analysis** — ele traz as habilidades de modelagem compartilhadas e todos os conectores de dados. Adicione verticais para os fluxos de trabalho que você precisa.

| Plugin | O que adiciona |
|---|---|
| **[financial-analysis](./plugins/vertical-plugins/financial-analysis)** *(core)* | Comps, DCF, LBO, 3-statement, QC de deck, auditoria de Excel. Todos os 11 conectores de dados. |
| **[investment-banking](./plugins/vertical-plugins/investment-banking)** | CIMs, teasers, cartas de processo, listas de compradores, modelos de fusão, acompanhamento de negócios. |
| **[equity-research](./plugins/vertical-plugins/equity-research)** | Notas de resultados, iniciações, atualizações de modelo, acompanhamento de tese e catalisadores. |
| **[private-equity](./plugins/vertical-plugins/private-equity)** | Sourcing, triagem, checklists de due diligence, memos de IC, monitoramento de portfólio. |
| **[wealth-management](./plugins/vertical-plugins/wealth-management)** | Revisões de clientes, planos financeiros, rebalanceamento, relatórios, TLH. |
| **[fund-admin](./plugins/vertical-plugins/fund-admin)** | Reconciliação de GL, rastreamento de divergências, acréscimos, roll-forwards, comentários de variância, conferência de NAV. |
| **[operations](./plugins/vertical-plugins/operations)** | Análise de documentos KYC e avaliação por grade de regras. |
| **[lseg](./plugins/partner-built/lseg)** *(parceiro)* | RV de bonds, curvas de swap, carry de FX, vol de opções, monitoramento de taxas macro em dados da LSEG. |
| **[sp-global](./plugins/partner-built/spglobal)** *(parceiro)* | Tear sheets, prévias de resultados, resumos de financiamento no S&P Capital IQ. |

## Integrações MCP

Todos os conectores estão centralizados no plugin principal **financial-analysis** e compartilhados entre os demais.

| Provedor | URL |
|---|---|
| [Daloopa](https://www.daloopa.com/) | `https://mcp.daloopa.com/server/mcp` |
| [Morningstar](https://www.morningstar.com/) | `https://mcp.morningstar.com/mcp` |
| [S&P Global](https://www.spglobal.com/) | `https://kfinance.kensho.com/integrations/mcp` |
| [FactSet](https://www.factset.com/) | `https://mcp.factset.com/mcp` |
| [Moody's](https://www.moodys.com/) | `https://api.moodys.com/genai-ready-data/m1/mcp` |
| [MT Newswires](https://www.mtnewswires.com/) | `https://vast-mcp.blueskyapi.com/mtnewswires` |
| [Aiera](https://www.aiera.com/) | `https://mcp-pub.aiera.com` |
| [LSEG](https://www.lseg.com/) | `https://api.analytics.lseg.com/lfa/mcp` |
| [PitchBook](https://pitchbook.com/) | `https://premium.mcp.pitchbook.com/mcp` |
| [Chronograph](https://www.chronograph.pe/) | `https://ai.chronograph.pe/mcp` |
| [Egnyte](https://www.egnyte.com/) | `https://mcp-server.egnyte.com/mcp` |

> O acesso ao MCP pode exigir uma assinatura ou chave de API do provedor.

## Claude para Microsoft 365 — Ferramentas de Instalação

Se sua empresa usa o Claude dentro do Excel, PowerPoint, Word e Outlook via o suplemento do Microsoft 365, [`claude-for-msft-365-install/`](./claude-for-msft-365-install) são as ferramentas de administração para provisioná-lo na **sua própria nuvem** — Vertex AI, Bedrock ou um gateway LLM interno — em vez da API da Anthropic.

É um plugin do Claude Code (não um plugin do Cowork) que guia um administrador de TI na geração do manifesto do suplemento customizado, concessão do consentimento de administrador do Azure e gravação de configuração de roteamento por usuário via Microsoft Graph. Instale com:

```bash
claude plugin install claude-for-msft-365-install@claude-for-financial-services
/claude-for-msft-365-install:setup
```

Isso é separado dos agentes e plugins verticais acima — é a rampa de acesso que implanta o suplemento em um tenant, após o qual os agentes e habilidades aqui são o que é executado dentro dele.

## Personalizando

Estes são templates de referência — eles melhoram quando você os ajusta para como sua empresa trabalha.

- **Troque conectores** — aponte `.mcp.json` para seus provedores de dados e sistemas internos.
- **Adicione contexto da empresa** — inclua sua terminologia, processos e padrões de formatação nos arquivos de habilidades.
- **Traga seus templates** — `/ppt-template` ensina ao Claude seus layouts de PowerPoint com marca.
- **Ajuste o escopo do agente** — edite `agents/<slug>.md` para corresponder a como sua equipe realmente executa o fluxo de trabalho.
- **Adicione os seus próprios** — copie a estrutura para fluxos de trabalho que ainda não cobrimos.

## Referência de Habilidades e Comandos

<details>
<summary><b>financial-analysis</b> — modelagem principal, Excel, QC de deck</summary>

| Habilidade | Comando | Descrição |
|---|---|---|
| comps-analysis | `/comps` | Análise de empresas comparáveis com múltiplos de negociação |
| dcf-model | `/dcf` | Avaliação por DCF com WACC e análise de sensibilidade |
| lbo-model | `/lbo` | Modelo de aquisição alavancada |
| 3-statement-model | `/3-statement-model` | Preencher templates de modelo financeiro de 3 demonstrações |
| audit-xls | `/debug-model` | Auditoria de modelo Excel — rastreamento de fórmulas, detecção de hardcode, verificações de saldo |
| clean-data-xls | — | Normalizar e limpar dados tabulares no Excel |
| deck-refresh | — | Revinculação e atualização de gráficos/tabelas incorporados em um deck |
| competitive-analysis | `/competitive-analysis` | Cenário competitivo e posicionamento de mercado |
| ib-check-deck | — | QC de apresentações para erros e consistência |
| pptx-author | — | Produzir um arquivo `.pptx` em modo headless (modo Agente Gerenciado) |
| xlsx-author | — | Produzir um arquivo `.xlsx` em modo headless (modo Agente Gerenciado) |
| ppt-template-creator | `/ppt-template` | Criar habilidades de template de PPT reutilizáveis |
| skill-creator | — | Guia para criação de novas habilidades |

</details>

<details>
<summary><b>investment-banking</b> — materiais e execução de negócios</summary>

| Habilidade | Comando | Descrição |
|---|---|---|
| strip-profile | `/one-pager` | Perfis de empresa de uma página para pitch books |
| pitch-deck | — | Preencher templates de pitch deck com dados |
| datapack-builder | — | Construir data packs a partir de CIMs e arquivamentos |
| cim-builder | `/cim` | Rascunhar Memorandos de Informação Confidencial |
| teaser | `/teaser` | Teasers anônimos de empresa de uma página |
| buyer-list | `/buyer-list` | Universo de compradores estratégicos e financeiros |
| merger-model | `/merger-model` | Análise de M&A por acréscimo/diluição |
| process-letter | `/process-letter` | Instruções de lance e correspondência de processo |
| deal-tracker | `/deal-tracker` | Acompanhar negócios ativos, marcos e itens de ação |

</details>

<details>
<summary><b>equity-research</b> — cobertura e publicação</summary>

| Habilidade | Comando | Descrição |
|---|---|---|
| earnings-analysis | `/earnings` | Relatórios de atualização trimestral pós-resultados |
| earnings-preview | `/earnings-preview` | Análise de cenários pré-resultados e métricas-chave |
| initiating-coverage | `/initiate` | Relatórios de iniciação de cobertura de qualidade institucional |
| model-update | `/model-update` | Atualizar modelos financeiros com novos dados |
| morning-note | `/morning-note` | Notas para reunião matinal e ideias de negociação |
| sector-overview | `/sector` | Relatórios de panorama da indústria e temáticos |
| thesis-tracker | `/thesis` | Manter e atualizar teses de investimento |
| catalyst-calendar | `/catalysts` | Rastrear catalisadores futuros em toda a cobertura |
| idea-generation | `/screen` | Triagem de ações e geração de ideias |

</details>

<details>
<summary><b>private-equity</b> — sourcing até operações de portfólio</summary>

| Habilidade | Comando | Descrição |
|---|---|---|
| deal-sourcing | `/source` | Descobrir empresas, verificar CRM, rascunhar abordagem a fundadores |
| deal-screening | `/screen-deal` | Passagem rápida de aprovação/rejeição em CIMs e teasers recebidos |
| dd-checklist | `/dd-checklist` | Checklists de diligência por workstream |
| dd-meeting-prep | `/dd-prep` | Preparar para apresentações da gestão e chamadas com especialistas |
| unit-economics | `/unit-economics` | Coortes de ARR, LTV/CAC, retenção líquida, qualidade de receita |
| returns-analysis | `/returns` | Tabelas de sensibilidade de TIR/MOIC |
| ic-memo | `/ic-memo` | Elaboração de memo para comitê de investimento |
| portfolio-monitoring | `/portfolio` | Acompanhar KPIs e variações de empresas do portfólio |
| value-creation-plan | `/value-creation` | Planos de 100 dias pós-fechamento e pontes de EBITDA |
| ai-readiness | `/ai-readiness` | Avaliar a prontidão de IA de uma empresa do portfólio |

</details>

<details>
<summary><b>wealth-management</b> — fluxos de trabalho de assessor</summary>

| Habilidade | Comando | Descrição |
|---|---|---|
| client-review | `/client-review` | Preparar para reuniões com clientes com desempenho e pontos de discussão |
| financial-plan | `/financial-plan` | Projeções de aposentadoria, educação, herança e fluxo de caixa |
| portfolio-rebalance | `/rebalance` | Análise de desvio de alocação e rebalanceamento com eficiência fiscal |
| client-report | `/client-report` | Relatórios de desempenho voltados ao cliente |
| investment-proposal | `/proposal` | Propostas para clientes em potencial |
| tax-loss-harvesting | `/tlh` | Identificar oportunidades de TLH e gerenciar wash sales |

</details>

## Contribuindo

Tudo aqui é markdown e YAML. Fork, edite, abra um PR. Para novo conteúdo:

- Nova habilidade → adicione em `plugins/vertical-plugins/<vertical>/skills/`, depois execute `python3 scripts/sync-agent-skills.py` para propagar para qualquer agente que a inclua.
- Novo agente → `plugins/agent-plugins/<slug>/` (com `agents/<slug>.md` + `skills/`) e um `managed-agent-cookbooks/<slug>/` correspondente.
- Nova tradução → crie `README.<código-do-idioma>.md` (ex.: `README.pt-BR.md`) e adicione um link no seletor de idiomas no topo de `README.md` e de cada arquivo de tradução existente.
- Execute `python3 scripts/check.py` antes de fazer push — ele valida todos os manifestos, verifica se todas as referências cruzadas de arquivos resolvem e falha se alguma habilidade incluída divergiu de sua fonte vertical.

## Licença

[Apache License 2.0](./LICENSE)
# Changelog

Todas as alterações relevantes deste projecto são documentadas neste ficheiro.

O formato segue [Keep a Changelog](https://keepachangelog.com/pt-PT/1.0.0/),
e o versionamento segue [Semantic Versioning](https://semver.org/lang/pt-BR/).

---
## [1.2.0] — 2026-08-XX

### Corrigido
- Visibilidade, em modo escuro, dos botões de navegação do topo (Pesquisa e Estatísticas) aquando da ação _hover_

## [1.1.0] — 2026-08-12

### Adicionado
- **Pesquisa avançada por campos independentes** — novo painel expansível (botão `+ Avançada`) com formulário dividido em quatro secções: Identificação, Filiação (batismo/óbito), Casamento — Nubentes, e Casamento — Filiação dos nubentes (pai/mãe do noivo e da noiva)
- **Inferência automática do tipo de registo** — com base nos campos preenchidos na pesquisa avançada, o tipo (Batismos e Óbitos / Casamentos / Todos) é determinado automaticamente e indicado em tempo real por um chip no topo do painel
- **Novo endpoint `/api/pesquisar-avancado`** — aceita campos separados e gera condições SQL independentes por campo (`AND`), eliminando a mistura de termos entre campos que existia na pesquisa simples
- **Facetas em cascata** — ao seleccionar um valor numa faceta, os valores disponíveis nas restantes actualizam-se para mostrar apenas o que coexiste com a selecção activa (comportamento equivalente ao AutoFiltro do Excel)
- **Faceta "Pais & Mães" unificada para casamentos** — agrega pai/mãe do noivo e pai/mãe da noiva numa única faceta, permitindo refinar por qualquer combinação de nomes de ambos os lados
- **Badge de filtros activos** nas facetas — grupos com selecções activas ficam assinalados com um contador laranja

### Alterado
- Campo de texto geral desactivado visualmente quando a pesquisa avançada está activa — os dois modos são mutuamente exclusivos
- Filtro de Tipo passou de `Todos` para `Automático` quando usado em conjunto com a pesquisa avançada
- Facetas laterais adaptam os títulos consoante o tipo de resultados: "Pai" e "Mãe" para batismos/óbitos, "Pais & Mães" quando os resultados incluem casamentos
- Botões `+ Avançada` e `Rede` compactados em mobile (só ícone, sem texto)
- Grelha do painel avançado: 3 colunas em desktop, 2 em tablet, 1 em mobile

### Corrigido
- Inputs da pesquisa avançada não respeitavam o tema escuro (fundo e texto hardcoded)
- Texto do indicador de tipo inferido invisível em modo escuro
- Duplicações e conflitos no `style.css` (regras `html.dark .fed-chip` duplicadas, conflito entre `grid` e `flex` nos botões em mobile)

---

## [1.0.0] — 2026-08-01

### Adicionado
- Interface pública de pesquisa com texto livre (insensível a maiúsculas e acentos, multi-termo com três níveis de relevância)
- Pesquisa IA em linguagem natural com Claude Haiku, com fallback por padrões regex
- Três tipos de registo: Batismos, Casamentos e Óbitos
- Filtros por tipo, período e fonte
- Painel de facetas lateral (desktop) e drawer (mobile) com filtros por tipo, localidade, pai, mãe e período
- Modal de detalhe com todos os campos organizados por secções
- Vista de estatísticas com totais globais, detalhe por freguesia e gráficos de distribuição por década
- Área de administração restrita a IPs de rede local
- Importação de ficheiros Excel (`.xlsx`/`.xls`) com suporte a múltiplas folhas, validação antes de confirmar, detecção de duplicados e modo de actualização
- Campo de freguesia com autocomplete nas importações
- Extracção automática do código do arquivo distrital a partir da referência FONTE
- Histórico de importações por freguesia com datas extremas
- Reset da base de dados com dupla confirmação
- Painel de auditoria de acessos (últimos 90 dias) com eventos suspeitos
- Rodapé editável na área de administração
- Rate limiting por IP com bloqueio automático de 5 minutos
- Validação e sanitização de inputs com detecção de padrões maliciosos
- Validação de magic bytes nos uploads
- Headers de segurança HTTP (CSP, X-Frame-Options, etc.)
- Interface responsiva para desktop, tablet e mobile
- Modo escuro — toggle no cabeçalho para alternar entre tema claro e escuro; preferência persistida via `localStorage`
- Suporte a federação entre instâncias com autenticação por token UUID v4
- Deploy via Docker Compose

---

[1.1.0]: https://github.com/Qui3t0wL/Liber/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/Qui3t0wL/Liber/releases/tag/v1.0.0

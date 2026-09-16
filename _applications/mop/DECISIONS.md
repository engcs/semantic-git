# Decisions - MOP

## Cabeçalho

O padrão MOP concretiza o contrato de dados por meio de componentes comuns de detalhamento, agregação, catalogação e publicação, organizados pelas escolhas abaixo. Fórmulas, variáveis, populações e casos de borda continuam sendo decisões de cada indicador.

## Corpo

- **D-001** - Estruturar cada indicador nas etapas fato detalhado, KPI fato, catálogo e KPI final. Atende R-007 e R-009.
- **D-002** - Identificar a série por uma chave CCIO composta pelo indicador base, visão, grão temporal e versão. Atende R-001.
- **D-003** - Usar o grão mensal como padrão de publicação, permitindo que cada indicador defina outros grãos temporais, preservando as datas de referência, apuração e congelamento. Atende R-002.
- **D-004** - Preservar as ocorrências no menor grão do indicador, agregá-las inicialmente no nível contrato e consolidar as medidas nos níveis regional e distribuidora. Atende R-003 e R-007.
- **D-005** - Manter fatos e resultados nas apurações `VIVA` e `CONGELADA` e reuni-los no catálogo do indicador. Atende R-004 e R-009.
- **D-006** - Apurar versões em paralelo e incorporar versão, status da versão e origem à identidade de cada resultado. Atende R-005.
- **D-007** - Incorporar a visão à identidade da série como recorte da população apurada. Atende R-008.
- **D-008** - Dar precedência ao controle manual de expurgo e zerar a contribuição da linha sem removê-la do detalhe. Atende R-006.
- **D-009** - Compor medidas auditáveis no KPI fato a partir de valores base e, quando aplicável, suplementos, preservando separadamente sua origem e seu grão antes de calcular a fórmula específica no KPI final. Atende R-007.

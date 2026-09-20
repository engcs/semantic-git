# CSC mop
format: csc-md/2
target: mop
source_commit: ae1ea2c39f379d605037118bd249da05072bc146
authority: DERIVED
generation: SIMULATED

## Requirements
- R-001 | Identificar inequivocamente cada série por indicador, visão, grão temporal e versão da regra de negócio.
- R-002 | Organizar o detalhe e os resultados por competência, preservando a data de referência, a data de apuração e, quando aplicável, a data de congelamento.
- R-003 | Disponibilizar resultados consistentes nos níveis organizacionais aplicáveis, incluindo contrato, regional e distribuidora.
- R-004 | Distinguir a apuração recalculável da fotografia histórica preservada.
- R-005 | Permitir a apuração paralela de diferentes versões, preservando a identidade, o estado e a origem de cada resultado.
- R-006 | Permitir expurgos de negócio sem remover a ocorrência original nem perder a justificativa da exceção.
- R-007 | Permitir reconciliar o resultado do indicador com suas medidas componentes, incluindo eventuais suplementos, e com as ocorrências consideradas ou desconsideradas na apuração.
- R-008 | Tratar cada visão como um recorte explícito das ocorrências que podem participar da apuração.
- R-009 | Proteger os resultados históricos contra recálculo ou substituição silenciosa.

## Decisions
- D-001 -> R-007,R-009 | Estruturar cada indicador nas etapas fato detalhado, KPI fato, catálogo e KPI final.
- D-002 -> R-001 | Identificar a série por uma chave CCIO composta pelo indicador base, visão, grão temporal e versão.
- D-003 -> R-002 | Usar o grão mensal como padrão de publicação, permitindo que cada indicador defina outros grãos temporais, preservando as datas de referência, apuração e congelamento.
- D-004 -> R-003,R-007 | Preservar as ocorrências no menor grão do indicador, agregá-las inicialmente no nível contrato e consolidar as medidas nos níveis regional e distribuidora.
- D-005 -> R-004,R-009 | Manter fatos e resultados nas apurações `VIVA` e `CONGELADA` e reuni-los no catálogo do indicador.
- D-006 -> R-005 | Apurar versões em paralelo e incorporar versão, status da versão e origem à identidade de cada resultado.
- D-007 -> R-008 | Incorporar a visão à identidade da série como recorte da população apurada.
- D-008 -> R-006 | Dar precedência ao controle manual de expurgo e zerar a contribuição da linha sem removê-la do detalhe.
- D-009 -> R-007 | Compor medidas auditáveis no KPI fato a partir de valores base e, quando aplicável, suplementos, preservando separadamente sua origem e seu grão antes de calcular a fórmula específica no KPI final.

## Operations
- O-001 | Cada indicador define sua unidade elementar no menor grão disponível, preservando o dia e a equipe quando fizerem parte da ocorrência.
- O-002 | Cada unidade recebe uma data de referência, da qual são derivadas as competências temporais necessárias à apuração.
- O-003 | Cada unidade é situada na hierarquia organizacional formada por equipe, contrato, regional e distribuidora.
- O-004 | A unidade é relacionada às demais entidades necessárias para receber suas classificações de negócio.
- O-005 | As classificações determinam a população apurada e a contribuição individual para cada medida do indicador.
- O-006 | Ocorrências expurgadas permanecem no detalhe e na auditoria, mas deixam de contribuir para as medidas agregadas.
- O-007 | As contribuições são inicialmente preservadas no menor grão temporal e organizacional necessário ao indicador.
- O-008 | As contribuições no menor grão do indicador são consolidadas no período e no nível organizacional definidos para publicação.
- O-009 | No nível contrato, as unidades são agrupadas por competência, visão, versão e demais dimensões próprias do indicador.
- O-010 | Quando uma medida prevê suplementos, eles são associados aos valores base no mesmo grão antes da agregação do período, preservando separadamente sua origem.
- O-011 | As medidas do nível contrato são posteriormente consolidadas nos níveis regional e distribuidora.
- O-012 | Os valores acumulados são obtidos pela soma temporal das medidas dentro de cada série e nível organizacional.
- O-013 | A fórmula específica do indicador é aplicada às medidas já agregadas para produzir os resultados do período e acumulado.

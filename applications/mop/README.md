# MOP

Este diretório é uma aplicação do Semantic Git ao framework MOP. Ele contém o estado
semântico comum necessário para representar indicadores do framework sem
confundir o conhecimento governado com sua implementação física.

O RDO deste diretório reúne identidade, período, versão, visão, hierarquia,
expurgo, apuração viva, apuração congelada e publicação.

As premissas semânticas específicas dos indicadores estão em
[`foundations/INDICATOR_SEMANTICS.md`](foundations/INDICATOR_SEMANTICS.md).
Esse anexo é pré-ontológico, pertence ao MOP e não faz parte do núcleo do
Semantic Git.

Regras específicas de um indicador devem viver em um namespace próprio e ser
governadas por mudanças semânticas compatíveis com o
[`SEMANTIC_GIT.md`](../../SEMANTIC_GIT.md) da raiz.

O conteúdo deste diretório é uma aplicação conceitual do Semantic Git ao MOP. Ele não
é um executor, um projeto dbt ou uma definição de indicador específico.

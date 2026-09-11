# Plano de Implementação: Sistema de Gestão de Manutenção de Máquinas Pesadas

## Contexto
O usuário deseja um sistema para gerenciar manutenção de máquinas pesadas (escavadeiras, retroescavadeiras, patrol, etc.). Os requisitos incluem:
- Registro de peças utilizadas em cada manutenção.
- Registro do mecânico responsável.
- Histórico de manutenção por máquina.
- Envio automático de relatório via WhatsApp após cada registro.

## Abordagem Recomendada
Considerando que o usuário solicitou uma "planilha", mas precisa de automação (WhatsApp), a melhor solução é um sistema híbrido ou automação baseada em Sheets:

1. **Base de Dados/Frontend**: Google Sheets (familiar para o usuário, fácil de editar e visualizar) ou um banco de dados SQL simples com uma interface de entrada de dados. Para este plano, **recomendo uma pequena aplicação WEB (Flask/FastAPI)** para facilitar a estruturação dos dados e a automação do WhatsApp, integrada a um banco de dados (SQLite), onde os dados podem ser exportados como CSV/Excel se necessário para "parecer" uma planilha.
2. **Integração WhatsApp**: Uso de uma API de WhatsApp (ex: Twilio ou um serviço de Gateway de WhatsApp) disparado após cada inserção de manutenção no sistema.

## Arquitetura Proposta
- **Backend**: Python (FastAPI).
- **Banco de Dados**: SQLite (simples, sem necessidade de servidor extra).
- **Interface**: Uma pequena página web simples para entrada de dados (ou uma API que consome dados de um formulário).
- **Automação WhatsApp**: Disparo de requisição POST para API de WhatsApp.

## Etapas do Plano
1. **Modelagem de Dados**: Definir as tabelas de Máquinas, Mecânicos, Peças, Manutenções.
2. **Desenvolvimento do Backend**: Criar a API para manipular esses dados.
3. **Desenvolvimento da Interface**: Criar formulário(s) simples para entrada de dados.
4. **Implementação do envio WhatsApp**: Configurar a integração da API de WhatsApp.
5. **Testes**: Validar o fluxo de registro e envio da mensagem.

## Verificação
- A máquina deve ter um histórico acessível (listar manutenções por ID da máquina).
- O envio do WhatsApp deve ser testado com uma manutenção fictícia.

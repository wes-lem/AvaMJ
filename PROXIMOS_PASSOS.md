# Próximos passos – AvaMJ x Proposta / Escopo

Com base na **Proposta de Sistema (Manus)** e no **Escopo do Projeto**, este documento alinha o que já existe no AvaMJ com o que falta para chegar na visão da plataforma.

---

## O que o AvaMJ já tem (base pronta)

| Área | Status atual |
|------|----------------|
| Backend FastAPI + MySQL | ✅ Estrutura, models (User, XP, Badge, Level, GradeHistory) |
| LTI Launch (receber aluno do Moodle) | ✅ Rota `/auth/lti/launch` (parcial) |
| API Gamificação (ranking, XP, medalhas) | ✅ Rotas; retorno ainda mock |
| API Dashboard (notas, resumo) | ✅ Rotas; retorno ainda mock |
| Chatbot (Professor Virtual) | ✅ Rota; integração OpenAI pendente |
| Sincronização notas Moodle (cron) | ✅ APScheduler; `moodle_client` vazio |
| Regras de nível/medalha (nota > 80 = ouro, etc.) | ✅ `level_calculator.py` |
| Frontend (Bootstrap) | ✅ Dashboard, Ranking, Chatbot, base, error |
| Redirecionamento raiz → dashboard | ✅ |

---

## Prioridade 1 – Dados reais (Moodle + Banco)

**Objetivo:** O sistema passar a usar dados reais do Moodle e do banco, em vez de mocks.

1. **Completar integração Moodle (API)**
   - Em `services/moodle_client.py`: implementar chamadas à API REST do Moodle (token no `.env`):
     - Listar cursos; obter notas por curso/usuário; listar usuários de um curso.
   - Documentar no README ou em `config.py` as funções necessárias (ex.: `core_grades_get_grades`, `core_enrol_get_enrolled_users`).

2. **Sincronização de notas (tasks.py)**
   - Implementar `sync_grades_from_moodle()`:
     - Para cada curso configurado, buscar notas via `moodle_client`;
     - Inserir/atualizar em `GradeHistory` (model `analytics`);
     - Opcional: ao registrar nota, chamar `level_calculator` e persistir XP/Badge/Level em `gamification`.

3. **APIs que devolvem dados do banco**
   - **Ranking:** Em `api_gamification.py`, buscar da tabela de níveis/XP (e usuários), ordenar por XP total, retornar lista real.
   - **Dashboard:** Em `api_dashboard.py`, buscar `GradeHistory` por `user_id`, calcular média, evolução, e (se possível) um indicador simples de “tendência” ou projeção (conforme Escopo – “projeção de proficiência”).

4. **Frontend – gráficos com dados reais**
   - Em `dashboard_aluno.html` / `charts.js`: consumir `/api/dashboard/user/{id}/grades` e `/summary`, preencher gráficos (Chart.js) com notas e evolução.

**Entregável:** Aluno que vem do Moodle (LTI) vê seu ranking e seu dashboard com notas reais sincronizadas.

---

## Prioridade 2 – Autenticação e perfis

**Objetivo:** Saber quem está logado e exibir apenas o que é permitido para aquele perfil (Proposta: Aluno, Professor, Coordenador, Gestor, Admin).

1. **Sessão após LTI**
   - No `auth_lti.py`: ao processar o launch, criar sessão (cookie ou JWT) com `user_id`, `email`, `nome`, e **perfil** (inicialmente “aluno” para quem vem do Moodle).
   - Definir como o Moodle envia o perfil (custom claim, role, etc.) ou manter um mapeamento no AvaMJ (ex.: tabela `users` com campo `role`).

2. **Perfis no banco**
   - Incluir em `User` (ou tabela de perfis) o campo `role`: `aluno | professor | coordenador | gestor | admin`.
   - Rotas que hoje usam `user_id` fixo devem passar a usar o usuário da sessão.

3. **Rotas protegidas**
   - Middleware ou dependency que exige sessão válida nas páginas `/dashboard`, `/ranking`, `/chatbot` e nas APIs correspondentes.
   - Opcional: restringir por perfil (ex.: dashboard de gestor só para `gestor` e `admin`).

**Entregável:** Acesso controlado por login (LTI) e telas/APIs respeitando perfil.

---

## Prioridade 3 – Professor Virtual (IA) de verdade

**Objetivo:** Chatbot que realmente tira dúvidas, em linguagem adequada ao 5º ano (Escopo e Proposta).

1. **Integrar OpenAI ou LLM brasileiro**
   - Em `services/ai_agent.py`: usar `OPENAI_API_KEY` (ou API de LLM brasileiro) com prompt de sistema definindo o “Professor Virtual”:
     - Linguagem simples, adequada ao 5º ano;
     - Foco em LP e Matemática, BNCC/SAEB;
     - Não dar resposta pronta; guiar o raciocínio (resolução guiada).

2. **Contexto do aluno (opcional mas importante)**
   - Enviar para a IA: últimas notas por habilidade/descritor (se tiver no banco), turma, ano. Assim o agente pode “sugerir próximos passos” e atividades (conforme Escopo).

3. **Relatório de dúvidas para o professor**
   - Salvar em banco (ex.: tabela `chat_messages` ou `doubt_log`) as dúvidas mais frequentes por turma/conteúdo; rota ou tela para o professor/coordenação ver (Escopo – “mapeamento de dúvidas”).

**Entregável:** Chat que responde com IA educacional e, se possível, insumos para o professor.

---

## Prioridade 4 – Gamificação alinhada ao SAEB

**Objetivo:** Medalhas e missões por descritor/habilidade (Proposta: “Mestre da Inferência”, “Campeão das Frações”, etc.).

1. **Badges por competência/descritor**
   - Estender modelo `Badge` (ou criar tabela de “tipos de badge”) com descritor SAEB / habilidade.
   - `level_calculator` ou serviço equivalente: ao atingir critério (ex.: nota ≥ X em atividade do descritor Y), conceder badge e XP.

2. **Missões e trilhas no backend**
   - Modelo “Missão” (nome, descritor, tipo, prazo) e “Progresso da missão” por aluno; API para listar missões ativas e concluídas.
   - Ranking cooperativo (por turma/equipe), conforme Proposta: evitar ranking punitivo; destacar superação pessoal e equipe.

3. **Frontend**
   - Ranking já existe; alimentar com dados reais (Prioridade 1).
   - Tela ou bloco “Minhas medalhas” e “Missões da semana” consumindo as novas APIs.

**Entregável:** Gamificação com medalhas por habilidade e missões, refletida no ranking e nas telas.

---

## Prioridade 5 – Painéis por perfil (Gestor, Coordenador, Professor)

**Objetivo:** Dashboards diferentes conforme o perfil (Proposta e Escopo).

1. **Gestor**
   - Indicadores por escola (se houver multi-escola), evolução IDEB simulada, mapas de risco (ex.: alunos com baixa participação ou nota em queda).
   - APIs: agregar por escola/turma a partir de `GradeHistory` e de uso (se tiver log de acesso).

2. **Coordenador**
   - Desempenho por turma, engajamento, uso da plataforma; listagem de alunos em risco.
   - Reuso de APIs do dashboard + filtros por turma/escola.

3. **Professor**
   - Dificuldades por habilidade/descritor, sugestão de reensino, relatório individual do aluno (já encaminhado pelo Escopo).
   - APIs: notas e evolução por aluno/turma; relatório de dúvidas do chatbot (Prioridade 3).

4. **Frontend**
   - Novas telas ou um mesmo “dashboard” que muda conforme `role` (gestor/coordenador/professor), cada um com seus widgets e gráficos.

**Entregável:** Cada perfil com seu painel útil para decisão pedagógica e de gestão.

---

## Prioridade 6 – Itens mais ligados ao Moodle / Conteúdo

Estes dependem mais do **Moodle** e da **produção de conteúdo** do que do AvaMJ em si; o AvaMJ pode apenas consumir dados via API e exibir resumos.

- **Cursos e trilhas no Moodle:** Reforço SAEB LP e Matemática, trilhas por ano (2º, 5º, 9º) e por proficiência – construção no Moodle; AvaMJ pode listar cursos/trilhas via API e mostrar “próximas atividades” no dashboard.
- **H5P, videoaulas, livro digital, simulados SAEB:** Produção didática e configuração no Moodle; AvaMJ exibe resultados (notas, conclusões) já sincronizados.
- **Formação de 50 professores (24–40h):** Curso no Moodle + certificação; no AvaMJ pode existir apenas link ou área “Formação” e, se houver API, indicador de conclusão.

---

## Ordem sugerida de execução

1. **Prioridade 1** – Dados reais (Moodle + banco + APIs + gráficos).  
2. **Prioridade 2** – Autenticação e perfis (sessão LTI + roles + rotas protegidas).  
3. **Prioridade 3** – Professor Virtual com IA real e relatório de dúvidas.  
4. **Prioridade 4** – Gamificação SAEB (badges por descritor, missões, ranking cooperativo).  
5. **Prioridade 5** – Painéis por perfil (gestor, coordenador, professor).  
6. **Prioridade 6** – Acompanhar entregas do Moodle/conteúdo e integrar via API onde fizer sentido.

---

## Resumo em uma frase

**Próximo passo imediato:** implementar a **integração real com a API do Moodle** (notas e usuários), preencher **GradeHistory** e **gamificação** no banco, e fazer as **APIs de ranking e dashboard** e o **frontend** usarem esses dados; em seguida, fechar **sessão/perfis** e **Professor Virtual com IA**.

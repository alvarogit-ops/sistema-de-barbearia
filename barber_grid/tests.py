"""
Testes automatizados do Barber Grid.

Como rodar (na pasta onde está o manage.py, com o venv ativado):

    python manage.py test barber_grid

Organização:
    1. AgendamentoTests          -> cliente agenda (e o que o sistema recusa)
    2. ConflitoHorarioTests      -> dois agendamentos no mesmo horário
    3. HorariosDisponiveisTests  -> a lista de horários livres de um dia
    4. CancelamentoTests         -> cliente cancela o próprio agendamento
    5. PermissoesTests           -> quem pode (ou não) abrir cada página
    6. PainelBarbeiroTests       -> agenda, confirmar/cancelar, serviços
    7. AutenticacaoTests         -> registro, login e logout
    8. MinhasReservasTests       -> início e "Minhas reservas"
    9. ProblemasConhecidosTests  -> falhas reais do sistema, ainda não corrigidas

Sobre a classe 9: cada teste ali descreve o comportamento CORRETO, mas está
marcado com @expectedFailure porque o sistema ainda não funciona assim.
Quando você corrigir o problema, o teste vai avisar "unexpected success":
é só apagar a linha @unittest.expectedFailure daquele teste.
"""

import datetime
import unittest
from datetime import time, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.db import IntegrityError, transaction
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import (
    Agendamento,
    BloqueioHorario,
    Cliente,
    DIAS_FERIADO,
    HorariodeFuncionamento,
    Servico,
)


# ---------------------------------------------------------------------------
# Funções auxiliares para escolher datas que nunca "envelhecem"
# ---------------------------------------------------------------------------

def proximo_dia_util(minimo_dias=7):
    """Um dia de segunda a sexta, no futuro, que não seja feriado."""
    dia = timezone.localdate() + timedelta(days=minimo_dias)
    while dia.weekday() >= 5 or (dia.month, dia.day) in DIAS_FERIADO:
        dia += timedelta(days=1)
    return dia


def proximo_domingo():
    dia = timezone.localdate() + timedelta(days=1)
    while dia.weekday() != 6:
        dia += timedelta(days=1)
    return dia


def proximo_natal_em_dia_de_semana():
    """25/12 futuro que caia de segunda a sexta (para o teste de feriado
    não ser confundido com um dia em que a barbearia já fecharia)."""
    ano = timezone.localdate().year
    while True:
        dia = datetime.date(ano, 12, 25)
        if dia > timezone.localdate() and dia.weekday() < 5:
            return dia
        ano += 1


# ---------------------------------------------------------------------------
# Base: cria o "cenário" usado por todos os testes
# ---------------------------------------------------------------------------

# Só nos testes: usa um método de senha rápido para a suíte não demorar.
# (No sistema real continua o método seguro padrão do Django.)
@override_settings(
    PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"]
)
class BaseTestCase(TestCase):
    SENHA = "Senha#Forte2026"

    def setUp(self):
        # A view de horários busca exatamente o registro de id=1.
        self.funcionamento = HorariodeFuncionamento.objects.create(
            id=1,
            dia_inicio=0,   # segunda
            dia_fim=5,      # sábado
            horario_inicio=time(8, 0),
            horario_fim=time(18, 0),
        )

        # O sistema procura exatamente o usuário "barbeirofelipe".
        self.barbeiro = User.objects.create_user(
            username="barbeirofelipe",
            email="felipe@teste.com",
            password=self.SENHA,
            first_name="Felipe",
            is_staff=True,
        )

        self.user_cliente = User.objects.create_user(
            username="maria@teste.com",
            email="maria@teste.com",
            password=self.SENHA,
            first_name="Maria",
        )
        self.cliente = Cliente.objects.create(
            usuario=self.user_cliente, telefone="84999990000"
        )

        self.user_outro = User.objects.create_user(
            username="joao@teste.com",
            email="joao@teste.com",
            password=self.SENHA,
            first_name="João",
        )
        self.outro_cliente = Cliente.objects.create(
            usuario=self.user_outro, telefone="84988880000"
        )

        self.servico = Servico.objects.create(
            nome_servico="Corte",
            preco=Decimal("40.00"),
            duracao_minutos=30,
        )

        self.dia = proximo_dia_util()

    # ----- atalhos -----

    def entrar(self, usuario):
        self.client.force_login(usuario)

    def agendar(self, cliente=None, data=None, horario=time(10, 0),
                status="solicitado"):
        """Cria um agendamento direto no banco (sem passar pela tela)."""
        return Agendamento.objects.create(
            cliente=cliente or self.cliente,
            servico=self.servico,
            barbeiro=self.barbeiro,
            data=data or self.dia,
            horario=horario,
            status=status,
        )

    def postar_agendamento(self, data=None, horario="10:00"):
        """Simula o clique em 'Confirmar' na tela de confirmação."""
        data = data or self.dia
        if isinstance(data, datetime.date):
            data = data.isoformat()
        dados = {"data": data}
        if horario is not None:
            dados["horario"] = horario
        return self.client.post(
            reverse("confirmar_agendamento", args=[self.servico.id]), dados
        )

    def url_voltar_agendamento(self):
        return reverse("agendamento", args=[self.servico.id])

    def mensagens(self, resposta):
        return [str(m) for m in get_messages(resposta.wsgi_request)]

    def horarios_do_dia(self, data):
        resposta = self.client.get(
            reverse("horarios_disponiveis"), {"data": data.isoformat()}
        )
        return resposta, resposta.json()["horarios_disponiveis"]


# ---------------------------------------------------------------------------
# 1. Agendamento
# ---------------------------------------------------------------------------

class AgendamentoTests(BaseTestCase):

    def test_cliente_agenda_com_sucesso(self):
        self.entrar(self.user_cliente)

        resposta = self.postar_agendamento()

        self.assertEqual(Agendamento.objects.count(), 1)
        agendamento = Agendamento.objects.get()
        self.assertRedirects(
            resposta,
            reverse("enviado", args=[agendamento.id]),
            fetch_redirect_response=False,
        )
        self.assertEqual(agendamento.cliente, self.cliente)
        self.assertEqual(agendamento.servico, self.servico)
        self.assertEqual(agendamento.barbeiro, self.barbeiro)
        self.assertEqual(agendamento.data, self.dia)
        self.assertEqual(agendamento.horario, time(10, 0))

    def test_agendamento_novo_comeca_como_solicitado(self):
        self.entrar(self.user_cliente)

        self.postar_agendamento()

        self.assertEqual(Agendamento.objects.get().status, "solicitado")

    def test_tela_de_agendamento_abre_para_cliente(self):
        self.entrar(self.user_cliente)

        resposta = self.client.get(self.url_voltar_agendamento())

        self.assertEqual(resposta.status_code, 200)

    def test_tela_de_confirmacao_abre_com_data_e_horario(self):
        self.entrar(self.user_cliente)

        resposta = self.client.get(
            reverse("confirmar_agendamento", args=[self.servico.id]),
            {"data": self.dia.isoformat(), "horario": "10:00"},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context["servico"], self.servico)
        self.assertEqual(resposta.context["horario"], "10:00")

    def test_servico_inexistente_da_404(self):
        self.entrar(self.user_cliente)

        resposta = self.client.get(reverse("agendamento", args=[9999]))

        self.assertEqual(resposta.status_code, 404)

    def test_nao_agenda_data_passada(self):
        self.entrar(self.user_cliente)
        ontem = timezone.localdate() - timedelta(days=1)

        resposta = self.postar_agendamento(data=ontem)

        self.assertRedirects(
            resposta, self.url_voltar_agendamento(),
            fetch_redirect_response=False,
        )
        self.assertEqual(Agendamento.objects.count(), 0)
        self.assertIn(
            "Não é possível agendar para uma data passada.",
            self.mensagens(resposta),
        )

    def test_nao_agenda_horario_que_ja_passou(self):
        self.entrar(self.user_cliente)
        uma_hora_atras = timezone.localtime() - timedelta(hours=1)

        resposta = self.postar_agendamento(
            data=uma_hora_atras.date(),
            horario=uma_hora_atras.strftime("%H:%M"),
        )

        self.assertRedirects(
            resposta, self.url_voltar_agendamento(),
            fetch_redirect_response=False,
        )
        self.assertEqual(Agendamento.objects.count(), 0)

    def test_nao_agenda_em_feriado_nacional(self):
        self.entrar(self.user_cliente)

        resposta = self.postar_agendamento(
            data=proximo_natal_em_dia_de_semana()
        )

        self.assertRedirects(
            resposta, self.url_voltar_agendamento(),
            fetch_redirect_response=False,
        )
        self.assertEqual(Agendamento.objects.count(), 0)
        self.assertIn(
            "Não é possível agendar em um feriado nacional.",
            self.mensagens(resposta),
        )

    def test_nao_agenda_com_data_invalida(self):
        self.entrar(self.user_cliente)

        resposta = self.postar_agendamento(data="isso-nao-e-data")

        self.assertRedirects(
            resposta, self.url_voltar_agendamento(),
            fetch_redirect_response=False,
        )
        self.assertEqual(Agendamento.objects.count(), 0)

    def test_nao_agenda_sem_horario(self):
        self.entrar(self.user_cliente)

        resposta = self.postar_agendamento(horario=None)

        self.assertRedirects(
            resposta, self.url_voltar_agendamento(),
            fetch_redirect_response=False,
        )
        self.assertEqual(Agendamento.objects.count(), 0)

    def test_barbeiro_nao_agenda_como_cliente(self):
        self.entrar(self.barbeiro)

        resposta = self.postar_agendamento()

        self.assertRedirects(
            resposta, reverse("inicio"), fetch_redirect_response=False
        )
        self.assertEqual(Agendamento.objects.count(), 0)

    def test_usuario_sem_cadastro_de_cliente_nao_agenda(self):
        sem_perfil = User.objects.create_user(
            username="sem@perfil.com", password=self.SENHA
        )
        self.entrar(sem_perfil)

        resposta = self.postar_agendamento()

        self.assertRedirects(
            resposta, reverse("inicio"), fetch_redirect_response=False
        )
        self.assertEqual(Agendamento.objects.count(), 0)

    def test_visitante_sem_login_nao_agenda(self):
        resposta = self.postar_agendamento()

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/login", resposta.url)
        self.assertEqual(Agendamento.objects.count(), 0)


# ---------------------------------------------------------------------------
# 2. Conflito de horário
# ---------------------------------------------------------------------------

class ConflitoHorarioTests(BaseTestCase):

    def test_horario_ocupado_nao_aceita_segundo_agendamento(self):
        self.agendar(cliente=self.outro_cliente, horario=time(10, 0))
        self.entrar(self.user_cliente)

        resposta = self.postar_agendamento(horario="10:00")

        self.assertRedirects(
            resposta, self.url_voltar_agendamento(),
            fetch_redirect_response=False,
        )
        self.assertEqual(Agendamento.objects.count(), 1)
        self.assertIn("Este horário já está agendado.", self.mensagens(resposta))

    def test_horario_confirmado_tambem_bloqueia(self):
        self.agendar(
            cliente=self.outro_cliente, horario=time(10, 0), status="confirmado"
        )
        self.entrar(self.user_cliente)

        self.postar_agendamento(horario="10:00")

        self.assertEqual(Agendamento.objects.count(), 1)

    def test_horario_cancelado_pode_ser_agendado_de_novo(self):
        self.agendar(
            cliente=self.outro_cliente, horario=time(10, 0), status="cancelado"
        )
        self.entrar(self.user_cliente)

        resposta = self.postar_agendamento(horario="10:00")

        self.assertEqual(Agendamento.objects.count(), 2)
        novo = Agendamento.objects.get(cliente=self.cliente)
        self.assertRedirects(
            resposta,
            reverse("enviado", args=[novo.id]),
            fetch_redirect_response=False,
        )

    def test_horarios_diferentes_no_mesmo_dia_sao_permitidos(self):
        self.agendar(cliente=self.outro_cliente, horario=time(10, 0))
        self.entrar(self.user_cliente)

        self.postar_agendamento(horario="10:30")

        self.assertEqual(Agendamento.objects.count(), 2)

    def test_mesmo_horario_em_dias_diferentes_e_permitido(self):
        self.agendar(cliente=self.outro_cliente, horario=time(10, 0))
        self.entrar(self.user_cliente)
        outro_dia = proximo_dia_util(minimo_dias=14)
        if outro_dia == self.dia:
            outro_dia = proximo_dia_util(minimo_dias=15)

        self.postar_agendamento(data=outro_dia, horario="10:00")

        self.assertEqual(Agendamento.objects.count(), 2)

    def test_banco_de_dados_impede_dois_agendamentos_ativos_iguais(self):
        self.agendar(cliente=self.cliente, horario=time(10, 0))

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.agendar(cliente=self.outro_cliente, horario=time(10, 0))

    def test_banco_de_dados_aceita_cancelado_junto_com_ativo(self):
        self.agendar(cliente=self.cliente, horario=time(10, 0),
                     status="cancelado")

        self.agendar(cliente=self.outro_cliente, horario=time(10, 0))

        self.assertEqual(Agendamento.objects.count(), 2)


# ---------------------------------------------------------------------------
# 3. Horários disponíveis
# ---------------------------------------------------------------------------

class HorariosDisponiveisTests(BaseTestCase):

    def test_lista_horarios_de_meia_em_meia_hora(self):
        resposta, horarios = self.horarios_do_dia(self.dia)

        self.assertEqual(resposta.status_code, 200)
        for esperado in ("08:00", "08:30", "11:30", "13:00", "17:30"):
            self.assertIn(esperado, horarios)

    def test_nao_oferece_horario_de_almoco_nem_apos_o_expediente(self):
        _, horarios = self.horarios_do_dia(self.dia)

        for proibido in ("12:00", "12:30", "18:00"):
            self.assertNotIn(proibido, horarios)

    def test_horario_ocupado_some_da_lista(self):
        self.agendar(horario=time(9, 0))

        _, horarios = self.horarios_do_dia(self.dia)

        self.assertNotIn("09:00", horarios)
        self.assertIn("09:30", horarios)

    def test_horario_cancelado_volta_para_a_lista(self):
        self.agendar(horario=time(9, 0), status="cancelado")

        _, horarios = self.horarios_do_dia(self.dia)

        self.assertIn("09:00", horarios)

    def test_domingo_nao_tem_horarios(self):
        resposta, horarios = self.horarios_do_dia(proximo_domingo())

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(horarios, [])

    def test_feriado_nao_tem_horarios(self):
        resposta, horarios = self.horarios_do_dia(
            proximo_natal_em_dia_de_semana()
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(horarios, [])

    def test_data_passada_nao_tem_horarios(self):
        ontem = timezone.localdate() - timedelta(days=1)

        resposta, horarios = self.horarios_do_dia(ontem)

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(horarios, [])

    def test_hoje_nao_oferece_horarios_que_ja_passaram(self):
        agora = timezone.localtime()

        _, horarios = self.horarios_do_dia(agora.date())

        for horario in horarios:
            self.assertGreater(horario, agora.strftime("%H:%M"))

    def test_data_invalida_retorna_erro_400(self):
        resposta = self.client.get(
            reverse("horarios_disponiveis"), {"data": "abc"}
        )

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(resposta.json()["horarios_disponiveis"], [])

    def test_sem_data_retorna_lista_vazia(self):
        resposta = self.client.get(reverse("horarios_disponiveis"))

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.json()["horarios_disponiveis"], [])


# ---------------------------------------------------------------------------
# 4. Cancelamento
# ---------------------------------------------------------------------------

class CancelamentoTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.agendamento = self.agendar(horario=time(10, 0))
        self.url = reverse("cancelar_agendamento", args=[self.agendamento.id])

    def test_cliente_cancela_o_proprio_agendamento(self):
        self.entrar(self.user_cliente)

        resposta = self.client.post(self.url)

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(
            resposta.json(), {"sucesso": True, "status": "Cancelado"}
        )
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.status, "cancelado")

    def test_horario_cancelado_fica_livre_para_outro_cliente(self):
        self.entrar(self.user_cliente)
        self.client.post(self.url)

        # Se o horário não tivesse sido liberado, isto daria IntegrityError.
        self.agendar(cliente=self.outro_cliente, horario=time(10, 0))

        self.assertEqual(
            Agendamento.objects.exclude(status="cancelado").count(), 1
        )

    def test_cliente_nao_cancela_agendamento_de_outro(self):
        self.entrar(self.user_outro)

        resposta = self.client.post(self.url)

        self.assertEqual(resposta.status_code, 404)
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.status, "solicitado")

    def test_barbeiro_nao_cancela_por_esta_rota_de_cliente(self):
        self.entrar(self.barbeiro)

        resposta = self.client.post(self.url)

        self.assertEqual(resposta.status_code, 404)
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.status, "solicitado")

    def test_cancelar_por_get_nao_e_permitido(self):
        self.entrar(self.user_cliente)

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 405)
        self.assertEqual(resposta.json(), {"sucesso": False})
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.status, "solicitado")

    def test_visitante_sem_login_nao_cancela(self):
        resposta = self.client.post(self.url)

        self.assertEqual(resposta.status_code, 302)
        self.assertIn("/login", resposta.url)
        self.agendamento.refresh_from_db()
        self.assertEqual(self.agendamento.status, "solicitado")


# ---------------------------------------------------------------------------
# 5. Permissões
# ---------------------------------------------------------------------------

class PermissoesTests(BaseTestCase):

    def test_paginas_de_cliente_exigem_login(self):
        paginas = [
            reverse("inicio"),
            reverse("pagina_servicos"),
            reverse("usuario_historico"),
            reverse("editar_perfil"),
            reverse("alterar_senha"),
            reverse("agendamento", args=[self.servico.id]),
            reverse("confirmar_agendamento", args=[self.servico.id]),
        ]
        for url in paginas:
            with self.subTest(url=url):
                resposta = self.client.get(url)
                self.assertEqual(resposta.status_code, 302)
                self.assertIn("/login", resposta.url)

    def test_paginas_do_barbeiro_exigem_login(self):
        paginas = [
            reverse("painel_admin"),
            reverse("admin_confirmar"),
            reverse("editar_perfil_admin"),
        ]
        for url in paginas:
            with self.subTest(url=url):
                resposta = self.client.get(url)
                self.assertEqual(resposta.status_code, 302)
                self.assertIn("/login", resposta.url)

    def test_cliente_nao_acessa_painel_do_barbeiro(self):
        self.entrar(self.user_cliente)

        for nome in ("painel_admin", "admin_confirmar"):
            with self.subTest(pagina=nome):
                resposta = self.client.get(reverse(nome))
                self.assertRedirects(
                    resposta, reverse("inicio"),
                    fetch_redirect_response=False,
                )

    def test_cliente_nao_acessa_cadastros_de_staff(self):
        self.entrar(self.user_cliente)

        paginas = [
            reverse("servico"),
            reverse("novo_servico"),
            reverse("dados_negocio"),
            reverse("alterar_senha_admin"),
        ]
        for url in paginas:
            with self.subTest(url=url):
                resposta = self.client.get(url)
                self.assertEqual(resposta.status_code, 302)
                self.assertIn("login", resposta.url)

    def test_outro_funcionario_nao_acessa_painel_do_felipe(self):
        outro = User.objects.create_user(
            username="outrobarbeiro", password=self.SENHA, is_staff=True
        )
        self.entrar(outro)

        resposta = self.client.get(reverse("painel_admin"))

        self.assertRedirects(
            resposta, reverse("inicio"), fetch_redirect_response=False
        )

    def test_felipe_acessa_todas_as_paginas_do_painel(self):
        self.entrar(self.barbeiro)

        paginas = [
            reverse("painel_admin"),
            reverse("admin_confirmar"),
            reverse("servico"),
            reverse("novo_servico"),
            reverse("dados_negocio"),
            reverse("editar_perfil_admin"),
            reverse("alterar_senha_admin"),
        ]
        for url in paginas:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_barbeiro_e_enviado_para_o_perfil_de_admin(self):
        self.entrar(self.barbeiro)

        resposta = self.client.get(reverse("editar_perfil"))

        self.assertRedirects(
            resposta, reverse("editar_perfil_admin"),
            fetch_redirect_response=False,
        )

    def test_cliente_nao_abre_perfil_de_admin(self):
        self.entrar(self.user_cliente)

        resposta = self.client.get(reverse("editar_perfil_admin"))

        self.assertRedirects(
            resposta, reverse("inicio"), fetch_redirect_response=False
        )


# ---------------------------------------------------------------------------
# 6. Painel do barbeiro
# ---------------------------------------------------------------------------

class PainelBarbeiroTests(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.entrar(self.barbeiro)

    def _acao(self, agendamento, acao):
        return self.client.post(
            reverse("admin_confirmar"),
            {"agendamento_id": agendamento.id, "acao": acao},
        )

    def test_agenda_mostra_so_os_agendamentos_do_dia_escolhido(self):
        do_dia = self.agendar(horario=time(9, 0))
        outro_dia = proximo_dia_util(minimo_dias=20)
        if outro_dia == self.dia:
            outro_dia = proximo_dia_util(minimo_dias=21)
        self.agendar(data=outro_dia, horario=time(9, 0))

        resposta = self.client.get(
            reverse("painel_admin"), {"data": self.dia.isoformat()}
        )

        self.assertEqual(list(resposta.context["agendamentos"]), [do_dia])

    def test_agenda_filtra_por_status(self):
        self.agendar(horario=time(9, 0), status="solicitado")
        confirmado = self.agendar(horario=time(9, 30), status="confirmado")

        resposta = self.client.get(
            reverse("painel_admin"),
            {"data": self.dia.isoformat(), "status": "confirmado"},
        )

        self.assertEqual(list(resposta.context["agendamentos"]), [confirmado])

    def test_agenda_ordenada_por_horario(self):
        tarde = self.agendar(horario=time(15, 0))
        manha = self.agendar(horario=time(9, 0))

        resposta = self.client.get(
            reverse("painel_admin"), {"data": self.dia.isoformat()}
        )

        self.assertEqual(list(resposta.context["agendamentos"]), [manha, tarde])

    def test_barbeiro_confirma_agendamento(self):
        agendamento = self.agendar()

        resposta = self._acao(agendamento, "confirmar")

        self.assertRedirects(
            resposta, reverse("admin_confirmar"),
            fetch_redirect_response=False,
        )
        agendamento.refresh_from_db()
        self.assertEqual(agendamento.status, "confirmado")

    def test_barbeiro_cancela_agendamento(self):
        agendamento = self.agendar()

        self._acao(agendamento, "cancelar")

        agendamento.refresh_from_db()
        self.assertEqual(agendamento.status, "cancelado")

    def test_acao_invalida_nao_altera_o_agendamento(self):
        agendamento = self.agendar()

        self._acao(agendamento, "apagar-tudo")

        agendamento.refresh_from_db()
        self.assertEqual(agendamento.status, "solicitado")

    def test_agendamento_ja_confirmado_nao_muda_de_novo(self):
        agendamento = self.agendar(status="confirmado")

        self._acao(agendamento, "cancelar")

        agendamento.refresh_from_db()
        self.assertEqual(agendamento.status, "confirmado")

    def test_lista_a_confirmar_mostra_so_solicitados(self):
        solicitado = self.agendar(horario=time(9, 0), status="solicitado")
        self.agendar(horario=time(9, 30), status="confirmado")
        self.agendar(horario=time(10, 0), status="cancelado")

        resposta = self.client.get(reverse("admin_confirmar"))

        self.assertEqual(list(resposta.context["agendamentos"]), [solicitado])

    def test_cliente_nao_consegue_confirmar_agendamento(self):
        agendamento = self.agendar()
        self.client.logout()
        self.entrar(self.user_cliente)

        resposta = self._acao(agendamento, "confirmar")

        self.assertRedirects(
            resposta, reverse("inicio"), fetch_redirect_response=False
        )
        agendamento.refresh_from_db()
        self.assertEqual(agendamento.status, "solicitado")

    def test_barbeiro_cadastra_servico(self):
        resposta = self.client.post(
            reverse("novo_servico"),
            {
                "nome_servico": "Barba",
                "preco": "25.50",
                "duracao_minutos": "20",
                "ativo": "on",
            },
        )

        self.assertRedirects(
            resposta, reverse("servico"), fetch_redirect_response=False
        )
        barba = Servico.objects.get(nome_servico="Barba")
        self.assertEqual(barba.preco, Decimal("25.50"))
        self.assertEqual(barba.duracao_minutos, 20)
        self.assertTrue(barba.ativo)

    def test_cadastro_de_servico_rejeita_dados_invalidos(self):
        antes = Servico.objects.count()

        dados_ruins = [
            {"nome_servico": "", "preco": "10", "duracao_minutos": "10"},
            {"nome_servico": "X", "preco": "-5", "duracao_minutos": "10"},
            {"nome_servico": "X", "preco": "10", "duracao_minutos": "0"},
            {"nome_servico": "X", "preco": "abc", "duracao_minutos": "10"},
        ]
        for dados in dados_ruins:
            with self.subTest(dados=dados):
                resposta = self.client.post(reverse("novo_servico"), dados)
                self.assertEqual(resposta.status_code, 200)

        self.assertEqual(Servico.objects.count(), antes)

    def test_cliente_nao_cadastra_servico(self):
        self.client.logout()
        self.entrar(self.user_cliente)
        antes = Servico.objects.count()

        resposta = self.client.post(
            reverse("novo_servico"),
            {"nome_servico": "Golpe", "preco": "1", "duracao_minutos": "1"},
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertEqual(Servico.objects.count(), antes)

    def test_lista_de_servicos_filtra_ativos_e_inativos(self):
        inativo = Servico.objects.create(
            nome_servico="Antigo", preco=Decimal("10"), duracao_minutos=10,
            ativo=False,
        )

        so_ativos = self.client.get(reverse("servico"), {"ativo": "true"})
        so_inativos = self.client.get(reverse("servico"), {"ativo": "false"})

        self.assertEqual(list(so_ativos.context["servicos"]), [self.servico])
        self.assertEqual(list(so_inativos.context["servicos"]), [inativo])


# ---------------------------------------------------------------------------
# 7. Autenticação
# ---------------------------------------------------------------------------

class AutenticacaoTests(BaseTestCase):

    def _dados_registro(self, **extra):
        dados = {
            "nome": "Carlos Silva",
            "telefone": "84977770000",
            "email": "carlos@teste.com",
            "senha": "Barbearia#2026x",
        }
        dados.update(extra)
        return dados

    def test_registro_cria_usuario_e_cliente(self):
        resposta = self.client.post(reverse("registro"), self._dados_registro())

        self.assertRedirects(
            resposta, reverse("login"), fetch_redirect_response=False
        )
        usuario = User.objects.get(email="carlos@teste.com")
        self.assertEqual(usuario.username, "carlos@teste.com")
        self.assertEqual(usuario.first_name, "Carlos Silva")
        self.assertTrue(usuario.check_password("Barbearia#2026x"))
        self.assertFalse(usuario.is_staff)
        self.assertEqual(usuario.cliente.telefone, "84977770000")

    def test_registro_exige_todos_os_campos(self):
        for campo in ("nome", "telefone", "email", "senha"):
            with self.subTest(campo=campo):
                resposta = self.client.post(
                    reverse("registro"), self._dados_registro(**{campo: ""})
                )
                self.assertEqual(resposta.status_code, 200)
        self.assertFalse(User.objects.filter(email="carlos@teste.com").exists())

    def test_registro_recusa_email_ja_cadastrado(self):
        antes = User.objects.count()

        resposta = self.client.post(
            reverse("registro"),
            self._dados_registro(email="maria@teste.com"),
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(User.objects.count(), antes)

    def test_registro_recusa_senha_fraca(self):
        resposta = self.client.post(
            reverse("registro"), self._dados_registro(senha="123")
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(User.objects.filter(email="carlos@teste.com").exists())

    def test_login_de_cliente_vai_para_lista_de_servicos(self):
        resposta = self.client.post(
            reverse("login"),
            {"username": "maria@teste.com", "senha": self.SENHA},
        )

        self.assertRedirects(
            resposta, reverse("pagina_servicos"),
            fetch_redirect_response=False,
        )

    def test_login_do_barbeiro_vai_para_o_painel(self):
        resposta = self.client.post(
            reverse("login"),
            {"username": "barbeirofelipe", "senha": self.SENHA},
        )

        self.assertRedirects(
            resposta, reverse("painel_admin"), fetch_redirect_response=False
        )

    def test_login_com_senha_errada_nao_entra(self):
        resposta = self.client.post(
            reverse("login"),
            {"username": "maria@teste.com", "senha": "errada"},
        )

        self.assertEqual(resposta.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_so_funciona_por_post(self):
        self.entrar(self.user_cliente)

        self.client.get(reverse("logout"))
        self.assertIn("_auth_user_id", self.client.session)

        resposta = self.client.post(reverse("logout"))
        self.assertRedirects(
            resposta, reverse("login"), fetch_redirect_response=False
        )
        self.assertNotIn("_auth_user_id", self.client.session)


# ---------------------------------------------------------------------------
# 8. Início e "Minhas reservas"
# ---------------------------------------------------------------------------

class MinhasReservasTests(BaseTestCase):

    def test_inicio_mostra_a_proxima_reserva_ativa(self):
        cancelado = self.agendar(horario=time(9, 0), status="cancelado")
        proximo = self.agendar(horario=time(11, 0))
        self.agendar(horario=time(15, 0))
        self.entrar(self.user_cliente)

        resposta = self.client.get(reverse("inicio"))

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta.context["proxima_reserva"], proximo)
        self.assertNotEqual(resposta.context["proxima_reserva"], cancelado)

    def test_inicio_sem_reservas(self):
        self.entrar(self.user_cliente)

        resposta = self.client.get(reverse("inicio"))

        self.assertIsNone(resposta.context["proxima_reserva"])

    def test_inicio_nao_mostra_reserva_de_outro_cliente(self):
        self.agendar(cliente=self.outro_cliente)
        self.entrar(self.user_cliente)

        resposta = self.client.get(reverse("inicio"))

        self.assertIsNone(resposta.context["proxima_reserva"])

    def test_minhas_reservas_separa_proximas_e_historico(self):
        futuro = self.agendar(horario=time(10, 0))
        passado = self.agendar(
            data=timezone.localdate() - timedelta(days=10),
            horario=time(10, 0),
        )
        self.agendar(cliente=self.outro_cliente, horario=time(11, 0))
        self.entrar(self.user_cliente)

        resposta = self.client.get(reverse("usuario_historico"))

        self.assertEqual(resposta.context["proximos"], [futuro])
        self.assertEqual(resposta.context["historico"], [passado])

    def test_lista_de_servicos_abre_para_cliente(self):
        self.entrar(self.user_cliente)

        resposta = self.client.get(reverse("pagina_servicos"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Corte")


# ---------------------------------------------------------------------------
# 9. Problemas conhecidos (ainda NÃO corrigidos no sistema)
#
# Cada teste abaixo descreve o comportamento correto. Enquanto o sistema não
# for corrigido, ele "falha como esperado" e a suíte continua verde.
# Quando corrigir o problema, apague a linha @unittest.expectedFailure.
# ---------------------------------------------------------------------------

class ProblemasConhecidosTests(BaseTestCase):

    @unittest.expectedFailure
    def test_detalhe_do_agendamento_exige_login(self):
        agendamento = self.agendar()

        resposta = self.client.get(
            reverse("detalhe_agendamento", args=[agendamento.id])
        )

        self.assertEqual(resposta.status_code, 302)

    @unittest.expectedFailure
    def test_cliente_nao_ve_detalhe_de_agendamento_de_outro(self):
        agendamento = self.agendar(cliente=self.outro_cliente)
        self.entrar(self.user_cliente)

        resposta = self.client.get(
            reverse("detalhe_agendamento", args=[agendamento.id])
        )

        self.assertIn(resposta.status_code, (403, 404))

    @unittest.expectedFailure
    def test_cliente_nao_ve_tela_enviado_de_outro(self):
        agendamento = self.agendar(cliente=self.outro_cliente)
        self.entrar(self.user_cliente)

        resposta = self.client.get(
            reverse("enviado", args=[agendamento.id])
        )

        self.assertIn(resposta.status_code, (403, 404))

    @unittest.expectedFailure
    def test_historico_geral_nao_e_publico(self):
        self.agendar()

        resposta = self.client.get(reverse("historico_agendamentos"))

        self.assertEqual(resposta.status_code, 302)

    @unittest.expectedFailure
    def test_servico_inativo_nao_aparece_para_o_cliente(self):
        Servico.objects.create(
            nome_servico="Servico Desativado", preco=Decimal("10"),
            duracao_minutos=10, ativo=False,
        )
        self.entrar(self.user_cliente)

        resposta = self.client.get(reverse("pagina_servicos"))

        self.assertNotContains(resposta, "Servico Desativado")

    @unittest.expectedFailure
    def test_nao_agenda_servico_inativo(self):
        self.servico.ativo = False
        self.servico.save()
        self.entrar(self.user_cliente)

        self.postar_agendamento()

        self.assertEqual(Agendamento.objects.count(), 0)

    @unittest.expectedFailure
    def test_inicio_nao_quebra_para_usuario_sem_cadastro_de_cliente(self):
        sem_perfil = User.objects.create_user(
            username="sem@perfil.com", password=self.SENHA
        )
        self.entrar(sem_perfil)

        resposta = self.client.get(reverse("inicio"))

        self.assertEqual(resposta.status_code, 200)

    @unittest.expectedFailure
    def test_horarios_nao_quebram_sem_horario_de_funcionamento(self):
        HorariodeFuncionamento.objects.all().delete()

        resposta = self.client.get(
            reverse("horarios_disponiveis"), {"data": self.dia.isoformat()}
        )

        self.assertEqual(resposta.status_code, 200)

    @unittest.expectedFailure
    def test_bloqueio_de_horario_remove_horarios_da_lista(self):
        BloqueioHorario.objects.create(
            data_inicio=self.dia,
            data_fim=self.dia,
            horario_inicio=time(14, 0),
            horario_fim=time(16, 0),
            motivo="Curso",
        )

        _, horarios = self.horarios_do_dia(self.dia)

        self.assertNotIn("14:00", horarios)
        self.assertNotIn("15:30", horarios)
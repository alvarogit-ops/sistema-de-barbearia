from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import AgendamentoForm, ClienteForm, ServicoForm
from .models import Agendamento, Cliente, Servico


class CadastroClientesTests(TestCase):
    def setUp(self):
        self.barbeiro = User.objects.create_user(
            username='barbeiro',
            email='barbeiro@example.com',
            password='senha-segura',
            is_staff=True,
        )
        self.cliente_app = User.objects.create_user(
            username='cliente',
            email='cliente@example.com',
            password='senha-segura',
        )
        self.url = reverse('clientes')

    def test_formulario_exige_nome_e_contato(self):
        form = ClienteForm(data={
            'nome_cliente': '   ',
            'sobrenome_cliente': '',
            'telefone': '',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('nome_cliente', form.errors)
        self.assertIn('telefone', form.errors)

    def test_barbeiro_cadastra_cliente_e_ve_na_lista(self):
        self.client.force_login(self.barbeiro)

        resposta = self.client.post(self.url, {
            'nome_cliente': 'João',
            'sobrenome_cliente': 'Silva',
            'telefone': '11999999999',
        }, follow=True)

        self.assertEqual(Cliente.objects.count(), 1)
        cliente = Cliente.objects.get()
        self.assertEqual(cliente.nome_cliente, 'João')
        self.assertEqual(cliente.telefone, '11999999999')
        self.assertContains(resposta, 'João Silva')
        self.assertContains(resposta, '11999999999')
        self.assertContains(resposta, 'Cliente cadastrado com sucesso.')

    def test_barbeiro_visualiza_clientes_cadastrados(self):
        Cliente.objects.create(
            nome_cliente='Maria',
            sobrenome_cliente='Souza',
            telefone='21988887777',
        )
        self.client.force_login(self.barbeiro)

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Maria Souza')
        self.assertContains(resposta, '21988887777')

    def test_cadastro_sem_obrigatorios_nao_cria_cliente(self):
        self.client.force_login(self.barbeiro)

        resposta = self.client.post(self.url, {
            'nome_cliente': '',
            'telefone': '',
        })

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(Cliente.objects.count(), 0)
        self.assertContains(resposta, 'Informe o nome do cliente.')
        self.assertContains(resposta, 'Informe o telefone ou contato do cliente.')

    def test_usuario_sem_permissao_nao_acessa_cadastro(self):
        self.client.force_login(self.cliente_app)

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 403)


class AutenticacaoViewsTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='cliente',
            email='cliente@example.com',
            password='senha-segura',
        )

    def test_login_credenciais_invalidas_mostra_mensagem(self):
        resposta = self.client.post(reverse('login'), {
            'email': 'cliente@example.com',
            'senha': 'errada',
        })

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Credenciais inválidas!')

    def test_registro_senhas_diferentes_nao_cria_usuario(self):
        resposta = self.client.post(reverse('registro'), {
            'nome_usuario': 'novo',
            'email': 'novo@example.com',
            'telefone': '11999999999',
            'senha': 'abc12345',
            'confirmar_senha': 'outra',
        })

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(User.objects.filter(email='novo@example.com').count(), 0)
        self.assertContains(resposta, 'As senhas não são iguais!')

    def test_registro_username_duplicado_nao_gera_500(self):
        resposta = self.client.post(reverse('registro'), {
            'nome_usuario': 'cliente',
            'email': 'outro@example.com',
            'telefone': '11999999999',
            'senha': 'abc12345',
            'confirmar_senha': 'abc12345',
        })

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Este nome de usuário já está cadastrado!')

    def test_registro_persiste_telefone_e_redireciona(self):
        resposta = self.client.post(reverse('registro'), {
            'nome_usuario': 'maria',
            'email': 'maria@example.com',
            'telefone': '21988887777',
            'senha': 'abc12345',
            'confirmar_senha': 'abc12345',
        }, follow=True)

        self.assertRedirects(resposta, reverse('login'))
        user = User.objects.get(email='maria@example.com')
        cliente = Cliente.objects.get(user=user)
        self.assertEqual(cliente.telefone, '21988887777')
        self.assertContains(resposta, 'Conta criada com sucesso')

    def test_home_lista_agendamentos_do_usuario(self):
        cliente = Cliente.objects.create(
            user=self.usuario,
            nome_cliente='cliente',
            telefone='11999999999',
        )
        servico = Servico.objects.create(
            nome_servico='Corte',
            preco='40.00',
            duracao_minutos=30,
        )
        agendamento = Agendamento.objects.create(
            usuario=cliente,
            data_agendamento='2026-09-01',
            horario_agendamento='10:00:00',
        )
        agendamento.servico.add(servico)

        outro = Cliente.objects.create(nome_cliente='Outro', telefone='11000000000')
        outro_agendamento = Agendamento.objects.create(
            usuario=outro,
            data_agendamento='2026-09-02',
            horario_agendamento='11:00:00',
        )
        outro_agendamento.servico.add(servico)

        self.client.force_login(self.usuario)
        resposta = self.client.get(reverse('index'))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Corte')
        self.assertEqual(list(resposta.context['agendamentos']), [agendamento])

    def test_logout_get_nao_encerra_sessao(self):
        self.client.force_login(self.usuario)

        resposta = self.client.get(reverse('logout'))

        self.assertEqual(resposta.status_code, 405)
        self.assertTrue(resposta.wsgi_request.user.is_authenticated)


class CadastroServicosTests(TestCase):
    def setUp(self):
        self.barbeiro = User.objects.create_user(
            username='barbeiro',
            email='barbeiro@example.com',
            password='senha-segura',
            is_staff=True,
        )
        self.cliente_app = User.objects.create_user(
            username='cliente',
            email='cliente@example.com',
            password='senha-segura',
        )
        self.url = reverse('servicos')

    def test_formulario_exige_nome_preco_e_duracao(self):
        form = ServicoForm(data={
            'nome_servico': '   ',
            'preco': '',
            'duracao_minutos': '',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('nome_servico', form.errors)
        self.assertIn('preco', form.errors)
        self.assertIn('duracao_minutos', form.errors)

    def test_formulario_rejeita_preco_e_duracao_invalidos(self):
        form = ServicoForm(data={
            'nome_servico': 'Barba',
            'preco': '0',
            'duracao_minutos': '0',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('preco', form.errors)
        self.assertIn('duracao_minutos', form.errors)

    def test_barbeiro_cadastra_servico_e_ve_na_lista(self):
        self.client.force_login(self.barbeiro)

        resposta = self.client.post(self.url, {
            'nome_servico': 'Corte',
            'preco': '45.50',
            'duracao_minutos': '40',
        }, follow=True)

        self.assertEqual(Servico.objects.count(), 1)
        servico = Servico.objects.get()
        self.assertEqual(servico.nome_servico, 'Corte')
        self.assertEqual(str(servico.preco), '45.50')
        self.assertEqual(servico.duracao_minutos, 40)
        self.assertContains(resposta, 'Corte')
        self.assertContains(resposta, '45.50')
        self.assertContains(resposta, '40 min')
        self.assertContains(resposta, 'Serviço cadastrado com sucesso.')

    def test_barbeiro_visualiza_servicos_cadastrados(self):
        Servico.objects.create(
            nome_servico='Barba',
            preco='25.00',
            duracao_minutos=20,
        )
        self.client.force_login(self.barbeiro)

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Barba')
        self.assertContains(resposta, '25.00')
        self.assertContains(resposta, '20 min')

    def test_cadastro_sem_obrigatorios_nao_cria_servico(self):
        self.client.force_login(self.barbeiro)

        resposta = self.client.post(self.url, {
            'nome_servico': '',
            'preco': '',
            'duracao_minutos': '',
        })

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(Servico.objects.count(), 0)
        self.assertContains(resposta, 'Informe o nome do serviço.')
        self.assertContains(resposta, 'Informe o preço do serviço.')
        self.assertContains(resposta, 'Informe a duração estimada do atendimento.')

    def test_usuario_sem_permissao_nao_acessa_cadastro(self):
        self.client.force_login(self.cliente_app)

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, 403)


class AgendamentoClienteTests(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='cliente',
            email='cliente@example.com',
            password='senha-segura',
        )
        self.cliente = Cliente.objects.create(
            user=self.usuario,
            nome_cliente='cliente',
            telefone='11999999999',
        )
        self.servico = Servico.objects.create(
            nome_servico='Corte',
            preco='40.00',
            duracao_minutos=30,
        )
        self.data = timezone.localdate() + timedelta(days=1)
        self.horario = '10:00'

    def test_cliente_agenda_e_ve_na_lista(self):
        self.client.force_login(self.usuario)

        resposta = self.client.post(reverse('index'), {
            'servico': [self.servico.pk],
            'data_agendamento': self.data.isoformat(),
            'horario_agendamento': self.horario,
        }, follow=True)

        self.assertEqual(Agendamento.objects.count(), 1)
        agendamento = Agendamento.objects.get()
        self.assertEqual(agendamento.usuario, self.cliente)
        self.assertEqual(list(agendamento.servico.all()), [self.servico])
        self.assertContains(resposta, 'Agendamento realizado com sucesso.')
        self.assertContains(resposta, 'Corte')
        self.assertContains(resposta, 'Pendente')
        self.assertEqual(agendamento.status, Agendamento.Status.PENDENTE)

    def test_horario_ocupado_nao_cria_agendamento(self):
        ocupado = Agendamento.objects.create(
            usuario=self.cliente,
            data_agendamento=self.data,
            horario_agendamento=self.horario,
        )
        ocupado.servico.add(self.servico)
        self.client.force_login(self.usuario)

        resposta = self.client.post(reverse('index'), {
            'servico': [self.servico.pk],
            'data_agendamento': self.data.isoformat(),
            'horario_agendamento': self.horario,
        })

        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(Agendamento.objects.count(), 1)
        self.assertContains(resposta, 'Este horário já está ocupado')

    def test_formulario_exige_servico_data_e_horario(self):
        form = AgendamentoForm(data={
            'servico': [],
            'data_agendamento': '',
            'horario_agendamento': '',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('servico', form.errors)
        self.assertIn('data_agendamento', form.errors)
        self.assertIn('horario_agendamento', form.errors)

    def test_usuario_sem_cliente_vinculado_consegue_agendar(self):
        solto = User.objects.create_user(
            username='semperfil',
            email='semperfil@example.com',
            password='senha-segura',
        )
        self.client.force_login(solto)

        resposta = self.client.post(reverse('index'), {
            'servico': [self.servico.pk],
            'data_agendamento': self.data.isoformat(),
            'horario_agendamento': self.horario,
        }, follow=True)

        self.assertContains(resposta, 'Agendamento realizado com sucesso.')
        cliente = Cliente.objects.get(user=solto)
        agendamento = Agendamento.objects.get()
        self.assertEqual(agendamento.usuario, cliente)
        self.assertEqual(cliente.nome_cliente, 'semperfil')


class ExclusaoClienteEStatusTests(TestCase):
    def setUp(self):
        self.barbeiro = User.objects.create_user(
            username='barbeiro',
            email='barbeiro@example.com',
            password='senha-segura',
            is_staff=True,
        )
        self.cliente_app = User.objects.create_user(
            username='cliente',
            email='cliente@example.com',
            password='senha-segura',
        )
        self.cliente = Cliente.objects.create(
            nome_cliente='Maria',
            sobrenome_cliente='Souza',
            telefone='21988887777',
        )
        self.servico = Servico.objects.create(
            nome_servico='Corte',
            preco='40.00',
            duracao_minutos=30,
        )

    def test_barbeiro_exclui_cliente(self):
        self.client.force_login(self.barbeiro)

        resposta = self.client.post(
            reverse('excluir_cliente', args=[self.cliente.pk]),
            follow=True,
        )

        self.assertEqual(Cliente.objects.count(), 0)
        self.assertContains(resposta, 'Cliente Maria Souza excluído.')

    def test_usuario_comum_nao_exclui_cliente(self):
        self.client.force_login(self.cliente_app)

        resposta = self.client.post(reverse('excluir_cliente', args=[self.cliente.pk]))

        self.assertEqual(resposta.status_code, 403)
        self.assertTrue(Cliente.objects.filter(pk=self.cliente.pk).exists())

    def test_barbeiro_confirma_agendamento(self):
        agendamento = Agendamento.objects.create(
            usuario=self.cliente,
            data_agendamento='2026-09-01',
            horario_agendamento='10:00:00',
        )
        agendamento.servico.add(self.servico)
        self.client.force_login(self.barbeiro)

        resposta = self.client.post(
            reverse('atualizar_status_agendamento', args=[agendamento.pk]),
            {'status': Agendamento.Status.CONFIRMADO},
            follow=True,
        )

        agendamento.refresh_from_db()
        self.assertEqual(agendamento.status, Agendamento.Status.CONFIRMADO)
        self.assertContains(resposta, 'Confirmado')

    def test_lista_agendamentos_do_mais_recente_para_o_mais_antigo(self):
        antigo = Agendamento.objects.create(
            usuario=self.cliente,
            data_agendamento='2026-09-01',
            horario_agendamento='10:00:00',
        )
        recente = Agendamento.objects.create(
            usuario=self.cliente,
            data_agendamento='2026-09-03',
            horario_agendamento='09:00:00',
        )
        self.client.force_login(self.barbeiro)

        resposta = self.client.get(reverse('painel_admin'))

        self.assertEqual(list(resposta.context['agendamentos']), [recente, antigo])


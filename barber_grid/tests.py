from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .forms import ClienteForm
from .models import Cliente


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

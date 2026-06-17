from django.db import models


class TipoServico(models.Model):
    nome = models.CharField(max_length=50, unique=True)

class Servico(models.Model):
    """Tipos de serviço que a barbearia oferece, tipo cabelo, barba, sobrancelha"""
    nome = models.CharField(max_length=100) #mid fade, fade, degradê, etc
    preco = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    tipo = models.ForeignKey(TipoServico, on_delete=models.CASCADE, related_name="servicos") #cabelo, barba, sobrancelha

    def __str__(self):
        return self.nome




class Cliente(models.Model):
    cliente_nome = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)



class Barbeiro(models.Model):
    barbeiro_nome = models.CharField(max_length=100, null=True)
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.barbeiro_nome


class Agendamento(models.Model):
    """Um agendamento para barbearia marcado pelo cliente"""
    barbeiro = models.ForeignKey(Barbeiro, on_delete=models.CASCADE)
    cliente_nome = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, blank=True)
    cliente_nome_balcao =models.CharField(max_length=100, blank=True, null=True) 
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, null=True, blank=True, related_name = "agendamentos_por_servico") 
    data_agendada = models.DateTimeField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #cliente_nome = f"{self.cliente_nome.cliente_nome if self.cliente_nome else (self.cliente_nome_balcao or 'Anônimo')}"
        servico_nome = f"{self.servico.nome if self.servico else 'Sem serviço'}" #tudo na mesma linha, toda lógica dentro de {}
        #return f"{cliente_nome}- {servico_nome}" #deixar com {} cada um



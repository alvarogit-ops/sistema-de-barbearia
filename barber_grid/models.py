from django.db import models


class Servico(models.Model):
    """Tipos de serviço que a barbearia oferece, tipo cabelo, barba, sobrancelha"""
    nome = models.CharField(max_length=100) #mid fade, fade, degradê, etc
    preco = models.DecimalField(max_digits=5, null=True, decimal_places=2)
    tipo = models.CharField(max_length=50, blank=True) #cabelo, barba, sobrancelha

    def __str__(self):
        return self.nome

class Agendamento(models.Model):
    """Um agendamento para barbearia marcado pelo cliente"""
    barbeiro = models.CharField(max_length=100, null=True) #o que é blank? Blank é usado para campos de texto, permitindo que eles sejam deixados em branco. Null é usado para campos de banco de dados, permitindo que eles sejam nulos. No caso do barbeiro, ele pode ser deixado em branco ou nulo, dependendo da necessidade do sistema. Se o barbeiro for obrigatório, então null=False e blank=False devem ser usados.
    cliente_nome = models.CharField(max_length=100, null=True, blank=True)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, null=True, blank=True, related_name = "agendamentos_por_servico") 
    tipo = models.ForeignKey(Servico, on_delete=models.CASCADE, related_name = "agendamentos_por_tipo")
    data_agendada = models.DateTimeField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        servico_nome = {self.cliente_nome} - {self.servico.nome if self.servico else 'Sem serviço'} #tudo na mesma linha
        return f"{self.cliente_nome  or f'Anônimo - {self.Servico.nome}'}"

class Cliente(models.Model):
    nome = models.CharField(max_length=100, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, null=True, blank=True)


#que id vou usar para o cliente? o nome do cliente é suficiente? ou preciso de um modelo de cliente separado?           
                                
                                
from .models import DadosNegocio


def dados_negocio_context(request):
    return {
        "negocio": DadosNegocio.objects.first(),
    }


## Correção do Erro de Migrações

- [ ] Confirmar causa do erro (migration 0003 aponta para pai 0002 inexistente)
- [ ] Resetar migrações do app barber_grid (apagar 0001 e 0003, manter apenas __init__.py)
- [ ] Rodar `python manage.py makemigrations barber_grid`
- [ ] Rodar `python manage.py migrate`
- [ ] (Opcional) Checar `admin.py`/`__str__` para evitar erro quando `servico` for None


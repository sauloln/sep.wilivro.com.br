# SEP V2.1 — Correções e melhorias de funcionalidade

## O que foi corrigido nesta versão
1) Botões **Excluir** nas telas de cadastro (Locais, Depósitos, Produtos, Clientes, Patrimônio)
2) Autocomplete funcionando (Select2) — incluído **jQuery** no base.html
3) Depósitos: seleção de Local por busca
4) Produtos: **importação em massa** CSV/XLSX + download de modelo
5) Projetos: seleção de **Cliente** e **Local** por busca
6) Patrimônio: seleção de Local por busca + **importação em massa** CSV/XLSX + modelo
7) Inventário/Contagem: seleção de Depósito e Produto por busca
8) Movimentação de Estoque: seleção de Produto/Depósitos por busca
9) Movimentação de Patrimônio: formulário semelhante ao estoque + lista de movimentações

## Implantação no servidor (patch seguro)
### 1) Backup e parar serviço
```bash
cd /home/ubuntu
sudo systemctl stop sep
tar -czf sep_backup_$(date +%F_%H%M).tar.gz sep
```

### 2) Substituir arquivos
Envie **sep_v2_1_core.zip** e **sep_v2_1_templates.zip** para `/home/ubuntu/sep` e execute:
```bash
cd /home/ubuntu/sep
unzip -o sep_v2_1_core.zip
unzip -o sep_v2_1_templates.zip
```

### 3) Verificação e reinício
```bash
cd /home/ubuntu/sep
source .venv/bin/activate
python -m py_compile app.py
sudo systemctl restart sep
sudo systemctl status sep --no-pager
```

Logs:
```bash
journalctl -u sep -n 200 --no-pager
```

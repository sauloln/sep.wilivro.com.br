from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Configuracao(db.Model):
    __tablename__ = "configuracao"
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(80), unique=True, nullable=False)
    valor = db.Column(db.String(500), nullable=False)

class Estado(db.Model):
    __tablename__ = "estado"
    id = db.Column(db.Integer, primary_key=True)
    sigla = db.Column(db.String(2), unique=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    municipios = db.relationship("Municipio", backref="estado", lazy=True)

class Municipio(db.Model):
    __tablename__ = "municipio"
    id = db.Column(db.Integer, primary_key=True)  # IBGE id if imported
    nome = db.Column(db.String(120), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey("estado.id"), nullable=False)
    locais = db.relationship("Local", backref="municipio", lazy=True)

class Local(db.Model):
    __tablename__ = "local"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(50), nullable=False, default="escritorio")  # escritorio, cliente, grafica, almoxarifado, outro
    endereco = db.Column(db.String(250), nullable=True)
    municipio_id = db.Column(db.Integer, db.ForeignKey("municipio.id"), nullable=False)
    observacao = db.Column(db.Text, nullable=True)

class Cliente(db.Model):
    __tablename__ = "cliente"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(180), nullable=False)
    cnpj = db.Column(db.String(20), nullable=True)
    contato = db.Column(db.String(120), nullable=True)
    telefone = db.Column(db.String(40), nullable=True)
    email = db.Column(db.String(120), nullable=True)

class Projeto(db.Model):
    __tablename__ = "projeto"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(180), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=True)
    local_id = db.Column(db.Integer, db.ForeignKey("local.id"), nullable=True)
    status = db.Column(db.String(40), nullable=False, default="ativo")
    data_inicio = db.Column(db.Date, nullable=True)
    data_fim = db.Column(db.Date, nullable=True)
    observacao = db.Column(db.Text, nullable=True)

class PatrimonioItem(db.Model):
    __tablename__ = "patrimonio_item"
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(20), unique=True, nullable=False)  # PAT-000001
    categoria = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.String(250), nullable=False)
    marca = db.Column(db.String(120), nullable=True)
    modelo = db.Column(db.String(120), nullable=True)
    serial = db.Column(db.String(120), nullable=True)
    data_aquisicao = db.Column(db.Date, nullable=True)
    valor = db.Column(db.Float, nullable=True)

    status = db.Column(db.String(40), nullable=False, default="em_uso")  # em_uso, em_estoque, alocado, manutencao, baixado
    local_atual_id = db.Column(db.Integer, db.ForeignKey("local.id"), nullable=True)
    projeto_atual_id = db.Column(db.Integer, db.ForeignKey("projeto.id"), nullable=True)
    projeto_atual = db.relationship("Projeto", foreign_keys=[projeto_atual_id])
    projeto_id = db.Column(db.Integer, db.ForeignKey("projeto.id"), nullable=True)
    responsavel = db.Column(db.String(120), nullable=True)
    observacao = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class PatrimonioMov(db.Model):
    __tablename__ = "patrimonio_mov"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("patrimonio_item.id"), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tipo = db.Column(db.String(40), nullable=False)  # entrada, transferencia, manutencao, baixa
    origem_local_id = db.Column(db.Integer, db.ForeignKey("local.id"), nullable=True)
    destino_local_id = db.Column(db.Integer, db.ForeignKey("local.id"), nullable=True)
    projeto_id = db.Column(db.Integer, db.ForeignKey("projeto.id"), nullable=True)
    responsavel = db.Column(db.String(120), nullable=True)
    observacao = db.Column(db.Text, nullable=True)
    qtd = db.Column(db.Integer, nullable=False, default=1)

class Deposito(db.Model):
    __tablename__ = "deposito"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(40), nullable=False, default="interno")  # interno, grafica, terceiro
    local_id = db.Column(db.Integer, db.ForeignKey("local.id"), nullable=True)
    observacao = db.Column(db.Text, nullable=True)

class Produto(db.Model):
    __tablename__ = "produto"
    id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(60), unique=True, nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(30), nullable=False, default="insumo")  # insumo, acabado
    unidade = db.Column(db.String(20), nullable=False, default="UN")
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    estoque_minimo = db.Column(db.Float, nullable=True)
    observacao = db.Column(db.Text, nullable=True)

class EstoqueSaldo(db.Model):
    __tablename__ = "estoque_saldo"
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    deposito_id = db.Column(db.Integer, db.ForeignKey("deposito.id"), nullable=False)
    saldo = db.Column(db.Float, nullable=False, default=0)
    __table_args__ = (db.UniqueConstraint("produto_id", "deposito_id", name="uq_prod_deposito"),)

class EstoqueMov(db.Model):
    __tablename__ = "estoque_mov"
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    tipo = db.Column(db.String(30), nullable=False)  # entrada, saida, transferencia, ajuste
    produto_id = db.Column(db.Integer, db.ForeignKey("produto.id"), nullable=False)
    deposito_origem_id = db.Column(db.Integer, db.ForeignKey("deposito.id"), nullable=True)
    deposito_destino_id = db.Column(db.Integer, db.ForeignKey("deposito.id"), nullable=True)
    qtd = db.Column(db.Float, nullable=False)
    custo_unit = db.Column(db.Float, nullable=True)
    documento_ref = db.Column(db.String(120), nullable=True)
    observacao = db.Column(db.Text, nullable=True)

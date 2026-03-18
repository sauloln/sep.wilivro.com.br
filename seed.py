import argparse
import requests
from app import create_app
from models import db, Estado, Municipio

IBGE_ESTADOS = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
IBGE_MUNICIPIOS = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"

def seed_ibge():
    app = create_app()
    with app.app_context():
        db.create_all()

        estados = requests.get(IBGE_ESTADOS, timeout=30).json()
        # IBGE returns list; each has id, sigla, nome
        for e in estados:
            est = Estado.query.filter_by(sigla=e["sigla"]).first()
            if not est:
                est = Estado(id=int(e["id"]), sigla=e["sigla"], nome=e["nome"])
                db.session.add(est)
        db.session.commit()

        for est in Estado.query.all():
            url = IBGE_MUNICIPIOS.format(uf=est.sigla)
            municipios = requests.get(url, timeout=60).json()
            for m in municipios:
                mid = int(m["id"])
                exists = Municipio.query.get(mid)
                if not exists:
                    db.session.add(Municipio(id=mid, nome=m["nome"], estado_id=est.id))
            db.session.commit()

        print("OK: import IBGE concluído. Estados:", Estado.query.count(), "Municípios:", Municipio.query.count())

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ibge", action="store_true", help="Importar Estados/Municípios via IBGE")
    args = ap.parse_args()
    if args.ibge:
        seed_ibge()
    else:
        print("Use: python seed.py --ibge")

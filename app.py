from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, extract, case, or_
from models.model import Cliente, Reserva, Habitacion, Pago, PagoEfectivo, PagoTarjeta, PagoQr, Factura, Usuario
from models.base import engine

from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key_fallback")
CORS(app)

# Create SQLAlchemy session
Session = sessionmaker(bind=engine)
db_session = Session()

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth'

@login_manager.user_loader
def load_user(user_id):
    return db_session.query(Usuario).get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('auth.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        action = request.form['action']
        username = request.form['username']
        password = request.form['password']
        if action == 'register':
            if db_session.query(Usuario).filter_by(username=username).first():
                flash('El usuario ya existe', 'danger')
            else:
                new_user = Usuario(
                    username=username,
                    password=generate_password_hash(password)
                )
                db_session.add(new_user)
                db_session.commit()
                flash('Usuario creado exitosamente', 'success')
                return redirect(url_for('auth'))
        elif action == 'login':
            user = db_session.query(Usuario).filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('Sesión iniciada exitosamente', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Usuario o contraseña incorrectos', 'danger')
                return redirect(url_for('auth'))
    return render_template('auth.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth'))

@app.route('/listclientes')
@login_required
def listclientes():
    return render_template('index.html')

# API Routes for CRUD
@app.route('/api/list_clientes', methods=['GET'])
@login_required
def api_list_clientes():
    clientes = db_session.query(Cliente).all()
    data = [
        {
            "id_cliente": c.id_cliente,
            "ci": c.ci,
            "nombre": c.nombre,
            "telefono": c.telefono,
            "correo_electronico": c.correo_electronico,
            "lineadireccion1": c.lineadireccion1,
            "lineadireccion2": c.lineadireccion2,
            "ciudad": c.ciudad,
            "region": c.region,
            "pais": c.pais
        } for c in clientes
    ]
    return jsonify(data)

@app.route('/api/opciones', methods=['GET'])
@login_required
def obtener_opciones():
    ciudades = db_session.query(Cliente.ciudad).distinct().all()
    regiones = db_session.query(Cliente.region).distinct().all()
    paises = db_session.query(Cliente.pais).distinct().all()
    return jsonify({
        "ciudades": sorted([c[0] for c in ciudades if c[0]]),
        "regiones": sorted([r[0] for r in regiones if r[0]]),
        "paises": sorted([p[0] for p in paises if p[0]])
    })

@app.route('/add/clientes', methods=['POST'])
@login_required
def crear_cliente():
    try:
        data = request.json
        nuevo = Cliente(
            ci=data.get('ci'),
            nombre=data.get('nombre'),
            telefono=data.get('telefono'),
            correo_electronico=data.get('correo_electronico'),
            lineadireccion1=data.get('lineadireccion1'),
            lineadireccion2=data.get('lineadireccion2'),
            ciudad=data.get('ciudad'),
            region=data.get('region'),
            pais=data.get('pais')
        )
        db_session.add(nuevo)
        db_session.commit()
        return jsonify({"mensaje": "Cliente agregado correctamente"})
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 400

@app.route('/del/clientes/<int:id>', methods=['DELETE'])
@login_required
def eliminar_cliente(id):
    cliente = db_session.query(Cliente).get(id)
    if cliente:
        db_session.delete(cliente)
        db_session.commit()
        return jsonify({"mensaje": "Cliente eliminado correctamente"})
    return jsonify({"error": "Cliente no encontrado"}), 404

@app.route('/upd/clientes/<int:id>', methods=['PUT'])
@login_required
def actualizar_cliente(id):
    try:
        data = request.json
        cliente = db_session.query(Cliente).get(id)
        if not cliente:
            return jsonify({"error": "Cliente no encontrado"}), 404
        cliente.ci = data.get("ci")
        cliente.nombre = data.get("nombre")
        cliente.telefono = data.get("telefono")
        cliente.correo_electronico = data.get("correo_electronico")
        cliente.lineadireccion1 = data.get("lineadireccion1")
        cliente.lineadireccion2 = data.get("lineadireccion2")
        cliente.ciudad = data.get("ciudad")
        cliente.region = data.get("region")
        cliente.pais = data.get("pais")
        db_session.commit()
        return jsonify({"mensaje": "Cliente actualizado correctamente"})
    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 400

# API Routes for Dashboard Charts
@app.route('/api/reservas_por_mes', methods=['GET'])
@login_required
def reservas_por_mes():
    reservas = db_session.query(
        func.to_char(Reserva.fecha_inicio, 'YYYY-MM').label('mes'),
        func.count().label('total')
    ).group_by('mes').order_by('mes').all()
    data = [{"mes": r.mes, "total": r.total} for r in reservas]
    return jsonify(data)

@app.route('/api/reservas_por_habitacion', methods=['GET'])
@login_required
def reservas_por_habitacion():
    reservas = db_session.query(
        Habitacion.id_habitacion,
        func.coalesce(Habitacion.piso, 0).label('piso'),
        func.count(Reserva.id_reserva).label('total')
    ).outerjoin(Reserva, Habitacion.id_habitacion == Reserva.id_habitacion
    ).group_by(Habitacion.id_habitacion, Habitacion.piso
    ).order_by(Habitacion.id_habitacion).all()
    data = [{"habitacion": f"Habitación {r.id_habitacion} (Piso {r.piso})", "total": r.total} for r in reservas]
    return jsonify(data)

@app.route('/api/pagos_por_metodo', methods=['GET'])
@login_required
def pagos_por_metodo():
    try:
        # Contar pagos por subtipo
        efectivo = db_session.query(func.count(PagoEfectivo.id_pago)).scalar() or 0
        tarjeta = db_session.query(func.count(PagoTarjeta.id_pago)).scalar() or 0
        qr = db_session.query(func.count(PagoQr.id_pago)).scalar() or 0
        total_pagos = db_session.query(func.count(Pago.id_pago)).scalar() or 0
        sin_clasificar = total_pagos - (efectivo + tarjeta + qr)

        labels = ["Efectivo", "Tarjeta", "QR", "Sin Clasificar"]
        data = [efectivo, tarjeta, qr, sin_clasificar if sin_clasificar >= 0 else 0]
        
        logger.debug(f"Pagos por método: {labels} -> {data}")
        return jsonify({"labels": labels, "data": data})
    except Exception as e:
        logger.error(f"Error en pagos_por_metodo: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/facturas_por_mes', methods=['GET'])
@login_required
def facturas_por_mes():
    facturas = db_session.query(
        func.to_char(Factura.fecha, 'YYYY-MM').label('mes'),
        func.sum(Factura.monto).label('total')
    ).group_by('mes').order_by('mes').all()
    data = [{"mes": r.mes, "total": float(r.total) if r.total else 0.0} for r in facturas]
    return jsonify(data)

@app.route('/api/metricas', methods=['GET'])
@login_required
def metricas():
    # Mes Top de Reservas
    mes_top = db_session.query(
        func.to_char(Reserva.fecha_inicio, 'YYYY-MM').label('mes'),
        func.count().label('total')
    ).group_by('mes').order_by(func.count().desc()).first()
    
    # Total Facturado
    total_facturado = db_session.query(func.sum(Factura.monto)).scalar() or 0.0
    
    # Total de Reservas
    total_reservas = db_session.query(Reserva).count()
    
    # Clientes Activos (con al menos una reserva)
    clientes_activos = db_session.query(func.count(func.distinct(Reserva.id_cliente))).scalar()
    
    return jsonify({
        "mes_top": mes_top.mes if mes_top else "N/A",
        "reservas_mes_top": mes_top.total if mes_top else 0,
        "total_facturado": float(total_facturado),
        "total_reservas": total_reservas,
        "clientes_activos": clientes_activos
    })

if __name__ == '__main__':
    app.run(debug=True)
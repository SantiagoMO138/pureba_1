from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Text, Sequence, DateTime, Boolean, func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import UniqueConstraint
from flask_login import UserMixin

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'cliente'
    id_cliente = Column(Integer, primary_key=True)
    ci = Column(String(100), unique=True, nullable=False)
    nombre = Column(String(100))
    telefono = Column(String(20))
    correo_electronico = Column(String(100))
    lineadireccion1 = Column(String(50), nullable=False)
    lineadireccion2 = Column(String(50))
    ciudad = Column(String(50), nullable=False)
    region = Column(String(50))
    pais = Column(String(50))
    reservas = relationship('Reserva', back_populates='cliente')
    pagos = relationship('Pago', back_populates='cliente')

    def __repr__(self):
        return f"<Cliente(id_cliente={self.id_cliente}, ci={self.ci}, nombre={self.nombre})>"

    @staticmethod
    def mostrar_todos_los_clientes(session):
        clientes = session.query(Cliente).all()
        for cliente in clientes:
            print("ID Cliente:", cliente.id_cliente)
            print("CI:", cliente.ci)
            print("Nombre:", cliente.nombre)
            print("Teléfono:", cliente.telefono)
            print("Correo:", cliente.correo_electronico)
            print("Dirección 1:", cliente.lineadireccion1)
            print("Dirección 2:", cliente.lineadireccion2)
            print("Ciudad:", cliente.ciudad)
            print("Región:", cliente.region)
            print("País:", cliente.pais)
            print("-------------------------------------------")

class TipoHabitacion(Base):
    __tablename__ = 'tipo_habitacion'
    id_tipo = Column(Integer, primary_key=True)
    nombre_tipo = Column(String(50))
    descripcion = Column(Text)
    habitaciones = relationship('Habitacion', back_populates='tipo_habitacion')

    def __repr__(self):
        return f"<TipoHabitacion(id_tipo={self.id_tipo}, nombre_tipo={self.nombre_tipo})>"

    @staticmethod
    def mostrar_todos_los_tipos(session):
        tipos = session.query(TipoHabitacion).all()
        for tipo in tipos:
            print("ID Tipo:", tipo.id_tipo)
            print("Nombre Tipo:", tipo.nombre_tipo)
            print("Descripción:", tipo.descripcion)
            print("-------------------------------------------")

class Habitacion(Base):
    __tablename__ = 'habitacion'
    id_habitacion = Column(Integer, primary_key=True)
    piso = Column(Integer)
    id_tipo = Column(Integer, ForeignKey('tipo_habitacion.id_tipo'))
    disponibilidad_habitacion = Column(Boolean)
    tipo_habitacion = relationship('TipoHabitacion', back_populates='habitaciones')
    hoteles = relationship('HabitacionHotel', back_populates='habitacion')
    reservas = relationship('Reserva', back_populates='habitacion')
    precios = relationship('PrecioDia', back_populates='habitacion')

    def __repr__(self):
        return f"<Habitacion(id_habitacion={self.id_habitacion}, piso={self.piso})>"

    @staticmethod
    def mostrar_todas_las_habitaciones(session):
        habitaciones = session.query(Habitacion).all()
        for habitacion in habitaciones:
            print("ID Habitación:", habitacion.id_habitacion)
            print("Piso:", habitacion.piso)
            print("Tipo ID:", habitacion.id_tipo)
            print("Disponibilidad:", habitacion.disponibilidad_habitacion)
            print("-------------------------------------------")

class Hotel(Base):
    __tablename__ = 'hotel'
    id_hotel = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    ubicacion = Column(String(100))
    habitaciones = relationship('HabitacionHotel', back_populates='hotel')
    empleados = relationship('Empleado', back_populates='hotel')

    def __repr__(self):
        return f"<Hotel(id_hotel={self.id_hotel}, nombre={self.nombre})>"

    @staticmethod
    def mostrar_todos_los_hoteles(session):
        hoteles = session.query(Hotel).all()
        for hotel in hoteles:
            print("ID Hotel:", hotel.id_hotel)
            print("Nombre:", hotel.nombre)
            print("Ubicación:", hotel.ubicacion)
            print("-------------------------------------------")

class HabitacionHotel(Base):
    __tablename__ = 'habitacion_hotel'
    id_habitacion = Column(Integer, ForeignKey('habitacion.id_habitacion'), primary_key=True)
    id_hotel = Column(Integer, ForeignKey('hotel.id_hotel'), primary_key=True)
    habitacion = relationship('Habitacion', back_populates='hoteles')
    hotel = relationship('Hotel', back_populates='habitaciones')

    def __repr__(self):
        return f"<HabitacionHotel(id_habitacion={self.id_habitacion}, id_hotel={self.id_hotel})>"

    @staticmethod
    def mostrar_todas_las_habitaciones_hotel(session):
        relaciones = session.query(HabitacionHotel).all()
        for relacion in relaciones:
            print("ID Habitación:", relacion.id_habitacion)
            print("ID Hotel:", relacion.id_hotel)
            print("-------------------------------------------")

class Empleado(Base):
    __tablename__ = 'empleado'
    id_empleado = Column(Integer, primary_key=True)
    codigo_empleado = Column(Integer, unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido1 = Column(String(50), nullable=False)
    apellido2 = Column(String(50))
    extension = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False)
    id_hotel = Column(Integer, ForeignKey('hotel.id_hotel'), nullable=False)
    id_empleado_jefe = Column(Integer, ForeignKey('empleado.id_empleado'))
    puesto = Column(String(50))
    hotel = relationship('Hotel', back_populates='empleados')
    jefe = relationship('Empleado', remote_side=[id_empleado])
    subordinados = relationship('Empleado', back_populates='jefe')

    def __repr__(self):
        return f"<Empleado(id_empleado={self.id_empleado}, nombre={self.nombre})>"

    @staticmethod
    def mostrar_todos_los_empleados(session):
        empleados = session.query(Empleado).all()
        for empleado in empleados:
            print("ID Empleado:", empleado.id_empleado)
            print("Código Empleado:", empleado.codigo_empleado)
            print("Nombre:", empleado.nombre)
            print("Apellido1:", empleado.apellido1)
            print("Apellido2:", empleado.apellido2)
            print("Extensión:", empleado.extension)
            print("Email:", empleado.email)
            print("ID Hotel:", empleado.id_hotel)
            print("ID Jefe:", empleado.id_empleado_jefe)
            print("Puesto:", empleado.puesto)
            print("-------------------------------------------")

class PrecioDia(Base):
    __tablename__ = 'precio_dia'
    id_precio = Column(Integer, primary_key=True)
    id_habitacion = Column(Integer, ForeignKey('habitacion.id_habitacion'))
    fecha = Column(Date, nullable=False)
    precio = Column(Numeric(10, 2))
    habitacion = relationship('Habitacion', back_populates='precios')
    __table_args__ = (UniqueConstraint('id_habitacion', 'fecha'),)

    def __repr__(self):
        return f"<PrecioDia(id_precio={self.id_precio}, fecha={self.fecha})>"

    @staticmethod
    def mostrar_todos_los_precios(session):
        precios = session.query(PrecioDia).all()
        for precio in precios:
            print("ID Precio:", precio.id_precio)
            print("ID Habitación:", precio.id_habitacion)
            print("Fecha:", precio.fecha)
            print("Precio:", precio.precio)
            print("-------------------------------------------")

class Reserva(Base):
    __tablename__ = 'reserva'
    id_reserva = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'), nullable=False)
    id_habitacion = Column(Integer, ForeignKey('habitacion.id_habitacion'), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    cliente = relationship('Cliente', back_populates='reservas')
    habitacion = relationship('Habitacion', back_populates='reservas')
    estancias = relationship('Estancia', back_populates='reserva')

    def __repr__(self):
        return f"<Reserva(id_reserva={self.id_reserva}, fecha_inicio={self.fecha_inicio})>"

    @staticmethod
    def mostrar_todas_las_reservas(session):
        reservas = session.query(Reserva).all()
        for reserva in reservas:
            print("ID Reserva:", reserva.id_reserva)
            print("ID Cliente:", reserva.id_cliente)
            print("ID Habitación:", reserva.id_habitacion)
            print("Fecha Inicio:", reserva.fecha_inicio)
            print("Fecha Fin:", reserva.fecha_fin)
            print("-------------------------------------------")

class Estancia(Base):
    __tablename__ = 'estancia'
    id_estancia = Column(Integer, primary_key=True)
    id_reserva = Column(Integer, ForeignKey('reserva.id_reserva'), nullable=False)
    fecha_entrada = Column(DateTime, nullable=False)
    fecha_salida = Column(DateTime)
    observaciones = Column(Text)
    reserva = relationship('Reserva', back_populates='estancias')

    def __repr__(self):
        return f"<Estancia(id_estancia={self.id_estancia}, id_reserva={self.id_reserva})>"

    @staticmethod
    def mostrar_todas_las_estancias(session):
        estancias = session.query(Estancia).all()
        for estancia in estancias:
            print("ID Estancia:", estancia.id_estancia)
            print("ID Reserva:", estancia.id_reserva)
            print("Fecha Entrada:", estancia.fecha_entrada)
            print("Fecha Salida:", estancia.fecha_salida)
            print("Observaciones:", estancia.observaciones)
            print("-------------------------------------------")

class Pago(Base):
    __tablename__ = 'pago'
    id_pago = Column(Integer, primary_key=True)
    id_cliente = Column(Integer, ForeignKey('cliente.id_cliente'))
    fecha = Column(Date)
    monto = Column(Numeric(10, 2))
    cliente = relationship('Cliente', back_populates='pagos')
    pago_efectivo = relationship('PagoEfectivo', uselist=False, back_populates='pago')
    pago_tarjeta = relationship('PagoTarjeta', uselist=False, back_populates='pago')
    pago_qr = relationship('PagoQr', uselist=False, back_populates='pago')
    facturas = relationship('Factura', back_populates='pago')

    def __repr__(self):
        return f"<Pago(id_pago={self.id_pago}, monto={self.monto})>"

    @staticmethod
    def mostrar_todos_los_pagos(session):
        pagos = session.query(Pago).all()
        for pago in pagos:
            print("ID Pago:", pago.id_pago)
            print("ID Cliente:", pago.id_cliente)
            print("Fecha:", pago.fecha)
            print("Monto:", pago.monto)
            print("-------------------------------------------")

class PagoEfectivo(Base):
    __tablename__ = 'pago_efectivo'
    id_pago = Column(Integer, ForeignKey('pago.id_pago'), primary_key=True)
    recibido_por = Column(String(100))
    pago = relationship('Pago', back_populates='pago_efectivo')

    def __repr__(self):
        return f"<PagoEfectivo(id_pago={self.id_pago}, recibido_por={self.recibido_por})>"

    @staticmethod
    def mostrar_todos_los_pagos_efectivo(session):
        pagos = session.query(PagoEfectivo).all()
        for pago in pagos:
            print("ID Pago:", pago.id_pago)
            print("Recibido Por:", pago.recibido_por)
            print("-------------------------------------------")

class PagoTarjeta(Base):
    __tablename__ = 'pago_tarjeta'
    id_pago = Column(Integer, ForeignKey('pago.id_pago'), primary_key=True)
    numero_tarjeta = Column(String(20))
    tipo_tarjeta = Column(String(50))
    codigo_autorizacion = Column(String(50))
    pago = relationship('Pago', back_populates='pago_tarjeta')

    def __repr__(self):
        return f"<PagoTarjeta(id_pago={self.id_pago}, tipo_tarjeta={self.tipo_tarjeta})>"

    @staticmethod
    def mostrar_todos_los_pagos_tarjeta(session):
        pagos = session.query(PagoTarjeta).all()
        for pago in pagos:
            print("ID Pago:", pago.id_pago)
            print("Número Tarjeta:", pago.numero_tarjeta)
            print("Tipo Tarjeta:", pago.tipo_tarjeta)
            print("Código Autorización:", pago.codigo_autorizacion)
            print("-------------------------------------------")

class PagoQr(Base):
    __tablename__ = 'pago_qr'
    id_pago = Column(Integer, ForeignKey('pago.id_pago'), primary_key=True)
    referencia_qr = Column(String(100))
    app_utilizada = Column(String(50))
    pago = relationship('Pago', back_populates='pago_qr')

    def __repr__(self):
        return f"<PagoQr(id_pago={self.id_pago}, app_utilizada={self.app_utilizada})>"

    @staticmethod
    def mostrar_todos_los_pagos_qr(session):
        pagos = session.query(PagoQr).all()
        for pago in pagos:
            print("ID Pago:", pago.id_pago)
            print("Referencia QR:", pago.referencia_qr)
            print("App Utilizada:", pago.app_utilizada)
            print("-------------------------------------------")

class Factura(Base):
    __tablename__ = 'factura'
    id_factura = Column(Integer, primary_key=True)
    id_pago = Column(Integer, ForeignKey('pago.id_pago'))
    fecha = Column(Date)
    monto = Column(Numeric(10, 2))
    nombre_facturado = Column(String(100))
    ci = Column(String(100), nullable=False)
    pago = relationship('Pago', back_populates='facturas')

    def __repr__(self):
        return f"<Factura(id_factura={self.id_factura}, monto={self.monto})>"

    @staticmethod
    def mostrar_todas_las_facturas(session):
        facturas = session.query(Factura).all()
        for factura in facturas:
            print("ID Factura:", factura.id_factura)
            print("ID Pago:", factura.id_pago)
            print("Fecha:", factura.fecha)
            print("Monto:", factura.monto)
            print("Nombre Facturado:", factura.nombre_facturado)
            print("CI:", factura.ci)
            print("-------------------------------------------")

class Usuario(Base, UserMixin):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Usuario(id={self.id}, username={self.username})>"

    @staticmethod
    def mostrar_todos_los_usuarios(session):
        usuarios = session.query(Usuario).all()
        for usuario in usuarios:
            print("ID Usuario:", usuario.id)
            print("Username:", usuario.username)
            print("-------------------------------------------")
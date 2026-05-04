from app.db import SessionLocal
from app.models.vendedor import Vendedor
from app.models.producto import Producto
from app.models.cliente import Cliente
from app.models.pedido import Pedido
from app.models.pedido_producto import PedidoProducto


def seed():
    db = SessionLocal()
    try:
        # Verificar si ya hay datos
        if db.query(Vendedor).first():
            print("⚠️  La base de datos ya tiene datos, omitiendo seed...")
            return

        print("🌱 Iniciando seed...")

        # Vendedores
        vendedores = [
            Vendedor(
                nombre="Carlos Pérez",
                email="carlos@tienda.com",
                telefono="912345678",
                zona="Norte",
            ),
            Vendedor(
                nombre="María López",
                email="maria@tienda.com",
                telefono="923456789",
                zona="Sur",
            ),
            Vendedor(
                nombre="Juan Rodríguez",
                email="juan@tienda.com",
                telefono="934567890",
                zona="Centro",
            ),
        ]
        db.add_all(vendedores)
        db.flush()
        print("✅ Vendedores creados")

        # Productos
        productos = [
            Producto(
                nombre="Laptop Gamer",
                descripcion="RTX 4060, 16GB RAM",
                precio=999999,
                stock=10,
                id_vendedor=vendedores[0].id,
            ),
            Producto(
                nombre="Mouse Inalámbrico",
                descripcion="DPI ajustable",
                precio=29999,
                stock=50,
                id_vendedor=vendedores[0].id,
            ),
            Producto(
                nombre="Teclado Mecánico",
                descripcion="Switch Red",
                precio=79999,
                stock=30,
                id_vendedor=vendedores[1].id,
            ),
            Producto(
                nombre='Monitor 27"',
                descripcion="144Hz, 1ms",
                precio=349999,
                stock=15,
                id_vendedor=vendedores[1].id,
            ),
            Producto(
                nombre="Auriculares RGB",
                descripcion="Sonido 7.1",
                precio=59999,
                stock=25,
                id_vendedor=vendedores[2].id,
            ),
        ]
        db.add_all(productos)
        db.flush()
        print("✅ Productos creados")

        # Clientes
        clientes = [
            Cliente(nombre="Ana González", email="ana@gmail.com", telefono="945678901"),
            Cliente(
                nombre="Pedro Martínez", email="pedro@gmail.com", telefono="956789012"
            ),
            Cliente(
                nombre="Laura Sánchez", email="laura@gmail.com", telefono="967890123"
            ),
        ]
        db.add_all(clientes)
        db.flush()
        print("✅ Clientes creados")

        # Pedidos
        pedido1 = Pedido(id_cliente=clientes[0].id, estado="En espera", total=0)
        pedido2 = Pedido(id_cliente=clientes[1].id, estado="Preparando", total=0)
        pedido3 = Pedido(id_cliente=clientes[2].id, estado="Entregado", total=0)
        db.add_all([pedido1, pedido2, pedido3])
        db.flush()
        print("✅ Pedidos creados")

        # Pedido Productos
        items = [
            PedidoProducto(
                id_pedido=pedido1.id,
                id_producto=productos[0].id,
                cantidad=1,
                precio_unitario=productos[0].precio,
            ),
            PedidoProducto(
                id_pedido=pedido1.id,
                id_producto=productos[1].id,
                cantidad=2,
                precio_unitario=productos[1].precio,
            ),
            PedidoProducto(
                id_pedido=pedido2.id,
                id_producto=productos[2].id,
                cantidad=1,
                precio_unitario=productos[2].precio,
            ),
            PedidoProducto(
                id_pedido=pedido3.id,
                id_producto=productos[3].id,
                cantidad=1,
                precio_unitario=productos[3].precio,
            ),
            PedidoProducto(
                id_pedido=pedido3.id,
                id_producto=productos[4].id,
                cantidad=3,
                precio_unitario=productos[4].precio,
            ),
        ]
        db.add_all(items)

        # Calcular totales
        pedido1.total = sum(
            i.precio_unitario * i.cantidad for i in items if i.id_pedido == pedido1.id
        )
        pedido2.total = sum(
            i.precio_unitario * i.cantidad for i in items if i.id_pedido == pedido2.id
        )
        pedido3.total = sum(
            i.precio_unitario * i.cantidad for i in items if i.id_pedido == pedido3.id
        )

        db.commit()
        print("✅ Pedido productos creados")
        print("🎉 Seed completado exitosamente")

    except Exception as e:
        db.rollback()
        print(f"❌ Error en seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()

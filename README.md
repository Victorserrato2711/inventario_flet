# 📦 Sistema de Inventario y Ventas (PyME)

## 🚀 Descripción
Este proyecto es un sistema de **gestión de inventario y ventas** diseñado para pequeñas y medianas empresas.  
Su objetivo es ofrecer un flujo **simple, estable y auditable** para registrar entradas de productos y ventas, mantener trazabilidad completa y generar comprobantes en PDF.

---

## ✨ Funcionalidades principales
- **Login y seguridad**
  - Autenticación de usuarios mediante login.
  - Opción para cambiar contraseña y mantener seguridad.
  - Asociación de cada operación al usuario autenticado.

- **Entradas de productos**
  - Registro de entradas con ID único.
  - Asociación al usuario que realiza la operación.
  - Actualización automática de inventario.
  - Generación de ticket PDF como comprobante.

- **Ventas**
  - Registro de ventas con ID único.
  - Métodos de pago soportados: efectivo y tarjeta.
  - Registro de detalles de productos vendidos.
  - Generación de ticket PDF con desglose de productos, total, pago y cambio.

- **Gestión de productos y categorías**
  - Agregar nuevos productos al inventario.
  - Crear y administrar categorías de productos.
  - Visualización del inventario completo con cantidades actualizadas.

- **Reportes**
  - Valor total del inventario.
  - Productos agrupados por categoría.
  - Productos con bajo stock (alerta preventiva).

- **Trazabilidad y auditoría**
  - Cada operación queda registrada con fecha, hora y usuario.
  - Tickets PDF sirven como evidencia verificable.
  - Validaciones evitan registros inválidos (usuario inexistente, producto no encontrado, cantidad ≤ 0).

- **Interfaz gráfica (Flet)**
  - Pantallas claras para entradas, ventas y reportes.
  - Buscador por ID de entrada.
  - Botones de acción intuitivos (Registrar, Guardar, Volver, Imprimir).

---

## 🛠️ Tecnologías utilizadas
- **Python**
- **Flet** (UI multiplataforma)
- **SQLAlchemy** (ORM y consultas SQL)
- **PostgreSQL** (según configuración)
- **FPDF** (generación de tickets PDF)

---

## 📑 Flujo de trabajo
1. **Login** → guarda el `usuario_id` en la sesión (`page.usuario_id`).
2. **Cambio de contraseña** → permite actualizar credenciales de forma segura.
3. **Registrar Entrada** → se valida producto y cantidad, se guarda en DB y se genera ticket PDF.
4. **Registrar Venta** → se valida pago, se guarda en DB, se registran detalles y se genera ticket PDF.
5. **Pantalla de Entradas** → muestra todas las entradas y permite buscar por ID.
6. **Gestión de Productos** → agregar nuevos productos y categorías.
7. **Reportes** → consultar inventario, categorías y productos con bajo stock.
8. **Tickets PDF** → se generan automáticamente al registrar operaciones.

---

## ✅ Estado actual
El sistema cumple con:
- **Login y seguridad**: autenticación y cambio de contraseña.
- **Trazabilidad**: cada movimiento tiene ID, usuario y fecha.
- **Auditoría**: tickets PDF y registros en DB permiten verificación.
- **Funcionalidad**: flujo completo de entradas y ventas, con validaciones y comprobantes.
- **Gestión de productos y categorías**: agregar, organizar y visualizar inventario.
- **Reportes básicos**: inventario, categorías y stock bajo.

---

## 🔮 Posibles mejoras futuras
- Alertas configurables (ej. stock crítico).
- Reimpresiones de Tickets desde la interfaz.

---

## ⚙️ Instalación y ejecución

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/Victorserrato2711/inventario_flet.git
cd inventario_flet

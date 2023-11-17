// JavaScript (caja_registradora.js)
let carrito = [];

function agregarAlCarrito() {
    const productoSelect = document.getElementById('producto');
    const selectedOption = productoSelect.options[productoSelect.selectedIndex];
    const producto = selectedOption.text;
    const precio = parseFloat(selectedOption.getAttribute('data-precio'));
    const cantidad = parseInt(document.getElementById('cantidad').value);
  
    if (!isNaN(precio) && !isNaN(cantidad) && cantidad > 0) {
      const totalProducto = precio * cantidad;
      
      carrito.push({ producto, precio, cantidad, totalProducto });
  
      actualizarCarrito();
      limpiarFormulario();
    } else {
      alert('Ingresa cantidad válida.');
    }
  }
  
  function actualizarCarrito() {
    const tablaCarrito = document.getElementById('tablaCarrito');
    const totalElement = document.getElementById('total');
  
    // Limpia el contenido actual de la tabla
    tablaCarrito.innerHTML = '';
  
    let totalCompra = 0;
  
    carrito.forEach((item, index) => {
      const row = tablaCarrito.insertRow();
      const cellProducto = row.insertCell(0);
      const cellPrecio = row.insertCell(1);
      const cellCantidad = row.insertCell(2);
      const cellTotalProducto = row.insertCell(3);
  
      // Ajusta las celdas con la información del item
      cellProducto.innerHTML = item.producto;
      cellPrecio.innerHTML = `$${item.precio.toFixed(2).replace(/\.?0+$/, '')}`;
      cellCantidad.innerHTML = item.cantidad;
      cellTotalProducto.innerHTML = `$${item.totalProducto.toFixed(2).replace(/\.?0+$/, '')}`;
  
      // Actualiza el total de la compra
      totalCompra += item.totalProducto;
    });
  
    // Muestra el total de la compra
    totalElement.innerText = `Total: $${totalCompra.toFixed(2).replace(/\.?0+$/, '')}`;
  }
  
function limpiarFormulario() {
  document.getElementById('producto').value = '';
  document.getElementById('precio').value = '';
  document.getElementById('cantidad').value = '';
}

function facturar() {
  const totalCompra = carrito.reduce((total, item) => total + item.totalProducto, 0);
  alert(`Factura emitida. Total a pagar: $${totalCompra.toFixed(2)}`);

  // Puedes enviar el carrito al servidor para procesar la factura y actualizar inventario, etc.
  // Por ejemplo, mediante una solicitud AJAX con fetch o axios.
  // Aquí se muestra una versión simplificada sin la comunicación con el servidor.
  reiniciarCaja();
}

function reiniciarCaja() {
  carrito = [];
  actualizarCarrito();
}

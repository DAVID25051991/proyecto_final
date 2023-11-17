/**
 * Vista previa de imagen perfil cargada
 */
function readURL(input) {
  if (input.files && input.files[0]) {
    var imageUrl = URL.createObjectURL(input.files[0]);
    $("#imagePreview").css("background-image", "url(" + imageUrl + ")");
    $("#imagePreview").hide();
    $("#imagePreview").fadeIn(650);
  }
}

$("#imageUpload").change(function () {
  readURL(this);
});

/**
 * Formatear cantidad en salario
 */
function formatearCantidad(inputElementId) {
  let salario = document.querySelector(`#${inputElementId}`);
  if (salario) {
    salario.addEventListener("input", (inputClick) => {
      let cantidad = inputClick.target.value.replace(/\D/g, ""); // Eliminar caracteres no numéricos
      cantidad = parseInt(cantidad, 10); // Convertir a número entero
      if (isNaN(cantidad)) {
        cantidad = 0; // Si no se puede convertir a número, se establece en 0
      }
      // Formatear la cantidad y asignarla al campo de entrada
      inputClick.target.value =
        "$ " +
        cantidad.toLocaleString("es-CO", {
          minimumFractionDigits: 0,
          maximumFractionDigits: 0,
        });
    });
  }
}

formatearCantidad("precio");
formatearCantidad("total");
formatearCantidad("pago");
formatearCantidad("cambio");

/**
 * Eliminar un producto
 */
async function eliminarProducto(idProducto, fotoProducto) {
  try {
    if (confirm(`¿Estás seguro que deseas eliminar el producto con ID ${idProducto}?`)) {
      const response = await axios.post("/eliminar-producto", { idProducto, fotoProducto });

      if (response.data.success) {
        // Eliminar la fila de la tabla en el cliente
        const productoRow = document.getElementById(`producto_${idProducto}`);
        if (productoRow) {
          productoRow.remove();
          recalcularTotal(); // Actualizar el total después de eliminar un producto
        } else {
          console.error(`No se encontró la fila del producto con ID ${idProducto}`);
        }
      } else {
        console.error("Error al eliminar el producto");
      }
    }
  } catch (error) {
    console.error("Error de red al intentar eliminar el producto", error);
  }
}

/**
 * Función para agregar un producto (debes implementarla según tu lógica)
 */
// Variable para almacenar los productos en el carrito
let carrito = [];

// Función para agregar un producto al carrito
function agregarAlCarrito(producto) {
  carrito.push(producto);
  console.log(`Producto agregado al carrito: ${producto.nombre}`);
  recalcularTotal(); // Llamada a la función para recalcular el total
  // Puedes realizar acciones adicionales aquí, como actualizar la interfaz de usuario
}

// Función para recalcular el total basado en los productos en el carrito
function recalcularTotal() {
  let total = 0;
  carrito.forEach((producto) => {
    total += producto.precio * producto.cantidad;
  });

  // Actualizar el campo de total en el formulario
  document.getElementById("total").value = total.toFixed(2); // Ajusta el total a dos decimales
}

// Ejemplo de uso (llamada a la función cuando el usuario hace clic en un botón)
const productoEjemplo = {
  nombre: "Ejemplo de producto",
  precio: 19.99,
  cantidad: 1,
};

// Agregar producto al carrito cuando el usuario hace clic en un botón
document.getElementById("botonAgregarAlCarrito").addEventListener("click", function () {
  agregarAlCarrito(productoEjemplo);
});

/**
 * Función para actualizar la vista previa de la imagen de perfil cargada
 */
function readURL(input) {
  if (input.files && input.files[0]) {
    var imageUrl = URL.createObjectURL(input.files[0]);
    $("#imagePreview").css("background-image", "url(" + imageUrl + ")");
    $("#imagePreview").hide();
    $("#imagePreview").fadeIn(650);
  }
}

$("#imageUpload").change(function () {
  readURL(this);
});

/**
 * Formatear cantidad en salario
 */
let salario = document.querySelector("#precio");
if (salario) {
  salario.addEventListener("input", (inputClick) => {
    let cantidad = inputClick.target.value.replace(/\D/g, "");
    cantidad = parseInt(cantidad, 10);
    if (isNaN(cantidad)) {
      cantidad = 0;
    }
    inputClick.target.value =
      "$ " +
      cantidad.toLocaleString("es-CO", {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0,
      });
  });
}

// Incluir la nueva función para calcular el cambio
function calcularCambio() {
  const total = parseFloat($("#total").val().replace(/[^\d.-]/g, '')) || 0;
  const pago = parseFloat($("#pago").val().replace(/[^\d.-]/g, '')) || 0;

  const cambio = pago - total;

  $("#cambio").val(`$ ${cambio.toFixed(2)}`);
}

$("#pago").on("input", calcularCambio);

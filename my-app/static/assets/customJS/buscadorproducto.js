async function buscadorTable2(tableId2) {
  let input, busqueda2, url;
  url = "/buscando-producto";

  input = document.getElementById("search2");
  busqueda2 = input.value.toUpperCase();

  const dataPeticion = { busqueda2 };
  const headers = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
  };

  try {
    const response = await axios.post(url, dataPeticion, { headers });
    if (!response.status) {
      console.log(`HTTP error! status: ${response.status}`);
    }

    if (response.data.fin === 0) {
      $(`#${tableId2} tbody`).html("");
      $(`#${tableId2} tbody`).html(`
      <tr>
        <td colspan="6" style="text-align:center;color: red;font-weight: bold;">No resultados para la busqueda: <strong style="text-align:center;color: #222;">${busqueda2}</strong></td>
      </tr>`);
      return false;
    }

    if (response.data) {
      $(`#${tableId2} tbody`).html("");
      let miData = response.data;
      $(`#${tableId2} tbody`).append(miData);
    }
  } catch (error) {
    console.error(error);
  }
}

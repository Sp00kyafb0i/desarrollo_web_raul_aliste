async function cargarActividades() {
  const res = await fetch('/api/actividades');
  const data = await res.json();
  const tbody = document.querySelector('#tabla tbody');
  tbody.innerHTML = "";
  data.forEach(act => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${act.id}</td>
      <td>${act.fechaInicio}</td>
      <td>${act.sector}</td>
      <td>${act.nombre}</td>
      <td>${act.tema}</td>
      <td>${act.notaPromedio !== null ? act.notaPromedio.toFixed(1) : '-'}</td>
      <td><button onclick="evaluar(${act.id}, this)">Evaluar</button></td>
    `;
    tbody.appendChild(tr);
  });
}

async function evaluar(id, btn) {
  const nota = prompt("Ingrese nota entre 1 y 7:");
  const notaInt = parseInt(nota);
  if (isNaN(notaInt) || notaInt < 1 || notaInt > 7) {
    alert("Nota inválida.");
    return;
  }
  const res = await fetch('/api/nota?actividadId=' + id + '&nota=' + notaInt, { method: 'POST' });
  const json = await res.json();
  if (json.success) {
    const td = btn.parentElement.previousElementSibling;
    td.textContent = json.nuevoPromedio.toFixed(1);
  }
}

cargarActividades();

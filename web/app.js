"use strict";

// Pilot app: a small task list. The baseline behaviour is what the first acceptance tests protect.
const tareas = [
  { titulo: "Escribir la especificación", estado: "Pendiente" },
  { titulo: "Revisar el pull request", estado: "En curso" },
  { titulo: "Publicar la versión", estado: "Hecha" },
];

const lista = document.getElementById("lista");

function pintar() {
  lista.replaceChildren(...tareas.map((t) => {
    const li = document.createElement("li");
    li.dataset.estado = t.estado;
    const titulo = document.createElement("span");
    titulo.className = "titulo";
    titulo.textContent = t.titulo;            // textContent: task titles are never parsed as HTML
    const estado = document.createElement("span");
    estado.className = "estado";
    estado.textContent = t.estado;
    li.append(titulo, " ", estado);
    return li;
  }));
}

document.getElementById("nueva").addEventListener("submit", (e) => {
  e.preventDefault();
  const campo = document.getElementById("titulo");
  const titulo = campo.value.trim();
  if (!titulo) { return; }
  tareas.push({ titulo, estado: "Pendiente" });
  campo.value = "";
  pintar();
  renderContador();
});

function renderContador() {
  const pendientes = tareas.filter((t) => t.estado !== "Hecha").length;
  document.getElementById("contador-pendientes").textContent = "Pendientes: " + pendientes;
}

pintar();
renderContador();

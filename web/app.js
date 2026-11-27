(function () {
  var visor = document.getElementById('visor');
  var grande = visor.querySelector('img');
  var cerrar = visor.querySelector('button');

  function cerrarVisor() {
    visor.hidden = true;
    grande.removeAttribute('src');
    grande.alt = '';
  }

  document.querySelector('.galeria').addEventListener('click', function (e) {
    var mini = e.target.closest('img');
    if (!mini) return;
    grande.src = mini.getAttribute('src');
    grande.alt = mini.alt;
    visor.hidden = false;
    cerrar.focus();
  });
  cerrar.addEventListener('click', cerrarVisor);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !visor.hidden) cerrarVisor();
  });
})();

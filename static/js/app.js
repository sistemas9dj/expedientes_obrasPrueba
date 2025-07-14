function cerrarModal(idModal) {
       var modal = document.getElementById(idModal);
       modal.style.display = "none"; //  o modal.classList.remove('show');
       //  Si quieres ocultar el fondo oscuro:
       //  document.querySelector('.modal-overlay').style.display = 'none';
     }

// Función para cerrar el modal al hacer clic fuera de él (opcional)
window.onclick = function(event) {
       var modals = document.getElementsByClassName('modal');
       for (var i = 0; i < modals.length; i++) {
         if (event.target == modals[i]) {
           modals[i].style.display = "none";
         }
       }
}

$(document).ready(function () {
    // MODAL Update INSPECTOR - Muestra los datos del Inspector seleccionado
    $('#update_Inspector').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let apellido = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDINSPECTOREditHIDDEN').val(id);
        modal.find('#NOMBREEdit').val(nombre);
        modal.find('#APELLIDOEdit').val(apellido);
    });

    // MODAL ELIMINAR INSPECTOR - Muestra los datos del Inspector seleccionado
    $('#delete_Inspector').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let apellido = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDINSPECTORDelHIDDEN').val(id);

        // Cambiar el título
        modal.find('.modal-title2').text('¿Estás seguro de eliminar el Inspector: ' + apellido +  ','  + nombre + ' ?');
        modal.find('#NOMBREDel').val(nombre);
        modal.find('#APELLIDODel').val(apellido);
     
    });

     // MODAL Update EstadoExpediente - Muestra los datos del Estado del Expediente
    $('#update_EstadoExpediente').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDESTADOEXPEDIENTEEditHIDDEN').val(id);
        modal.find('#NOMBREEdit').val(nombre);
        modal.find('#DESCRIPCIONEdit').val(descripcion);
    });

    // MODAL ELIMINAR EstadoExpediente - Muestra los datos del Estado del Expediente
    $('#delete_EstadoExpediente').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDESTADOEXPEDIENTEDelHIDDEN').val(id);
        modal.find('.modal-title2').text('¿Estás seguro de eliminar el Estado: ' + nombre + ' de los Expediente ?');     
    });


    // MODAL Update EstadoInspeccion - Muestra los datos del Estado de la Inspeccion
    $('#update_EstadoInspeccion').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDESTADOINSPECCIONEditHIDDEN').val(id);
        modal.find('#NOMBREEdit').val(nombre);
        modal.find('#DESCRIPCIONEdit').val(descripcion);
    });

    // MODAL ELIMINAR EstadoInspeccion - Muestra los datos del Estado de la Inspeccion
    $('#delete_EstadoInspeccion').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDESTADOINSPECCIONDelHIDDEN').val(id);
        modal.find('.modal-title2').text('¿Estás seguro de eliminar el Estado: ' + nombre + ' de las Inspecciones ?');     
    });

  // MODAL Update TipoExpediente - Muestra los datos del Tipo de Expediente
    $('#update_TipoExpediente').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDTIPOEXPEDIENTEEditHIDDEN').val(id);
        modal.find('#NOMBREEdit').val(nombre);
        modal.find('#DESCRIPCIONEdit').val(descripcion);
    });

    // MODAL ELIMINAR TipoExpediente - Muestra los datos del Tipo de Expediente
    $('#delete_TipoExpediente').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDTIPOEXPEDIENTEDelHIDDEN').val(id);
        modal.find('.modal-title2').text('¿Estás seguro de eliminar el Tipo: ' + nombre + ' de Expediente ?');     
    });
    

     // MODAL Update TipoObra - Muestra los datos del Tipo de Obra
    $('#update_TipoObra').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDTIPOOBRAEditHIDDEN').val(id);
        modal.find('#NOMBREEdit').val(nombre);
        modal.find('#DESCRIPCIONEdit').val(descripcion);
    });

    // MODAL ELIMINAR TipoObra - Muestra los datos del Tipo de Obra
    $('#delete_TipoObra').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDTIPOOBRADelHIDDEN').val(id);
        modal.find('.modal-title2').text('¿Estás seguro de eliminar el Tipo: ' + nombre + ' de Obra ?');     
    });


    // MODAL Update TipoProfesion - Muestra los datos del Tipo de Profesion
    $('#update_TipoProfesion').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDTIPOPROFESIONEditHIDDEN').val(id);
        modal.find('#NOMBREEdit').val(nombre);
        modal.find('#DESCRIPCIONEdit').val(descripcion);
    });

    // MODAL ELIMINAR TipoProfesion - Muestra los datos del Tipo de Profesion
    $('#delete_TipoProfesion').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDTIPOPROFESIONDelHIDDEN').val(id);
        modal.find('.modal-title2').text('¿Estás seguro de eliminar el Tipo: ' + nombre + ' de Profesion ?');     
    });


    // MODAL Update Profesional - Muestra los datos del Profesional
    $('#update_Profesional').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDPROFESIONALEditHIDDEN').val(id);
        modal.find('#NOMBREEdit').val(nombre);
        modal.find('#DESCRIPCIONEdit').val(descripcion);
    });

    // MODAL ELIMINAR Profesional - Muestra los datos del Profesional
    $('#delete_Profesional').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let descripcion = button.data('descripcion');

        let modal = $(this);
        modal.find('#IDPROFESIONALDelHIDDEN').val(id);
        modal.find('.modal-title2').text('¿Estás seguro de eliminar el Profesional: ' + nombre );     
    });
});


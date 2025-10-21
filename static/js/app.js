
function handleMask(event,mask){with(event){
		stopPropagation()
		preventDefault()
		if(!charCode)return
		var c=String.fromCharCode(charCode)
		if(c.match(/\D/))return
		with(target){var val=value.substring(0,selectionStart)+c+value.substr(selectionEnd)
		var pos=selectionStart+1}}
		var nan=count(val,/\D/,pos)
		val=val.replace(/\D/g,'')
		var mask=mask.match(/^(\D*)(.+9)(\D*)$/)
		if(!mask)return
		if(val.length>count(mask[2],/9/))return
		for(var txt='',im=0,iv=0;im<mask[2].length&&iv<val.length;im+=1){var c=mask[2].charAt(im)
		txt+=c.match(/\D/)?c:val.charAt(iv++)}
		with(event.target){value=mask[1]+txt+mask[3]
		selectionStart=selectionEnd=pos+(pos==1?mask[1].length:count(value,/\D/,pos)-nan)}
		function count(str,c,e){e=e||str.length
		for(var n=0,i=0;i<e;i+=1)if(str.charAt(i).match(c))n+=1
		return n}}
        
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

// Cuando se abre el modal Update Expediente
$('#update_Expediente').on('show.bs.modal', async function (event) {
    let button = $(event.relatedTarget);
    let idExpediente = button.data('id');  // el botón que abre el modal debe tener data-id

    let modal = $(this);
    modal.find('#IDEXPEDIENTEEditHIDDEN').val(idExpediente);

    //PROPIETARIOS
    // 🔹 1) Limpio tabla antes de cargar
    let tabla = document.getElementById("tablaPropietariosEdit");
    tabla.innerHTML = `
        <tr>          
            <td class="hr" width="10" align="left"></td>
            <td class="hr" width="10" align="left"></td>
            <td class="hr" width="50" align="left"><strong>CUIL/CUIT</strong></td>
            <td class="hr" width="50" align="left"><strong>APELLIDO</strong></td>
            <td class="hr" width="50" align="left"><strong>NOMBRE</strong></td>
            <td class="hr" width="50" align="left"><strong>PPAL.</strong></td>
        </tr>
    `;

    // 🔹 2) Llamo al backend para traer propietarios del expediente
    try {
        const resp = await fetch(`/expediente/${idExpediente}/propietarios`);
        
        if (!resp.ok) throw new Error("Error al cargar propietarios");
        const propietarios = await resp.json();
        // 🔹 3) Renderizo cada propietario en la tabla
        propietarios.forEach((p, idx) => {
            let style = (idx % 2 === 0) ? "dr" : "sr";
            let ppal = p.figuraPpal ? "SI" : "NO";

            let fila = `
                <td class='${style}' width='2'>
                    <input type='hidden' name='propEdit${idx+1}' id='propEdit${idx+1}' 
                        value='${p.cuil_cuit}/${p.apellido}/${p.nombre}/${p.figuraPpal}/${p.calle}/${p.nroCalle}/${p.piso}/${p.dpto}/${p.areaCelular}/${p.nroCelular}/${p.email}'>
                </td>
                <td class='${style}' width='10'>
                    <button type='button' class='btn' onClick='deletePropietarioEdit(${idx+1})' title='Borrar Propietario'>
                        <i class='icon-trash'></i>
                    </button>
                </td>
                <td class='${style}' width='50' align='left'>${p.apellido}</td>
                <td class='${style}' width='50' align='left'>${p.nombre}</td>
                <td class='${style}' width='50' align='left'>${p.cuil_cuit}</td>
                <td class='${style}' width='50' align='left'>${ppal}</td>
            `;

            let row = document.createElement("TR");
            row.id = idx+1;
            row.innerHTML = fila;
            tabla.appendChild(row);
        });

        // Actualizo el contador de filas
        document.getElementById("idFilaEdit").value = propietarios.length;
    
    } catch (err) {
        console.error("Error cargando propietarios: ", err);
        alert("No se pudieron cargar los propietarios");
    }

    //PROPFESIONALES
    // 🔹 1) Limpio tabla antes de cargar
    tabla = document.getElementById("tablaProfesionalesEdit");
    tabla.innerHTML = `
        <tr>          
            <td class="hr" width="10" align="left"></td>
            <td class="hr" width="10" align="left"></td>
            <td class="hr" width="50" align="left"><strong>PROFESIONAL</strong></td>
            <td class="hr" width="50" align="left"><strong>PPAL.</strong></td>
        </tr>
    `;

    // 🔹 2) Llamo al backend para traer PROFESIONALES del expediente
    try {
        const resp = await fetch(`/expediente/${idExpediente}/profesionales`);
        
        if (!resp.ok) throw new Error("Error al cargar profesionales");
            const profesionales = await resp.json();
            // 🔹 3) Renderizo cada profesional en la tabla
            profesionales.forEach((p, idx) => {
                let style = (idx % 2 === 0) ? "dr" : "sr";
                let ppal = p.figuraPpal ? "SI" : "NO";

                // valor= idProfesional + "/" + contactoPpal;
                let fila = `
                    <td class='${style}' width='2'>
                        <input type='hidden' name='profEdit${idx+1}' id='profEdit${idx+1}' 
                            value='${p.idProfesional}/${p.contactoPpal}'>
                    </td>
                    <td class='${style}' width='10'>
                        <button type='button' class='btn' onClick='deleteProfesionalEdit(${idx+1})' title='Borrar Profesional'>
                            <i class='icon-trash'></i>
                        </button>
                    </td>
                    <td class='${style}' width='50' align='left'>${p.apellido}, ${p.nombre} /Mat. ${p.matricula}</td>
                    <td class='${style}' width='50' align='left'>${ppal}</td>
                `;

                let row = document.createElement("TR");
                row.id = idx+1;
                row.innerHTML = fila;
                tabla.appendChild(row);
        });

        // Actualizo el contador de filas
        document.getElementById("idFilaEdit").value = propietarios.length;
    } catch (err) {
            console.error("Error cargando profesionales: ", err);
            alert("No se pudieron cargar los profesionales");
        }

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
        modal.find('.modal-title2').text('¿Estás seguro de eliminar el Tipo de Profesión: ' + nombre + ' ?');     
    });

 
    // MODAL Update Profesional - Muestra los datos del Profesional
    $('#update_Profesional').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nombre = button.data('nombre');
        let apellido = button.data('apellido');
        let cuil = button.data('cuil');
        let calle = button.data('calle');
        let nrocalle = button.data('nrocalle');
        let piso = button.data('piso');
        let dpto = button.data('dpto');
        let areacel = button.data('areacel');
        let nrocel = button.data('nrocel');
        let idtipoprofesion = button.data('idtipoprof');
        let matricula = button.data('matricula');
        let razonsocial = button.data('razonsocial');
        let mail = button.data('mail');
     
        let modal = $(this);

        modal.find('#IDPROFESIONALEditHIDDEN').val(id);
        modal.find('#apellidoEdit').val(apellido);
        modal.find('#nombreEdit').val(nombre);
        modal.find('#cuil_cuitEdit').val(cuil);
        modal.find('#calleEdit').val(calle);
        modal.find('#nroCalleEdit').val(nrocalle);
        modal.find('#pisoEdit').val(piso);
        modal.find('#dptoEdit').val(dpto);
        modal.find('#areaCelularEdit').val(areacel);
        modal.find('#nroCelularEdit').val(nrocel);
        modal.find('#idTipoProfesionEdit').val(idtipoprofesion);
        //modal.find('.modal-body #IdTipoProfesionEdit').val(idtipoprofesion);

        modal.find('#matriculaEdit').val(matricula);
        modal.find('#razonSocialEdit').val(razonsocial);
        modal.find('#emailEdit').val(mail);

    });

    // MODAL ELIMINAR Profesional - Muestra los datos del Profesional
    $('#delete_Profesional').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let apellido = button.data('apellido');
        let nombre = button.data('nombre');
        
        let modal = $(this);
        modal.find('#IDPROFESIONALDelHIDDEN').val(id);
        modal.find('.modal-title2').text('¿Estás seguro de eliminar el Profesional: ' + apellido + ', ' + nombre );     
    });


   // MODAL Update Expediente - Muestra los datos del Expediente
    $('#update_Expediente').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
    
        let id = button.data('id');
        let idTipoObra = button.data('idtipoobra');
        let nroExpediente = button.data('nroexpediente');
        let nroPartida = button.data('nropartida');
        let nroExpedienteMesaEntrada = button.data('nroexpedientemesaentr');
        let anioMesaEntrada = button.data('aniomesaentr');
        let sucesion = button.data('sucesion');
        let observaciones = button.data('observaciones');
        let idEstadoExpediente = button.data('idestadoexpediente');
       
        let modal = $(this);

        modal.find('#IDEXPEDIENTEEditHIDDEN').val(id);
        modal.find('#idTipoObraEdit').val(idTipoObra);
        modal.find('#nroExpedienteEdit').val(nroExpediente);
        modal.find('#nroPartidaEdit').val(nroPartida);
        modal.find('#nroExpedienteMesaEntradaEdit').val(nroExpedienteMesaEntrada);
        modal.find('#anioMesaEntradaEdit').val(anioMesaEntrada);
        modal.find('#sucesionEdit').val(sucesion);
        modal.find('#observacionesEdit').val(observaciones);
        modal.find('#idEstadoExpedienteEdit').val(idEstadoExpediente);
        modal.find('#IDESTADOEXPEDIENTEEditHIDDEN').val(idEstadoExpediente);
             
    });

    // MODAL ELIMINAR Expediente - Muestra los datos del Expediente
    $('#delete_Expediente').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget);
        let id = button.data('id');
        let nroExpediente = button.data('nroexpediente');
        
        let modal = $(this);
        modal.find('#IDEXPEDIENTEDelHIDDEN').val(id);
        modal.find('.modal-title2').text('¿Estás seguro de eliminar el Expediente: ' +  nroExpediente );     
    });
    
});


    //Estado Expediente
    //Estado de Expediente = "Liquidacion Derecho Construccion Urbanismo"
    ESTADO_LIQ_DER_CONTRUCCION_URB = 11

    function insertarPropietario(sufijo){
        const idFilaInput = document.getElementById("idFila" + sufijo);
        let idFila = Number(idFilaInput.value);

        // Leo Datos Personales
        let nombre = document.getElementById("nombre" + sufijo).value;
        let apellido = document.getElementById("apellido" + sufijo).value;
        let cuil_cuit = document.getElementById("cuil_cuit" + sufijo).value;
        let figuraPpal = document.getElementById("figuraPpal" + sufijo).value;

        // Leo datos Contacto
        let calle = document.getElementById("calle" + sufijo).value;
        let nroCalle = document.getElementById("nroCalle" + sufijo).value;
        let piso = document.getElementById("piso" + sufijo).value;
        let dpto = document.getElementById("nroDpto" + sufijo).value;
        let areaCelular = document.getElementById("areaCelular" + sufijo).value;
        let nroCelular = document.getElementById("nroCelular" + sufijo).value;
        let email = document.getElementById("email" + sufijo).value;

        if(nombre === ''){ alert("El Nombre del Propietario es obligatorio."); return; }
        if(apellido === ''){ alert("El Apellido del Propietario es obligatorio."); return; }
        if(cuil_cuit === ''){ alert("La CUIL/CUIT es obligatoria."); return; }

        let valor = cuil_cuit + "/" + apellido + "/" + nombre + "/" + figuraPpal + "/" +
                    calle + "/" + nroCalle + "/" + piso + "/" + dpto + "/" +
                    areaCelular + "/" + nroCelular + "/" + email;

        let style = (idFila % 2 !== 0) ? "sr" : "dr";
        let ppal = (figuraPpal == 0) ? "NO" : "SI";

        let fila = `
            <td class="${style}" width="2">
                <input type="hidden" name="prop${sufijo}${idFila}" id="prop${sufijo}${idFila}" value="${valor}">
            </td>
            <td class="${style}" width="10">
                <button type="button" class="btn" onclick="deletePropietario('${sufijo}', ${idFila})">
                    <i class="icon-trash"></i>
                </button>
            </td>
            <td class="${style}" width="50">${apellido}</td>
            <td class="${style}" width="50">${nombre}</td>
            <td class="${style}" width="50">${cuil_cuit}</td>
            <td class="${style}" width="50">${ppal}</td>
        `;

        let tr = document.createElement("tr");
        tr.id = "filaProp" + sufijo + idFila;
        tr.innerHTML = fila;

        document.getElementById("tablaPropietarios" + sufijo).appendChild(tr);

        idFilaInput.value = idFila + 1;
    }

    function deletePropietario(sufijo, idFila){
        const fila = document.getElementById("filaProp" + sufijo + idFila);
        if (fila) fila.remove();
    } 

    function insertarProfesionales(sufijo){
        const idFilaInput = document.getElementById("idFilaProf" + sufijo);
        let idFila = Number(idFilaInput.value);

        // Leo Profesional (formato: id*Apellido,Nombre/Matrícula)
        let profesionalFull = document.getElementById("idProfesional" + sufijo).value;

        if(profesionalFull === ''){
            alert("El Profesional es de ingreso obligatorio.");
            return;
        }

        // Extraigo ID
        let pos = profesionalFull.indexOf("*");
        let idProfesional = profesionalFull.substring(0, pos);
        let profesional = profesionalFull.substring(pos + 1);

        let contactoPpal = document.getElementById("contactoPpal" + sufijo).value;

        let valor = idProfesional + "/" + contactoPpal;

        let style = (idFila % 2 !== 0) ? "sr" : "dr";
        let ppal = (contactoPpal == 0) ? "NO" : "SI";

        let fila = `
            <td class="${style}" width="2">
                <input type="hidden" name="prof${sufijo}${idFila}" id="prof${sufijo}${idFila}" value="${valor}">
            </td>
            <td class="${style}" width="10">
                <button type="button" class="btn" onclick="deleteProfesional('${sufijo}', ${idFila})">
                    <i class="icon-trash"></i>
                </button>
            </td>
            <td class="${style}" width="50">${profesional}</td>
            <td class="${style}" width="50">${ppal}</td>
        `;

        let tr = document.createElement("tr");
        tr.id = "filaProf" + sufijo + idFila;
        tr.innerHTML = fila;

        document.getElementById("tablaProfesionales" + sufijo).appendChild(tr);

        idFilaInput.value = idFila + 1;
    }

    function deleteProfesional(sufijo, idFila){
        const fila = document.getElementById("filaProf" + sufijo + idFila);
        if (fila) fila.remove();
    }

    
    //Validaciones
  /*  function validarEstadoExpediente(sufijo) {
    //Funcion que valida el ingreso obligatorio de los campos
    //  EstadoExpediente =  Liquidación Derecho Construcción Urbanismo (valor 11)

        //alert ("A validar estado ");

        const selectEstado = document.getElementById("idEstadoExpediente"+sufijo).value;
        if (selectEstado !== "11") return true; // No aplica validación
        
        const selectPago = document.getElementById("idTipoPago"+sufijo).value;
        const fechaContado = document.getElementById("fechaPagoContado"+sufijo).value;
        const cantCuotas = document.getElementById("cantCuotas"+sufijo).value;
        const fechaPrimera = document.getElementById("fechaPagoPrimerCta"+sufijo).value;
        const fechaUltima = document.getElementById("fechaPagoUltimaCta"+sufijo).value;

        //alert ("fechaContado: " + fechaContado);
        //alert ("cantCuotas: " + cantCuotas);
        //alert ("fechaPrimera: " + fechaPrimera);
        //alert ("fechaUltima: " + fechaUltima);

        if (selectPago === "1"){ //Corresponde a Tipopago = CONTADO
            if(!fechaContado){
                    alert('Se ha seleccionado estado de Expediente: Liquidación Derecho Construcción Urbanismo y tipo de pago CONTADO por lo tanto debe ingresar la fecha de Pago');
                    return false;
            }
        }else{
                if(!cantCuotas){
                    alert('Se ha seleccionado estado de Expediente: Liquidación Derecho Construcción Urbanismo y tipo de pago CUOTAS por lo tanto debe ingresar la cantidad de ctas del plan seleccioando');
                    return false;   
                }

                if(cantCuotas <= 1){
                    alert('Se ha seleccionado estado de Expediente: Liquidación Derecho Construcción Urbanismo y tipo de pago CUOTAS por lo tanto la cantidad de ctas debe ser superior a l.');
                    return false;   
                }

                if(!fechaPrimera){
                    alert('Se ha seleccionado estado de Expediente: Liquidación Derecho Construccion Urbanismo y tipo de pago CUOTAS por lo tanto debe ingresar las fecha de Pago de la primera Cta');
                    return false;   
                }

                if (!fechaUltima){
                    alert('Se ha seleccionado estado de Expediente: Liquidación Derecho Construccion Urbanismo y tipo de pago CUOTAS por lo tanto debe ingresar las fecha de Pago de la última Cta');
                    return false;   
                }
        }

        return true; 
    }
   
    */

    
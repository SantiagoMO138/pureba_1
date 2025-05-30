$(document).ready(function () {
    $.ajax({
        url: "/api/list_clientes",
        method: "GET",
        dataType: "json",
        success: function (data) {
            cargarTabla(data);
        },
        error: function (xhr, status, error) {
            console.error("Error al cargar los datos:", error);
        }
    });
    cargarOpcionesFormulario();
});

function cargarTabla(data) {
    const cuerpo = data.map(d => [
        d.id_cliente,
        d.ci,
        d.nombre,
        d.telefono,
        d.correo_electronico,
        d.lineadireccion1,
        d.lineadireccion2 || '',
        d.ciudad,
        d.region || '',
        d.pais || ''
    ]);

    $('#tablaClientes').DataTable({
        data: cuerpo,
        columns: [
            { title: "ID", visible: false },
            { title: "CI" },
            { title: "Nombre" },
            { title: "Teléfono" },
            { title: "Correo Electrónico" },
            { title: "Dirección 1" },
            { title: "Dirección 2" },
            { title: "Ciudad" },
            { title: "Región" },
            { title: "País" },
            {
                title: "Acciones",
                orderable: false,
                searchable: false,
                className: "text-center",
                render: function (data, type, row, meta) {
                    const id = row[0];
                    return `
                    <button class="btn btn-sm btn-warning btn-editar me-1">
                        <i class="fas fa-edit"></i> Editar
                    </button>
                    <button class="btn btn-sm btn-danger btn-eliminar" data-id="${id}">
                        <i class="fas fa-trash-alt"></i> Eliminar
                    </button>`;
                }
            }
        ],
        responsive: true
    });
}

function cargarOpcionesFormulario() {
    $.ajax({
        url: '/api/opciones',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            llenarCombo('#addCiudad', data.ciudades);
            llenarCombo('#addRegion', data.regiones);
            llenarCombo('#addPais', data.paises);
            llenarCombo('#editarCiudad', data.ciudades);
            llenarCombo('#editarRegion', data.regiones);
            llenarCombo('#editarPais', data.paises);
        },
        error: function () {
            console.error("Error al cargar combos");
        }
    });
}

function llenarCombo(selector, valores) {
    const select = $(selector);
    select.empty();
    select.append('<option value="">-- Seleccione --</option>');
    valores.forEach(v => {
        select.append(`<option value="${v}">${v}</option>`);
    });
}

// Add Client
$('#formAgregar').on('submit', function (e) {
    e.preventDefault();

    const datos = {
        ci: this.ci.value,
        nombre: this.nombre.value,
        telefono: this.telefono.value,
        correo_electronico: this.correo_electronico.value,
        lineadireccion1: this.lineadireccion1.value,
        lineadireccion2: this.lineadireccion2.value,
        ciudad: this.ciudad.value,
        region: this.region.value,
        pais: this.pais.value
    };

    $.ajax({
        url: '/add/clientes',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(datos),
        success: function (response) {
            $('#modalAgregar').modal('hide');
            $('#formAgregar')[0].reset();
            $('#tablaClientes').DataTable().destroy();
            cargarDatos();
            mostrarToast('👤 Cliente agregado con éxito', 'success');
        },
        error: function () {
            alert('Error al guardar el cliente.');
        }
    });
});

function cargarDatos() {
    $('#loader').removeClass('d-none');
    $.ajax({
        url: "/api/list_clientes",
        method: "GET",
        dataType: "json",
        success: function (data) {
            $('#tablaClientes').DataTable().clear().destroy();
            cargarTabla(data);
        },
        error: function () {
            alert("Error al cargar datos");
        },
        complete: function () {
            $('#loader').addClass('d-none');
        }
    });
}

function mostrarToast(mensaje, tipo = 'primary') {
    const toastEl = $('#toastNotificacion');
    const toastBody = $('#toastMensaje');

    toastEl.removeClass('bg-primary bg-success bg-danger bg-warning');
    toastEl.addClass(`bg-${tipo}`);
    toastBody.text(mensaje);

    const toast = new bootstrap.Toast(toastEl[0]);
    toast.show();
}

// Delete Client
$('#tablaClientes').on('click', '.btn-eliminar', function () {
    const id = $(this).data('id');
    if (confirm("¿Estás seguro de eliminar este cliente?")) {
        $.ajax({
            url: `/del/clientes/${id}`,
            method: 'DELETE',
            success: function () {
                mostrarToast('❌ Cliente eliminado', 'danger');
                cargarDatos();
            },
            error: function () {
                alert("Error al eliminar");
            }
        });
    }
});

// Edit Client
$('#tablaClientes').on('click', '.btn-editar', function () {
    const row = $(this).closest('tr');
    const data = $('#tablaClientes').DataTable().row(row).data();
    $('#editarId').val(data[0]);
    $('#editarCi').val(data[1]);
    $('#editarNombre').val(data[2]);
    $('#editarTelefono').val(data[3]);
    $('#editarCorreo').val(data[4]);
    $('#editarLineaDireccion1').val(data[5]);
    $('#editarLineaDireccion2').val(data[6]);
    $('#editarCiudad').val(data[7]);
    $('#editarRegion').val(data[8]);
    $('#editarPais').val(data[9]);

    const modal = new bootstrap.Modal(document.getElementById('modalEditar'));
    modal.show();
});

// Save Edit
$('#formEditar').on('submit', function (e) {
    e.preventDefault();
    const id = $('#editarId').val();

    const datos = {
        ci: $('#editarCi').val(),
        nombre: $('#editarNombre').val(),
        telefono: $('#editarTelefono').val(),
        correo_electronico: $('#editarCorreo').val(),
        lineadireccion1: $('#editarLineaDireccion1').val(),
        lineadireccion2: $('#editarLineaDireccion2').val(),
        ciudad: $('#editarCiudad').val(),
        region: $('#editarRegion').val(),
        pais: $('#editarPais').val()
    };

    $.ajax({
        url: `/upd/clientes/${id}`,
        method: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(datos),
        success: function () {
            $('#modalEditar').modal('hide');
            mostrarToast('✏️ Cliente actualizado', 'warning');
            cargarDatos();
        },
        error: function () {
            alert('Error al actualizar');
        }
    });
});
//var data2 = {"0": [1001, 1002, 20009], "10": [1003, 1004, 1006, 1001, 1002, 1003, 1004, 1006, 2010, 9002], "8": [1007], "9": [1010], "7": [1011], "6": [1012], "4": [1012]}
var data = '{{ data_json | safe}}';
var data_services = '{{ data_json_services | safe }}'
var data_recomendar = '{{ data_json_recomendar | safe }}'
var data_calificacion_instalaciones_amenidades = '{{ data_json_calificacion_instalaciones_amenidades | safe }}'
var data_capacidad_asesor_generar_confianza = '{{ data_json_calificacion_atencion_asesor | safe }}'
var data_calificacion_asesor_general = '{{ data_json_data_calificacion_asesor_general | safe }}'


//Se trasforman las variables a tipo object "JDSON"
var data = JSON.parse(data);
var data_services = JSON.parse(data_services);
var data_recomendar = JSON.parse(data_recomendar);
var data_calificacion_instalaciones_amenidades = JSON.parse(data_calificacion_instalaciones_amenidades);
var data_capacidad_asesor_generar_confianza = JSON.parse(data_capacidad_asesor_generar_confianza);
var data_calificacion_asesor_general = JSON.parse(data_calificacion_asesor_general);



Highcharts.chart('container1', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',
        backgroundColor: '#F4F4F4',
    },
    title: {
        text: 'Calificación al programar cita'
    },
    tooltip: {
        pointFormatter: function () {
            return 'Orden(es): ' + data[this.name].join(', ');
        }
    },
    series: [{
        name: 'Cantidad',
        colorByPoint: true,
        data: processData(data)
    }]
});

// Configuración de la gráfica de barras de tipos de servicio
Highcharts.chart('container2', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'bar',
        backgroundColor: '#F4F4F4',
    },
    title: {
        text: 'Distribución de servicios'
    },

    plotOptions: {
        series: {
            borderWidth: 0,
            dataLabels: {
                enabled: true,
                format: '{point.y:.1f}%'
            }
        }
    },

    tooltip: {
        pointFormatter: function () {
            return 'Orden(es): ' + data_services[this.name].join(', ');
        }
    },
    series: [{
        name: 'Cantidad',
        colorByPoint: true,
        data: processData(data_services)
    }],
    xAxis: {
        categories: Object.keys(data_services)
    },
    yAxis: {
        title: {
            text: ''
        }
    },
});

Highcharts.chart('container3', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',
        backgroundColor: '#F4F4F4',
    },
    title: {
        text: 'Recomiendan Mitsubishi San Angel',
        align: 'center',
    },
    tooltip: {
        pointFormatter: function () {
            return 'Orden(es): ' + data_recomendar[this.name].join(', ');
        }
    },


    series: [{
        name: 'Cantidad',
        colorByPoint: true,
        data: processData(data_recomendar)
    }]
});

Highcharts.chart('container4', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',
        backgroundColor: '#F4F4F4',
    },
    title: {
        text: 'Calificación del servicio en general'
    },
    tooltip: {
        pointFormatter: function () {
            return 'Orden(es): ' + data_calificacion_instalaciones_amenidades[this.name].join(', ');
        }
    },
    series: [{
        name: 'Calificacinoes',
        colorByPoint: true,
        data: processData(data_calificacion_instalaciones_amenidades)
    }]
});

Highcharts.chart('container5', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',
        backgroundColor: '#F4F4F4',
    },
    title: {
        text: 'Calificación de la entrega'
    },
    tooltip: {
        pointFormatter: function () {
            return 'Orden(es): ' + data_capacidad_asesor_generar_confianza[this.name].join(', ');
        }
    },
    series: [{
        name: 'Cantidad',
        colorByPoint: true,
        data: processData(data_capacidad_asesor_generar_confianza)
    }]
});

Highcharts.chart('container6', {
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        type: 'pie',
        backgroundColor: '#F4F4F4',
    },
    title: {
        text: 'Calificación general al asesor'
    },
    tooltip: {
        pointFormatter: function () {
            return 'Orden(es): ' + data_calificacion_asesor_general[this.name].join(', ');
        }
    },
    series: [{
        name: 'Cantidad',
        colorByPoint: true,
        data: processData(data_calificacion_asesor_general)
    }]
});

// Función para convertir el JSON en un formato que Highcharts.js pueda entender
function processData(data) {
    var processedData = [];
    for (var key in data) {
        processedData.push({ name: key, y: data[key].length });
    }
    return processedData;
}


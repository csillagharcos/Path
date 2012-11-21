jqplot_percent = {
    seriesDefaults: { renderer: $.jqplot.BarRenderer },
    axes: {
        xaxis:{
            renderer:$.jqplot.CategoryAxisRenderer,
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            tickOptions: {
                labelPosition: 'end',
                fontSize: 10
            }
        },
        yaxis:{
            ticks: [0,25,50,75,100],
            tickOptions: {
                formatString: '%.2f'
            }
        }
    },
    highlighter: {
        show: true,
        tooltipAxes: 'y',
        formatString: '%.2f%'
    }
}

var jqplot_time = {
    seriesDefaults: {renderer: $.jqplot.BarRenderer},
    axes: {
        xaxis:{
            renderer:$.jqplot.CategoryAxisRenderer,
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            tickOptions: {
                angle: -30,
                labelPosition: 'end',
                fontSize: 10
            }
        },
        yaxis:{
            renderer:$.jqplot.DateAxisRenderer,
            ticks: ['00:00:00', '00:30:00', '01:00:00', '01:30:00', '02:00:00', '02:30:00', '03:00:00'],
            tickOptions:{
                formatString: '%T'
            }
        }
    },
    highlighter: {
        show: true,
        tooltipAxes: 'y',
        formatString: '<span class="font-size: 12px">%s</span>'
    }
}

var jqplot_days = {
    seriesDefaults: {renderer: $.jqplot.BarRenderer},
    axes: {
        xaxis:{
            renderer:$.jqplot.CategoryAxisRenderer,
            tickRenderer: $.jqplot.CanvasAxisTickRenderer,
            tickOptions: {
                angle: -30,
                labelPosition: 'end',
                fontSize: 10
            }
        },
        yaxis:{
            ticks: [0,5,10,15,20,25,30],
            tickOptions:{
                formatString: '%.2f'
            }
        }
    },
    highlighter: {
        show: true,
        tooltipAxes: 'y',
        formatString: '<span class="font-size: 12px">%.2f</span>'
    }
}
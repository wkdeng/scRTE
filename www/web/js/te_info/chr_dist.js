/**
 * @author [Wankun Deng]
 * @email [dengwankun@gmail.com]
 * @create date 2023-05-04 18:19:24
 * @modify date 2023-05-16 00:26:07
 * @desc [description]
 */

Highcharts.setOptions({
    colors: ["#386cb0", "#fdb462", "#7fc97f", "#ef3b2c", "#662506", "#a6cee3", "#fb9a99"]
});


function showChrDist(data) {
    const chartChrDist = Highcharts.chart('container_chr_dist', {
        title: {
            text: 'Number of Locuses in Each Chromosome',
            align: 'left'
        },
        subtitle: {
            text: "",
            align: 'left'
        },
        xAxis: {
            title: {
                text: 'Chromosome',
            },
            categories: ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY', 'chrM', 'others']
        },
        yAxis: {
            title: {
                text: 'Number of Locuses'
            }
        },
        credits: {
            enabled: false
        },
        legend: {
            enabled: false
        },
        series: [{ name: 'Locus number', type: 'column', colorByPoint: true, data: data }]
    });
    document.getElementById('plain_chrdist').addEventListener('click', () => {
        series = chartChrDist.series
        series[0].update({ type: 'column' })
        chartChrDist.update({
            chart: {
                inverted: false,
                polar: false
            },
        });
    });
    document.getElementById('inverted_chrdist').addEventListener('click', () => {
        series = chartChrDist.series
        series[0].update({ type: 'column' })
        chartChrDist.update({
            chart: {
                inverted: true,
                polar: false
            }
        });
    });
    document.getElementById('line_chrdist').addEventListener('click', () => {
        series = chartChrDist.series
        series[0].update({ type: 'line' })
        chartChrDist.update({
            chart: {
                inverted: false,
                polar: false
            }
        });
    });
    document.getElementById('pie_chrdist').addEventListener('click', () => {
        series = chartChrDist.series
        series[0].update({ type: 'pie' })
        chartChrDist.update({
            chart: {
                inverted: false,
                polar: false
            }
        });
    });
}
function showChrEaDist(data) {
    const chartChrEaDist = Highcharts.chart('container_chrea_dist', {
        chart: {
            type: 'heatmap',
            // inverted: true,
            spacingBottom: 15,
            spacingTop: 10,
            spacingLeft: 10,
            spacingRight: 10,
        },
        colorAxis: {
            min: 0,
            minColor: '#FFFFFF',
            maxColor: Highcharts.getOptions().colors[0]
        },
        title: {
            text: 'Number of Locus in Each Chromosome',
            align: 'left'
        },
        subtitle: {
            text: "",
            align: 'left'
        },
        xAxis: {
            title: {
                text: 'Chromosome',
            },
            categories: ['chr1', 'chr2', 'chr3', 'chr4', 'chr5', 'chr6', 'chr7', 'chr8', 'chr9', 'chr10', 'chr11', 'chr12', 'chr13', 'chr14', 'chr15', 'chr16', 'chr17', 'chr18', 'chr19', 'chr20', 'chr21', 'chr22', 'chrX', 'chrY', 'chrM']

        },
        yAxis: {
            title: {
                text: 'Location on Chromosome (Bins)'
            },
            categories: Array(100).fill().map((element, index) => index)
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            series: {
                turboThreshold: 0
            }
        },
        legend: {
            align: 'right',
            layout: 'vertical',
            margin: 0,
            verticalAlign: 'top',
            y: 30,
            symbolHeight: 280
        },
        series: [{
            name: 'Locus number',
            borderWidth: 0,
            data: data,
            datalabels: { enabled: false }
        }],
        // responsive: {
            // rules: [{
            //     condition: {
            //         maxWidth: 500
            //     },
            //     chartOptions: {
            //         yAxis: {
            //             labels: {
            //                 formatter: function () {
            //                     return this.value.charAt(0);
            //                 }
            //             }
            //         }
            //     }
            // }]
        // }

    });
}

function showRegionDist(data) {
    Highcharts.chart('container_region_dist', {
        title: {
            text: 'Number of Locus in Genomic Regions',
            align: 'left'
        },
        subtitle: {
            text: "",
            align: 'left'
        },
        xAxis: {
            title: {
                text: 'Chromosome',
            },
            categories: ['Genic', 'Intergenic']

        },
        yAxis: {
            title: {
                text: 'Number of Locuses'
            }
        },
        credits: {
            enabled: false
        },
        legend: {
            enabled: false
        },
        series: [{ name: 'Locus number', type: 'pie', colorByPoint: true, data: data }]
    });
}
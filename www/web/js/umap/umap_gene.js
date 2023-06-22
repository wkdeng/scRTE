Highcharts.setOptions({
    colors: ["#386cb0","#fdb462","#7fc97f","#ef3b2c","#662506","#a6cee3","#fb9a99"]
  });
 
const qstring = window.location.search;
const uparams = new URLSearchParams(qstring);
var dataset=uparams.get('KW');
  async function getGeneExpData(gene) {
    if(gene == null){
      gene='AluY'
    }
    const response = await fetch(
        '/scARE/cgi/get_gene_umap.py?Gene='+gene+'&Dataset='+dataset
    );
    return response.json();
  }
  
  maxColor = new Highcharts.Color('#ff0000'); // red
  calculateColor = function( min, max, value) {
      color = new Highcharts.Color('#ffff00');
      minCol= new Highcharts.Color('#000000');
      interval = max - min;
      adjustedValue = value - min;
      alpha = adjustedValue / interval;
      if(value > 0){
        return color.tweenTo(maxColor, alpha);
      }else{
        return 'rgba(200,200,200,50)';
      }
  }
  getGeneExpData(document.getElementById('geneInput').value).then(data => {
    var [min, max] = d3.extent(data.flatMap(d => d.value));
    var data_s=[];
    data.forEach(elm => {
            data_s.push({ x:elm.x,y:elm.y,cell_id:elm.CELL,value:elm.value,color:calculateColor(min, max, elm.value)});
            
      });
    umap_gene_chart = Highcharts.chart('container_gene_exp', {
      chart: {
        type: 'scatter',
        zoomType: 'xy'
      },
      title: {
        text: 'Gene Expression',
        align: 'left'
      },
      subtitle: {
        text:
        dataset,
        align: 'left'
      },
      xAxis: {
        title: {
          text: 'UMAP_1'
        },
        labels: {
          format: '{value}'
        },
        startOnTick: true,
        endOnTick: true,
        showLastLabel: true
      },
      yAxis: {
        title: {
          text: 'UMAP_2'
        },
        labels: {
          format: '{value}'
        }
      },
      credits: {
        enabled: false
      },
      legend: {
        enabled: false
      },
      plotOptions: {
        series: {
            turboThreshold: 0
        },
        scatter: {
          marker: {
            radius: 2.5,
            symbol: 'circle',
            states: {
              hover: {
                enabled: true,
                lineColor: 'rgb(100,100,100)'
              }
            }
          },
          states: {
            hover: {
              marker: {
                enabled: false
              }
            }
          }
        }
      },
    //   series:{
    //     turboThreshold: 0
    //   },
      tooltip: {
        pointFormat: 'Cell: {point.cell_id} <br/> UMAP_1: {point.x} <br/> UMAP_2: {point.y} </br> Expression: {point.value}'
      },
      series:[{
        name:"",
        data: data_s
      }]
    }
    );
    $("div[aria-live='assertive']").attr("aria-atomic", true);
  }
  );


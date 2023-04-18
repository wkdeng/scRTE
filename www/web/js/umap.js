Highcharts.setOptions({
    colors: ["#386cb0","#fdb462","#7fc97f","#ef3b2c","#662506","#a6cee3","#fb9a99"]
  });
  
  const series = [{
    name: 'Excitatory Neurons',
    id: 'Ex',
    marker: {
      symbol: 'circle'
    }
  },
  {
    name: 'Inhibitory Neurons',
    id: 'In',
    marker: {
      symbol: 'circle'
    }
  },{
    name: 'Oligodentrocyte Progenitor Cells',
    id: 'Opc',
    marker: {
      symbol: 'circle'
    }
  },{
    name: 'Oligodendrocytes',
    id: 'Oli',
    marker: {
      symbol: 'circle'
    }
  },{
    name: 'Astrocytes',
    id: 'Ast',
    marker: {
      symbol: 'circle'
    }
  },{
    name: 'Microglia',
    id: 'Mic',
    marker: {
      symbol: 'circle'
    }
  },{
    name: 'Pericytes',
    id: 'Per',
    marker: {
      symbol: 'circle'
    }
  }];
  
  const serries_map={'Ex':0,'In':1,'Opc':2,'Oli':3,'Ast':4,'Mic':5,'Per':6}
  async function getData() {
    const response = await fetch(
        '/cgi/get_data_umap.py?Dataset=SRR11422700'
    );
    return response.json();
  }
  
  
  getData().then(data => {
    const getData = CellType => {
      const temp = [];
      data.forEach(elm => {
        if (elm.CELL_TYPE === CellType) {
          temp.push({ x:elm.UMAP_1,y:elm.UMAP_2,cell_id:elm.CELL});
        //   temp.push([elm.UMAP_1,elm.UMAP_2]);
        }
      });
      return temp;
    };
    series.forEach(s => {
      s.data = getData(s.id);
    });
  
    const chart = Highcharts.chart('container', {
      chart: {
        type: 'scatter',
        zoomType: 'xy'
      },
      title: {
        text: 'Cell Type UMAP',
        align: 'left'
      },
      subtitle: {
        text:
        'SRR11422700',
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
        enabled: true
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
        pointFormat: 'Cell: {point.cell_id} <br/> UMAP_1: {point.x} <br/> UMAP_2: {point.y} </br> '
      },
      series
    });
    document.getElementById('cell_types').addEventListener('change', () => {
        var series=chart.series;
        var cell_types=document.getElementById('cell_types').value;
        for(let i=0; i< series.length; i++){
            if(cell_types==-1 || i==cell_types){
                series[i].show();}
            else{
                series[i].hide();
                }            
        }


      });
  });


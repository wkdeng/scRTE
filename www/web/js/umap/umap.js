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
    id: 'OPC',
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
    name: 'Endothelial',
    id: 'Endo',
    marker: {
      symbol: 'circle'
    }
  },{
    name: 'VLMC',
    id: 'VLMC',
    marker: {
      symbol: 'circle'
    }
  }];
  
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);

  async function getCellUMAPData() {
    const response = await fetch(
        '/scARE/cgi/get_data_umap.py?Dataset='+urlParams.get('KW')
    );
    return response.json();
  }
  
  
  getCellUMAPData().then(data => {
    const parseCellUMAP = CellType => {
      const temp = [];
      data.forEach(elm => {
        if (elm.CELL_TYPE === CellType) {
          temp.push({ x:elm.UMAP_1,y:elm.UMAP_2,cell_id:elm.CELL});
        }
      });
      return temp;
    };
    series.forEach(s => {
      s.data = parseCellUMAP(s.id);
    });
  
    umap_chart = Highcharts.chart('container_umap', {
      chart: {
        type: 'scatter',
        zoomType: 'xy'
      },
      title: {
        text: 'Cell Clutering',
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
      tooltip: {
        pointFormat: 'Cell: {point.cell_id} <br/> UMAP_1: {point.x} <br/> UMAP_2: {point.y} </br> '
      },
      series
    });
    $("div[aria-live='assertive']").attr("aria-atomic", true);
    document.getElementById('cell_types').addEventListener('change', () => {
        var series=umap_chart.series;
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


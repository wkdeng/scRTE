Highcharts.setOptions({
    colors: ["#386cb0","#fdb462","#7fc97f","#ef3b2c","#662506","#a6cee3","#fb9a99"]
  });
  
//   const series = [{
//     name: 'Excitatory Neurons',
//     id: 'Ex',
//     marker: {
//       symbol: 'circle'
//     }
//   },
//   {
//     name: 'Inhibitory Neurons',
//     id: 'In',
//     marker: {
//       symbol: 'circle'
//     }
//   },{
//     name: 'Oligodentrocyte Progenitor Cells',
//     id: 'Opc',
//     marker: {
//       symbol: 'circle'
//     }
//   },{
//     name: 'Oligodendrocytes',
//     id: 'Oli',
//     marker: {
//       symbol: 'circle'
//     }
//   },{
//     name: 'Astrocytes',
//     id: 'Ast',
//     marker: {
//       symbol: 'circle'
//     }
//   },{
//     name: 'Microglia',
//     id: 'Mic',
//     marker: {
//       symbol: 'circle'
//     }
//   },{
//     name: 'Pericytes',
//     id: 'Per',
//     marker: {
//       symbol: 'circle'
//     }
//   }];
  const series=[{
        name:'Alzheimer\'s Disease',
        id:'AD',
        marker: {
            symbol:'circle'
        }
    },{
        name:'Pakinson\'s Disease',
        id:'PD',
        marker: {
            symbol:'circle'
        }
    },{
        name:'Amyotrophic Lateral Sclerosis',
        id:'ALS',
        marker: {
            symbol:'circle'
        }
    },{
        name:'Control',
        id:'Control',
        marker:{
            symbol:'circle'
    }}]

  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);
  async function getData() {
      const response = await fetch(
          '/cgi/get_TE_cell_count.py?Name='+urlParams.get('Name')
      );
      return response.json();
    }

  
  const cell_map={'Ex':0,'In':1,'Opc':2,'Oli':3,'Ast':4,'Mic':5,'Per':6}

  getData().then(data => {
    const getData = disease => {
      const temp = [0,0,0,0,0,0,0];
      data.forEach(elm => {
        if (elm.disease === disease) {
            temp[cell_map[elm.cell_type]]=elm.number_of_cells;
        }
      });
      return temp;
    };
    series.forEach(s => {
      s.data = getData(s.id);
    });
  
    const chart = Highcharts.chart('container_cell_count', {
      chart: {
        type: 'column',
      },
      title: {
        text: 'Number of Cells',
        align: 'left'
      },
      subtitle: {
        text:
        'Random generated data',
        align: 'left'
      },
      xAxis: {
        title: {
          text: 'Cell Type'
        },
        categories: ['Excitatory Neuron', 'Inhibitory Neuron', 'OPC', 'Oligodendrocyte', 'Astrocyte', 'Microglia', 'Pericyte'],
        crosshair: true
      },
      yAxis: {
        title: {
          text: 'Number of Cells'
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
    //   series:{
    //     turboThreshold: 0
    //   },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
      series
    });


    document.getElementById('plain').addEventListener('click', () => {
        chart.update({
          chart: {
            inverted: false,
            polar: false
          }
        });
      });
      
      document.getElementById('inverted').addEventListener('click', () => {
        chart.update({
          chart: {
            inverted: true,
            polar: false
          }
        });
      });
      
    //   document.getElementById('polar').addEventListener('click', () => {
    //     chart.update({
    //       chart: {
    //         inverted: false,
    //         polar: true
    //       },
    //       subtitle: {
    //         text: 'Chart option: Polar | Source: ' +
    //           '<a href="https://www.nav.no/no/nav-og-samfunn/statistikk/arbeidssokere-og-stillinger-statistikk/helt-ledige"' +
    //           'target="_blank">NAV</a>'
    //       }
    //     });
    //   });



  });


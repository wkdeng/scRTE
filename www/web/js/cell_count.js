/**
 * @author [Wankun Deng]
 * @email [dengwankun@gmail.com]
 * @create date 2023-04-24 16:47:12
 * @modify date 2023-04-24 17:46:37
 * @desc [description]
 */
Highcharts.setOptions({
    colors: ["#386cb0","#fdb462","#7fc97f","#ef3b2c","#662506","#a6cee3","#fb9a99"]
  });
  
  const series2=[{
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

  const uparams2 = new URLSearchParams(window.location.search);
  if(dataset==null){
    var dataset = uparams2.get('KW');
  }
  async function getCellCountData() {
      const response = await fetch(
          '/cgi/get_cell_count.py?KW='+dataset+'&Cata='+uparams2.get('Cata')
      );
      return response.json();
    }

  
  const cell_map={'Ex':0,'In':1,'Opc':2,'Oli':3,'Ast':4,'Mic':5,'Per':6}

  getCellCountData().then(data => {
    const parseCellCount = disease => {
      const temp = [0,0,0,0,0,0,0];
      data.forEach(elm => {
        if (elm.disease === disease) {
            temp[cell_map[elm.cell_type]]=elm.number_of_cells;
        }
      });
      return temp;
    };
    series2.forEach(s => {
      s.data = parseCellCount(s.id);
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
        dataset,
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
        series:series2
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
  });


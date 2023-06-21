/**
 * @author [Wankun Deng]
 * @email [dengwankun@gmail.com]
 * @create date 2023-04-24 16:47:12
 * @modify date 2023-06-14 09:50:46
 * @desc [description]
 */
Highcharts.setOptions({
    colors: ["#386cb0","#fdb462","#7fc97f","#ef3b2c","#662506","#a6cee3","#fb9a99"]
  });
  

  if(!cellType){
    var cellType = uparams.get('KW');
  }
  async function getCellCountData() {
      const response = await fetch(
          '/scARE/cgi/get_cell_count.py?KW='+cellType+'&Cate=Cell'
      );
      return response.json();
    }


  getCellCountData().then(data => {
    const chart = Highcharts.chart('cellCountDisease', {
      title: {
        text: 'Number of Cells',
        align: 'left'
      },
      subtitle: {
        text:"Cell type: "+cellType,
        align: 'left'
      },
      xAxis: {
        title: {
          text: 'Disease Type'
        },
        categories: ['Alzheimer\'s Disease','Pakinson\'s Disease', 'Amyotrophic Lateral Sclerosis', 'Control']
        // crosshair: true
      },
      yAxis: {
        title: {
          text: 'Number of Cells'
        }
      },
      credits: {
        enabled: false
      },
      legend: {
        enabled: false
      },
        series:[{name:'Cell number',type:'column',colorByPoint: true,data:data}]
    });
    $("div[aria-live='assertive']").attr("aria-atomic", true);
    document.getElementById('plain_dis').addEventListener('click', () => {
        chart.update({
          chart: {
            inverted: false,
            polar: false
          },
          xAxis: {
            title: {
              text: 'Disease Type'
            },
            categories: ['Alzheimer\'s Disease','Pakinson\'s Disease', 'Amyotrophic Lateral Sclerosis', 'Control']
            // crosshair: true
          },
        });
      });
      
      document.getElementById('inverted_dis').addEventListener('click', () => {
        chart.update({
          chart: {
            inverted: true,
            polar: false
          },
          xAxis: {
            title: {
              text: 'Disease Type'
            },
            categories: ['Alzheimer\'s Disease','Pakinson\'s Disease', 'Amyotrophic Lateral Sclerosis', 'Control']
            // crosshair: true
          }
        });
      });

  });


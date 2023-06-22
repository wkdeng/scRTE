/**
 * @author [Wankun Deng]
 * @email [dengwankun@gmail.com]
 * @create date 2023-05-01 11:42:21
 * @modify date 2023-06-14 09:50:51
 * @desc [description]
 */


Highcharts.setOptions({
    colors: ["#386cb0","#fdb462","#7fc97f","#ef3b2c","#662506","#a6cee3","#fb9a99"]
  });
  

  if(!cellType){
    var cellType = uparams.get('KW');
  }
  async function getTECellCountData() {
      const response = await fetch(
          '/scARE/cgi/get_cell_count.py?KW='+cellType+'&Cate=Cell_TE'
      );
      return response.json();
    }


    getTECellCountData().then(data => {
    categories=[];
    dataset_count=data[0]

    const chartTECount = Highcharts.chart('cellCountTE', {
      title: {
        text: 'Number of Cells',
        align: 'left'
      },
      subtitle: {
        text: "Cell type: "+cellType,
        align: 'left'
      },
      xAxis: {
        title: {
          text: 'TE Family'
        },
        type: 'category'
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
        series:[{name:'Cell number',type:'column',colorByPoint: true,data:dataset_count}],
        drilldown: {breadcrumbs:{position:{align:'right'}},series: data[1]}
    });
    $("div[aria-live='assertive']").attr("aria-atomic", true);
    document.getElementById('plain_te').addEventListener('click', () => {
        chartTECount.update({
            chart: {
            inverted: false,
            polar: false
          },
        });
      });
      
      document.getElementById('inverted_te').addEventListener('click', () => {
        chartTECount.update({
          chart: {
            inverted: true,
            polar: false
          }
        });
      });
    //   document.getElementById('polar_te').addEventListener('click', () => {
    //     chartTECount.update({
    //       chart: {
    //         inverted: false,
    //         polar: true
    //       }
    //     });
    //   });
  });


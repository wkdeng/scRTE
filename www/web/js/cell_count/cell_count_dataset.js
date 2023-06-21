/**
 * @author [Wankun Deng]
 * @email [dengwankun@gmail.com]
 * @create date 2023-04-28 15:36:56
 * @modify date 2023-06-14 09:50:39
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
          '/scARE/cgi/get_cell_count.py?KW='+cellType+'&Cate=Cell_Dataset'
      );
      return response.json();
    }


  getCellCountData().then(data => {
    categories=[];
    // dataset_count=data[0]
    
    data.forEach(element => {
        categories.push(element.name);
    });

    const chartDatasetCount = Highcharts.chart('cellCountDataset', {
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
          text: 'Dataset'
        },
        categories: categories
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
    document.getElementById('plain_dat').addEventListener('click', () => {
        chartDatasetCount.update({
            chart: {
            inverted: false,
            polar: false
          },
        });
      });
      
      document.getElementById('inverted_dat').addEventListener('click', () => {
        chartDatasetCount.update({
          chart: {
            inverted: true,
            polar: false
          }
        });
      });
  });


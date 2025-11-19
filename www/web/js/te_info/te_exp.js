/**
 * @author [Wankun Deng]
 * @email [dengwankun@gmail.com]
 * @create date 2023-05-23 01:01:15
 * @modify date 2023-06-14 09:52:34
 * @desc [description]
 */

Highcharts.setOptions({
    colors: ["#386cb0","#fdb462","#7fc97f","#ef3b2c","#662506","#a6cee3","#fb9a99"]
  });

const uparams2 = new URLSearchParams(window.location.search);
if(te_name==null){
    var te_name = uparams2.get('Name');
  }
async function getTEExpData() {
      const response = await fetch(
          '/scARE/cgi/te_info/get_te_exp_boxplot.py?Name='+te_name
      );
      return response.json();
    }

getTEExpData().then(data => {
    if(data[0]=='No data'){
        document.getElementById("exp_body").innerHTML='Expression not detected in any cell type.'
    }else{
        plot_data=data[0]
        labels=data[1]
        var keys=Object.keys(plot_data)
        var row=0;
        for(var i = 0; i < keys.length; i++) {
            var key = keys[i];
            row=Math.floor(i/2)
            if(i%2==0){
                document.getElementById("exp_body").innerHTML += '<div class="row" id="exp_row_'+row+'" "></div>'
                //document.getElementById('exp_row_'+row).innerHTML+='<div class="col-md-5"><div class="card-body" id="exp_'+key+'" style="align-items: center;"></div></div>'
            }
            var width=6
            if(i%2==0 && i==(keys.length-1)){
                width=12
            }
            document.getElementById('exp_row_'+row).innerHTML+='<div class="col-md-'+width+'"><div class="card-body" id="exp_'+key+'" style="align-items: center;"></div></div>'
        }
        for(var i = 0; i < keys.length; i++) {
            var key = keys[i];
            var dataset=plot_data[key]
            var label=labels[key]
            Highcharts.chart('exp_'+key, {
            chart: {
                type: 'boxplot',
            },
            title: {
                text: key,
                align: 'left'
            },
            subtitle: {
                text:"",
                align: 'left'
            },
            xAxis: {
                title: {
                text: 'Cell Type'
                },
                categories: label,
                crosshair: true
            },
            yAxis: {
                title: {
                text: 'Normalized read counts'
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
                series:dataset
            });
            // break;
        }
    }
    $("div[aria-live='assertive']").attr("aria-atomic", true);
  });


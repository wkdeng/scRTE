/**
 * @author [Wankun Deng]
 * @email [dengwankun@gmail.com]
 * @create date 2023-05-23 01:01:15
 * @modify date 2023-05-23 09:32:01
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
          '/cgi/te_info/get_te_exp_boxplot.py?Name='+te_name
      );
      return response.json();
    }

  
getTEExpData().then(data => {
    plot_data=data[0]
    labels=data[1]
    var keys=Object.keys(plot_data)
    console.log(keys)
    for(var i = 0; i < keys.length; i++) {
        var key = keys[i];
        // plot_data[key][0]['name']=key
    // }
    // for(var key in plot_data){
        dataset=plot_data[key]
        label=labels[key]
        console.log(key)
        console.log(dataset)
        console.log(label)
        document.getElementById("exp_body").innerHTML += '<div id="exp_'+key+'" style="width:100%; height:400px;"></div>'
        var add_chart='exp_'+key
        add_chart=function(){
            console.log("Creating chart for "+key)
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
                categories: label[0],
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
                series:plot_data[key]
            });}
        add_chart()
        // break;
    }
  });


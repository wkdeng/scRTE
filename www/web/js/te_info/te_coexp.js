/**
 * @author [Wankun Deng]
 * @email [dengwankun@gmail.com]
 * @create date 2023-06-13 10:16:42
 * @modify date 2023-06-21 10:55:50
 * @desc [description]
 */
Highcharts.setOptions({
    colors: ["#386cb0","#fdb462","#7fc97f","#ef3b2c","#662506","#a6cee3","#fb9a99"]
  });
var rte,gene,dataset,disease,cell;
async function get_coexp_data(from) {
    if(from=='te_info'){
        rte=document.getElementById('current_te').value
        gene=document.getElementById('geneInput').value     
    }else{
        rte=document.getElementById('geneInput1').value
        gene=document.getElementById('geneInput2').value
    }
    dataset=document.getElementById('co_exp_dt').value
    disease=document.getElementById('co_exp_di').value
    cell=document.getElementById('co_exp_c').value 
    
    var url='cgi/te_info/get_te_coexp.py?RTE='+rte+'&Gene='+gene+'&Dataset='+dataset+'&Condition='+disease+'&Cell='+cell
    if(rte==gene){
        return['No data','Cannot compare the same gene/RTE']
    }
    const response = await fetch(url);
    return response.json();
    }
function get_coexp(args){
    get_coexp_data(args).then(data => {
        if(data[0]=='No data'){
            document.getElementById("coexp_scatter").innerHTML=data[1]
        }else{
            /**create scatter plot */
            var dots=JSON.parse(data['dots'])
            var regression=JSON.parse(data['regression_line'])
            
            Highcharts.chart('coexp_scatter', {
            chart: {
                zoomType: 'xy'
            },
            title: {
                text: 'Correlation between '+gene+' and '+rte+' expression',
                align: 'left'
            },
            subtitle: {
                text: 'R<sup>2</sup>: '+regression[0]+', p-value: '+regression[1],
                align: 'left'
            },
            xAxis: {
                title: {
                text: rte
                },
                labels: {
                    format: '{value}'},
                startOnTick: true,
                endOnTick: true,
                showLastLabel: true
            },
            yAxis: {
                title: {
                text: gene
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
                line: {
                    lineWidth: 2,
                    color:"#386cb0",
                    dashStyle: 'LongDash'
                }
            },
                series:[{name:'Expression',data:dots,marker:{radius:3,opacity:0.5,fillColor:'rgba(237,86,27,0.5)'},type:'scatter'},
                        {name:'Regression line',data:[regression[2],regression[3]],marker:{enabled:false},type:'line'}]
            });
            /**create boxplot */
            box_data=data['boxplot']
            labels=data['labels']
            Highcharts.chart('coexp_box', {
                chart: {
                    type: 'boxplot',
                },
                title: {
                    text: '',
                    align: 'left'
                },
                subtitle: {
                    text:"",
                    align: 'left'
                },
                xAxis: {
                    categories: labels,
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
                    enabled: false
                },
                    series:box_data
                });
            $("div[aria-live='assertive']").attr("aria-atomic", true);
        }
      });  
      
}
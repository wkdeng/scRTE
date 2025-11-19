/**
 * @author [Wankun Deng]
 * @email [dengwankun@gmail.com]
 * @create date 2023-05-29 00:49:48
 * @modify date 2023-06-13 15:58:59
 * @desc [description]
 */


const uparams2 = new URLSearchParams(window.location.search);
if(te_name==null){
    var te_name = uparams2.get('Name');
  }
async function getTEExpData() {
      const response = await fetch(
          '/scARE/cgi/te_info/get_te_exp_boxplotly.py?Name='+te_name
      );
      return response.json();
    }

  
getTEExpData().then(data => {

    if('NO_EXP' in data){
        document.getElementById("exp_body").innerHTML='<span style="color:red">No expression data available for this TE</span>'
    }else{
    
    for(const key in data){
        dataset=data[key]
        console.log(dataset)
        document.getElementById("exp_body").innerHTML += '<div id="exp_'+key+'" style="height:500px;"></div>'
        var layout = {
            yaxis: {
              title: 'Normalized Expression'
            },
            boxmode: 'group',
            title: key
          };
        Plotly.newPlot('exp_'+key, dataset, layout,{responsive: true});
    }}
  });


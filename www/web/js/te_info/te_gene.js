/**
 * @author [Wankun Deng]
 * @email [dengwankun@gmail.com]
 * @create date 2023-05-07 17:27:05
 * @modify date 2023-05-08 13:59:59
 * @desc [description]
 */
 function showNetwork(name_) {
        // network chart
        var netData;
        function updateNetwork(){
            showLabel=document.getElementById('showLabel').value=='true';
            console.log(showLabel);
            // netData=JSON.parse(response);
            netChart=ForceGraph(netData,{nodeID:d => d.id,
                        nodeGroup:d => d.group,
                        nodeTitle:d => d.id,
                        linkStrokeWidth:d => 1,
                        width:500,
                        height:500,
                        showLabel:showLabel});
            document.getElementById('container_network').innerHTML='';
            document.getElementById('container_network').appendChild(netChart);
        }
        
        $.get('/scARE/cgi/te_info/get_te_gene_net.py',{Name: name_,Degree:document.getElementById('degree').value},
                function(response){
                    netData=JSON.parse(response);
                    updateNetwork();
                }
        );
        document.getElementById('degree').addEventListener('change',function(){
        $.get('/scARE/cgi/te_info/get_te_gene_net.py',{Name: name_,Degree:document.getElementById('degree').value},
            function(response){
                    netData=JSON.parse(response);
                    updateNetwork();
                }
            );
        });
        document.getElementById('showLabel').addEventListener('change',function(){
            updateNetwork();
        });
    }
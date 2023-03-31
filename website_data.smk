###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-08 11:04:54
 # @modify date 2023-03-08 11:04:54
 # @desc [description]
###

DATA_FOLDER='wwww/mysql'
INTERMEDIATE='data/website'
NTHREAD=10
PYTHON='python3'

RMSK='../universal_data/rmsk/rmsk_GRCh38.txt'
GENE_BED='../universal_data/ref/GRCh38/genes.bed'


rule all:
    input:
        DATA_FOLDER+'/te_fam.sql',
        DATA_FOLDER+'/te_net.sql',
        DATA_FOLDER+'/te_basic.sql'


rule te_fam:
    input:RMSK
    output:DATA_FOLDER+'/te_fam.sql'
    params:
        script='scripts/TE_class.py',
        python=PYTHON
    log:
        'log/te_fam.log'
    shell:"{params.python} {params.script} {input} {output}> {log} 2>&1 "


rule download_consensus:
    input:RMSK
    output: INTERMEDIATE+'/Dfam.embl'
    params:
        intermediate=INTERMEDIATE
    log:
        "log/download_te_consensus.log"
    shell:"""wget -O {params.intermediate}/Dfam.embl.gz https://www.dfam.org/releases/Dfam_3.7/families/Dfam_curatedonly.embl.gz > {log} 2>&1
    gunzip {params.intermediate}/Dfam.embl.gz"""

rule te_basic:
    input:
        rmsk=RMSK,
        consensus=INTERMEDIATE+'/Dfam.embl'
    output: DATA_FOLDER+'/te_basic.sql'
    params:
        script='scripts/TE_basic.py',
        python=PYTHON
    log:
        'log/te_basic.log'
    shell:"{params.python} {params.script} {input.rmsk} {input.consensus} {output}> {log} 2>&1 "


rule te_gene_net:
    input:
        rmsk=RMSK,
        gene_bed=GENE_BED
    output:
        DATA_FOLDER+'/te_net.sql'
    log:
        'log/te_gene_net.log'
    params:
        script='script/TE_net.py',
        python=PYTHON
    shell:"{params.python} {params.script} {input.rmsk} {input.gene_bed} {output} > {log} 2>&1"  
###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-08 11:04:54
 # @modify date 2023-03-08 11:04:54
 # @desc [description]
###

DATA_FOLDER='www/mysql'
INTERMEDIATE='data/website'
NTHREAD=10
PYTHON='python3'

RMSK='../universal_data/rmsk/rmsk_GRCh38.txt'
GENE_BED='../universal_data/ref/GRCh38/genes.bed'
CHR_LEN='../universal_data/ref/GRCh38/STAR/chrNameLength.txt'
DATASET_ID='AD_HS_00001'

rule all:
    input:
        DATA_FOLDER+'/te_fam.sql',
        DATA_FOLDER+'/te_net.sql',
        DATA_FOLDER+'/te_basic.sql',
        DATA_FOLDER+'/cell_umap.sql',
        DATA_FOLDER+'/gene_dict.sql',
        DATA_FOLDER+'/te_gene.sql',
        DATA_FOLDER+'/meta.sql',
        DATA_FOLDER+'/sample2dataset.sql'

rule cell_umap:
    input:
        'data/3/cell_umap.txt'
    output:
        DATA_FOLDER+'/cell_umap.sql'
    log:
        'log/cell_umap.log'
    params:
        script='scripts/Data_Cell_Umap.py',
        python=PYTHON,
        dataset_id=DATASET_ID
    shell:"{params.python} {params.script} {input} {output} {params.dataset_id} > {log} 2>&1"

rule cell_exp:
    input:
        'data/3/cell_exp.txt'
    output:
        DATA_FOLDER+'/gene_dict.sql',
        DATA_FOLDER+'/cell_exp_0.sql'
    log:
        'log/cell_exp.log'
    params:
        script='scripts/Data_Cell_Exp.py',
        python=PYTHON,
        out_path=DATA_FOLDER,
        dataset_id=DATASET_ID
    shell:"{params.python} {params.script} {input} {params.out_path} {params.dataset_id}> {log} 2>&1"
    
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
        consensus=INTERMEDIATE+'/Dfam.embl',
        gene_bed=GENE_BED
    output: DATA_FOLDER+'/te_basic.sql'
    params:
        script='scripts/TE_basic.py',
        python=PYTHON,
        chr_len=CHR_LEN
    log:
        'log/te_basic.log'
    shell:"{params.python} {params.script} {input.rmsk} {input.consensus} {output} {params.chr_len} {input.gene_bed}> {log} 2>&1 "


rule te_gene_net:
    input:
        rmsk=RMSK,
        gene_bed=GENE_BED
    output:
       sql=DATA_FOLDER+'/te_net.sql',
       txt=DATA_FOLDER+'/network.txt'
    log:
        'log/te_gene_net.log'
    params:
        script='scripts/TE_net.py',
        python=PYTHON
    shell:"{params.python} {params.script} {input.rmsk} {input.gene_bed} {output.sql} {output.txt} > {log} 2>&1"  


rule te_gene:
    input:
        DATA_FOLDER+'/network.txt'
    output:
        DATA_FOLDER+'/te_gene.sql'
    log:
        'log/te_gene.log'
    params:
        script='scripts/TE_gene.py',
        python=PYTHON
    shell:"{params.python} {params.script} {input} {output} > {log} 2>&1"

rule meta:
    input:
        'data/Dataset.meta.txt'
    output:
        meta=DATA_FOLDER+'/meta.sql',
        sample2dataset=DATA_FOLDER+'/sample2dataset.sql'
    log:
        'log/meta.log'
    params:
        script='scripts/Dataset_meta.py',
        python=PYTHON
    shell:"{params.python} {params.script} {input} {output.meta} {output.sample2dataset} > {log} 2>&1"
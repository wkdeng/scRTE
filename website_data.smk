###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-08 11:04:54
 # @modify date 2023-03-08 11:04:54
 # @desc [description]
###

DATA_FOLDER='www/mysql'
INTERMEDIATE='data/all_datasets'
NTHREAD=10
PYTHON='python3'

RMSK='../universal_data/rmsk/rmsk_GRCh38.txt'
GENE_BED='../universal_data/ref/GRCh38/genes.bed'
GENE_GTF='../universal_data/ref/GRCh38/gencode.v43.basic.annotation.gtf'
CHR_LEN='../universal_data/ref/GRCh38/STAR/chrNameLength.txt'
SEURAT_OBJ_FOLDER='data/seurat_objs'
DATASET_META='data/Dataset.meta.txt'
MODE='overwrite'

rule all:
    input:
        INTERMEDIATE+'/cell_exp.log',
        INTERMEDIATE+'/cell_umap.log',
        DATA_FOLDER+'/te_fam.sql',
        # DATA_FOLDER+'/te_net.sql',
        DATA_FOLDER+'/te_basic.sql',
        DATA_FOLDER+'/cell_umap.sql',
        DATA_FOLDER+'/gene_dict.sql',
        # DATA_FOLDER+'/te_gene.sql',
        DATA_FOLDER+'/meta.sql',
        DATA_FOLDER+'/sample2dataset.sql',
        DATA_FOLDER+'/subfam_cellcount.sql',
        DATA_FOLDER+'/te_exp_boxplot.sql',
        DATA_FOLDER+'/exp_de.sql',
        DATA_FOLDER+'/AD_HS_00001.txt'

rule extract_cell_umap:
    input:
        DATASET_META
    output:
        INTERMEDIATE+'/cell_umap.log'
    log:
        'log/extract_cell_umap.log'
    params:
        script='scripts/get_cell_umap.r',
        cmd='Rscript',
        input_folder=SEURAT_OBJ_FOLDER,
        output_folder=INTERMEDIATE
    shell:"{params.cmd} {params.script} {params.input_folder} {params.output_folder} > {log} 2>&1"        

rule extract_cell_exp:
    input:
        DATASET_META
    output:
        INTERMEDIATE+'/cell_exp.log'
    log:
        'log/extract_cell_exp.log'
    params:
        script='scripts/get_cell_exp.r',
        cmd='Rscript',
        input_folder=SEURAT_OBJ_FOLDER,
        output_folder=INTERMEDIATE
    shell:"{params.cmd} {params.script} {params.input_folder} {params.output_folder} > {log} 2>&1"

rule cell_umap:
    input:
        INTERMEDIATE+'/cell_umap.log'
    output:
        DATA_FOLDER+'/cell_umap.sql'
    log:
        'log/cell_umap.log'
    params:
        script='scripts/data_cell_umap.py',
        python=PYTHON,
        input_path=INTERMEDIATE
    shell:"{params.python} {params.script} {params.input_path} {output} > {log} 2>&1"

rule cell_exp:
    input:
        cell_exp=INTERMEDIATE+'/cell_exp.log',
        cell_umap=INTERMEDIATE+'/cell_umap.log'
    output:
        DATA_FOLDER+'/gene_dict.sql',
        DATA_FOLDER+'/cell_exp_0.sql'
    log:
        'log/cell_exp.log'
    params:
        script='scripts/data_cell_exp.py',
        python=PYTHON,
        out_path=DATA_FOLDER,
        input_dir=INTERMEDIATE,
        mode=MODE,
        gtf=GENE_GTF,
        rmsk=RMSK
    shell:"{params.python} {params.script} {params.input_dir} {params.out_path} {params.mode} {params.gtf} {params.rmsk}> {log} 2>&1"

rule cell_exp_list:
    input:
        cell_exp=INTERMEDIATE+'/cell_exp.log', 
    output:
        DATA_FOLDER+'/AD_HS_00001.txt'
    log:
        'log/cell_exp_list.log'
    params:
        script='scripts/data_expressed_genelist.py',
        python=PYTHON,
        out_path=DATA_FOLDER,
        input_dir=INTERMEDIATE,
        gtf=GENE_GTF,
        rmsk=RMSK
    shell:"{params.python} {params.script} {params.input_dir} {params.out_path} {params.gtf} {params.rmsk}> {log} 2>&1"


rule te_exp_de:
    input:
        cell_exp=DATA_FOLDER+'/cell_exp_0.sql',
        cell_umap=DATA_FOLDER+'/cell_umap.sql'
    output:
        DATA_FOLDER+'/exp_de.sql'
    log:
        'log/te_exp_de.log'
    params:
        script='scripts/data_te_exp_de.py',
        python=PYTHON,
        out_path=DATA_FOLDER,
        input_path=INTERMEDIATE,
        rmsk=RMSK
    shell:"{params.python} {params.script} {params.input_path} {params.out_path} {params.rmsk} > {log} 2>&1"


rule te_cellcount:
    input:
        rmsk=RMSK,
        cell_exp=DATA_FOLDER+'/cell_exp_0.sql',
        cell_umap=DATA_FOLDER+'/cell_umap.sql'
    output:
        DATA_FOLDER+'/subfam_cellcount.sql',
        DATA_FOLDER+'/fam_cellcount.sql'
    log:
        'log/te_cellcount.log'
    params:
        script='scripts/data_te_cell_count.py',
        python=PYTHON,
        out_path=DATA_FOLDER,
        input_path=INTERMEDIATE,
        gtf=GENE_GTF,
    log:
        'log/te_cellcount.log'
    shell:"{params.python} {params.script} {params.input_path} {params.out_path} {input.rmsk}> {log} 2>&1"


rule te_exp_boxplot:
    input:
      rmsk=RMSK,
      cell_exp=DATA_FOLDER+'/cell_exp_0.sql'
    output:
        DATA_FOLDER+'/te_exp_boxplot.sql'
    log:
        'log/te_exp_boxplot.log'
    params:
        script='scripts/data_te_exp_boxplot.py',
        python=PYTHON,
        out_path=DATA_FOLDER,
        input_path=INTERMEDIATE
    shell:"{params.python} {params.script} {params.input_path} {input.rmsk} {params.out_path} > {log} 2>&1"


rule te_fam:
    input:RMSK
    output:DATA_FOLDER+'/te_fam.sql'
    params:
        script='scripts/te_class.py',
        python=PYTHON
    log:
        'log/te_fam.log'
    shell:"{params.python} {params.script} {input} {output}> {log} 2>&1 "


# rule download_consensus:
#     input:RMSK
#     output: INTERMEDIATE+'/Dfam.embl'
#     params:
#         intermediate=INTERMEDIATE
#     log:
#         "log/download_te_consensus.log"
#     shell:"""wget -O {params.intermediate}/Dfam.embl.gz https://www.dfam.org/releases/Dfam_3.7/families/Dfam_curatedonly.embl.gz > {log} 2>&1
#     gunzip {params.intermediate}/Dfam.embl.gz"""


rule te_basic:
    input:
        rmsk=RMSK,
        consensus=INTERMEDIATE+'/Dfam.embl',
        gene_bed=GENE_BED
    output: DATA_FOLDER+'/te_basic.sql'
    params:
        script='scripts/te_basic.py',
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
        script='scripts/te_net.py',
        python=PYTHON
    shell:"{params.python} {params.script} {input.rmsk} {input.gene_bed} {output.sql} {output.txt} > {log} 2>&1"  


# rule te_gene:
#     input:
#         DATA_FOLDER+'/network.txt'
#     output:
#         DATA_FOLDER+'/te_gene.sql'
#     log:
#         'log/te_gene.log'
#     params:
#         script='scripts/te_gene.py',
#         python=PYTHON
#     shell:"{params.python} {params.script} {input} {output} > {log} 2>&1"

rule meta:
    input:
        DATASET_META
    output:
        meta=DATA_FOLDER+'/meta.sql',
        sample2dataset=DATA_FOLDER+'/sample2dataset.sql'
    log:
        'log/meta.log'
    params:
        script='scripts/dataset_meta.py',
        python=PYTHON
    shell:"{params.python} {params.script} {input} {output.meta} {output.sample2dataset} > {log} 2>&1"


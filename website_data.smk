###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-08 11:04:54
 # @modify date 2023-03-08 11:04:54
 # @desc [description]
###

# nohup snakemake --snakefile website).smk --latency-wait 60 --jobs 50 --rerun-incomplete &
# configfile: "scRTE.yaml"

# SAMPLE_GRP=config['sample_group']
# SAMPLES=config['samples']
DATA_FOLDER='wwww/mysql'
NTHREAD=10
PYTHON='python3'

RMSK='../universal_data/rmsk/rmsk_GRCh38.txt'


rule all:
    input:
        DATA_FOLDER+'/te_fam.sql'


rule te_fam:
    input:RMSK
    output:DATA_FOLDER+'/te_fam.sql'
    params:
        script='scripts/TE_class.py',
        python=PYTHON
    log:
        'log/te_fam.log'
    shell:"{params.python} {params.script} {input} {output}> {log} 2>&1 "
###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-08 11:04:54
 # @modify date 2023-03-08 11:04:54
 # @desc [description]
###

# nohup snakemake --snakefile scRTE.smk --latency-wait 60 --jobs 50 --rerun-incomplete &
configfile: "scRTE.yaml"

# SAMPLE_GRP=config['sample_group']
SAMPLES=config['samples']
SAMPLE_FOLDER=config['sample_folder']
LIB_TYPE=config['library_type']
NTHREAD=config['nthread']
LIB_PLATFORM=config['lib_platform']

CELLRANGER_REF=config['cellranger_ref']
scTE_REF=config['scTE_ref']
soloTE_ANNOTATION=config['solote_annotation']
soloTE_SCRIPT=config['soloTE_script']
# READ_TAIL='' if LIB_TYPE=='single' else '_1'


rule all:
    input:
        # fq=expand('{sample_folder}/raw/{sample}/{sample}_1.fastq',sample_folder=SAMPLE_FOLDER,sample=SAMPLES )#,
        bam=expand('{sample_folder}/cellcount/{sample}/outs/possorted_genome_bam.bam',sample_folder=SAMPLE_FOLDER,sample=SAMPLES),
        scte=expand('{sample_folder}/scte/{sample}/{sample}.csv',sample_folder=SAMPLE_FOLDER,sample=SAMPLES),
        solote=expand('{sample_folder}/solote/{sample}/matrix.mtx',sample_folder=SAMPLE_FOLDER,sample=SAMPLES)


rule download_fq:
    input: 
        SAMPLE_FOLDER+'/Meta.csv'
    output:
        temp(SAMPLE_FOLDER+'/raw/{sample}/{sample}_S1_L001_R1_001.fastq'),
        temp(SAMPLE_FOLDER+'/raw/{sample}/{sample}_S1_L001_R2_001.fastq')
    params:
        output_folder=SAMPLE_FOLDER+'/raw/{sample}',
        sample='{sample}'
    log:
        'log/download_fq_{sample}.log'
    run:
        import os
        import subprocess
        import sys
        sample=params.sample
        output_folder=params.output_folder

        if not os.path.isfile(f'{output_folder}/{sample}_1.fastq'):
            if not os.path.isdir(params.sample):
                subprocess.call(f'prefetch {sample} --max-size u',shell=True)
            subprocess.call(f'fasterq-dump -O {output_folder} -S --include-technical  {sample}',shell=True)

        if os.path.isfile(f'{output_folder}/{sample}_3.fastq'):
            r1_len=int(open(f'{output_folder}/{sample}_1.fastq').readline().strip().split("length=")[1])
            r2_len=int(open(f'{output_folder}/{sample}_2.fastq').readline().strip().split("length=")[1])
            r3_len=int(open(f'{output_folder}/{sample}_3.fastq').readline().strip().split("length=")[1])
            if r1_len < 25 and r2_len >=25 and r3_len >= 10:
                subprocess.call(f'mv {output_folder}/{sample}_2.fastq {output_folder}/{sample}_S1_L001_R1_001.fastq',shell=True) 
                subprocess.call(f'mv {output_folder}/{sample}_3.fastq {output_folder}/{sample}_S1_L001_R2_001.fastq',shell=True) 
            elif r1_len >=25:
                subprocess.call(f'mv {output_folder}/{sample}_1.fastq {output_folder}/{sample}_S1_L001_R1_001.fastq',shell=True) 
                subprocess.call(f'mv {output_folder}/{sample}_2.fastq {output_folder}/{sample}_S1_L001_R2_001.fastq',shell=True) 
            else:
                sys.exit(1)
        else:
            subprocess.call(f'mv {output_folder}/{sample}_1.fastq {output_folder}/{sample}_S1_L001_R1_001.fastq',shell=True) 
            subprocess.call(f'mv {output_folder}/{sample}_2.fastq {output_folder}/{sample}_S1_L001_R2_001.fastq',shell=True) 
        subprocess.call(f'rm -rf {sample}', shell=True)
        for file_ in range(1,4):
            if os.path.isfile(f'{output_folder}/{sample}_{file_}.fastq'):
                subprocess.call(f'rm {output_folder}/{sample}_{file_}.fastq',shell=True)

rule cell_ranger:
    input:
        r1=SAMPLE_FOLDER+'/raw/{sample}/{sample}_S1_L001_R1_001.fastq',
        r2=SAMPLE_FOLDER+'/raw/{sample}/{sample}_S1_L001_R2_001.fastq'
    output:
        SAMPLE_FOLDER+'/cellcount/{sample}/outs/possorted_genome_bam.bam'
    params:
        sample='{sample}',
        ref=CELLRANGER_REF,
        fq_folder=SAMPLE_FOLDER+'/raw',
        sample_folder=SAMPLE_FOLDER,
        nthread=NTHREAD
    log:
        'log/cell_ranger_{sample}.log'
    shell:"""\
    cellranger count --id={params.sample}_S1 --transcriptome={params.ref} --fastqs={params.fq_folder} --sample={params.sample} --localcores={params.nthread} --localmem=64 > {log} 2>&1
    mv {params.sample}_S1/* {params.sample_folder}/cellcount/{params.sample}/
    """

rule scTE:
    input:
        bam=SAMPLE_FOLDER+'/cellcount/{sample}/outs/possorted_genome_bam.bam'
    output:
        SAMPLE_FOLDER+'/scte/{sample}/{sample}.csv'
    params:
        nthread=NTHREAD,
        umi="UR",
        cb="CR",
        ref_lib=scTE_REF,
        sample='{sample}',
        sample_folder=SAMPLE_FOLDER
    log:
        'log/scte_{sample}.log'
    shell:"""mkdir -p {params.sample_folder}/scte/{params.sample}
          scTE -i {input.bam} -o {params.sample} -x {params.ref_lib} -UMI {params.umi} -CB {params.cb} --min_genes 200 --thread {params.nthread} > {log} 2>&1
          mv {params.sample}.csv {params.sample_folder}/scte/{params.sample}/  > {log} 2>&1 """

rule soloTE:
    input:
        bam=SAMPLE_FOLDER+'/cellcount/{sample}/outs/possorted_genome_bam.bam'
    output:
        SAMPLE_FOLDER+'/solote/{sample}/matrix.mtx'
    params:
        nthread=NTHREAD,
        output_folder=SAMPLE_FOLDER+'/solote',
        sample='{sample}',
        te_anno=soloTE_ANNOTATION,
        soloTE_script=soloTE_SCRIPT
    log:
        'log/solote_{sample}.log'
    shell:"""python3 {params.soloTE_script} --threads {params.nthread} --bam {input.bam} --teannotation {params.te_anno} --outputprefix {params.sample} --outputdir {params.output_folder}
    mv {params.output_folder}__SoloTE_temp/{params.output_folder}_SoloTE_output/* {params.output_folder}/"""

rule scTE_normalize:
    input: SAMPLE_FOLDER+'/scte/{sample}/{sample}.csv'
    output: SAMPLE_FOLDER+'/scte/{sample}/{sample}_normalized.csv'
    params: sample='{sample}'
    log: 'log/scte_normalize_{sample}.log'
    shell:"""\
    python3 {SCRIPT_FOLDER}/TE_scTE_normalize.py -i {input} -o {output} > {log} 2>&1
    """

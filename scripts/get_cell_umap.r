# /**
#  * @author [Wankun Deng]
#  * @email [dengwankun@gmail.com]
#  * @create date 2023-05-09 10:06:03
#  * @modify date 2023-05-09 10:06:03
#  * @desc [description]
#  */
args = commandArgs(trailingOnly = TRUE)
data_folder<-args[1]
out_folder<-args[2]
library(Seurat)
cell_meta<-NULL
for(file_name in list.files(data_folder,pattern = 'rds')){
    dataset<-strsplit(file_name,'\\.')[[1]][1]
    print(dataset)
    seurat_obj<-readRDS(paste0(data_folder,'/',file_name))
    seurat_obj@meta.data$UMAP_1<-seurat_obj@reductions[['umap']]@cell.embeddings[,1]
    seurat_obj@meta.data$UMAP_2<-seurat_obj@reductions[['umap']]@cell.embeddings[,2]
    seurat_obj@meta.data$dataset<-dataset
    seurat_obj@meta.data$stage<-'N/A'
    if (!('msex' %in% colnames(seurat_obj@meta.data))){
        seurat_obj@meta.data$msex<-'N/A'
    }
    if (!('age_death' %in% colnames(seurat_obj@meta.data))){
        seurat_obj@meta.data$age_death<-'N/A'
    }
    if(is.null(cell_meta)){
        cell_meta<-seurat_obj@meta.data[,c('predicted.celltype','Diagnosis','stage','msex','age_death','UMAP_1','UMAP_2','dataset')]
    }else{
        cell_meta<-rbind(cell_meta,seurat_obj@meta.data[,c('predicted.celltype','Diagnosis','stage','msex','age_death','UMAP_1','UMAP_2','dataset')])
    }
}
write.table(cell_meta,paste0(out_folder,'/cell_umap.txt'),row.names = ,quote = F,sep = '\t',col.names = T)

# /**
#  * @author [Wankun Deng]
#  * @email [dengwankun@gmail.com]
#  * @create date 2023-05-09 10:59:27
#  * @modify date 2023-05-09 10:59:27
#  * @desc [description]
#  */
library(Seurat)
args = commandArgs(trailingOnly = TRUE)
data_folder<-args[1]
out_folder<-args[2]

exp_mtxs<-list()
for(file_name in list.files(data_folder,pattern = 'rds')){
    dataset<-strsplit(file_name,'\\.')[[1]][1]
    print(dataset)
    seurat_obj<-readRDS(paste0(data_folder,'/',file_name))
    exp_mtx<-as.data.frame(t(as.data.frame(GetAssayData(seurat_obj,slot = 'data'))))
    exp_mtx$UMAP_1<-seurat_obj@reductions[['umap']]@cell.embeddings[,1]
    exp_mtx$UMAP_2<-seurat_obj@reductions[['umap']]@cell.embeddings[,2]

    exp_mtxs[[length(exp_mtxs)+1]]<-exp_mtx
}

all_genes<-colnames(exp_mtxs[[1]])
for(i in 2:length(exp_mtxs)){
    all_genes<-union(all_genes,colnames(exp_mtxs[[i]]))
}
all_genes<-sort(unique(all_genes))
length(all_genes)
for(i in 1:length(exp_mtxs)){
    print("Processing exp_mtxs[[i]]")
    # create columns not existing in exp_mtxs[[i]]
    for(j in setdiff(all_genes,colnames(exp_mtxs[[i]]))){
        exp_mtxs[[i]][,j]<-0
    }
    exp_mtxs[[i]]<-exp_mtxs[[i]][,all_genes]
}
exp_mtx2<-do.call(rbind,exp_mtxs)
write.table(exp_mtx2,paste0(out_folder,'/cell_exp.txt'),row.names = T,quote = F,sep = '\t',col.names = T)
print('Done writing expression file')

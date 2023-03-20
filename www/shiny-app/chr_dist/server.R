library(shiny)
library(jsonlite)
library(ggplot2)

asc <- function(x) { charToRaw(x) }


shinyServer(function(input, output,session) {

  rv<-reactiveValues(chr_dist='')
  
  output$distPlot <- renderPlot({

    observe({
      query <- parseQueryString(session$clientData$url_search)
        if (!is.null(query[['chr_dist']])) {
          rv$chr_dist=query[['chr_dist']]
        }
      })

      chr_dist<- scan(text = gsub("[^0-9,]","",rv$chr_dist), sep = ",", quiet = TRUE)
      chr<-c('chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13',
            'chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22','chrX','chrY','chrM','others')
      chr<-data.frame(unlist(chr),unlist(chr_dist))
      colnames(chr)<-c('Chromosome','Number')
      ggplot(data=chr)+geom_bar(aes(x=Chromosome,y=Number,fill=Chromosome),stat='identity')+theme(legend.position = 'none')

  })
})



library(shiny)
library(jsonlite)
library(ggplot2)

asc <- function(x) { charToRaw(x) }


shinyServer(function(input, output,session) {

  rv<-reactiveValues(tmp_file='')
  
  output$distPlot <- renderPlot({
    observe({
      query <- parseQueryString(session$clientData$url_search)
        if (!is.null(query[['tmp_file']])) {
          rv$tmp_file=query[['tmp_file']]
        }
      })
      tmp_file<- rv$tmp_file
      df<-as.matrix(fromJSON(paste0('/tmp/',tmp_file)))
      row.names(df)<-c('chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13',
            'chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22','chrX','chrY','chrM')
      colnames(df)<-seq(1,100)
      
      heatmap(t(df), Colv = NA, Rowv = NA, )
      legend("topright", legend = c("Low", "Medium", "High"), fill = heat.colors(3))

  })
})



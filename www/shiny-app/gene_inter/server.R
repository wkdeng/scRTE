###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-21 14:17:23
 # @modify date 2023-03-21 14:17:23
 # @desc [description]
###
library(shiny)
library(jsonlite)
library(ggplot2)

asc <- function(x) { charToRaw(x) }


shinyServer(function(input, output,session) {

  rv<-reactiveValues(gene_inter='')
  
  output$distPlot <- renderPlot({

    observe({
      query <- parseQueryString(session$clientData$url_search)
        if (!is.null(query[['gene_inter']])) {
          rv$gene_inter=query[['gene_inter']]
        }
      })

      gene_inter<- scan(text = gsub("[^0-9,]","",rv$gene_inter), sep = ",", quiet = TRUE)
      Type<-c('Genic','Intergenic')
      Type<-data.frame(unlist(Type),unlist(gene_inter))
      colnames(Type)<-c('Type','Number')
      ggplot(data=Type)+geom_bar(aes(x="",y=Number,fill=Type),stat='identity',width=1)+coord_polar('y',start=0)+xlab('')

  })
})



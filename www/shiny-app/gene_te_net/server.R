library(shiny)
library(jsonlite)
library(ggplot2)
library(igraph)


shinyServer(function(input, output,session) {
  
  output$network <- renderPlot({

    
    # create data:
    links <- data.frame(
        source=c("A","A", "A", "A", "A","J", "B", "B", "C", "C", "D","I"),
        target=c("B","B", "C", "D", "J","A","E", "F", "G", "H", "I","I"),
        importance=(sample(1:4, 12, replace=T))
        )
    nodes <- data.frame(
        name=LETTERS[1:10],
        carac=c( rep("young",3),rep("adult",2), rep("old",5))
        )
    
    # Turn it into igraph object
    network <- graph_from_data_frame(d=links, vertices=nodes, directed=F) 
    
    # Make a palette of 3 colors
    library(RColorBrewer)
    coul  <- brewer.pal(3, "Set1") 
    
    # Create a vector of color
    my_color <- coul[as.numeric(as.factor(V(network)$carac))]
    
    plot(network, vertex.color=my_color, edge.width=E(network)$importance*2 )
    legend("bottomleft", legend=levels(as.factor(V(network)$carac))  , col = coul , bty = "n", pch=20 , pt.cex = 3, cex = 1.5, text.col=coul , horiz = FALSE, inset = c(0.1, 0.1))
    })
})


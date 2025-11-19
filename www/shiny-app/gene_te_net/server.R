###
# @author [Wankun Deng]
# @email [dengwankun@gmail.com]
# @create date 2023-03-21 14:16:47
# @modify date 2023-03-21 14:16:47
# @desc [description]
###
library(shiny)
library(jsonlite)
library(ggplot2)
library(igraph)


shinyServer(function(input, output, session) {
  rv <- reactiveValues(te_node = "")

  output$network <- renderPlot({
    req(input$OrderN)
    observe({
      query <- parseQueryString(session$clientData$url_search)
      if (!is.null(query[["te_node"]])) {
        rv$te_node <- query[["te_node"]]
      }
    })

    df <- read.csv("network.txt", sep = ",", header = T)

    # create data:
    links <- data.frame(
      source = df$name,
      target = df$gn
    )

    tes <- unique(df$name)
    node_te_idx <- which(tes == rv$te_node)
    genes <- unique(df$gn)
    nodes <- data.frame(
      name = c(tes, genes),
      carac = c(rep("TE", node_te_idx - 1), rv$te_node, rep("TE", length(tes) - node_te_idx), rep("Gene", length(genes)))
    )

    order <- input$OrderN
    # order<-2
    # Turn it into igraph object
    network <- graph_from_data_frame(d = links, vertices = nodes, directed = F)
    network <- make_ego_graph(network, nodes = c(rv$te_node), order = order, mode = "all")[[1]]

    # Make a palette of 3 colors
    library(RColorBrewer)
    coul <- brewer.pal(3, "Dark2")

    # Create a vector of color
    my_color <- coul[as.numeric(as.factor(V(network)$carac))]

    plot(network, vertex.color = my_color, edge.width = 2, vertex.size = 5, vertex.label = NA)
    legend(x = 1, y = -0.7, legend = levels(as.factor(V(network)$carac)), col = coul, bty = "n", pch = 20, pt.cex = 1, cex = 1, text.col = coul, horiz = FALSE, inset = c(0.1, 0.1))
  })
})

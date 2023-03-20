# library(shiny)

# # Define UI for application that plots random distributions 
# shinyUI(fluidPage(
  
#   # Application tit
#   # Show a plot of the generated distribution
#   mainPanel(
#     # plotOutput("distPlot", height=250),
#     uiOutput('uirend')
#   )
# ))


library(shiny)

# Define UI for application that plots random distributions 
shinyUI(fluidPage(
  
  # Application tit
  # Show a plot of the generated distribution
  mainPanel(
    plotOutput("distPlot", height=250)
  )
))
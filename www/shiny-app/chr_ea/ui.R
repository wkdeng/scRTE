###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-21 14:17:06
 # @modify date 2023-03-21 14:17:06
 # @desc [description]
###
library(shiny)

# Define UI for application that plots random distributions 
shinyUI(fluidPage(
  
  # Application tit
  # Show a plot of the generated distribution
  mainPanel(
    plotOutput("distPlot", height=250)
  )
))
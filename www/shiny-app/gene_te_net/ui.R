###
 # @author [Wankun Deng]
 # @email [dengwankun@gmail.com]
 # @create date 2023-03-21 14:16:51
 # @modify date 2023-03-21 14:16:51
 # @desc [description]
###
library(shiny)

shinyUI(fluidPage(
    numericInput('OrderN', 'Order', value = 1),
    plotOutput("network")
))
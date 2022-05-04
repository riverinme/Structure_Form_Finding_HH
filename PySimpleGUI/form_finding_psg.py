# -*- coding: utf-8 -*-
"""
Created on Wed May  4 15:03:05 2022

@author: hh414
"""

import PySimpleGUI as sg

sg.theme('DarkAmber')

# All the stuff inside your window.
layout = [[sg.Text('1, 选择模式/Select a Mode')],
          [sg.Radio('单索/Cable or Arch', "RadioDemo", default=True, size=(20, 1)),
           sg.Radio('索网/Web', "RadioDemo", size=(10, 1)),
           sg.Radio('SAP2000', "RadioDemo", size=(10, 1))],
          [sg.HSep()],
          [sg.Text('2, 设置参数/Parameters')],
          [sg.HSep()],
          [sg.Text('3, 数据检查/Data Check')],
          [sg.HSep()],
          [sg.Text('4,'), sg.Button("润/Run")],
          [sg.Multiline(size=(70, 5))],
          [sg.HSep()],
          [sg.Text('Enter something on Row 2'), sg.InputText()],
          [sg.Button('Ok'), sg.Button('Cancel')]]

# Create the Window
window = sg.Window('结构找形/Form-finding by HH', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()

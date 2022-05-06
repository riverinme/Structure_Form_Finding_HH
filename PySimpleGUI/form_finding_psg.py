# -*- coding: utf-8 -*-
"""
Created on Wed May  4 15:03:05 2022

@author: hh414
"""

import PySimpleGUI as sg

sg.theme('DarkAmber')

# All the stuff inside your window.
layout = [[sg.Text('1, 选择模式/Select a Mode')],
          [sg.Radio('单索/Cable or Arch', "Modes", default=True, size=(20, 1), key="Mode1"),
           sg.Radio('索网/Web', "Modes", size=(10, 1), key="Mode2"),
           sg.Radio('SAP2000', "Modes", size=(10, 1), key="Mode3")],
          [sg.HSep()],
          [sg.Text('2, 设置约束/Constrains')],
          [sg.HSep()],
          [sg.Text('3, 设置预荷载/Pre-loading')],
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
    print(event)
    print(values)
    # print('You entered ', values)
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break


window.close()

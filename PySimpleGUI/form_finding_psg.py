# -*- coding: utf-8 -*-
"""
Created on Wed May  4 15:03:05 2022

@author: hh414
"""

import PySimpleGUI as sg

sg.theme('DarkAmber')

# All the stuff inside your window.
layout = [[sg.Text('1, 选择模式/Select a Mode')],
          [sg.Radio('索网/Cables or Archs', "Modes", default=True,
                    size=(20, 1), key="Mode1"),
           sg.Radio('SAP2000', "Modes",
                    size=(10, 1), key="Mode2")],
          [sg.HSep()],
          [sg.Text('2, 设置网格/Joints')],
          [sg.Text('列数/Columns: ', size=(11, 1)),
           sg.Input(key='m', size=(10, 1), enable_events=True),
          sg.Text('  行数/Rows: ', size=(10, 1)),
           sg.Input(key='n', size=(10, 1), enable_events=True)],
          [sg.Text('Status: '), sg.Text('', key="mn_status")],
          [sg.HSep()],
          [sg.Text('3, 边界条件/Boundary Conditions')],
          [sg.Radio('所有角点约束/All Corners Constrained', "boundary", default=True,
                    size=(30, 1), key="boundary1"),
           sg.Radio('所有边约束/All Edges Constrained', "boundary",
                    size=(30, 1), key="boundary2")],
          [sg.HSep()],
          [sg.Text("4, 初始标高/Initial Z Coordinates")],
          [sg.Text("", size=(1, 1)), sg.Input(key='LU', size=(5, 1)),
           sg.Text("...", size=(5, 1)), sg.Input(key='RU', size=(5, 1))],
          [sg.Text("", size=(1, 1)), sg.Text("...", size=(5, 1)),
           sg.Text("...", size=(5, 1)), sg.Text("...", size=(5, 1))],
          [sg.Text("", size=(1, 1)), sg.Input(key='LD', size=(5, 1)),
           sg.Text("...", size=(5, 1)), sg.Input(key='RD', size=(5, 1))],
          [sg.HSep()],
          [sg.Text("5, 附加约束/Addtional Constrains")],
          [sg.HSep()],
          [sg.Text('4, 设置预荷载/Pre-loading')],
          [sg.HSep()],
          [sg.Text('5,'), sg.Button("润/Run")],
          [sg.Multiline(size=(70, 5))],
          ]


# Create the Window
window = sg.Window('结构找形/Form-finding by HH', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    print(event)
    print(values)

    # print('You entered ', values)
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == "m":
        try:
            m = int(values["m"])
            window['mn_status'].update(
                "")
        except Exception:
            window['mn_status'].update("---Error: not a number---")
    if event == "n":
        try:
            n = int(values["n"])
            window['mn_status'].update(
                "")
        except Exception:
            window['mn_status'].update("---Error: not a number---")
    try:
        print(m, n)
        if m < 2 and n < 1:
            m = 2
            n = 1
        elif n < 1:
            n = 1
        elif m < 2:
            m = 2
        print(m, n)
        window['mn_status'].update(
            f"{m} columns and {n} rows of joints...")

    except Exception:
        continue

window.close()

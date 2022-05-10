# -*- coding: utf-8 -*-
"""
Created on Wed May  4 15:03:05 2022

@author: hh414
"""

import PySimpleGUI as sg

sg.theme('DarkAmber')

MAX_ROWS = 1
MAX_COL = 3

column_title = [[sg.Text("", size=(3, 1), justification='right'),
                 sg.Text("列号/Col. No.", size=(11, 1)),
                 sg.Text("行号/Row No.", size=(11, 1)),
                 sg.Text("标高/Init. Z", size=(11, 1))]]
columm_layout = [[sg.Text(str(i+1), size=(3, 1), justification='right')] + [sg.InputText("0", size=(12, 1), pad=(
    1, 1), border_width=0, justification='center', key=(i, j), enable_events=True) for j in range(MAX_COL)] for i in range(MAX_ROWS)]

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
          [sg.Text('3, 约束/Constrains')],
          [sg.Text('-约束形式/Constrain Form')],
          [sg.Radio('所有角点约束/All Corners Constrained', "boundary", default=True,
                    size=(30, 1), key="boundary1", enable_events=True),
           sg.Radio('所有边约束/All Edges Constrained', "boundary",
                    size=(30, 1), key="boundary2", enable_events=True)],
          [sg.Text("-约束点标高/Constrained Point Z Coordinates")],
          [sg.Text("", size=(1, 1)), sg.Input('0', key='LU', size=(5, 1),
                                              enable_events=True),
           sg.Text("...", size=(5, 1)), sg.Input('0', key='RU', size=(5, 1),
                                                 enable_events=True)],
          [sg.Text("", size=(1, 1)), sg.Text("...", size=(5, 1)),
           sg.Text("...", size=(5, 1)), sg.Text("...", size=(5, 1))],
          [sg.Text("", size=(1, 1)), sg.Input('0', key='LD', size=(5, 1),
                                              enable_events=True),
           sg.Text("...", size=(5, 1)), sg.Input('0', key='RD', size=(5, 1),
                                                 enable_events=True)],
          [sg.Text("-附加约束/Addtional Constrains")],
          [sg.Text("", size=(1, 1)),
           sg.Text("附加约束数量/No. of Addtional Constrains"),
           sg.Input('0', key='ac', size=(5, 1),
                    enable_events=True)],
          [sg.Col(column_title)],
          [sg.Col(columm_layout)],
          [sg.HSep()],
          [sg.Text('4, 设置预荷载/Pre-loading')],
          [sg.HSep()],
          [sg.Text('5, 设置力密度/Force Density')],
          [sg.HSep()],
          [sg.Text('6,'), sg.Button("润/Run")],
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
        if m < 2 and n < 1:
            m = 2
            n = 1
        elif n < 1:
            n = 1
        elif m < 2:
            m = 2
        window['mn_status'].update(
            f"{m} columns and {n} rows of joints...")
    except Exception:
        continue

    try:
        if m and n:
            if n > 1:
                if values["boundary1"]:
                    constrains = [[0, 0], [m-1, 0], [0, n-1], [m-1, n-1]]
                elif values["boundary2"]:
                    constrains = []
                    for w in range(m):
                        for v in range(n):
                            if v == 0 or v == n-1:
                                constrains.append([w, v])
                            else:
                                if w == 0 or w == m-1:
                                    constrains.append([w, v])
            else:
                constrains = [[0, 0], [m-1, 0]]
    except Exception:
        continue

    try:
        if m and n:
            try:
                LD = int(values['LD'])
            except Exception:
                LD = 0
            try:
                RD = int(values['RD'])
            except Exception:
                RD = 0
            try:
                LU = int(values['LU'])
            except Exception:
                LU = 0
            try:
                RU = int(values['RU'])
            except Exception:
                RU = 0

            if n > 1:
                if values["boundary1"]:
                    boundary_z = [[0, 0, LD], [m-1, 0, RD],
                                  [0, n-1, LU], [m-1, n-1, RU]]
                elif values["boundary2"]:
                    boundary_z = []
                    for w in range(m):
                        for v in range(n):
                            if v == 0:
                                boundary_z.append([w, v, LD+(RD-LD)/(m-1)*w])
                            elif v == n-1:
                                boundary_z.append([w, v, LU+(RU-LU)/(m-1)*w])
                            elif w == 0 and 0 < v < n-1:
                                boundary_z.append([w, v, LD+(LU-LD)/(n-1)*v])
                            elif w == m-1 and 0 < v < n-1:
                                boundary_z.append([w, v, RD+(RU-RD)/(n-1)*v])
            else:
                boundary_z = [[0, 0, LD], [m-1, 0, RD]]
    except Exception:
        continue

window.close()

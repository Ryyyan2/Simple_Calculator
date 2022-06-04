import numpy as np
import math
import PySimpleGUI as sg
import pandas as pd

# GUI code
sg.theme('Black')

 
EXCEL_FILE = 'CYLINDRICAL.xlsx'
df = pd.read_excel(EXCEL_FILE)
 


layout =[     
    [sg.Push(), sg.Text('CYLINDRICAL MEXE CALCULATOR', font= ("BankGothic Lt BT", 15)), sg.Push()],
    [sg.Text('Forward Kinematics Calculator', font= ("BankGothic Lt BT", 12))],
    [sg.Text('Fill out the following fields:', font= ("BankGothic Lt BT", 10)), 
     sg.Push(),sg.Text('Click this before solving Forward Kinematics==>', font= ("BankGothic Lt BT", 12)),sg.Button('O', font= ("BankGothic Lt BT", 15), size=(5,0), button_color =('white','silver')), sg.Push()],

    [sg.Text('a1 =', font= ("BankGothic Md BT", 10)),sg.InputText('10', key= 'a1', size=(20,10)),
     sg.Text('T1 =', font= ("BankGothic Md BT", 10)),sg.InputText('0', key= 'T1', size=(20,10)),
     sg.Push(),sg.Text('For Jacobian Matrix -->', font= ("BankGothic Md BT", 10)), sg.Button('J', font= ("BankGothic Md BT", 12), size= (5,0), button_color=('white','maroon')), sg.Push()],
     
    [sg.Text('a2 =', font= ("BankGothic Md BT", 10)),sg.InputText('20', key= 'a2', size=(20,10)),
     sg.Text('d2 =', font= ("BankGothic Md BT", 10)),sg.InputText('0', key= 'd2', size=(20,10)),
     sg.Push(),sg.Text('For Determinant -->', font= ("BankGothic Md BT", 10)),sg.Button('Det(J)', font= ("BankGothic Md BT",12), size=(5,0), button_color=('white', 'maroon')),sg.Push()],
    
    
    [sg.Text('a3 =', font= ("BankGothic Md BT", 10)),sg.InputText('30', key= 'a3', size=(20,10)),
     sg.Text('d3 =', font= ("BankGothic Md BT", 10)),
     sg.InputText('0', key= 'd3', size=(20,10)),
     sg.Push(),sg.Text('For Inverse of J -->', font= ("BankGothic Md BT", 10)),sg.Button('INV J', font= ("BankGothic Md BT",12), size=(5,0), button_color=('white', 'maroon')),sg.Push()],
  
    [sg.Button('Solve Forward Kinematics', font = ("BankGothic Md BT", 12), button_color=('white','maroon'),tooltip= 'Click the silver button frist!'),sg.Push(),
     sg.Button('Solve Inverse Kinematics', font =("BankGothic Md BT", 12), button_color=('white','blue'),tooltip= 'Click the silver button frist!'),sg.Push(),
     sg.Push(),sg.Text('Transpose of J -->', font= ("BankGothic Md BT", 10)),sg.Button('TRANS J', font= ("BankGothic Md BT",12), size=(5,0), button_color=('white', 'maroon')), sg.Push()],
     
    [sg.Frame('Position Vector: ',[[
        sg.Text('X =', font= ("BankGothic Md BT", 10)), sg.InputText(key='X', size=(10,1)),
        sg.Text('Y =', font= ("BankGothic Md BT", 10)), sg.InputText(key='Y', size=(10,1)),
        sg.Text('Z =', font= ("BankGothic Md BT", 10)), sg.InputText(key='Z', size=(10,1))]]),
        sg.Push(), sg.Button('Inverse Kinematics', font= ("BankGothic Md BT", 12), size= (20,0), button_color=('white','gold')), sg.Push(),
        sg.Push(), sg.Button('Path and Trajectory Planning', font= ("BankGothic Md BT", 12), size=(20,0), button_color=('white','gold')), sg.Push(),

],
    
    [sg.Push(), sg.Frame('H0_3 Transformation Matrix =',[[sg.Output(size=(60,12))]]),
     sg.Push(),sg.Image('Cylindrical.gif'), sg.Push()],
    [sg.Submit(font= ("BankGothic Md BT", 10)), sg.Exit(font=("BankGothic Md BT", 10))]
 
    
     
    
] 
  

window = sg.Window('CYLINDRICAL Manipualtor Forward Kinematics', layout, resizable=True)

while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event == 'Solve Inverse Kinematics':
                a1 = float(values['a1'])
                a2 = float(values['a2'])
                a3 = float(values['a3'])

                X = float(values['X'])
                Y = float(values['Y'])
                Z = float(values['Z'])

                try:
                    Th1 = (np.arctan(Y/X))
                except:
                    Th1 = -1
                    sg.popup('Warning! Present values cause error.')
                    sg.popup('Please restart the GUI then assign proper values!')
                    break

                Th1_a = np.arctan(Y/X)
                Th1 = np.degrees(Th1_a)
             
                d2 = Z - a1 - a2

             
                d3 = math.sqrt((X**2)+(Y**2)) - a3

                Th1 = window['IK_Th1'].Update(np.around(Th1,3))
                d2 = window['IK_d2'].Update(np.around(d2,3))
                d3 = window['IK_d3'].Update(np.around(d3,3))                                               

            elif event == 'Submit':
                df = df.append(values, ignore_index=True)
                df.to_excel(EXCEL_FILE, index=False)
                sg.popup('Data Saved!')
                window.close()


disable_J = window['J']
disable_DETJ = window['Det(J)']
disable_IV = window['INV J']
disable_TJ = window['TRANS J']
disable_IK = window['Inverse Kinematics']
disable_PT = window['Path and Trajectory Planning']
disable_FK = window['Solve Forward Kinematics']



def clear_input():
    for key in values:
        window[key]('')
    return None 

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    elif event == 'Click this before Solving \n Forward Kinematics':
        disable_FK.update(disabled=False)
        disable_J.update(disabled=True)
        disable_DETJ.update(disabled=True)
        disable_IV.update(disabled=True)
        disable_TJ.update(disabled=True)
        


    elif event == 'Solve Forward Kinematics':
      
        a1 = float(values['a1'])
        a2 = float(values['a2'])
        a3 = float(values['a3'])

        
        T1 = float(values['T1'])

        d2 = float(values['d2'])
        d3 = float(values['d3'])

       
        T1 = ((T1)/180.0)*np.pi

       
        PT = [[(0.0/180.0)*np.pi+float(T1),(0.0/180.0)*np.pi,0,float(a1)],
                [(270.0/180.0)*np.pi,(270.0/180.0)*np.pi,0,float(a2)+float(d2)],
                [(0.0/180.0)*np.pi,(0.0/180.0)*np.pi,0,float(a3)+float(d3)]]

    

        i = 0
        H0_1 = [[np.cos(PT[i][0]),-np.sin(PT[i][0])*np.cos(PT[i][1]),np.sin(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.cos(PT[i][0])],
                [np.sin(PT[i][0]),np.cos(PT[i][0])*np.cos(PT[i][1]),-np.cos(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.sin(PT[i][0])],
                [0,np.sin(PT[i][1]),np.cos(PT[i][1]),PT[i][3]],
                [0,0,0,1]]

        i = 1
        H1_2 = [[np.cos(PT[i][0]),-np.sin(PT[i][0])*np.cos(PT[i][1]),np.sin(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.cos(PT[i][0])],
                [np.sin(PT[i][0]),np.cos(PT[i][0])*np.cos(PT[i][1]),-np.cos(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.sin(PT[i][0])],
                [0,np.sin(PT[i][1]),np.cos(PT[i][1]),PT[i][3]],
                [0,0,0,1]]

        i = 2
        H2_3 = [[np.cos(PT[i][0]),-np.sin(PT[i][0])*np.cos(PT[i][1]),np.sin(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.cos(PT[i][0])],
                [np.sin(PT[i][0]),np.cos(PT[i][0])*np.cos(PT[i][1]),-np.cos(PT[i][0])*np.sin(PT[i][1]),PT[i][2]*np.sin(PT[i][0])],
                [0,np.sin(PT[i][1]),np.cos(PT[i][1]),PT[i][3]],
                [0,0,0,1]]

        H0_1 = np.matrix(H0_1)

        H0_2 = np.dot(H0_1,H1_2)
        H0_3 = np.dot(H0_2,H2_3)

        print("H0_3=")
        print(np.matrix(H0_3))

        X0_3 = H0_3[0,3]
        print("X = ")
        print (X0_3)

        Y0_3 = H0_3[1,3]
        print("Y = ")
        print (Y0_3)

        Z0_3 = H0_3[2,3]
        print("Z = ")
        print (Z0_3)

        disable_J.update(disabled=False)
        

        
    elif event == 'Submit' :
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('Data saved!')
    elif event == 'Jacobian Matrix (J)':
        
        ### Jacobian Matrix
        
        try:
            H0_1 = np.matrix(H0_1) 
        except:
            H0_1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart Gui then go first "Click this before Solving Forward Kinematics"!')
            break

        
        Z_1 = [[0],[0],[1]] 
        iden = [[1,0,0],[0,1,0],[0,0,1]] 

   
        J1a = np.dot(iden,Z_1)
    

        J1b_1 = H0_3[0:3,3:]
        J1b_1 = np.matrix(J1b_1)

        J1b_2 = [[0],[0],[0]]

        J1b = J1b_1 - J1b_2

        J1 = [[(J1a[1,0]*J1b[2,0])-(J1a[2,0]*J1b[1,0])],
              [(J1a[2,0]*J1b[0,0])-(J1a[0,0]*J1b[2,0])],
              [(J1a[0,0]*J1b[1,0])-(J1a[1,0]*J1b[0,0])]]
       
       

        J2 = H0_1[0:3,0:3]
        J2 = np.dot(J2,Z_1)
       

        J3 = H0_2[0:3,0:3]
        J3 = np.dot(J3,Z_1)
       

       
        J4= np.dot(iden,Z_1)
       
        J5 = [[0],[0],[0]]
        J5 = np.matrix(J5)
       
        J6 = [[0],[0],[0]]
        J6 = np.matrix(J6)
     
 
        JM1 = np.concatenate((J1,J2,J3),1)
        
        JM2 = np.concatenate((J4,J5,J6),1)
       
        J = np.concatenate((JM1,JM2),0)
        
        (J)

        sg.popup ('J = ', J)
        DJ = np.linalg.det(JM1)
        if DJ == 0.0 >= DJ > -1.0:
           
           disable_IV.update(disabled=True)
           sg.popup('Warning: Jacobian Matrix is Non-Invertible')
        elif DJ !=0.0 or DJ != -0.0:
            disable_IV.update(disabled=False)

        
        disable_J.update(disabled=True)
        disable_DETJ.update(disabled=False)
        disable_TJ.update(disabled=False)

    elif event == 'Det(J)':
        try:
            JM1 = np.concatenate((J1,J2,J3),1) 
        except:
            JM1 = -1 #NAN
            sg.popup('Warning!')
            sg.popup('Restart Gui then go first "Click this before Solving Forward Kinematics"!')
            break
          
        DJ = np.linalg.det(JM1)
        
        sg.popup('DJ = ',DJ)

        if DJ == 0.0 >= DJ > -1.0:
           
           disable_IV.update(disabled=True)
           sg.popup('Warning: Jacobian Matrix is Non-Invertible')

    elif event == 'Inverse of J':
       
        try:
            JM1 = np.concatenate((J1,J2,J3),1) 
        except:
            JM1 = -1 
            sg.popup('Warning!')
            sg.popup('Restart Gui then go first "Click this before Solving Forward Kinematics"!')
            break

        IV = np.linalg.inv(JM1)
        
        sg.popup('IV = ',np.around(IV,3))

    elif event == 'Transpose of J':
      
        try:
            JM1 = np.concatenate((J1,J2,J3),1) 
        except:
            JM1 = -1 
            sg.popup('Warning!')
            sg.popup('Restart Gui then go first "Click this before Solving Forward Kinematics"!')
            break
       
        TJ = np.transpose(JM1)
       

        sg.popup('TJ = ',TJ)


    elif event == 'Solve Inverse Kinematics':
        window()
        
window.close()




















        

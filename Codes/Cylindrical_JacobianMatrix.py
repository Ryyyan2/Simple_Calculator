import numpy as np
import math
import PySimpleGUI as sg
import pandas as pd 

# GUI code

sg.theme('Black')

#excel read code
 
EXCEL_FILE = 'CYLINDRICAL.xlsx'
df = pd.read_excel(EXCEL_FILE)
 
# Layoutcode

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
  
#windows
window = sg.Window('CYLINDRICAL Manipualtor Forward Kinematics', layout, resizable= "true")

#variable code for disabling buttons
disable_J = window['J']
disable_DETJ = window['Det(J)']
disable_IV = window['INV J']
disable_TJ = window['TRANS J']
disable_IK = window['Inverse Kinematics']
disable_PT = window['Path and Trajectory Planning']

def clear_input():
    for key in values:
        window[key]('')
    return None

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break 
    if event == 'O':
        disable_J.Update(disabled=True)
        disable_DETJ.Update(disabled=True)
        disable_IV.Update(disabled=True)
        disable_TJ.Update(disabled=True)
        disable_IK.Update(disabled=True)
        disable_PT.Update(disabled=True)
        

    if event == 'Solve Forward Kinematics':
        
        #FORWARD KINEMATIC CODES
        a1 = float(values ['a1'])
        a2 = float(values ['a2'])
        a3 = float(values ['a3'])
#Joint Variable Thetas in degrees.

        T1 = float(values ['T1'])
        d2 = float(values ['d2'])
        d3 = float(values ['d3'])

# Joint Variable Thetas in radians.

        T1 = (T1/180.0)*np.pi
    
        
        DHPT = [[T1,(0.0/180.0)*np.pi,0,a1],
                [(270.0/180.0)*np.pi,(270.0/180.0)*np.pi,0,a2+d2], 
                [(0.0/180.0)*np.pi,(0.0/180.0)*np.pi,0,a3+d3]]

#np.trigo function (DHPT [row][column])

        i = 0
        H0_1 = [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),(DHPT[i][2])*np.cos(DHPT[i][0])],
                [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),DHPT[i][2]*np.sin(DHPT[i][0])],
                [0,np.sin(DHPT[i][1]),np.cos(DHPT [i][1]),DHPT[i][3]],
                [0,0,0,1]]
        
        i = 1
        H1_2 =  [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),(DHPT[i][2])*np.cos(DHPT[i][0])],
                 [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),(DHPT[i][2])*np.sin(DHPT[i][0])],
                 [0,np.sin(DHPT[i][1]),np.cos(DHPT [i][1]),DHPT[i][3]],
                 [0,0,0,1]]
        
        i = 2
        H2_3 =  [[np.cos(DHPT[i][0]),-np.sin(DHPT[i][0])*np.cos(DHPT[i][1]),np.sin(DHPT[i][0])*np.sin(DHPT[i][1]),(DHPT[i][2])*np.cos(DHPT[i][0])],
                 [np.sin(DHPT[i][0]),np.cos(DHPT[i][0])*np.cos(DHPT[i][1]),-np.cos(DHPT[i][0])*np.sin(DHPT[i][1]),(DHPT[i][2])*np.sin(DHPT[i][0])],
                 [0,np.sin(DHPT[i][1]),np.cos(DHPT [i][1]),DHPT[i][3]],
                 [0,0,0,1]]
        
        #matrices
        
        #print("H0_1= ")
        #print(np.matrix(H0_1))
        #print("H1_2= ")
        #print(np.matrix(H1_2))
        #print("H2_3= ")
        #print(np.matrix(H2_3))     
        
        H0_2 = np.dot(H0_1,H1_2)
        H0_3 = np.dot(H0_2,H2_3)
        
        print("H0_3 =")
        print(np.matrix(H0_3))
        
        X0_3 = H0_3[0,3]
        print("X = ",X0_3)
        
                
        Y0_3 = H0_3[1,3]
        print("Y = ",Y0_3)
                
        Z0_3 = H0_3[2,3]
        print("Z = ",Z0_3)
       
        
        disable_J.Update(disabled=False)
        disable_IK.Update(disabled=False)
        disable_PT.Update(disabled=False)
        
     
    if event == 'Submit':
        df = df.append(values, ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        sg.popup('DATA SAVED!!!',font= ("Brittanic Bold", 15))
    
    if event == 'J':
        Z_1 = [[0],[0],[1]]
        
        J1= [[1,0,0],[0,1,0],[0,0,1]]
        J1= np.dot(J1,Z_1)
        J1= np.matrix(J1)
        
        try: 
            H0_1 = np.matrix(H0_1)
        except:
            H0_1 = -1
            sg.popup('WARNING!!!',font= ("Brittanic Bold", 20))
            sg.popup('Restart the GUI then click first the silver button!!',font= ("Brittanic Bold", 20))
            break
            
            
        J2a = H0_1[0:3,0:3]
        J2a = np.dot(J2a,Z_1)
        
        J2b_1 = H0_3[0:3,3:]
        J2b_1 = np.matrix(J2b_1)
        
        J2b_2 = H0_1[0:3,3:]
        J2b_2 = np.matrix(J2b_2)
         
        J2b = J2b_1 - J2b_2
        
        J2 = [[(J2a[1,0]*J2b[2,0])-(J2a[2,0]*J2b[1,0])],
            [(J2a[2,0]*J2b[0,0])-(J2a[0,0]*J2b[2,0])],
            [(J2a[0,0]*J2b[1,0])-(J2a[1,0]*J2b[0,0])]]
        
        J3a = H0_1[0:3,0:3]
        J3a = np.dot(J3a,Z_1)
        
        J3b_1 = H0_3[0:3,3:]
        J3b_1 = np.matrix(J3b_1)
        
        J3b_2 = H0_2[0:3,3:]
        J3b_2 = np.matrix(J3b_2)
        
        J3b = J3b_1 - J3b_2
        
        J3 = [[(J3a[1,0]*J3b[2,0])-(J3a[2,0]*J3b[1,0])], 
            [(J3a[2,0]*J3b[0,0])-(J3a[0,0]*J3b[2,0])],
             [(J3a[0,0]*J3b[1,0])-(J3a[1,0]*J3b[0,0])]]
        
        J4 = [[0],[0],[0]]
        J4 = np.matrix(J4)
        
        J5= H0_1 [0:3,0:3]
        J5= np.dot(J5,Z_1)
        J5= np.matrix(J1)
        
        J6= H0_1 [0:3,0:3]
        J6= np.dot(J6,Z_1)
        J6= np.matrix(J1)
        
        JM1 = np.concatenate((J1,J2,J3),1)
        JM2 = np.concatenate((J4,J5,J6),1)
        
        J = np.concatenate((JM1,JM2),0)
        sg.popup('J =',J,font= ("Brittanic Bold", 15))
        
        DJ = np.linalg.det(JM1)
        if DJ == 0 or DJ == -0:
            disable_IV.Update(disabled=True)
            sg.popup('Jacobian Matrix is Non-Invertible!!',font= ("Brittanic Bold", 15)) 
        elif DJ != 0 or DJ != -0:
            disable_IV.Update(disabled=False)
        
        disable_J.Update(disabled=True)
        disable_DETJ.Update(disabled=False)
        disable_TJ.Update(disabled=False)
   
    if event == 'Det(J)':
        try: 
            JM1 = np.concatenate((J1,J2,J3),1)
        except:
            JM1 = -1
            sg.popup('WARNING!!!',font= ("Brittanic Bold", 20))
            sg.popup('Restart the GUI then click first the silver button!!',font= ("Brittanic Bold", 20))
            break
            
        DJ = np.linalg.det(JM1)
        sg.popup('DJ = ',DJ,font= ("Brittanic Bold", 15))
       
        if DJ == 0 or DJ == -0:
            disable_IV.Update(disabled=True)
            sg.popup('Jacobian Matrix is Non-Invertible!!',font= ("Brittanic Bold", 15))
        
    if event == 'INV J':
        
        try: 
            JM1 = np.concatenate((J1,J2,J3),1)
        except:
            JM1 = -1
            sg.popup('WARNING!!!',font= ("Brittanic Bold", 20))
            sg.popup('Restart the GUI then click first the silver button!!',font= ("Brittanic Bold", 20))
            break
            
        IJ = np.linalg.inv(JM1)
        sg.popup('IJ =',IJ,font= ("Brittanic Bold", 15))
          
    if event == 'TRANS J' :
        
        try: 
            JM1 = np.concatenate((J1,J2,J3),1)
        except:
            JM1 = -1
            sg.popup('WARNING!!!',font= ("Brittanic Bold", 20))
            sg.popup('Restart the GUI then click first the silver button!!',font= ("Brittanic Bold", 20))
            break 
            
        TJ = np.transpose(JM1)
         
        sg.popup('TJ =',TJ,font= ("Brittanic Bold", 15))
         
    elif event == 'Solve Inverse Kinematics':
           
        window.close()
   
  
    


    
 




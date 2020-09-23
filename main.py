"""
    FUZZY C MEANS ALGORITHMS:
        CLASSIC FCM
        TYPE-2 FCM
        SIGMA FCM

    CLUSTERING VALIDITY CRITERIONS

"""
import pkg_resources.py2_warn
import os
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
#from sklearn import metrics
#from sklearn.cluster import KMeans
from ClusteringValidity import ClusteringValidity
from FuzzyCMeans import FuzzyCMeans
from FuzzyCmeansType2 import FuzzyCMeansType2
from ExternalClusteringValidity import RandIndex, AdjustedRandIndex, JaccardCoefficient
from tkinter import messagebox
from tkinter import *
import pandas
from FCM_Sigma import FCM_Sigma
from math import *

########################### GUI
root = Tk()
root.title("FUZZY C MEANS CLUSTERING ALGORITHMS")

files = []


def OpenFile():
    filename = filedialog.askopenfilename(title="Select File",
                                          filetypes=(('File', '*.csv'), ('All file', '*.*')))
    #print(filename)
    if filename == '':
    	resp = messagebox.showerror("ERROR!", "You have not yet selected the data file.")

    files.append(filename)


    #print(files)


####################### frame 1 #######################
frame1 = LabelFrame(root, bg = 'gray32', text='MAIN FRAME', padx=20, pady=20)
frame1.pack(padx=20, pady=20)

####################### WARNING #######################
warning = Label(frame1, bg = 'gray32', text='WARNING').pack()
warn1 = Label(frame1, bg = 'gray32', text="\t1: Make sure that the data fields are numeric").pack()
warn2 = Label(frame1, bg = 'gray32',
            text="\t2: If your datasets have been labeled. Make sure the column containing the data label is in the LAST column of datasets").pack()
warn3 = Label(frame1, bg = 'gray32',
            text="\t3: If your datasets have ID field. Make sure the column containing the data ID is in the FIRST column of datasets").pack()

####################### SELECT FILE ####################
select_file = Label(frame1, bg = 'gray32', text="\tLet's choose your .CSV file: ").pack()
b1 = Button(frame1, bg = 'saddle brown', text='Open file', command=OpenFile).pack()

##### Datasets have been labeled ?
# def label(value):
#     myLabel = Label(frame1, text=value)
#     myLabel.pack()

####################### QUESTIONS #######################
labeled = StringVar()
labeled.set('?')
st5 = Label(frame1, bg = 'gray32', text='Have Datasets been labeled?').pack()
Radiobutton(frame1, bg = 'blue2', fg = 'red', text='Yes', variable=labeled, value='y').pack()
Radiobutton(frame1, bg = 'red', fg = 'blue2', text='No', variable=labeled, value='n').pack()

# myButton1 = Button(frame1, text='confirm', command=lambda: label(labeled.get()))
# myButton1.pack()

#### Datasets have ID field ?

# def ID(value):
#     myLabel = Label(frame1, text=value)
#     myLabel.pack()


IDs = StringVar()
IDs.set('?')
st6 = Label(frame1, bg = 'gray32', text='Do Datasets have ID field?').pack()
Radiobutton(frame1, bg = 'blue2', fg = 'red', text='Yes', variable=IDs, value='y').pack()
Radiobutton(frame1, bg = 'red', fg = 'blue2', text='No', variable=IDs, value='n').pack()

# myButton2 = Button(frame1, text='confirm', command=lambda: label(IDs.get()))
# myButton2.pack()


###### number of cluster
# K= IntVar()
Label(frame1, bg = 'gray32',
      text='How many cluster do you want? Import (K is integer, N is length of datasets, 1 < K < N) K = ').pack()
Ks = Entry(frame1, bg = 'CadetBlue2')
Ks.pack()
# def myK():
#     Label(frame2, text=Ks.get()).pack()
# Button(frame1, text='confirm K', command = myK).pack()

####### condition for terminate

Label(frame1,  bg = 'gray32', text='Select the stop condition (1e-4 <= epsilon <= 1e-3): epsilon = ').pack()
e = Entry(frame1, bg = 'CadetBlue2')
e.pack()

######## Fuzzy parameter

Label(frame1, bg = 'gray32', text='Select the FCM parameter (1.5 <= m <= 3.0): m = ').pack()
ms = Entry(frame1, bg = 'CadetBlue2')
ms.pack()

######### SELECT ALGORITHMS ####################################

fuzzy = IntVar()
st7 = Label(frame1, bg = 'gray32', text='Which Algorithm do you want to use?').pack()
Radiobutton(frame1,  bg = 'gray32', text='Classic FCM', variable=fuzzy, value=1).pack()
Radiobutton(frame1,  bg = 'gray32', text='Type-2 FCM', variable=fuzzy, value=2).pack()
Radiobutton(frame1,  bg = 'gray32', text='Sigma FCM', variable=fuzzy, value=3).pack()


############## Main ######################
def Main():
    #print("File name = ", files)
    if len(files) == 0:
    	resp = messagebox.showerror("ERROR!", "You have not yet selected the data file.")
    df_full = pandas.read_csv(files[-1], header=0)
    print("DF full = ", df_full)
    DATAFRAME = df_full.copy(deep = True)
    columns = list(df_full.columns)
    #print("Columns = ", columns)

    original_labels = None
    check_labels = labeled.get()
    if check_labels == 'y' or check_labels == 'Y':
        original_labels = list(map(str, df_full[columns[-1]]))
        df_full.drop(columns[-1], axis=1, inplace=True)
        del columns[-1]
    #print("DATA FRAME = ", df_full)

    check_id = IDs.get()
    if check_id == 'y' or check_id == 'Y':
        df_full.drop(columns[0], axis=1, inplace=True)
        del columns[0]

    df = df_full.dropna() #drop all row that have NA in any attribute
    df = df[columns]
    df = pd.get_dummies(df, dtype=float) # Convert categorical variable into dummy/indicator variables.
    df = df.dropna()
    data_frame = np.asarray(df, dtype=float)
    #print("DATA FRAME = ", data_frame)
    #print(type(data_frame))
    ################### PARAMETERS FOR CLUSTERING ##########################
    N = len(data_frame)
    K = int(Ks.get())
    epsilon = float(e.get())
    m = float(ms.get())

    #################### CLUSTERING VALIDITY ###############################
    def FuzzyC(my_clustering, title):
        my_cluster_centers, my_labels = my_clustering.FCM()
        my_compute_ind = ClusteringValidity(data_frame, K, N, my_labels)

        top = Toplevel(bg = 'gray62', height = 60, padx = 100, pady = 5, width = 120)
        top.title(title)
        Label(top, bg = 'saddle brown', font = ('Helvetica', '12'), text="Relative Clustering Validity Criteria").pack()
        frame11 = LabelFrame(top, bg = 'gray32', font = ('Helvetica', '10'), text='1: Davies-Bouldin Index:')
        frame11.pack()
        Label(frame11, text=my_compute_ind.DB_idx()).pack()

        frame12 = LabelFrame(top, bg = 'gray32', font = ('Helvetica', '10'), text='2: Calinski-Harabasz Index:')
        frame12.pack()
        Label(frame12, text=my_compute_ind.VRC_idx()).pack()

        frame13 = LabelFrame(top, bg = 'gray32', font = ('Helvetica', '10'), text='3: Dunn Index:')
        frame13.pack()
        Label(frame13, text=my_compute_ind.DN_idx()).pack()

        frame14 = LabelFrame(top, bg = 'gray32', font = ('Helvetica', '10'), text='4: Silhouette Width Index:')
        frame14.pack()
        Label(frame14, text=my_compute_ind.SWC_idx()).pack()

        frame15 = LabelFrame(top, bg = 'gray32', font = ('Helvetica', '10'), text='5: Simplified Silhouette Width Index:')
        frame15.pack()
        Label(frame15, text=my_compute_ind.SSWC_idx()).pack()

        frame16 = LabelFrame(top, bg = 'gray32', font = ('Helvetica', '10'), text='6: PBM Index:')
        frame16.pack()
        Label(frame16, text=my_compute_ind.PBM_idx()).pack()

        frame17 = LabelFrame(top, bg = 'gray32', font = ('Helvetica', '10'), text='7: C Index:')
        frame17.pack()
        Label(frame17, text=my_compute_ind.CI_idx()).pack()

        frame18 = LabelFrame(top, bg = 'gray32', font = ('Helvetica', '10'), text='8: Point Biserial Index:')
        frame18.pack()
        Label(frame18, text=my_compute_ind.PB_idx()).pack()

        frame19 = LabelFrame(top, bg = 'gray32', font = ('Helvetica', '10'), text='9: C per Sqrt(K) Index:')
        frame19.pack()
        Label(frame19, text=my_compute_ind.CK_idx()).pack()

        if check_labels == 'y' or check_labels == 'Y':
            Label(top, bg = 'saddle brown', font = ('Helvetica', '12'), text='External Clustering Validity Criteria').pack()
            RandI = RandIndex(N, data_frame, original_labels, my_labels)
            AdjustedRandI = AdjustedRandIndex(N, data_frame, original_labels, my_labels)
            JaccardCoeff = JaccardCoefficient(N, data_frame, original_labels, my_labels)

            frame110 = LabelFrame(top, bg = 'gray32', font = ('Helvetica', '10'), text='1: Rand Index:')
            frame110.pack()
            Label(frame110, text=RandI.RI()).pack()

            frame111 = LabelFrame(top, bg = 'gray32', font = ('Helvetica', '10'), text='2: Adjusted Rand Index:')
            frame111.pack()
            Label(frame111, text=AdjustedRandI.ARI()).pack()

            frame112 = LabelFrame(top, bg = 'gray32', font = ('Helvetica', '10'), text='3: Jaccard Coefficient:')
            frame112.pack()
            Label(frame112, text=JaccardCoeff.JC()).pack()

        dir = []

        def openDir():
            path = filedialog.askdirectory()
            if len(path) == 0:
                resp = messagebox.showerror("ERROR!", "You have not selected the directory.")
            else:
                mess = "Path to the directory: " + path
                resp = messagebox.showinfo("Notification!", mess)
            dir.append(path)

        def writeFile():
            l = files[-1].split('/')
            tmp = l[-1].split('.')
            tmp[0] = tmp[0] + '_RESULT'
            l[-1] = '.'.join(tmp)
            if len(dir) == 0:
                dir.append('/'.join(l[:-1]))
            print("DIRECTORY = ", dir)
            realPath = dir[-1] + '/' + l[-1]

            
            exist = os.path.exists(realPath)
            if exist:
                df_tmp = pandas.read_csv(realPath, header=0)
                print("DF tmp = ", df_tmp)
                new_col = list(df_tmp.columns)
                ll = new_col[-1].split('_')
                ll[-1] = str(int(ll[-1]) + 1)
                new_label = '_'.join(ll)
                df_tmp[new_label] = my_labels
                df_tmp.to_csv(realPath, index = False)
            
            else:
                DATAFRAME['Label_1'] = my_labels
                print("DATAFRAME = ", DATAFRAME)
                DATAFRAME.to_csv(realPath, index = False)
            """
            f = open(realPath, 'w')
            for item in my_labels:
                f.write(str(item) + '\n')
            f.close()
            """
            s = "Cluster data has been saved in path: " + realPath
            resp = messagebox.showinfo("SAVED", s)

        saveButton = Button(top, bg = 'CadetBlue2', font = ('Helvetica', '10'), fg = 'black', text='Choose a dir to save result.', command=openDir)
        saveButton.pack()
        saveResult = Button(top, bg = 'saddle brown', font = ('Helvetica', '10'), fg = 'black', text='Save file', command=writeFile)
        saveResult.pack()

    if (labeled.get() == '?'):
        resp = messagebox.showerror("ERROR", "Does your data have labeled? ")

    elif (IDs.get() == '?'):
        resp = messagebox.showerror("ERROR", "Does your data have ID? ")

    elif (K <= 1 or K >= N):
        resp = messagebox.showerror("ERROR", "Your number of cluster is not valid")

    elif (epsilon > 1e-3 or epsilon < 1e-4):
        resp = messagebox.showerror("ERROR", "Your stop condition is not valid")

    elif (m < 1.5 or m > 3):
        resp = messagebox.showerror("ERROR", "Your FCM parameter is not valid")

    elif ((m - floor(m)) != 0 and fuzzy.get() == 2):
        resp = messagebox.showerror("ERROR", "With Type-2 FCM m must be an integer")

    else:
        fuz = fuzzy.get()
        if fuz == 1:
            my_clustering = FuzzyCMeans(m, data_frame, N, K, epsilon)
            title1 = 'CLUSTERING VALIDITY :: CLASSIC FCM'
            FuzzyC(my_clustering,title1)

        elif (fuz == 2):
            my_clustering = FuzzyCMeansType2(m, data_frame, N, K, epsilon)
            title2 = 'CLUSTERING VALIDITY :: TYPE-2 FCM'
            FuzzyC(my_clustering, title2)

        elif (fuz == 3):
            my_clustering = FCM_Sigma(m, data_frame, N, K, epsilon)
            title3 = 'CLUSTERING VALIDITY :: SIGMA FCM'
            FuzzyC(my_clustering, title3)


Button(frame1, bg = 'saddle brown', text='Confirm', command=Main).pack()

################### frame 2 #############################
# frame2 = LabelFrame(root, text='Second Frame', padx=50, pady=50)
# frame2.pack(padx=20, pady=20)
# b2 = Button(frame2, text='don\'t click here').pack()
root.mainloop()

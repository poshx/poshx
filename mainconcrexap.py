import time
from threading import *
from tkinter import *
from tkinter import messagebox
import mysql.connector
import snap7
from datetime import date
from datetime import datetime
import traceback
import sys

import pandas as pd
#sys.setrecursionlimit(100)


class Application():
    def threading(self):
        self.t1 = Thread(target=self.check)
        self.t1.start()
    def threading2(self):
        self.t2 = Thread(target=self.atualizaDados)
        self.t2.start()


    def __init__(self):




        self.root = Tk()
        self.root.iconbitmap('icone_concrexap.ico')
        self.root.title("Painel de Informaçoes")
        self.root.geometry("380x290")
        self.root.configure(background= 'white')

        self.btnAtualiza = Button(self.root, text="Ultima Pesagem", command=self.ultimaPesagem)
        self.btnAtualiza.place(x=200, y=25)
        self.btnLimpa = Button(self.root, text=" X ", command=self.limparPesagem)
        self.btnLimpa.place(x=300, y=25, width= 25)
        self.imgrodape=PhotoImage(file="concrexap1.png")
        self.l_rodape=Label(self.root, image=self.imgrodape)
        self.l_rodape.place(x=87, y=235)

        self.img=PhotoImage(file="clperrorfinal.png")
        self.l_logo=Label(self.root)
        self.l_logo.place(x=25, y=20)

        self.imgok=PhotoImage(file="mysqlerror.png")
        self.l_logook=Label(self.root)
        self.l_logook.place(x=25, y=120)
        self.clp()
        self.threading()
        self.threading2()




        self.root.mainloop()
    def callback(self):
        self.img2 = PhotoImage(file="clpokfinal.png")
        self.l_logo.configure(image=self.img2)
        self.l_logo.image = self.img2
    def callback2(self):
        self.imgerror = PhotoImage(file="mysqlok.png")
        self.l_logook.configure(image=self.imgerror)
        self.l_logook.image = self.imgerror
    def callback3(self):
        self.img3 = PhotoImage(file="clperrorfinal.png")
        self.l_logo.configure(image=self.img3)
        self.l_logo.image = self.img3
    def callback4(self):
        self.imgerror4 = PhotoImage(file="mysqlerror.png")
        self.l_logook.configure(image=self.imgerror4)
        self.l_logook.image = self.imgerror4




    def clp(self):

        time.sleep(2)


        self.IP = '10.10.0.5'
        self.RACK = 0
        self.SLOT = 1

        self.DB_NUMBER = 1
        self.START_ADDRESS = 0
        self.SIZE = 264

        self.plc = snap7.client.Client()
        self.plc.connect(self.IP, self.RACK, self.SLOT)
        self.db = self.plc.db_read(self.DB_NUMBER, self.START_ADDRESS, self.SIZE)


        #self.temp_silo_01 = int.from_bytes(self.db[258:260], byteorder='big')

        #self.temp_silo_02 = int.from_bytes(self.db[260:262], byteorder='big')


        #print(self.plc.get_cpu_state())



        #db = plc.db_read(DB_NUMBER, START_ADDRESS, SIZE)

        #product_name = db[2:256].decode('UTF-8').strip('\x00')

        #product_value = int.from_bytes(db[256:258], byteorder='big')





    def check(self):
        print("conectando CLP...")
        time.sleep(2)
        while True:

            try:
                self.clp()

                self.conectado = self.plc.get_cpu_state()

                if self.conectado == "S7CpuStatusRun":


                    self.callback()

                else:
                    self.callback3()
                    print("fora")
                    print(self.conectado)
                    time.sleep(5)





            except Exception:
                self.callback3()


                traceback.print_exc()





    def conecta(self):
        self.conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            passwd="",
            database='sincronizado'

        )
        self.cursor = self.conn.cursor()
    def ultimaPesagem(self):
        self.conecta()

        self.query = (""" SELECT * FROM relatorio ORDER BY codigo ASC
                                                            """)
        self.df = pd.read_sql(self.query, self.conn)
        self.valor_cimento = self.df['cimento'].iloc[-1]
        self.valor_agregado = self.df['agregado'].iloc[-1]
        self.valor_data = self.df['data'].iloc[-1]
        self.texto_info = Label(self.root, text="Ultima Pesagem")
        self.texto_info.place(x=200, y=50)
        self.texto_data = Label(self.root, text="")
        self.texto_data.place(x=200, y=75)
        self.texto_cimento = Label(self.root, text="")
        self.texto_cimento.place(x=200, y=100)
        self.texto_agregado = Label(self.root, text="")
        self.texto_agregado.place(x=200, y=125)
        self.texto_data["text"] = self.valor_data
        self.texto_cimento["text"] = "Cimento: ", self.valor_cimento
        self.texto_agregado["text"] = "Agregado: ", self.valor_agregado
        self.conn.close()

    def limparPesagem(self):
        self.texto_info.destroy()
        self.texto_data.destroy()
        self.texto_cimento.destroy()
        self.texto_agregado.destroy()



    def atualizaDados(self):
        while True:

            try:
                time.sleep(2)

                self.conecta()
                self.callback2()
                self.now = datetime.now()
                self.date_time =self.now.strftime("%d/%m/%Y, %H:%M:%S")
                self.db = self.plc.db_read(self.DB_NUMBER, self.START_ADDRESS, self.SIZE)
                self.temp_silo_01 = int.from_bytes(self.db[258:260], byteorder='big')

                self.temp_silo_02 = int.from_bytes(self.db[260:262], byteorder='big')
                self.sinalBotao = int.from_bytes(self.db[262:264], byteorder='big')



                if self.sinalBotao == 1:



                    self.cursor.execute("INSERT INTO relatorio (cimento, agregado, data) VALUES ('{0}', '{1}', '{2}')".format(self.temp_silo_01, self.temp_silo_02, self.date_time))

                    self.conn.commit()
                    self.conn.close()
                    self.plc.disconnect
                    time.sleep(9)




            except Exception:
                traceback.print_exc()

                self.callback4()
                print("Falha na conexão")
                time.sleep(2)











        #threading.Thread(target=atualizaDados()).start()

        #temp_silo_02 = int.from_bytes(db[260:262], byteorder='big' )
        #print("temp02 = ",temp_silo_02)

        #temp_silo_03 = int.from_bytes(db[262:264], byteorder='big' )
        #print("temp03 = ",temp_silo_03)

        #temp_silo_04 = int.from_bytes(db[264:268], byteorder='big' )
        #print("temp04 = ",temp_silo_04)

if __name__== "__main__":
    Application()
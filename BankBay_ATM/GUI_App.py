from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from time import *
import mysql.connector
import datetime


"""
Class For ATM Machine
"""
timedelay=100

class AtmMachine(Tk):
    def __all_children(self) :
            _list = self.winfo_children()

            for item in _list :
                if item.winfo_children() :
                    _list.extend(item.winfo_children())
            return _list

    def __mainwindow(self,cardNumber):

        def delete_all():
            widget_list = self.__all_children()
            for item in widget_list:
                item.destroy()
            #cancel btn----------------
            self.reset=Button(self,cursor="hand2",bg="red4",fg="ivory",text="EXIT",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=self.__startwindow,bd=0)
            self.reset.place(relx=.89, rely=0.015)

        def only_numbers(char):
            return char.isdigit()
        self.validation = self.register(only_numbers)             

        def withdraw(cardNumber):
            def withdrawl_process(cardNumber,amount):
                amount=int(amount)
                delete_all()
                info(cardNumber)
                sql = "SELECT * FROM card_informations WHERE card_number='{}';".format(cardNumber)
                mycursor.execute(sql)
                result = mycursor.fetchone()
                balance=int(result[4])

                if(amount >= 100):
                    if(amount <=40000):
                        if(amount%100==0):
                            if(amount>balance):
                                self.permit_withdrawn_label=Label(self, text="  Insufficient Funds In Account ", font=("Bookman Old Style",30,"bold"),bg='navy', fg='red')
                                self.permit_withdrawn_label.place(relx=.45,rely=.48)
                                self.redirect=Button(self,cursor="hand2",bg="red4",fg="ivory",text="Ok",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=lambda:self.__mainwindow(cardNumber),bd=0)
                                self.redirect.place(relx=0.6, rely=0.65)
                                
                            else:
                                self.permit_withdrawn_label=Label(self, text=" Processing Your Amount Of ₹{}".format(amount), font=("Cascadia Code",28,"bold"),bg='navy', fg='green4')
                                self.permit_withdrawn_label.place(relx=.38,rely=.4)
                                try:
                                    sql = "UPDATE card_informations SET balance = balance - {} WHERE card_number='{}';".format(amount,cardNumber)
                                    my=mycursor.execute(sql)
                                    mydb.commit()
                                    messagebox.showinfo("Transaction Success","Your Withdrawl Process Was Successfully Completed")
                                    # sql = "SELECT * FROM card_informations WHERE card_number='{}';".format(cardNumber)
                                    # mycursor.execute(sql)
                                    # result = mycursor.fetchone()
                                    # balance=int(result[4])
                                    # self.savingsaccountbalance_label.configure(text="₹ "+str(balance))
                                    self.__mainwindow(cardNumber)
                                
                                except Exception as e:
                                    messagebox.showerror("Transaction Failed","Your Withdrawl Process FAILED..!")
                                self.__mainwindow(cardNumber)
                        else:
                            self.permit_withdrawn_label=Label(self, text="  Amount Should Be A Multiple Of ₹100 ", font=("Bookman Old Style",30,"bold"),bg='navy', fg='red')
                            self.permit_withdrawn_label.place(relx=.4,rely=.48)
                            self.redirect=Button(self,cursor="hand2",bg="red4",fg="ivory",text="Ok",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=lambda:self.__mainwindow(cardNumber),bd=0)
                            self.redirect.place(relx=0.6, rely=0.65)

                    else:
                        self.permit_withdrawn_label=Label(self, text="  Transaction Above ₹40,000 NOT ALLOWED ", font=("Bookman Old Style",30,"bold"),bg='navy', fg='red')
                        self.permit_withdrawn_label.place(relx=.36,rely=.48)
                        self.redirect=Button(self,cursor="hand2",bg="red4",fg="ivory",text="Ok",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=lambda:self.__mainwindow(cardNumber),bd=0)
                        self.redirect.place(relx=0.6, rely=0.65)

                else:
                    self.permit_withdrawn_label=Label(self, text="  Amount Should be More Than ₹100 ", font=("Bookman Old Style",30,"bold"),bg='navy', fg='red')
                    self.permit_withdrawn_label.place(relx=.4,rely=.48)
                    self.redirect=Button(self,cursor="hand2",bg="red4",fg="ivory",text="Ok",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=lambda:self.__mainwindow(cardNumber),bd=0)
                    self.redirect.place(relx=0.6, rely=0.65)


            delete_all()
            info(cardNumber)
            self.withdrawn_labe=Label(self, text="Enter The Amount You Want To Withdraw", font=("Cascadia Code",27,"bold"),bg='navy', fg='white')
            self.withdrawn_labe.place(relx=.42,rely=.33)
            
            self.permit_withdrawn_label=Label(self, text="  Must Be ₹100,₹500 or ₹2000 \n And Should Be Less than ₹40,000", font=("Cascadia Code",20,"bold"),bg='navy', fg='red')
            self.permit_withdrawn_label.place(relx=.52,rely=.4)

            self.withdrwal_amount=Entry(self, width=15,fg="yellow",bg="purple4",font=('Bookman Old Style',50),justify="center",relief="flat",highlightthickness=5,validate="key",validatecommand=(self.validation, '%S'))
            self.withdrwal_amount.place(relx=0.46, rely=0.50)
            self.withdrwal_amount.focus_set()
            #self.withdrwal_amount.insert(0,100)

            #rest btn----------------
            self.reset=Button(self,cursor="hand2",bg="red4",fg="ivory",text="Reset",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=exit,bd=0)
            self.reset.place(relx=0.55, rely=0.65)

            #proceed btn----------------
            self.proceed=Button(self,cursor="hand2",bg="green4",fg="ivory",text="Proceed",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=lambda:withdrawl_process(cardNumber,self.withdrwal_amount.get()),bd=0)
            self.proceed.place(relx=0.70, rely=0.65)
            self.bind("<Return>",lambda event :withdrawl_process(cardNumber,self.withdrwal_amount.get()))

        def upi(cardNumber):
            def upi_transferre(cardNumber,id,amount):
                delete_all()
                info(cardNumber)
                print(cardNumber,id,amount)
                
                pass
            delete_all()
            info(cardNumber)
            self.upi_labe=Label(self, text="Enter The UPI ID", font=("Cascadia Code",35,"bold"),bg='navy', fg='white')
            self.upi_labe.place(relx=.53,rely=.25)

            self.upi_id=Entry(self, width=18,fg="yellow",bg="purple4",font=('Bookman Old Style',50),justify="center",relief="flat",highlightthickness=5,)
            self.upi_id.place(relx=0.43, rely=0.36)
            self.upi_id.focus_set()
            self.upi_id.insert(0,'bishalde@paytm')

            self.withdrawn_labe=Label(self, text="Enter The Amount You Want To Transfer", font=("Cascadia Code",27,"bold"),bg='navy', fg='white')
            self.withdrawn_labe.place(relx=.43,rely=.52)
            

            self.withdrwal_amount=Entry(self, width=18,fg="yellow",bg="purple4",font=('Bookman Old Style',50),justify="center",relief="flat",highlightthickness=5,validate="key",validatecommand=(self.validation, '%S'))
            self.withdrwal_amount.place(relx=0.43, rely=0.595)
            #self.withdrwal_amount.insert(0,100)


            #rest btn----------------
            self.reset=Button(self,cursor="hand2",bg="red4",fg="ivory",text="Reset",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=exit,bd=0)
            self.reset.place(relx=0.55, rely=0.75)

            #proceed btn----------------
            self.proceed=Button(self,cursor="hand2",bg="green4",fg="ivory",text="Proceed",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=lambda:upi_transferre(cardNumber,self.upi_id.get(),float(self.withdrwal_amount.get())),bd=0)
            self.proceed.place(relx=0.70, rely=0.75)
            self.bind("<Return>",lambda event :upi_transferre(cardNumber,self.upi_id.get(),float(self.withdrwal_amount.get())))


        def info(cardNumber):
            sql = "SELECT * FROM card_informations WHERE card_number='{}';".format(cardNumber)
            mycursor.execute(sql)
            result = mycursor.fetchone()
            account_number=result[1]

            sql="SELECT * FROM `atm_accountdetails` WHERE `account_number` = 1;"
            result = mycursor.fetchone()
            print(result)


            self.ATM_label=Label(self, text="ATM", font=("Impact",50),bg='navy', fg='white')
            self.ATM_label.place(relx=.05,rely=.05)

            self.welcome_label=Label(self, text="Welcome", font=("Cascadia Code",25),bg='navy', fg='white')
            self.welcome_label.place(relx=.05,rely=.3)

            self.name_label=Label(self, text=result[1], font=("Consolas",30,"bold"),bg='navy', fg='yellow')
            self.name_label.place(relx=.05,rely=.35)

            self.card_label=Label(self, text="Card Number", font=("Cascadia Code",25),bg='navy', fg='white')
            self.card_label.place(relx=.05,rely=.42)

            card=str(result[0])
            self.card_labell=Label(self, text="{}-{}-{}".format(card[:4],card[4:8],card[8:]), font=("Consolas",25,"bold"),bg='navy', fg='yellow')
            self.card_labell.place(relx=.05,rely=.47)

            self.currentaccount_label=Label(self, text="Current Account #1", font=("Cascadia Code",25),bg='navy', fg='white')
            self.currentaccount_label.place(relx=.05,rely=.53)
            
            self.currentbalance_label=Label(self, text="₹ {0:.2f}".format(00.00), font=("OCR A Extended",27,"bold"),bg='navy', fg='yellow')
            self.currentbalance_label.place(relx=.05,rely=.58)

            self.savingsaccount_label=Label(self, text="Savings Account #2", font=("Cascadia Code",25),bg='navy', fg='white')
            self.savingsaccount_label.place(relx=.05,rely=.64)
            
            self.savingsaccountbalance_label=Label(self, text="₹ {0:.2f}".format(float(result[4])), font=("OCR A Extended",27,"bold"),bg='navy', fg='yellow')
            self.savingsaccountbalance_label.place(relx=.05,rely=.69)


        delete_all()
        info(cardNumber)

        self.withdraw_btn= Button(self,text="Get Cash",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=25,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,command=lambda:withdraw(cardNumber),cursor="hand2")
        self.withdraw_btn.place(relx=.43,rely=.25)

        self.deposit_btn= Button(self,text="Deposit",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=25,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,state=  DISABLED)
        self.deposit_btn.place(relx=.7,rely=.25)

        
        self.paymentsummary_btn= Button(self,text="Mini Statement",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=25,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,state=DISABLED)
        self.paymentsummary_btn.place(relx=.43,rely=.40)

        self.cards_btn= Button(self,text="Cards",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=25,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,state=  DISABLED)
        self.cards_btn.place(relx=.7,rely=.40)

        self.pinchange_btn= Button(self,text="PIN Change",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=25,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,state= DISABLED)
        self.pinchange_btn.place(relx=.43,rely=.55)

        self.account_btn= Button(self,text="Account Transfer",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=25,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,state=   DISABLED)
        self.account_btn.place(relx=.7,rely=.55)

        self.UPI_btn= Button(self,text="UPI Transfer",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=25,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,command=lambda: upi(cardNumber),cursor="hand2")
        self.UPI_btn.place(relx=.43,rely=.70)

        self.others_btn= Button(self,text="Others",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=25,fg="white",bd=0,bg="maroon4",relief=FLAT,state=   DISABLED)
        self.others_btn.place(relx=.7,rely=.70)

        self.quickcash_btn= Button(self,text="       ₹ 1000                                                        Quick Cash >>>",font=("Segoe UI Variable Text Light",20,"bold"),height=1,width=53,fg="white",bd=0,bg="red",relief=FLAT,anchor=W,state=DISABLED)
        self.quickcash_btn.place(relx=.43,rely=.85)

    def __verify(self,cardNumber,pinNumber):
        mycursor=mydb.cursor()
        sql = "SELECT * FROM card_informations WHERE card_number='{}' && pin_number='{}';".format(cardNumber, pinNumber)
        mycursor.execute(sql)
        result = mycursor.fetchone()
        if result != None :
            self.inser_pin_label.destroy()
            self.pinNumber.destroy()
            self.reset.destroy()
            self.proceed.destroy()
            self.try_label.destroy()
            self.alert_label.destroy()
            self.__mainwindow(cardNumber)

        else:
            if self.tried==0:
                self.proceed["state"] = DISABLED
                self.reset["state"] = DISABLED
            else:
                self.tried-=1
                self.alert_label.configure(text="Wrong PIN Number")
                self.try_label.configure(text="Try Left : {}".format(self.tried))
                self.pinNumber.delete(0, END)

    def __pindetails(self,cardNumber):
        self.tried=3
        def deletee():
            self.pinNumber.delete(0, END)

        self.inser_card_label.destroy()
        self.cardNumber.destroy()
        self.reset.destroy()
        self.proceed.destroy()
        

        #Alert-------------
        self.alert_label=Label(self, text="", font=("Arial Black",50,"bold"),bg='navy', fg='red')
        self.alert_label.place(relx=.3,rely=.05)

        #Tried Alert-------------
        self.try_label=Label(self, text="", font=("Arial Black",30,"bold"),bg='navy', fg='yellow')
        self.try_label.place(relx=.43,rely=.17)

        #Pin Label----------------
        self.inser_pin_label=Label(self, text="Enter PIN", font=("Cascadia Code",60,"bold"),bg='navy', fg='white')
        self.inser_pin_label.place(relx=.36,rely=.30)

        #pin number entry---------
        self.pinNumber=Entry(self, width=10,fg="yellow",bg="purple4",font=('Bookman Old Style',50),justify="center",relief="flat",highlightthickness=5,validate="key",validatecommand=(self.validation, '%S'),show="*")
        self.pinNumber.place(relx=0.36, rely=0.45)
        self.pinNumber.focus_set()
        self.pinNumber.insert(0,5741)

        #rest btn----------------
        self.reset=Button(self,cursor="hand2",bg="red4",fg="ivory",text="Reset",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=deletee,bd=0)
        self.reset.place(relx=0.38, rely=0.6)

        #proceed btn----------------
        self.proceed=Button(self,cursor="hand2",bg="green4",fg="ivory",text="Proceed",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=lambda:self.__verify(cardNumber,self.pinNumber.get()),bd=0)
        self.proceed.place(relx=0.52, rely=0.6)

        self.bind("<Return>",lambda event:self.__verify(cardNumber,self.pinNumber.get()))

    def __cardNumber(self):
        def deletee():
            self.cardNumber.delete(0, END)

        def only_numbers(char):
            return char.isdigit()
        self.validation = root.register(only_numbers)

        self.wait_label.destroy()
        self.card_inserted_label.destroy()
        self.lf.destroy()
        self.l.destroy()
        
        #Card Label----------------
        self.inser_card_label=Label(self, text="Enter Card Number", font=("Cascadia Code",60,"bold"),bg='navy', fg='white')
        self.inser_card_label.place(relx=.27,rely=.30)

        #card number entry---------
        self.cardNumber=Entry(self, width=20,fg="yellow",bg="purple4",font=('Bookman Old Style',50),justify="center",relief="flat",highlightthickness=5,validate="key",validatecommand=(self.validation, '%S'))
        self.cardNumber.place(relx=0.25, rely=0.45)
        self.cardNumber.focus_set()
        self.cardNumber.insert(0,100000000001)

        #rest btn----------------
        self.reset=Button(self,cursor="hand2",bg="red4",fg="ivory",text="Reset",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=deletee,bd=0)
        self.reset.place(relx=0.4, rely=0.6)

        #proceed btn----------------
        self.proceed=Button(self,cursor="hand2",bg="green4",fg="ivory",text="Proceed",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=lambda:self.__pindetails(self.cardNumber.get()),bd=0)
        self.proceed.place(relx=0.55, rely=0.6)

        self.bind("<Return>",lambda event:self.__pindetails(self.cardNumber.get()))
        
    def __next1(self):
        self.width=self.width+400
        self.lf.config(width=self.width)

        self.after(100,self.__cardNumber)

    def __stepTwo(self):
        self.v.destroy()
        self.inser_card_label.destroy()
        self.welcome_label.destroy()
        
        
        #label-----
        self.card_inserted_label=Label(self,text="Card Inserted Successfully",font=("Cascadia Code",50,"bold"),bg='navy', fg='white')
        self.card_inserted_label.place(relx=.17,rely=.25)

        #label-----
        #Welcome Laber----------------
        self.wait_label=Label(self, text="Please Wait...", font=("Bahnschrift SemiBold",45,"bold"),bg='navy', fg='yellow')
        self.wait_label.place(relx=.37,rely=.4)

        self.l=Frame(self,height=40,width=605,bg="white")
        self.l.place(relx=.30,rely=.60)

        self.width=200
        self.lf=Frame(self,height=35,width=self.width,bg="red")
        self.lf.place(relx=.3005,rely=.6015)

        self.after(100,self.__next1)

    def __startwindow(self):
        global mycursor,mydb
        
        widget_list = self.__all_children()
        for item in widget_list:
            item.destroy()

        #Insert_card_image--------------------------------
        self.Cimage = PhotoImage(file='Resources/Presentation1.png')
        self.v=Label(self, image=self.Cimage, bd=0)
        self.v.place(relx=.10,rely=.25)

        #Welcome Laber----------------
        self.welcome_label=Label(self, text="Welcome", font=("Arial Black",80,"bold"),bg='navy', fg='yellow')
        self.welcome_label.place(relx=.33,rely=.1)

        #Label Insert Card--------------------------------
        self.inser_card_label=Label(self, text="Please Insert Your Card .....", font=("Cascadia Code",40,"bold"),bg='navy', fg='white')
        self.inser_card_label.place(relx=.23,rely=.30)

        #cancel btn----------------
        self.reset=Button(self,cursor="hand2",bg="red4",fg="ivory",text="EXIT",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=self.__startwindow,bd=0)
        self.reset.place(relx=.89, rely=0.015)

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="bishalde",
                password="bishalde",
                database="ATM_Database"
                )
            mycursor=mydb.cursor()
            self.after(timedelay,self.__stepTwo())
            # self.after(timedelay,self.__mainwindow(100000000001))

        except Exception as e:
            print(e)
            messagebox.showinfo("Servel Low",e)
            self.__startwindow()

    def __init__(self):
        super().__init__()
        self.title('ATM GUI')
        self.attributes('-fullscreen', True)
        self["bg"]="navy"

        self.__startwindow()



if __name__=='__main__':
    root=AtmMachine()
    root.mainloop()
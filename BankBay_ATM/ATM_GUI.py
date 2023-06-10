#Required Modules ---------------------------------
from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from time import *
from datetime import *

import pymongo
myclient,mydb=None,None


"""
Class For ATM Machine
"""
timedelay=100

class AtmMachine(Tk):

    """Function To Delete All The elements From Window"""
    def __all_children(self) :
            _list = self.winfo_children()

            for item in _list :
                if item.winfo_children() :
                    _list.extend(item.winfo_children())
            return _list

    def __mainwindow(self,cardNumber):
        
        def ministatement(accountNumber,toAcccountNumber,reason,balance,amount):
            if(reason==None):
                data={"accountNumber":accountNumber,
                    "toAccountNumber":None,
                    "reason":"ATM Withdrawl",
                    "dateOfTransfer":datetime.now(),
                    "balance":balance,
                    "currentBalance":balance-amount
                }
            else:
                data={"accountNumber":accountNumber,
                    "toAccountNumber":toAcccountNumber,
                    "reason":reason,
                    "dateOfTransfer":datetime.now(),
                    "balance":balance,
                    "currentBalance":balance-amount
                }
            
            mycol=mydb["BankBay_miniStatement"]
            mycol.insert_one(data)

        """To delete the widgets while changing screen"""
        def delete_all():
            widget_list = self.__all_children()
            for item in widget_list:
                item.destroy()
            #cancel btn----------------
            self.reset=Button(self,cursor="hand2",bg="red4",fg="ivory",text="EXIT",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=self.__startwindow,bd=0)
            self.reset.place(relx=.89, rely=0.015)

        """To get entry as number only"""
        def only_numbers(char):
            return char.isdigit()
        self.validation = self.register(only_numbers)             

        def info(cardNumber):
            cardNumber=int(cardNumber)

            mycol=mydb["BankBay_cardInformations"]
            query={"cardNumber":cardNumber}
            result1=mycol.find_one(query)

            mycol=mydb["BankBay_personalDetails"]
            query={"accountNumber":result1["accountNumber"]}
            result2 = mycol.find_one(query)

            self.ATM_label=Label(self, text="BankBay", font=("Impact",50),bg='navy', fg='white')
            self.ATM_label.place(relx=.05,rely=.05)

            self.welcome_label=Label(self, text="Welcome", font=("Cascadia Code",25),bg='navy', fg='white')
            self.welcome_label.place(relx=.05,rely=.3)

            self.name_label=Label(self, text=result2['userName'], font=("Consolas",30,"bold"),bg='navy', fg='yellow')
            self.name_label.place(relx=.05,rely=.35)

            self.card_label=Label(self, text="Card Number", font=("Cascadia Code",25),bg='navy', fg='white')
            self.card_label.place(relx=.05,rely=.42)
            card=str(result1['cardNumber'])
            self.card_labell=Label(self, text="{}-{}-{}".format(card[:4],card[4:8],card[8:]), font=("Consolas",25,"bold"),bg='navy', fg='yellow')
            self.card_labell.place(relx=.05,rely=.47)

            self.currentaccount_label=Label(self, text="Current Account #1", font=("Cascadia Code",25),bg='navy', fg='white')
            self.currentaccount_label.place(relx=.05,rely=.53)
            
            self.currentbalance_label=Label(self, text="₹ {0:.2f}".format(00.00), font=("OCR A Extended",27,"bold"),bg='navy', fg='yellow')
            self.currentbalance_label.place(relx=.05,rely=.58)

            self.savingsaccount_label=Label(self, text="Savings Account #2", font=("Cascadia Code",25),bg='navy', fg='white')
            self.savingsaccount_label.place(relx=.05,rely=.64)
            
            mycol=mydb["BankBay_accountDetails"]
            query={"accountNumber":result1["accountNumber"]}
            result1 = mycol.find_one(query)

            bal=float(str(result1["balance"]))
            self.savingsaccountbalance_label=Label(self, text="₹ {0:.2f}".format(bal), font=("OCR A Extended",27,"bold"),bg='navy', fg='yellow')
            self.savingsaccountbalance_label.place(relx=.05,rely=.69)

        def withdraw(cardNumber):

            def withdrawl_process(cardNumber,amount):
                cardNumber=int(cardNumber)
                delete_all()
                amount=float(amount)
                info(cardNumber)

                mycol=mydb["BankBay_cardInformations"]
                query={"cardNumber":cardNumber}
                result = mycol.find_one(query)

                mycol=mydb["BankBay_accountDetails"]
                query={"accountNumber":int(result["accountNumber"])}
                result1 = mycol.find_one(query)
                balance=float(str(result1["balance"]))
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
                                    mycol=mydb["BankBay_accountDetails"]
                                    query={"accountNumber":result["accountNumber"]}
                                    updatequery={"$set":{"balance":balance-amount}}
                                    mycol.update_one(query,updatequery)

                                    reason=None
                                    ministatement(result["accountNumber"],None,reason,balance,amount)
                                    messagebox.showinfo("Transaction Success","Your Withdrawl Process Was Successfully Completed")
                                    self.__mainwindow(cardNumber)
                                
                                except Exception as e:
                                    messagebox.showerror("Transaction Failed","Your Withdrawl Process FAILED..!")
                                    print(e)
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
            def upi_transferre(cardNumber,idd,amount):
                cardNumber=int(cardNumber)
                upiId=idd
                amount=float(amount)

                delete_all()
                info(cardNumber)

                mycol=mydb["BankBay_cardInformations"]
                data=mycol.find_one({
                        "$or":[ 
                                {"UPIId1":upiId} , 
                                {"UPIID2":upiId} 
                               ]     
                    })
                if data!=None:
                    recvAccountNumber=data["accountNumber"]

                    senderQuery=mycol.find_one({"cardNumber":cardNumber})
                    senderAccountNumber=senderQuery["accountNumber"]

                    mycol = mydb["BankBay_accountDetails"]
                    balaquery=mycol.find_one({"accountNumber": int(senderAccountNumber)})
                    balance=balaquery["balance"]

                    mycol.update_one({"accountNumber": senderAccountNumber}, {"$inc": {"balance": -amount}})
                    mycol.update_one({"accountNumber": recvAccountNumber}, {"$inc": {"balance": amount}})

                    ministatement(senderAccountNumber,recvAccountNumber,"UPI Transaction",balance,amount)

                    messagebox.showinfo("Transcation Successful","Done")
                    self.__mainwindow(cardNumber)

                else:
                    messagebox.showerror("Transaction Failed","No Such UPI ID Found..!")
                    self.__mainwindow(cardNumber)


            delete_all()
            info(cardNumber)
            self.upi_labe=Label(self, text="Enter The UPI ID", font=("Cascadia Code",35,"bold"),bg='navy', fg='white')
            self.upi_labe.place(relx=.53,rely=.25)

            self.upi_id=Entry(self, width=18,fg="yellow",bg="purple4",font=('Bookman Old Style',50),justify="center",relief="flat",highlightthickness=5,)
            self.upi_id.place(relx=0.43, rely=0.36)
            self.upi_id.focus_set()
            self.upi_id.insert(0,'keshavi@bankbay')

            self.withdrawn_labe=Label(self, text="Enter The Amount You Want To Transfer", font=("Cascadia Code",27,"bold"),bg='navy', fg='white')
            self.withdrawn_labe.place(relx=.43,rely=.52)
            

            self.withdrwal_amount=Entry(self, width=18,fg="yellow",bg="purple4",font=('Bookman Old Style',50),justify="center",relief="flat",highlightthickness=5,validate="key",validatecommand=(self.validation, '%S'))
            self.withdrwal_amount.place(relx=0.43, rely=0.595)
            self.withdrwal_amount.insert(0,1000)

            #rest btn----------------
            self.reset=Button(self,cursor="hand2",bg="red4",fg="ivory",text="Reset",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=exit,bd=0)
            self.reset.place(relx=0.55, rely=0.75)

            #proceed btn----------------
            self.proceed=Button(self,cursor="hand2",bg="green4",fg="ivory",text="Proceed",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=lambda:upi_transferre(cardNumber,self.upi_id.get(),float(self.withdrwal_amount.get())),bd=0)
            self.proceed.place(relx=0.70, rely=0.75)
            self.bind("<Return>",lambda event :upi_transferre(cardNumber,self.upi_id.get(),float(self.withdrwal_amount.get())))


        def processMiniStatement(cardNumber):
            cardNumber=int(cardNumber)
            delete_all()
            info(cardNumber)

            self.transactionintro_label=Label(self, text="Last 10 Transactions Statement : ", font=("Cascadia Code",28,"bold"),bg='navy', fg='white')
            self.transactionintro_label.place(relx=.35,rely=.15)

            self.transId=Label(self, text="Transaction ID", font=("Cascadia Code",20,"bold"),bg='navy', fg='white')
            self.transId.place(relx=.25,rely=.25)

            self.toAccount=Label(self, text="To Account", font=("Cascadia Code",20,"bold"),bg='navy', fg='white')
            self.toAccount.place(relx=.40,rely=.25)

            self.reason=Label(self, text="Reason", font=("Cascadia Code",20,"bold"),bg='navy', fg='white')
            self.reason.place(relx=.53,rely=.25)

            self.dateOfTransaction=Label(self, text="Date", font=("Cascadia Code",20,"bold"),bg='navy', fg='white')
            self.dateOfTransaction.place(relx=.65,rely=.25)

            self.balance=Label(self, text="Balance", font=("Cascadia Code",20,"bold"),bg='navy', fg='white')
            self.balance.place(relx=.75,rely=.25)

            self.currentbalance=Label(self, text="Current Balance  ", font=("Cascadia Code",20,"bold"),bg='navy', fg='white')
            self.currentbalance.place(relx=.85,rely=.25)

            self.backbtn=Button(self, text=" << Back " , font=("Cascadia Code",17,"bold"),bg='green', fg='white',cursor='hand2',command=lambda : self.__mainwindow(cardNumber))
            self.backbtn.place(relx=.9,rely=.9)


            mycol=mydb["BankBay_cardInformations"]
            query={"cardNumber":cardNumber}
            result=mycol.find_one(query)

            mycol = mydb["BankBay_miniStatement"]
            query = { "accountNumber": result["accountNumber"] }
            mydoc = mycol.find(query).sort("dateOfTransfer",-1).limit(10)

            inc=0
            for row in mydoc:
                self.dataId=Label(self,text=row["_id"],font=("Cascadia Code",11,"bold"),bg='navy', fg='orange')
                self.dataId.place(relx=.25,rely=.35+inc)

                self.dataToAccount=Label(self,text=row["toAccountNumber"],font=("Cascadia Code",11,"bold"),bg='navy', fg='orange')
                self.dataToAccount.place(relx=.40,rely=.35+inc)

                self.dataReason=Label(self,text=row["reason"],font=("Cascadia Code",11,"bold"),bg='navy', fg='orange')
                self.dataReason.place(relx=.53,rely=.35+inc)

                self.dataDateOfTransaction=Label(self,text=row["dateOfTransfer"],font=("Cascadia Code",8,"bold"),bg='navy', fg='orange')
                self.dataDateOfTransaction.place(relx=.63,rely=.35+inc)

                self.dataBalance=Label(self,text="₹"+str(row["balance"]),font=("Cascadia Code",11,"bold"),bg='navy', fg='orange')
                self.dataBalance.place(relx=.77,rely=.35+inc)

                self.dataCurrentBalance=Label(self,text="₹"+str(row["currentBalance"]),font=("Cascadia Code",11,"bold"),bg='navy', fg='orange')
                self.dataCurrentBalance.place(relx=.87,rely=.35+inc)
                inc+=.05




        delete_all()
        info(cardNumber)


        self.withdraw_btn= Button(self,text="Get Cash",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=23,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,command=lambda:withdraw(cardNumber),cursor="hand2")
        self.withdraw_btn.place(relx=.43,rely=.25)

        self.deposit_btn= Button(self,text="Deposit",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=23,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,state=  DISABLED)
        self.deposit_btn.place(relx=.7,rely=.25)

        
        self.paymentsummary_btn= Button(self,text="Mini Statement",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=23,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,command=lambda:processMiniStatement(cardNumber),cursor="hand2")
        self.paymentsummary_btn.place(relx=.43,rely=.40)

        self.cards_btn= Button(self,text="Cards",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=23,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,state=  DISABLED)
        self.cards_btn.place(relx=.7,rely=.40)

        self.pinchange_btn= Button(self,text="PIN Change",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=23,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,state= DISABLED)
        self.pinchange_btn.place(relx=.43,rely=.55)

        self.account_btn= Button(self,text="Account Transfer",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=23,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,state=   DISABLED)
        self.account_btn.place(relx=.7,rely=.55)

        self.UPI_btn= Button(self,text="UPI Transfer",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=23,fg="white",bd=0,bg="SlateBlue2",relief=FLAT,command=lambda: upi(cardNumber),cursor="hand2")
        self.UPI_btn.place(relx=.43,rely=.70)

        self.others_btn= Button(self,text="Others",font=("Segoe UI Variable Text Light",20,"bold"),height=2,width=23,fg="white",bd=0,bg="maroon4",relief=FLAT,state= DISABLED)
        self.others_btn.place(relx=.7,rely=.70)

        self.quickcash_btn= Button(self,text="       ₹ 1000                                                        Quick Cash >>>",font=("Segoe UI Variable Text Light",20,"bold"),height=1,width=47,fg="white",bd=0,bg="red",relief=FLAT,anchor=W,state=DISABLED)
        self.quickcash_btn.place(relx=.43,rely=.85)




    """Function to verify PIN and Card"""
    def __verify(self,cardNumber,pinNumber):
        mycol=mydb["BankBay_cardInformations"]
        myquery = { "cardNumber": int(cardNumber), "pinNumber": int(pinNumber)}
        result=mycol.find_one(myquery)
        if result != None :
            #Delete all the widgets form the screen....
            widget_list = self.__all_children()
            for item in widget_list:
                item.destroy()
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


    """Function for PIN entry"""
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
   
    """Function for reading the cardnumber"""
    def __cardNumber(self):
        #for reset the field
        def deletee():
            self.cardNumber.delete(0, END)

        #to allow entry for numbers only
        def only_numbers(char):
            return char.isdigit()
        self.validation = root.register(only_numbers)

        #Delete all the widgets form the screen....
        widget_list = self.__all_children()
        for item in widget_list:
            item.destroy()
        
        #Exit btn----------------
        self.exit=Button(self,cursor="hand2",bg="red4",fg="ivory",text="EXIT",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=self.__startwindow,bd=0)
        self.exit.place(relx=.89, rely=0.015)

        #Insert Card Label----------------
        self.inser_card_label=Label(self, text="Enter Card Number", font=("Cascadia Code",60,"bold"),bg='navy', fg='white')
        self.inser_card_label.place(relx=.27,rely=.30)

        #card number entry---------
        self.cardNumber=Entry(self, width=20,fg="yellow",bg="purple4",font=('Bookman Old Style',50),justify="center",relief="flat",highlightthickness=5,validate="key",validatecommand=(self.validation, '%S'))
        self.cardNumber.place(relx=0.25, rely=0.45)
        self.cardNumber.focus_set()
        self.cardNumber.insert(0,'100000000001')

        #rest btn----------------
        self.reset=Button(self,cursor="hand2",bg="red4",fg="ivory",text="Reset",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=deletee,bd=0)
        self.reset.place(relx=0.4, rely=0.6)

        #proceed btn----------------
        self.proceed=Button(self,cursor="hand2",bg="green4",fg="ivory",text="Proceed",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=lambda:self.__pindetails(self.cardNumber.get()),bd=0)
        self.proceed.place(relx=0.55, rely=0.6)

        #binds the enter key to next operation
        self.bind("<Return>",lambda event:self.__pindetails(self.cardNumber.get()))


    """Function for increasing the width of the progressbar"""
    def __next1(self):
        #increase the width of the progressbar
        self.width=self.width+400
        self.lf.config(width=self.width)

        #calling the next function
        self.after(500,self.__cardNumber)
    
    """Function for progressbar"""
    def __stepTwo(self):
        #Delete all the widgets form the screen....
        widget_list = self.__all_children()
        for item in widget_list:
            item.destroy()

        #Exit btn----------------
        self.exit=Button(self,cursor="hand2",bg="red4",fg="ivory",text="EXIT",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=self.__startwindow,bd=0)
        self.exit.place(relx=.89, rely=0.015)

        #Card Inserted label-----
        self.card_inserted_label=Label(self,text="Card Inserted Successfully",font=("Cascadia Code",50,"bold"),bg='navy', fg='white')
        self.card_inserted_label.place(relx=.17,rely=.25)

        #Please Wait Label----------------
        self.wait_label=Label(self, text="Please Wait...", font=("Bahnschrift SemiBold",45,"bold"),bg='navy', fg='yellow')
        self.wait_label.place(relx=.37,rely=.4)

        #progressbar background---------
        self.l=Frame(self,height=40,width=605,bg="white")
        self.l.place(relx=.30,rely=.60)
        self.width=200
        self.lf=Frame(self,height=35,width=self.width,bg="red")
        self.lf.place(relx=.3005,rely=.6015)

        #calling the next function
        self.after(1000,self.__next1)

    """Function for Card Insertion Process"""
    def __startwindow(self):
        global myclient,mydb
        #Destroys every widget from the screen......
        widget_list = self.__all_children()
        for item in widget_list:
            item.destroy()

        #Insert_card_image--------------------------------
        self.Cimage = PhotoImage(file='Resources/Presentation1.png')
        self.v=Label(self, image=self.Cimage, bd=0)
        self.v.place(relx=.10,rely=.25)

        #Welcome Label----------------
        self.welcome_label=Label(self, text="Welcome", font=("Arial Black",80,"bold"),bg='navy', fg='yellow')
        self.welcome_label.place(relx=.33,rely=.1)

        #Label Insert Card--------------------------------
        self.inser_card_label=Label(self, text="Please Insert Your Card .....", font=("Cascadia Code",40,"bold"),bg='navy', fg='white')
        self.inser_card_label.place(relx=.23,rely=.30)

        #Exit btn----------------
        self.exit=Button(self,cursor="hand2",bg="red4",fg="ivory",text="EXIT",font=("Bahnschrift SemiBold",20,"bold"),height=1,width=10,command=self.__startwindow,bd=0)
        self.exit.place(relx=.89, rely=0.015)

        #Establishing Connection to the server...
        try:
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient["BankBay"]

            #class the next function .....
            self.after(timedelay,self.__stepTwo)

        except Exception as e:
            messagebox.showinfo("Servel Low","Unable To Connect To the server")
            self.__startwindow()

    """Default Constructor"""
    def __init__(self):
        super().__init__()
        self.title('ATM GUI')
        #For FullScreen Mode
        self.attributes('-fullscreen', True)
        #Background Color
        self["bg"]="navy"

        ##Calling The next function
        self.__startwindow()


"""Execution of the Code Starts From Here...."""
if __name__=='__main__':
    #Object Of AtmMachine Class
    root=AtmMachine()
    root.mainloop()












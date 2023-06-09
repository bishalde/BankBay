DROP DATABASE IF EXISTS atm_database;
CREATE DATABASE IF NOT EXISTS atm_database;
USE atm_database;


/*CardInformation table---------------------*/
CREATE TABLE IF NOT EXISTS card_informations(
    card_number BIGINT(12) AUTO_INCREMENT,
    account_number BIGINT(12) NOT NULL, 
    pin_number INT(4) NOT NULL,
    upiID_1 varchar(30) NOT NULL,
    upiID_2 varchar(30) NOT NULL,
    dateOfCreation date NOT NULL,
    PRIMARY KEY (card_number)
);

/*GLOBAL   GLOBAL  TransactionHistory Table--------------------*/
CREATE TABLE IF NOT EXISTS atm_GLOBALtransactionDetails(
    transactionID BIGINT NOT NULL,
    account_number BIGINT(12) NOT NULL,
    to_account_number BIGINT(12) NOT NULL,
    balance INT NOT NULL,
    dateoftransfer DATETIME NOT NULL,
    via varchar(50) NOT NULL,
    PRIMARY KEY(transactionID)
);

/*ministatement History--------------------------*/
CREATE TABLE IF NOT EXISTS atm_ministatement(
    transactionID BIGINT NOT NULL,
    account_number BIGINT(12) NOT NULL,
    to_account_number BIGINT(12) NOT NULL,
    dateoftransfer DATETIME NOT NULL,
    balance INT NOT NULL,
    via varchar(50) NOT NULL,
    PRIMARY KEY(transactionID)
); 

/*Account details-------------------------------------*/
CREATE TABLE atm_accountdetails (
    account_number BIGINT(12) NOT NULL PRIMARY KEY,
    User_name VARCHAR(50) NOT NULL,
    dateOfCreation DATE DEFAULT CURRENT_DATE(),
    loan BIGINT NOT NULL,
    balance BIGINT NOT NULL
);

/*Personal details-------------------------------*/
CREATE TABLE IF NOT EXISTS atm_personaldetails(
    account_number BIGINT NOT NULL AUTO_INCREMENT, 
    user_name VARCHAR(50) NOT NULL,
    user_dob DATE NOT NULL,
    user_email VARCHAR(100) NOT NULL,
    user_mobile VARCHAR(100) NOT NULL,
    street VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    sstate VARCHAR(50) NOT NULL,
    zip INT(10) NOT NULL,
    user_id varchar(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    PRIMARY KEY(account_number),
    FOREIGN KEY(account_number) REFERENCES atm_accountdetails(account_number)
);

#!/usr/bin/python3
import warnings
import time
import io
import os
import configparser
import mysql.connector
from mysql.connector import errorcode


def Select(stmnt):
    """ Executes prepared select staement """
    config = configparser.ConfigParser()
    config.read('config.ini')
    mysqld = config['mysql']
    cnx = mysql.connector.connect(
        user=mysqld['user'],
        password=mysqld['passwd'],
        host=mysqld['host'],
        database=mysqld['db']
    )
    cursor = cnx.cursor()
    cursor.execute(stmnt)
    result = cursor.fetchall()
    return result


def Insert(stmnt):
    """Inserts premade statement into table"""
    try:
        config = configparser.ConfigParser()
        config.read('/var/www/scripts/config.ini')
        mysqld = config['mysql']
        cnx = mysql.connector.connect(
            user=mysqld['user'],
            password=mysqld['passwd'],
            host=mysqld['host'],
            database=mysqld['db']
        )
        cursor = cnx.cursor()
        cursor.execute(stmnt)
        cnx.commit()
        cursor.close()
        cnx.close()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        cnx.close()

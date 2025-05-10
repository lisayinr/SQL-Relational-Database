# Overview

This is an inventory management system designed to manage and interact with a bookstore's product data using SQL relational database. This software uses Python to interact with a MySQL relational database of a hypothetical bookstore's inventory. The program allows a user to navigate through its features using a menu with options to view, search, summarize, insert, delete, and modify book inventory. 

The purpose of this software is to demonstrate how to build a database with user functionality using SQL relational database and Python. 

Video Demonstration of how my software works: [Software Demo Video](https://youtu.be/aUcfEwuB3NI)

# Relational Database

This program uses a MySQL relational database called bookstore_inventory. It contains two tables called category and product. The category table contains different generes of books (e.g., Mystery, Fantasy, Romance). The product table contains the information for indiviual books including name, quantity, price, and the book's category for genre. The structure of the database contains a one-to-many relationship between the two tables where one category can have many books, but each book can only have one category.

# Development Environment

* Visual Studio Code
* MySQL
* Python 3.12.1
* Git / Github
* mysql-connector-python
* python-dotenv

# Useful Websites

- [MySQL.com](https://dev.mysql.com/doc/refman/8.4/en/create-table-foreign-keys.html)
- [MySQL.com](https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html)
- [MySQL.com](https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html)
- [MySQL.com](https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html)
- [MySQL.com](https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html)
- [Programiz.com](https://www.programiz.com/sql/create-table)
- [Geeksforgeeks.org](https://www.geeksforgeeks.org/sql-create-table/)
- [Geeksforgeeks.com](https://www.geeksforgeeks.org/how-to-connect-python-with-sql-database/)
- [W3schools.com](https://www.w3schools.com/sql/sql_foreignkey.asp)
- [Youtube.com](https://www.youtube.com/watch?v=yxGzg0t_sQw)
- [Ioflood.com](https://ioflood.com/blog/python-dotenv-guide-how-to-use-environment-variables-in-python/)
- [Zignuts.com](https://www.zignuts.com/blog/connect-python-to-mysql-database)
- [Medium.com](https://medium.com/@dinuka.caldera/python-script-for-searching-any-record-in-mysql-databases-5298563b069e)

# Future Work

- Add user authentication
- Add the ability to import or expert data
- Create a web-based front end to use the program
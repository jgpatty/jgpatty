import sqlite3
import random
from unittest.mock import patch
import getpass
import os

conn = sqlite3.connect('data.db')
c = conn.cursor()
cursor = conn.cursor()

def get_total_tickets(cursor):
  cursor.execute("SELECT SUM(tickets) FROM sales")
  return cursor.fetchone()[0]

def pick_random_winner(cursor, total_tickets):
  winning_ticket = random.randint(1, total_tickets)

  cursor.execute("SELECT * FROM sales")  
  for row in cursor:
    for ticket in range(1, row[1]+1):
      if ticket == winning_ticket:
        return row[0], winning_ticket
  
  return None, None

while True:

  os.system('clear')

  print("\n1. Enter data\n2. View data\n3. Generate Random Ticket Winner\n4. Delete Record\n5. Quit\n")

  password = "headsofcopper" 

  choice = input("Choice: ")

  if choice == '1':

    name = input("Enter customer name: ")  
    tickets = input("Enter number of tickets: ")

    if not tickets.isdigit():
      print("Invalid input. Only enter a number.")
      continue

    tickets = int(tickets)

    if tickets <= 0:
      print("Tickets must be > 0")
      continue

    c.execute("SELECT * FROM sales WHERE customer=?", (name,))
    if c.fetchone():  
      print("Error: Name already exists")
      continue

    c.execute("INSERT INTO sales VALUES (?, ?)", (name, tickets))
    conn.commit() 

    print(f"{tickets} tickets added for {name}")

  elif choice == '2':
    
    c.execute("SELECT * FROM sales")
    rows = c.fetchall()

    print("\nListing of All Records:\n")
    for row in rows:
      print(f"{row[0]} - {row[1]} tickets")
    print()
 
  elif choice == '3':
    
    for i in range(5):
  
      cursor.execute("SELECT * FROM sales")

      for row in cursor:

        for ticket_num in range(row[1]):
          print("Name: " + row[0] + " - Ticket #" + str(ticket_num+1))
          print() 

    total_tickets = get_total_tickets(cursor)
    winner, winning_ticket = pick_random_winner(cursor, total_tickets)

    if winner:
      print(f"\nTotal Tickets: {total_tickets}") 
      print(f"Winning Ticket: {winning_ticket}")
      print(f"Winner: {winner}")
    else:
      print("\nNo winner found!")

  elif choice == '4':

  # Take input before mocking getpass
    entered_password = input("Enter password: ")

    with patch('getpass.getpass', return_value=entered_password):
   
      print(getpass.getpass("Enter password:"))
  
      if entered_password == password:

        print("\n!!!!!!!!Access Granted!!!!!!!!!!!\n")
   
        # Run restricted code
     
        name = input("Enter name to delete: ")
   
        c.execute("SELECT COUNT(*) FROM sales WHERE customer=?", (name,))
   
        count = c.fetchone()[0]
   
        if count == 0:
       
          print(f"Error: {name} not found in database")
       
        else:
       
          confirm = input(f"Are you sure you want to delete {name}? (y/n) ")
          if confirm.lower() == 'y':
            c.execute("DELETE FROM sales WHERE customer=?", (name,))
            conn.commit()
            print(f"{name} deleted successfully")
         
          else:
            print("Delete cancelled")

      else:
       print("\n!!!!!!!!!Incorrect password!!!!!!!!!")
     
  elif choice == '5':
    break

  else:
    print("Invalid choice, please enter 1, 2, 3, or 4")

conn.close()
os.system('clear')
print("Done")

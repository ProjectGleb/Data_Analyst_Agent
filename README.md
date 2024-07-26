# Data Analyst Agent
This agent based on the user query can interract with both relational (SQL) databases and non-relational databases(RAG). It intelligently queries them to retrieve the right information and can then write an analytical report on the contents.

Demo: https://drive.google.com/file/d/1e2z19zLvwFvYT28kQJ2IcUpvHXAxd4DJ/view?usp=sharing

## The database analyst is a crew of of 3 agents:
### **1. Manager agent**
  - Takes in a user query, and decides wether to retrieve information form a relational or a non-relational database. 
### **2. Relational database agent**
  - Constructs sql based queries to retrieve information from an SQL light database.
  - Check query syntax against schemas tool
### **3. Non-Relational (RAG) database agent**
  - Completes a full RAG cycle. 

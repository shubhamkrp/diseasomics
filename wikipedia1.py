# -*- coding: utf-8 -*-
"""wikipedia1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z1Rr6N526wfCkHcKeWqBAwyAGp5YEQ-h
"""

# according to python file opener,
# 'id: SYMP:' appears 1019 times in the file.
# 'id: DOID:' appears 14033 times in the file.

file1=open('/content/symp.obo','r')

#checking the count of ids in SYMP
count = 0

with open('/content/symp.obo', 'r') as file:
    for line in file:
        if line.startswith('id: SYMP:'):
            count += 1

# Print the count
print(f"The prefix 'id: SYMP:' appears {count} times in the file.")

file2=open('/content/doid.obo','r')

#checking the count of ids in DOID
count = 0

# Read and process the file
with open('/content/doid.obo', 'r') as file:
    for line in file:
        if line.startswith('id: DOID:'):
            count += 1

# Print the count
print(f"The prefix 'id: DOID:' appears {count} times in the file.")

#ACTUAL CODE STARTS HERE

import pandas as pd
!pip install pronto

import pronto

ontology1 = pronto.Ontology('/content/symp.obo')

# Fetching a single term to inspect its properties
term = next(iter(ontology1.terms()))

all_attributes=[]
# Listing all attributes and methods of the term object
attributes = dir(term)
#attributes_values = vars(term)
all_attributes.append(attributes)
print(all_attributes)

print(f'The ontology has {len(ontology1)} terms.')

ontology2 = pronto.Ontology('/content/doid.obo')

# Fetching a single term to inspect its properties
term2 = next(iter(ontology2.terms()))

all_attributes2=[]
# Listing all attributes and methods of the term object
attributes2 = dir(term)
#attributes_values = vars(term)
all_attributes2.append(attributes)
print(all_attributes2)

print(f'The ontology has {len(ontology2)} terms.')

!pip install wikipedia-api
import wikipediaapi

#Getting Wikipedia pages from here

wiki = wikipediaapi.Wikipedia('DiseasomicsRep (vaishnavipokkula@gmail.com)', 'en')

import numpy as np

#Getting wikipedia pages on disease name or synonym name
#55minute run time
wiki_wiki = wikipediaapi.Wikipedia('DiseasomicsRep (vaishnavipokkula@gmail.com)', 'en')

nameless_doid=[]

doid_nopage=[]
disease_pgtitle={}

for term in ontology2.terms():
  id_=term.id
  name_=term.name
  z = name_.replace(" ", "_")

  page_py = wiki_wiki.page(z)
  disease_pgtitle[id_] = {
        "name": name_,
        "pagetitle": z if page_py.exists() else None
    }

  if not page_py.exists():
    found = False
    for synonym in term.synonyms:
      y = synonym.description
      z = y.replace(" ", "_")
      page_py = wiki_wiki.page(z)
      if page_py.exists():
        disease_pgtitle[id_]["pagetitle"] = z
        found = True
        break
    if not found:
        doid_nopage.append(id_)

disease_list = [entry["name"] for entry in disease_pgtitle.values()]

disease_page_titles = []
for entry in disease_pgtitle.values():
    if entry.get("pagetitle"):
        disease_page_titles.append(entry["pagetitle"])
    else:
        disease_page_titles.append(None)  # default value

# Now page_titles should contain page titles corresponding to names in the order they were processed
#print(page_titles)

print(len(doid_nopage))
#9306 out of 14033 doids have no page in their name

import csv
file_path = 'doid_nopage.csv'

# Write the list to a CSV file
with open(file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows([[id_] for id_ in doid_nopage])  # Convert list to 2D list for CSV

print(f"CSV file saved as {file_path}")

#33 minute run time
#Getting parent disease pages for the rest
for id in doid_nopage:
  term=ontology2.get_term(id)
  found = False
  for kind in term.superclasses(distance=1):  # Use superclasses method to get 'is_a' relationships
    y = kind.name
    z = y.replace(" ", "_")
    page_py = wiki_wiki.page(z)
    if page_py.exists():
      disease_pgtitle[id]["superpagetitle"] = z
      found = True
      break  # Exit the loop if a page is found
  if not found:
    disease_pgtitle[id]["superpagetitle"] = None  # Explicitly set to None if no page is found

doid_stillnopg=[]
for id, details in disease_pgtitle.items():
  if "superpagetitle" in details and details["superpagetitle"] is None:
    doid_stillnopg.append(id)

print(len(doid_stillnopg))

import csv
file_path = 'doid_stillnopg.csv'

# Write the list to a CSV file
with open(file_path, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows([[id_] for id_ in doid_stillnopg])  # Convert list to 2D list for CSV

print(f"CSV file saved as {file_path}")

import csv

file_path = 'disease_pgtitle.csv'

# Write the dictionary to a CSV file
with open(file_path, 'w', newline='') as file:
    writer = csv.writer(file)

    # header
    writer.writerow(["DOID", "Name", "PageTitle", "SuperPageTitle"])

    # data rows
    for doid, details in disease_pgtitle.items():
        writer.writerow([doid, details["name"], details.get("pagetitle"), details.get("superpagetitle")])

print(f"CSV file saved as {file_path}")
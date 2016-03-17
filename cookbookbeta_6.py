import sys
import csv
import itertools
import string

f = open("Recipe DB.csv", "rU")
csvreader = csv.reader(f)
rawlist = list(csvreader)
masterlist = []

for item in rawlist:
	masterlist.append(item)
	
column_header = masterlist.pop(0)

'''

ID[0]
Recipe Title[1], 
Category[2]
Cookbook[3]
Page[4]
Ingredients[5]
Keywords[6]

'''
id = {} # **TBD** [ID number] : [recipe]
recipe_title = {} # [recipe] : [cookbook, category, page, ingredients]
category = {} # [category] : [recipe]
cookbook = {} # [cookbook] : [all recipes in cookbook]
cookbookcat = {} # [cookbook] : [all categories in cookbook]
ingredient_search = {} # [ingredient] : [all recipes containing ingredient] 
		
def integer_check():
	count = 0
	while count <= 5:
		try:
			v = int(raw_input("\n> "))
		except ValueError:
			print "\nPlease enter '1', '2', or '3':" 
		else: 
			count = 6
	return v # error handling for integer
		 
def insertIntoDict(k, v, aDict):
	key = string.capwords(k)
	value = string.capwords(v)
	if not key in aDict:
		aDict[key] = [value]
	else: 
		aDict[key].append(value)

def recipekey(): 
	for item in masterlist:
		r = item[1] 
		recipe = string.capwords(r)
		book = item[3]
		cat = item[2]
		page = item[4]
		ingredientsraw = item[5].split(", ")
		ingredients_list = filter(None, ingredientsraw)
		ingredients = list(set(ingredients_list)) # eliminates erroneous duplicates from database
		recipe_title[recipe] = (book, cat, page, ingredients) # adds to recipe_title{}
		for ingredient in ingredients:
			insertIntoDict(ingredient, recipe, ingredient_search) # adds to ingredient_search{}
		insertIntoDict(cat, recipe, category)  # adds to category{}
		insertIntoDict(book, recipe, cookbook) # adds to all dicts except coobookcat{} 
					
def cookbookcatkey():
	for item in masterlist:
		c = item[2]
		cat = string.capwords(c)
		b = item[3]
		book = string.capwords(b)
		if not book in cookbookcat:
			cookbookcat[book] = [cat]
		else:
			if not cat in cookbookcat[book]:
				cookbookcat[book].append(cat)  # adds to cookbookcat{}
				
def page_header(title):
	title = title.upper()
	print "\n" + (10 * "~")
	print title
	print (10 * "~") + "\n"
	
def printcategory(cat):
	c = category.get(cat)
	csort = sorted(c)
	print "\n~~~~\t%s    ~~~~" % cat.upper()
	show_all(csort) # prints formatted category with recipe
		
def show_all(dict):
	print "\n"
	for key in sorted(dict):
		print string.capwords(key)
	print "\n"

# Error Handling	
def item_check(key, dict):
	count = 0
	while count == 0:
		key = string.capwords(key)		
		if key == 'M':
			main()
		elif key == 'Q':
			sys.exit(0)	
		elif key not in dict:
			print ''' 
Hmm...
either "%s" does not exist in the database or you need to check your spelling! 
			
Try entering your choice again - OR - type 'Y' to look at all the available options: 
''' % (key) 
			key = raw_input('\n> ')
			if key == "Y":
				show_all(dict)
				print "\nNow choose one!\n"
		else:
			count = 1
	return key # checks user input exists in dict
		
def find_recipe(): # input recipe and returns Recipe title, Cookbook name, Category, and page
	rkey = raw_input('\n> ')
	recipe = item_check(rkey, recipe_title)
	rcap = recipe.upper()
	r = recipe_title[recipe]
	print '''
			\n~~~~\t%s\t~~~~\n
[ %s ]: page %s\n
CATEGORY: %s ''' % (rcap, r[0], r[2], r[1])

	ingredients = r[3]
	print "\nINGREDIENTS:"
	show_all(ingredients)
	goback() # recipe page
	
def find_ingredient():
	rawIng = raw_input('\n> ')
	formIng = string.capwords(rawIng)
	IngList = formIng.split(', ')
	recList = []
	for i in IngList:
		i = item_check(i, ingredient_search)
		i = ingredient_search[i]
		recList.append(i)	
	common = set(recList[0])
	for s in recList[1:]: # find common elements of a varying amount of lists
		common.intersection_update(s)	
	print "\nRecipes containing %s \n" % (', '.join(IngList))
	show_all(common)
	print "\nWhich recipe do you want to use?\n" 
	find_recipe()
	
def find_category():
	page_header("CATEGORIES")
	show_all(category)
	print "\nType in a category to see the available recipes:"
	ckey = raw_input('\n> ')
	cat = item_check(ckey, category)
	printcategory(cat)
	
	print "\nWhich recipe would you like to see?"
	find_recipe() # category page
		
def find_cookbook():
	page_header("COOKBOOKS")
	show_all(cookbook)
	print "\nWhich cookbook would you like to look at?"
	bkey = raw_input('\n> ')
	book = item_check(bkey, cookbook)
	b = cookbookcat[book]
	print "\n\n\t\t[ %s ]\n" % book.upper()
	for cat in b:
		printcategory(cat)
	print "\nWhich recipe would you like to see?"
	find_recipe() # cookbook page
	
def goback():
	print "\nPress 'M' for Menu or 'Q' to quit:"
	choiceraw = raw_input("> ")
	choice = choiceraw.title()
	if choice == 'M':
		main()
	elif choice == 'Q':
		sys.exit(0)
	else:
		goback()
		
def main():
	page_header("MAIN MENU")
	print "\nType 'R' to enter a specific recipe, or type 'I' to find a recipe containing a specific ingredient"
	print "\nType 'C' to pick a recipe from a category " 
	print "\nType 'B' to pick a recipe from a cookbook\n" 
	cont = 0
	while cont == 0:
		choiceraw = raw_input("\n> ")
		choice = choiceraw.upper()
		if choice == "R":
			print "\nWhat recipe are you looking for?"
			find_recipe()
			cont = 1
		elif choice == "C":
			find_category() 
			cont = 1
		elif choice == "B":
			find_cookbook()
			cont = 1
		elif choice == "I":
			print "\nType in the ingredients you want to cook with, separated by a COMMA. "
			find_ingredient()
			cont = 1
		elif choice == "Q":
			sys.exit(0)
		else:
			print "\nPlease enter 'R', 'C', or 'B' to find a recipe, or press 'Q' to quit:"
			cont = 0
		

recipekey()
cookbookcatkey()

print "\n\t---- Welcome to Kate's Cookbooks! ----\n\n"
main()



	

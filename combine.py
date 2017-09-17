import os
import sys
import glob
import numpy as np
import datetime as dt
import pandas as pd

def process_food(df):
	"""
	Need to process rows that tell us which meal is which
	Also need to remove these rows, as well as "TOTAL:" rows
	"""
	meal_rows = df[pd.isnull(df).sum(1) > 0]
	meal_names = meal_rows['Foods'].values
	meal_inds = meal_rows.index.values

	inds = np.array(meal_inds)
	meal_name = dict(zip(meal_inds, meal_names))
	def edit_row(row):
		return meal_name[np.max(inds[inds <= row.name])]

	df['Meal'] = df.apply(edit_row, axis=1)
	df = df.drop(meal_rows.index)
	df = df.drop(df[df['Foods'] == 'TOTAL:'].index)
	return df

def append_to_csv(indir):
	foods = []
	exers = []
	for infile in glob.glob(indir + '/2*.csv'): # e.g. 2016-06-27-foods.csv
		if not open(infile).read():
			continue
		print infile
		df = pd.read_csv(infile, sep='\t', header=0)
		df.rename(columns=lambda x: x.strip()) # remove whitespace
		dtstr = infile[infile.find('2'):infile.find('2')+10] # hack for dtstr
		df['Date'] = dtstr
		if 'food' in infile:
			df = process_food(df)
			foods.append(df)
		else:
			exers.append(df)
	food = pd.concat(foods)
	exer = pd.concat(exers)
	food.to_csv(indir + '/food.tsv', sep='\t')
	food.to_csv(indir + '/food.csv')
	exer.to_csv(indir + '/exercise.csv')

if __name__ == '__main__':
	append_to_csv(sys.argv[1])

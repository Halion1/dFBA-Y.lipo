import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def heatmap_flux(minimal_flux=0.05,save=False,**kwargs):
	"""
	Fonction qui plot un heat map en utilisant Seaborn
	la fonction prend n'importe quel nombre d'objet solutions produit par run_model_calpainopathie() ou define_boundary_and_run_model()
	"""
	list_df=list()
	for solution in kwargs["solutions"] :
		series=solution.fluxes[solution.fluxes!=0] #remove 0 values
		df=series.to_frame()
		df["name"]=df.index
		df = df.drop(df[df.fluxes < minimal_flux].index) #enlève les flux avec une valeur inférieur a minimal_flux
		list_df.append(df)
	#Quadraboucle qui s'assure que chaque DF contient les mêmes labels (que toutes les réactions soient présente dans chaque DF)
	#si ce n'est pas le cas rajoute une ligne avec pour valeur 0 dans les dataframe qui n'ont pas le label (Nom de réaction)
	for df in list_df :
		for i in df.index :
			for df2 in list_df :
				if i not in df2.index :
					df2.loc[i]=[0,i]
	# combine tous les DF dans un seul DF nommé results
	results=pd.DataFrame()
	compteur=0
	for name in kwargs["name_columns"] :
		results[name]=list_df[compteur]["fluxes"]
		compteur+=1

	#plot 
	fig, ax = plt.subplots(figsize=(20,50))
	ax=sns.heatmap(results)
	#savefig
	if save==True :
		fig = ax.get_figure()
		fig.savefig(kwargs["name_plot"]) 
	return results

- NDIAYE MAGAYE
- ALIPOUR HASSAN
Projet : Jeu de Reversi 10*10
Meilleur joueur = KidAI
Résumé = Utilisation de la technique de la mémorisation pour stocker les recherches précédentes, 
utilisation de l'algorithme Alpha-Beta Pruning pour optimiser Minimax, mise en œuvre d'une limite 
de temps dans Minimax, de la fonction IAIterativeDeepening, et mise en place d'une heuristique de 
jeu valorisant davantage les coins du plateau pour améliorer les performances de l'heuristique.

Dans notre projet, nous avons implémenté deux intelligences artificielles de la manière suivante :

Kidai :
Dans KidAI, nous avons utilisé la méthode IAIterativeDeepening pour prendre en compte le temps 
de décision, ainsi que pour trouver le meilleur mouvement, nous avons stocké toutes les mouvements
légaux dans une variable, puis nous avons envoyé un mouvement à la fois à la méthode Minimax pour 
obtenir le meilleur mouvement en comparant les meilleurs mouvements avec la valeur alpha renvoyée. 
Nous avons pris la plus grande valeur alpha renvoyée comme meilleur mouvement.Nous avons utilisé 
l'algorithme Pruning Alpha-Beta à l'intérieur de la méthode Minimax pour optimiser les performances, 
et nous avons également utilisé plusieurs fois la vérification de la limite de temps à l'intérieur 
de Minimax (car à des profondeurs supérieures, il restait un peu de temps avant d'entrer dans Minimax, 
mais lors de l'entrée dans l'algorithme Minimax, il utilisait beaucoup de temps et ignorait la limite 
de temps à son retour).La méthode get_move a été utilisée pour renvoyer les meilleures valeurs de mouvement 
dans la méthode IAIterativeDeepening, et enfin, nous avons implémenté l'heuristique de jeu dans la méthode evaluate, 
en attribuant une valeur plus élevée aux coins du plateau dans des états de jeu particuliers.

Deuxième joueur, LazyAI :
Dans la plupart des parties, il est mis en œuvre de manière similaire à KidAI, mais la principale 
différence réside dans la mise en œuvre de la méthode IAIterativeDeepening. Dans ce joueur, il entre 
simplement dans Minimax et examine chaque profondeur, choisissant le meilleur mouvement en fonction 
de la dernière profondeur examinée, et non en fonction du meilleur résultat obtenu. De plus, étant 
donné que parfois l'examen de la profondeur reste incomplet, nous stockons la dernière valeur obtenue 
dans une variable pour renvoyer le dernier meilleur mouvement en cas d'absence de meilleur mouvement.

Ensuite, nous avons implémenté une fonction human_player qui vérifie la validité de la valeur entrée, 
évitant ainsi les erreurs, et si le mouvement n'est pas autorisé, elle le rejette avant de prendre l'entrée. 
La fonction get_player_choice est utilisée pour que l'utilisateur choisisse avec quelle IA il souhaite 
jouer ou s'il souhaite observer un match entre deux IA.Enfin, la fonction play_game a été implémentée 
pour gérer les trois scénarios disponibles dans la fonction.

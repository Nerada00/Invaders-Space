def collision_une_coordonnee(mobile1,mobile2,fixe1,fixe2,vitesse):
    """
    Si [mobile1;mobile2] et [fixe1;fixe2] possèdent une intersection, renvoie le déplacement à effectuer pour en sortir.
    Le déplacement est toujours dans le sens contraire de la vitesse.
    Renvoie 0 s'il n'y a pas de collision.
    """
    if mobile1<fixe2 and mobile2>fixe1:
        if vitesse>0:
            return(fixe1-mobile2)
        return(fixe2-mobile1)
    return(0)


def collision_bloquante(position_mobile,dimensions_mobile,vitesse_mobile,position_fixe,dimensions_fixe):
    """
    Teste la collision d'un objet mobile avec un objet fixe.
    Les positions sont des tuples avec abscisse ordonnée.
    Les dimensions sont des tuples avec largeur et hauteur.
    La vitesse du mobile est un tuple avec abscisse ordonnée.
    La fonction renvoie vraie ou faux suivant qu'il y a une collision,
    ainsi que le déplacement à effectuer pour sortir le mobile de l'objet fixe
    Ce déplacement est un tuple, mis à (0,0) si il n'y a pas de collision.
    Comme nous avons une collision entre rectangles, il n'y a toujours qu'une coordonnées du déplacement
    qui est non nulle.
    La fonction renvoie enfin True et False s'il faut stopper la vitesse en abscisse,
    et False et true s'il faut stopper la vitesse en ordonnée.*
    ((0,0),False,False) signifie qu'il n'y a pas de collision.
    """
    deplacement_abscisse = collision_une_coordonnee(position_mobile[0],position_mobile[0]+dimensions_mobile[0],position_fixe[0],position_fixe[0]+dimensions_fixe[0],vitesse_mobile[0])
    deplacement_ordonnee = collision_une_coordonnee(position_mobile[1],position_mobile[1]+dimensions_mobile[1],position_fixe[1],position_fixe[1]+dimensions_fixe[1],vitesse_mobile[1])
    if deplacement_abscisse==deplacement_ordonnee==0:
        return((0,0),False,False)
    if abs(deplacement_abscisse)<abs(deplacement_ordonnee):
        return((deplacement_abscisse,0),True,False)
    return((0,deplacement_ordonnee),False,True)


def ajuster_vitesse(vitesse,arreter_abscisse,arreter_ordonnee):
    retour= vitesse
    if arreter_abscisse:
        retour = (0, retour[1])
    if arreter_ordonnee:
        retour = (retour[0],0)
    return(retour)


def deplacement_contraint(position_mobile,dimensions_mobile,vitesse_mobile,liste_positions_obstacles,liste_dimensions_obstacles):
    """
    Réalise un déplacement d'un mobile rectangulaire contraint par rapport à une liste d'obstacles rectangulaires.
    Les positions, dimensions et vitesses doivent être des tuples.
    Les deux listes sont des listes de tuples.
    La fonction renvoie la nouvelle position et la nouvelle vitesse, toujours sous forme de tuples.
    """
    position_prevue = (position_mobile[0]+vitesse_mobile[0],position_mobile[1]+vitesse_mobile[1])
    deplacements_collision = []
    arreter_vitesse_abscisse, arreter_vitesse_ordonnee = False, False
    for i in range(len(liste_positions_obstacles)):
        deplacement_collision, arreter_vitesse_abscisse_courant, arreter_vitesse_ordonnee_courant = collision_bloquante(position_prevue,dimensions_mobile,vitesse_mobile,liste_positions_obstacles[i],liste_dimensions_obstacles[i])
        deplacements_collision.append(deplacement_collision)
        arreter_vitesse_abscisse = arreter_vitesse_abscisse or arreter_vitesse_abscisse_courant
        arreter_vitesse_ordonnee = arreter_vitesse_ordonnee or arreter_vitesse_ordonnee_courant
    for deplacement in deplacements_collision:
        position_prevue = (position_prevue[0] + deplacement[0],position_prevue[1] + deplacement[1])
    vitesse_retour = ajuster_vitesse(vitesse_mobile,arreter_vitesse_abscisse,arreter_vitesse_ordonnee)
    position_retour =(position_prevue[0],position_prevue[1])
    return(position_retour,vitesse_retour)

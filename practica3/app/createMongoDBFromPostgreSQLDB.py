from database import mongo_client, dbConnect, dbCloseConnect


def get_data():

    all_data=[]
    movies_data=[]

    db_conn = dbConnect()

    #Consulta para los datos principales
    movies_list = list(db_conn.execute("SELECT A. movieid, A.movietitle, A.year, A.ratingmean, A.ratingcount\
                                    FROM imdb_movies as A\
                                    INNER JOIN imdb_moviecountries as B\
                                    ON A.movieid=B.movieid\
                                    WHERE B.country = 'UK'\
                                    ORDER BY A.year DESC\
                                    LIMIT 400;"))

    dbCloseConnect(db_conn)


    #Creamos una lista con las listas de cada peli que contienen, el diccionario id:generos y el año
    #Ejemplo: [{'112050': ['Comedy', 'Drama', 'Mystery']}, '1982']]
    list_id_genres_year=[]

    for movie in movies_list:
        id=str(movie[0])
        list_id_genres_year.append(get_movie_genres(id))

    #print(list_id_genres[0])
    #print(list_id_genres[0]['29955'])
    
    #print(list_id_genres_year)
   
    

    for movie in movies_list:
        
        id=str(movie[0])
        title_name=get_title(movie[1])
        year=movie[2]
        rating_mean=round(movie[3],1)
        rating_count=movie[4]

        #print(year)
        #print(rating_mean)
        #print(rating_count)


        #CONSULTA GENEROS
        movie_genres = get_movie_genres(id)
        list_genres = movie_genres[0][id]
        

        #CONSULTA DIRECTORES
        db_conn = dbConnect()
        movie_directors=list(db_conn.execute("SELECT C.directorname\
                                                FROM imdb_movies as A\
                                                INNER JOIN imdb_directormovies as B ON A.movieid=B.movieid\
                                                INNER JOIN imdb_directors as C ON B.directorid=C.directorid\
                                                WHERE B.movieid="+id))
        dbCloseConnect(db_conn)

        list_directors=[]
        for directors in movie_directors:
            list_directors.append(directors[0])

        #CONSULTA ACTORES
        db_conn = dbConnect()
        movie_actors=list(db_conn.execute("SELECT C.actorname\
                                                FROM imdb_movies as A\
                                                INNER JOIN imdb_actormovies as B ON A.movieid=B.movieid\
                                                INNER JOIN imdb_actors as C ON B.actorid=C.actorid\
                                                WHERE B.movieid="+id))
        dbCloseConnect(db_conn)

        list_actors=[]
        for actors in movie_actors:
            list_actors.append(actors[0])

        
        #CONSULTA PELIS RELACIONADAS
        related_movies=get_relates_movies(list_id_genres_year, list_genres, id)

        #print(movie)
        #print(list_genres)
        #print(list_directors)
        #print(list_actors)
        #print(related_movies)
        #print("--------------------------------------")


        movie_info={'title':title_name, 'genres':list_genres, 'year': year, 'number_of_votes':rating_count, 'average_rating':rating_mean, 'directors':list_directors, 'actors':list_actors, 'related_movies':related_movies}
        all_data.append(movie_info)
        


    return all_data




def get_movie_genres(id):

    #Creamos una lista con:
    #        -Un diccionario para cada pelicula con su id y sus generos 
    #        -El año de la peli

    db_conn = dbConnect()

    movie_year_genres=list(db_conn.execute("SELECT A.year, B.genre\
                                FROM imdb_movies as A\
                                INNER JOIN imdb_moviegenres as B\
                                ON A.movieid=B.movieid\
                                WHERE B.movieid="+id))
    dbCloseConnect(db_conn)

    #comprobamos que existe algún genero para la pelicula
    list_genres=[]
    year=0

    if movie_year_genres:
        year = movie_year_genres[0][0]
        for line in movie_year_genres:
            list_genres.append(line[1])

    
    dic={id: list_genres}
    all_movie_genres_year=[dic, year]

    #print(all_movie_genres_year)
    #print("-----------------------------")
    
    return all_movie_genres_year


#Función para eliminar los paréntesis del titulo
def get_title(name):

    aux=name.find("(")
    name_final=name[:aux-1]

    return name_final



#Devuelve una lista con 10 diccionarios dentro con el titulo, año y valoraciones medias de las 10 pelis relacionadas más actuales
def get_relates_movies(list_id_genres_year, list_genres, id):

    
    num_genres=len(list_genres)
    related_movies=[]

    if num_genres==0:
        return related_movies

    for elem in list_id_genres_year:
        counter=0

        k=list(elem[0])
        id_movie=k[0]
 
        #Comprobamos que la pelicula no sea ella misma
        if id_movie!=id:
            genres_movie=elem[0][id_movie]
            for gen in genres_movie:
                for gen_original in list_genres:
                    if gen == gen_original:
                        counter+=1
                        continue
        
        if counter >= num_genres/2 :
            l=[id_movie, elem[1]]
            related_movies.append(l)

    
    #Ordenamos la lista y nos quedamos con las 10 primeras pelis
    ordenada=sorted(related_movies, key=lambda l: l[1], reverse=True)
    top_10_related=ordenada[:10]
    #print(top_10_related)
    #print("---------------------")

    #Tenemos el id y el año, nos falta sacar el titulo y las valoraciones medias y ya devolverlo
    list_10_related=[]

    for elem in top_10_related:
        db_conn = dbConnect()
       
        movie_detials=list(db_conn.execute("SELECT movietitle, ratingmean\
                                            FROM imdb_movies\
                                            WHERE movieid="+elem[0]))
        dbCloseConnect(db_conn)

        movie_name=get_title(movie_detials[0][0])
        related_movie_details={'title':movie_name, 'year':int(elem[1]), 'average_rating':round(movie_detials[0][1],1)}
        
        list_10_related.append(related_movie_details)                                    
        #print(list_10_related)

    return list_10_related



#MongoDB
db = mongo_client['si1']
collection=db['topUK']
#print(get_data())
collection.insert_many(get_data())



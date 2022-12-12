import sqlite3


def get_query(query):
    """
    Получаем запрос в формате строки, возвращает данные в формате списка

    :param query:
    :return:
    """

    connection = sqlite3.connect("netflix.db")
    cursor = connection.cursor()
    cursor.execute(query)
    executed_query = cursor.fetchall()
    connection.close()
    return executed_query


def get_movie_by_title(title):
    """Получает название фильма в формате строки, возвращает словарь с информацией про него
    (Название, страна, год выпуска, жанры, описание). Если есть несколько фильмов с таким названием -
    возвращается информация о последнем по году выпуска"""

    query = f"""
            SELECT title, country, release_year, listed_in, description from netflix
            WHERE title = '{title}'
            ORDER BY release_year DESC
            LIMIT 1
            """

    raw_data = get_query(query)
    if not raw_data:
        return "Movie not found"

    result = {"title": raw_data[0][0],
              "country": raw_data[0][1],
              "release_year": raw_data[0][2],
              "genre": raw_data[0][3],
              "description": raw_data[0][4]
                }

    return result


def get_movies_by_period(min_year, max_year):
    """Принимает диапазон: начальный и конечный год в формате int,
    возвращает информацию о 100 фильмах из этого диапазона"""

    query = f"""
            SELECT title, release_year from netflix
            WHERE release_year BETWEEN {min_year} and {max_year} 
            LIMIT 100
    """
    raw_data = get_query(query)
    result = []

    for movie in raw_data:
        movie_info = {"title": movie[0],
                      "release_year": movie[1]}
        result.append(movie_info)

    return result


def get_movies_by_rating(rating):
    """Получает группу рейтинга, возвращает информацию о соответствующих фильмах"""

    if rating == 'children':
        query = f"""
            SELECT title, rating, description from netflix
            WHERE rating = 'G' 
    
        """
    elif rating == 'family':
        query = f"""
            SELECT title, rating, description from netflix
            WHERE rating IN ('G', 'PG', 'PG-13') 
        """
    elif rating == 'adult':
        query = f"""
            SELECT title, rating, description from netflix
            WHERE rating IN ('R', 'NC')
        """
    raw_data = get_query(query)

    result = []
    for movie in raw_data:
        movie_info = {"title": movie[0],
                      "rating": movie[1],
                      "description": movie[2]
                      }
        result.append(movie_info)

    return result


def get_movies_by_genre(genre):
    """Получает жанр в формате строки, возвращает 10 свежих фильмов этого жанра"""

    query = f"""
            SELECT title, description from netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC
            LIMIT 10
    """

    raw_data = get_query(query)
    result = []

    for movie in raw_data:
        movie_info = {"title": movie[0],
                      "description": movie[1]}
        result.append(movie_info)

    return result


def get_together_actors(actor1, actor2):
    """Получает двух актеров в формате строк, находит фильмы, где они снимались вдвоем,
    возвращает список актеров, Которые также снимались в этих фильмах (более, чем в 2-х из них)"""

    query = f"""
            SELECT `cast` from netflix
            WHERE `cast` LIKE '%{actor1}%' and `cast` LIKE '%{actor2}%'
    """

    raw_data = get_query(query)
    all_actors_list = []
    actors_list = []

    # создадим общий список всех актеров из всех кастов (с повторами)
    for actors in raw_data:
        # из кортежа в строку
        actors = ''.join(actors)

        # разделить строку на отдельных актеров
        actors = actors.split(', ')

        # присоединить каждого актера к списку
        for item in actors:
            all_actors_list.append(item)

    # создадим список, в котором окажутся актеры, сыгравшие больше 2 раз
    for actor in all_actors_list:
        counter = 0
        for item in all_actors_list:
            if item == actor:
                counter += 1

        if counter > 2:
            actors_list.append(actor)

    # удалим повторы
    actors_list = set(actors_list)

    # трансформируем обратно в список и удалим актеров, по которым искали
    actors_list = list(actors_list)
    actors_list.remove(actor1)
    actors_list.remove(actor2)

    return actors_list


def get_movie_by_request(movie_type, year, genre):
    query = f"""
            SELECT title, description from netflix
            WHERE `type`='{movie_type}' AND release_year = {year} AND listed_in LIKE '%{genre}%'      
    """

    raw_data = get_query(query)
    result = []

    for movie in raw_data:
        movie_info = {"title": movie[0],
                      "description": movie[1]}
        result.append(movie_info)

    return result

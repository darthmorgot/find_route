from trains.models import Train


def dfs_paths(graph, start, goal):
    """Функция поиска всех возможных маршрутов
    из одного города в другой. Вариант посещения
    одного и того же города более одного раза,
    не рассматривается.
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(qs):
    graph = {}

    for item in qs:
        graph.setdefault(item.from_city_id, set())
        graph[item.from_city_id].add(item.to_city_id)

    return graph


def get_routes(request, form) -> dict:
    context = {'form': form}
    trains = Train.objects.all().select_related('from_city', 'to_city')
    graph = get_graph(trains)

    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    transit_cities = data['transit_cities']
    travelling_time = data['travelling_time']

    all_paths = list(dfs_paths(graph, from_city.id, to_city.id))

    if not len(all_paths):
        raise ValueError('Подходящего маршрута не существует.')

    if transit_cities:
        temp_cities = [city.id for city in transit_cities]
        right_paths = []

        for route in all_paths:
            if all(city in route for city in temp_cities):
                right_paths.append(route)
        if not right_paths:
            raise ValueError('Маршрут через указанные города невозможен.')
    else:
        right_paths = all_paths

    routes = []
    all_trains = {}

    for train in trains:
        all_trains.setdefault((train.from_city_id, train.to_city_id), [])
        all_trains[(train.from_city_id, train.to_city_id)].append(train)

    for route in right_paths:
        tmp = {}
        tmp['trains'] = []
        total_time = 0

        for i in range(len(route) - 1):
            obj_list = all_trains[(route[i], route[i + 1])]
            obj = obj_list[0]
            total_time += obj.travel_time
            tmp['trains'].append(obj)

        tmp['total_time'] = total_time

        if total_time <= travelling_time:
            routes.append(tmp)

    if not routes:
        raise ValueError('Время в пути больше заданного.')

    sorted_routes = []

    if len(routes) == 1:
        sorted_routes = routes
    else:
        times = list(set(route['total_time'] for route in routes))
        times = sorted(times)

        for time in times:
            for route in routes:
                if time == route['total_time']:
                    sorted_routes.append(route)

    context['routes'] = sorted_routes
    context['cities'] = {'from_city': from_city, 'to_city': to_city}

    return context

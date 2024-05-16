import threading
import time

print_lock = threading.Lock()


class TableRow:
    def __init__(self, cost, next_hop):
        self.cost = cost
        self.next_hop = next_hop


class Update:
    def __init__(self, src, dst, new_cost):
        self.src = src
        self.dst = dst
        self.new_cost = new_cost


class Router:
    def __init__(self, id):
        self.id = id
        self.routing_table = {}
        self.neighbours = {}
        self.updates = []
        self.stop = False
        self.lock = threading.Lock()

    def run(self):
        while not self.stop:
            if len(self.updates) != 0:
                first_update, *others = self.updates
                self.update_routing_table(first_update)
                self.updates = others

    def update_neighbour(self, neighbour_id, cost):
        with self.lock:
            self.neighbours[neighbour_id] = cost
            self.update_routing_table(Update(self.id, neighbour_id, cost), False)
            with print_lock:
                print("MANUAL UPDATE")
                self.print_routing_table()

    def try_cheaper(self, dst):
        for neighbour_id, row in self.routing_table.items():
            neighbour_router = routers[neighbour_id]
            if dst in neighbour_router.routing_table:
                if dst not in self.routing_table or \
                        neighbour_router.routing_table[dst].cost + row.cost < self.routing_table[dst].cost:
                    self.routing_table[dst] = TableRow(cost=neighbour_router.routing_table[dst].cost + row.cost,
                                                       next_hop=neighbour_id)
        return self.routing_table[dst].cost

    def try_cheaper_use(self, use_router_id, new_updates):
        use_router = routers[use_router_id]
        for dst, row in use_router.routing_table.items():
            if dst != self.id:
                if dst not in self.routing_table or \
                        use_router.routing_table[dst].cost + self.neighbours[use_router_id] < self.routing_table[dst].cost:
                    self.routing_table[dst] = TableRow(
                        cost=use_router.routing_table[dst].cost + self.neighbours[use_router_id],
                        next_hop=use_router_id)
                    new_updates.append(Update(src=self.id, dst=dst,
                                              new_cost=use_router.routing_table[dst].cost + self.neighbours[use_router_id]))

    def update_routing_table(self, update, lock=True):
        new_updates = []

        def find_update():
            if update.dst == self.id or update.src == self.id:
                if update.dst == self.id:
                    update.src, update.dst = update.dst, update.src

                if update.dst not in self.routing_table:
                    self.routing_table[update.dst] = TableRow(next_hop=update.dst, cost=update.new_cost)
                    new_updates.append(update)
                else:
                    for dst, row in self.routing_table.items():
                        if row.next_hop == update.dst:
                            prev_cost = self.routing_table[dst].cost
                            if dst != row.next_hop:
                                self.routing_table[dst].cost = update.new_cost + routers[row.next_hop].routing_table[
                                    dst].cost
                            else:
                                self.routing_table[dst].cost = update.new_cost
                            new_cost = self.try_cheaper(dst)
                            if prev_cost != new_cost:
                                new_updates.append(Update(self.id, dst, new_cost))
            else:
                if update.dst in self.neighbours:
                    self.try_cheaper_use(update.dst, new_updates)
                if update.src in self.neighbours:
                    self.try_cheaper_use(update.src, new_updates)

        if lock:
            with self.lock:
                find_update()
        else:
            find_update()

        if len(new_updates) > 0:
            with print_lock:
                print("REGULAR UPDATE")
                self.print_routing_table()
            for upd in new_updates:
                self.send_update(upd, lock)

    def print_routing_table(self):
        print(f"Routing table for Router {self.id}:")
        for neighbour_id, row in self.routing_table.items():
            print(f"Destination: {neighbour_id}, Cost: {row.cost}")

    def send_update(self, update, lock=True):
        if lock:
            with self.lock:
                for neighbour_id in self.neighbours.keys():
                    neighbour_router = routers[neighbour_id]
                    neighbour_router.receive_update(update)
        else:
            for neighbour_id in self.neighbours.keys():
                neighbour_router = routers[neighbour_id]
                neighbour_router.receive_update(update)

    def receive_update(self, update):
        with self.lock:
            self.updates.append(update)


if __name__ == "__main__":
    routers = {}

    # Создаем маршрутизаторы
    for i in range(4):
        routers[i] = Router(i)

    # Устанавливаем связи между маршрутизаторами
    routers[0].update_neighbour(1, 1)
    routers[1].update_neighbour(0, 1)
    routers[1].update_neighbour(2, 1)
    routers[2].update_neighbour(1, 1)
    routers[2].update_neighbour(3, 2)
    routers[3].update_neighbour(2, 2)
    routers[3].update_neighbour(0, 7)
    routers[0].update_neighbour(3, 7)
    routers[0].update_neighbour(2, 3)
    routers[2].update_neighbour(0, 3)

    for router_id, router in routers.items():
        t = threading.Thread(target=router.run)
        t.start()

    time.sleep(2)
    routers[0].update_neighbour(1, 0)

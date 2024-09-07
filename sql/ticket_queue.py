import heapq
import itertools
from ticket_database import TicketDatabase, Ticket


class TicketQueue:
    def __init__(self, db_name='tickets.db'):
        self.db = TicketDatabase(db_name)
        self.queue = []
        self.counter = itertools.count()
        self.load_tickets()

    def load_tickets(self):
        tickets = self.db.get_all_tickets()
        for ticket in tickets:
            self.add_ticket(ticket)

    def add_ticket(self, ticket):
        priority = self.calculate_priority(ticket)
        count = next(self.counter)
        heapq.heappush(self.queue, (priority, count, ticket))
        self.db.add_ticket(ticket)  # Armazena o ticket no banco de dados

    def calculate_priority(self, ticket):
        urgency_score = {'alta': 3, 'média': 2, 'baixa': 1}
        client_score = {'vip': 3, 'regular': 1}
        urgency = urgency_score.get(ticket.urgency.lower(), 1)
        client = client_score.get(ticket.client_type.lower(), 1)
        return -(urgency * 2 + client)

    def get_next_ticket(self):
        if self.queue:
            priority, count, ticket = heapq.heappop(self.queue)
            # Atualiza o status do ticket no banco de dados
            self.db.update_ticket(ticket)
            return ticket
        return None

    def view_all_tickets(self):
        return sorted(self.queue)

    def update_ticket(self, ticket):
        self.db.update_ticket(ticket)  # Atualiza o ticket no banco de dados

    def delete_ticket(self, ticket_id):
        self.db.delete_ticket(ticket_id)  # Remove o ticket do banco de dados
        self.queue = [
            item for item in self.queue if item[2].ticket_id != ticket_id]
        heapq.heapify(self.queue)  # Reorganiza a fila após a remoção

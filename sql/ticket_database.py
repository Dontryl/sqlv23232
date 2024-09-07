import sqlite3


class Ticket:
    def __init__(self, ticket_id, urgency, client_type, problem_description, status="Em Aberto"):
        self.ticket_id = ticket_id
        self.urgency = urgency
        self.client_type = client_type
        self.problem_description = problem_description
        self.status = status  # O status pode ser "Em Aberto" ou "Resolvido"

    def marcar_como_resolvido(self):
        self.status = "Resolvido"

    def __repr__(self):
        return (f"Ticket ID: {self.ticket_id}, Urgency: {self.urgency}, "
                f"Client Type: {self.client_type}, Problem: {self.problem_description}, "
                f"Status: {self.status}")


class TicketDatabase:
    def __init__(self, db_name='tickets.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id TEXT PRIMARY KEY,
            urgency TEXT,
            client_type TEXT,
            problem_description TEXT,
            status TEXT
        )
        ''')
        self.conn.commit()

    def add_ticket(self, ticket):
        if self.get_ticket(ticket.ticket_id):
            # Se o ticket já existir, atualize-o
            self.update_ticket(ticket)
        else:
            # Caso contrário, insira um novo ticket
            self.cursor.execute('''
            INSERT INTO tickets (ticket_id, urgency, client_type, problem_description, status)
            VALUES (?, ?, ?, ?, ?)
            ''', (ticket.ticket_id, ticket.urgency, ticket.client_type, ticket.problem_description, ticket.status))
        self.conn.commit()

    def get_ticket(self, ticket_id):
        self.cursor.execute(
            'SELECT * FROM tickets WHERE ticket_id = ?', (ticket_id,))
        row = self.cursor.fetchone()
        if row:
            return Ticket(*row)
        return None

    def get_all_tickets(self):
        self.cursor.execute('SELECT * FROM tickets')
        rows = self.cursor.fetchall()
        return [Ticket(*row) for row in rows]

    def update_ticket(self, ticket):
        self.cursor.execute('''
        UPDATE tickets
        SET urgency = ?, client_type = ?, problem_description = ?, status = ?
        WHERE ticket_id = ?
        ''', (ticket.urgency, ticket.client_type, ticket.problem_description, ticket.status, ticket.ticket_id))
        self.conn.commit()

    def delete_ticket(self, ticket_id):
        self.cursor.execute(
            'DELETE FROM tickets WHERE ticket_id = ?', (ticket_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

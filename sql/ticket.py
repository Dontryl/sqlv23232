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

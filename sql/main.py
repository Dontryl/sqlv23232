import tkinter as tk
from tkinter import messagebox
from ticket import Ticket  # Importa a classe Ticket do arquivo ticket.py
# Importa a classe TicketQueue do arquivo ticket_queue.py
from ticket_queue import TicketQueue


class TicketSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticket Support System")

        self.ticket_queue = TicketQueue()  # Cria a fila de tickets

        # Labels e entradas para adicionar tickets
        self.label_ticket_id = tk.Label(root, text="Ticket ID:")
        self.label_ticket_id.grid(row=0, column=0, padx=10, pady=5)
        self.entry_ticket_id = tk.Entry(root)
        self.entry_ticket_id.grid(row=0, column=1, padx=10, pady=5)

        self.label_urgency = tk.Label(
            root, text="Urgency (Alta, Média, Baixa):")
        self.label_urgency.grid(row=1, column=0, padx=10, pady=5)
        self.entry_urgency = tk.Entry(root)
        self.entry_urgency.grid(row=1, column=1, padx=10, pady=5)

        self.label_client_type = tk.Label(
            root, text="Client Type (VIP, Regular):")
        self.label_client_type.grid(row=2, column=0, padx=10, pady=5)
        self.entry_client_type = tk.Entry(root)
        self.entry_client_type.grid(row=2, column=1, padx=10, pady=5)

        self.label_problem_description = tk.Label(
            root, text="Problem Description:")
        self.label_problem_description.grid(row=3, column=0, padx=10, pady=5)
        self.entry_problem_description = tk.Entry(root)
        self.entry_problem_description.grid(row=3, column=1, padx=10, pady=5)

        # Botão para adicionar tickets
        self.button_add_ticket = tk.Button(
            root, text="Add Ticket", command=self.add_ticket)
        self.button_add_ticket.grid(row=4, column=0, columnspan=2, pady=10)

        # Botão para visualizar todos os tickets
        self.button_view_tickets = tk.Button(
            root, text="View All Tickets", command=self.view_tickets)
        self.button_view_tickets.grid(row=5, column=0, columnspan=2, pady=10)

        # Botão para pegar o próximo ticket
        self.button_next_ticket = tk.Button(
            root, text="Get Next Ticket", command=self.get_next_ticket)
        self.button_next_ticket.grid(row=6, column=0, columnspan=2, pady=10)

        # Botão para marcar como resolvido
        self.button_mark_resolved = tk.Button(
            root, text="Mark as Resolved", command=self.mark_ticket_resolved)
        self.button_mark_resolved.grid(row=7, column=0, columnspan=2, pady=10)

        # Área de exibição de resultados
        self.text_area = tk.Text(root, height=10, width=50)
        self.text_area.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

    def add_ticket(self):
        """Adiciona um ticket na fila"""
        ticket_id = self.entry_ticket_id.get().strip()
        urgency = self.entry_urgency.get().strip()
        client_type = self.entry_client_type.get().strip()
        problem_description = self.entry_problem_description.get().strip()

        if not ticket_id or not urgency or not client_type or not problem_description:
            messagebox.showerror("Input Error", "All fields are required!")
            return

        # Criação do ticket
        ticket = Ticket(ticket_id, urgency, client_type, problem_description)
        self.ticket_queue.add_ticket(ticket)
        messagebox.showinfo(
            "Success", f"Ticket '{ticket_id}' added successfully!")

        # Limpa as entradas após adicionar
        self.entry_ticket_id.delete(0, tk.END)
        self.entry_urgency.delete(0, tk.END)
        self.entry_client_type.delete(0, tk.END)
        self.entry_problem_description.delete(0, tk.END)

    def view_tickets(self):
        """Exibe todos os tickets na fila"""
        tickets = self.ticket_queue.view_all_tickets()
        if not tickets:
            messagebox.showinfo("Ticket Queue", "No tickets in the queue.")
            return

        # Exibe os tickets na text area
        self.text_area.delete(1.0, tk.END)
        ticket_list = "\n".join(
            [f"Priority: {abs(priority)}, {ticket}" for priority, count, ticket in tickets])
        self.text_area.insert(tk.END, ticket_list)

    def get_next_ticket(self):
        """Obtém o próximo ticket de maior prioridade"""
        next_ticket = self.ticket_queue.get_next_ticket()
        if next_ticket:
            messagebox.showinfo("Next Ticket", f"Processing {next_ticket}")
        else:
            messagebox.showinfo("Next Ticket", "No more tickets in the queue.")

    def mark_ticket_resolved(self):
        """Marca um ticket como resolvido"""
        ticket_id = self.entry_ticket_id.get().strip()

        if not ticket_id:
            messagebox.showerror(
                "Input Error", "Please enter the Ticket ID to resolve.")
            return

        ticket = self.ticket_queue.db.get_ticket(ticket_id)
        if ticket:
            ticket.marcar_como_resolvido()
            self.ticket_queue.update_ticket(ticket)
            messagebox.showinfo(
                "Success", f"Ticket '{ticket_id}' marked as resolved!")
        else:
            messagebox.showerror(
                "Error", f"No ticket found with ID '{ticket_id}'.")

        # Atualiza a visualização dos tickets
        self.view_tickets()


if __name__ == "__main__":
    root = tk.Tk()
    app = TicketSystemGUI(root)
    root.mainloop()

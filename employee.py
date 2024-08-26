from datetime import datetime

class Employee:
    def __init__(self, emp_id, first_name, last_name, designation=None):
        self.emp_id = emp_id
        self.first_name = first_name
        self.last_name = last_name
        self.designation = designation
        self.events = []

    def add_event(self, event):
        """Add an event to the employee's event history."""
        self.events.append(event)

    def get_total_paid(self):
        """Calculate the total amount paid to the employee, including salary, bonuses, and reimbursements."""
        total_paid = 0
        for event in self.events:
            if event['event'] in {'SALARY', 'BONUS', 'REIMBURSEMENT'}:
                total_paid += event['value']
        return total_paid

    def get_onboard_date(self):
        """Return the onboard date of the employee if available."""
        for event in self.events:
            if event['event'] == 'ONBOARD':
                return event['date']
        return None

    def get_exit_date(self):
        """Return the exit date of the employee if available."""
        for event in self.events:
            if event['event'] == 'EXIT':
                return event['exit_date']
        return None

    def __str__(self):
        """Return a string representation of the employee."""
        return f"{self.emp_id}: {self.first_name} {self.last_name}, {self.designation}"


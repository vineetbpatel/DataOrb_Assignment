import csv
from datetime import datetime
from employee import Employee

class PayrollProcessor:
    def __init__(self):
        self.employees = {}

    def load_data(self, filename):
        """Load data from a .txt or .csv file and process each record."""
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                self.process_event(row)

    def process_event(self, event_data):
        """Process an event and update the employee's record accordingly."""
        sequence_no = event_data[0]
        emp_id = event_data[1]

        if event_data[5] == "ONBOARD":
            # ONBOARD event format: SequenceNo, EmpID, EmpFName, EmpLName, Designation, Event, Value, EventDate, Notes
            emp_fname = event_data[2]
            emp_lname = event_data[3]
            designation = event_data[4]
            event_date = datetime.strptime(event_data[7], '%d-%m-%Y')
            notes = event_data[8]

            if emp_id not in self.employees:
                self.employees[emp_id] = Employee(emp_id, emp_fname, emp_lname, designation)
            
            self.employees[emp_id].add_event({
                'event': 'ONBOARD',
                'date': event_date,
                'notes': notes,
            })

        elif event_data[5] in {"SALARY", "BONUS", "REIMBURSEMENT"}:
            # SALARY/BONUS/REIMBURSEMENT event format: SequenceNo, EmpID, Event, Value, EventDate, Notes
            event = event_data[5]
            value = float(event_data[3])
            event_date = datetime.strptime(event_data[4], '%d-%m-%Y')
            notes = event_data[5]

            if emp_id in self.employees:
                self.employees[emp_id].add_event({
                    'event': event,
                    'value': value,
                    'date': event_date,
                    'notes': notes,
                })

        elif event_data[5] == "EXIT":
            # EXIT event format: SequenceNo, EmpID, Event, Value, EventDate, Notes
            event = event_data[5]
            exit_date = datetime.strptime(event_data[3], '%d-%m-%Y')
            event_date = datetime.strptime(event_data[4], '%d-%m-%Y')
            notes = event_data[5]

            if emp_id in self.employees:
                self.employees[emp_id].add_event({
                    'event': 'EXIT',
                    'exit_date': exit_date,
                    'date': event_date,
                    'notes': notes,
                })

    def generate_reports(self):
        """Generate the required reports based on processed events."""
        self.generate_total_employees_report()
        self.generate_monthly_reports()
        self.generate_employee_financial_reports()
        self.generate_monthly_amount_report()
        self.generate_yearly_financial_report()

    def generate_total_employees_report(self):
        """Generate and print the total number of employees."""
        total_employees = len(self.employees)
        print(f"Total number of employees: {total_employees}")

    def generate_monthly_reports(self):
        """Generate monthly reports for onboarding and exiting employees."""
        monthly_joined = {}
        monthly_exited = {}

        for employee in self.employees.values():
            for event in employee.events:
                if event['event'] == 'ONBOARD':
                    month_year = event['date'].strftime('%m-%Y')
                    if month_year not in monthly_joined:
                        monthly_joined[month_year] = []
                    monthly_joined[month_year].append(employee)
                elif event['event'] == 'EXIT':
                    month_year = event['date'].strftime('%m-%Y')
                    if month_year not in monthly_exited:
                        monthly_exited[month_year] = []
                    monthly_exited[month_year].append(employee)

        print("Monthly Onboarding Report:")
        for month, employees in monthly_joined.items():
            print(f"{month}: {len(employees)} employees joined")
            for emp in employees:
                print(f"- {emp.emp_id}: {emp.first_name} {emp.last_name}, {emp.designation}")

        print("\nMonthly Exiting Report:")
        for month, employees in monthly_exited.items():
            print(f"{month}: {len(employees)} employees exited")
            for emp in employees:
                print(f"- {emp.first_name} {emp.last_name}")

    def generate_employee_financial_reports(self):
        """Generate financial reports for each employee."""
        print("\nEmployee Financial Reports:")
        for employee in self.employees.values():
            total_paid = 0
            for event in employee.events:
                if event['event'] in {'SALARY', 'BONUS', 'REIMBURSEMENT'}:
                    total_paid += event['value']
            print(f"{employee.emp_id}: {employee.first_name} {employee.last_name} - Total Paid: ${total_paid:.2f}")

    def generate_monthly_amount_report(self):
        """Generate monthly report of total amounts released."""
        monthly_amounts = {}

        for employee in self.employees.values():
            for event in employee.events:
                if event['event'] in {'SALARY', 'BONUS', 'REIMBURSEMENT'}:
                    month_year = event['date'].strftime('%m-%Y')
                    if month_year not in monthly_amounts:
                        monthly_amounts[month_year] = 0
                    monthly_amounts[month_year] += event['value']

        print("\nMonthly Amount Released Report:")
        for month, total_amount in monthly_amounts.items():
            print(f"{month}: Total Amount Released: ${total_amount:.2f}")

    def generate_yearly_financial_report(self):
        """Generate yearly financial report."""
        print("\nYearly Financial Report:")
        for employee in self.employees.values():
            for event in employee.events:
                if event['event'] in {'SALARY', 'BONUS', 'REIMBURSEMENT'}:
                    event_date = event['date'].strftime('%Y')
                    print(f"Event: {event['event']}, Emp Id: {employee.emp_id}, Event Date: {event_date}, Event Value: ${event['value']:.2f}")
                elif event['event'] == 'EXIT':
                    exit_date = event['exit_date'].strftime('%Y')
                    print(f"Event: EXIT, Emp Id: {employee.emp_id}, Exit Date: {exit_date}")


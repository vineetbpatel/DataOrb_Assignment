from payroll_processor import PayrollProcessor

def main():
    processor = PayrollProcessor()
    processor.load_data('employee_details.txt')
    processor.generate_reports()

if __name__ == "__main__":
    main()
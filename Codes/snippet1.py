from z3 import *

def separate_names(email_list):
    name_list = []

    for email in email_list:
        solver = Solver()
        email_var = StringVal(email)
        first_name_var = String('first_name')
        last_name_var = String('last_name')
        domain_var = String('example.com')  # Domain is assumed to be 'example.com'

        # Add constraints to the solver based on the formal specification
        solver.add(Or(email_var == Concat(first_name_var, "_", last_name_var, "@", domain_var), email_var == Concat(first_name_var, ".", last_name_var, "@", domain_var)))

        if solver.check() == sat:
            model = solver.model()
            first_name = model[first_name_var].as_string()
            last_name = model[last_name_var].as_string()
        else:
            first_name = "Unknown"
            last_name = "Unknown"

        name_list.append((first_name, last_name))

    return name_list

# Example input: list of email IDs
email_list = [
    "sadman.jashim.sakib@gmail.com",
    "john.doe@yahoo.com",
    "jane_smith@hotmail.com",
    "invalid.email"
]

# Separate names from email IDs using SMT solver
names = separate_names(email_list)

# Print the results
for first_name, last_name in names:
    print(f"First Name: {first_name}, Last Name: {last_name}")
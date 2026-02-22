insert_into_recruitment = """
insert into {table_name}_Candidates (id, name, lname, phone, email, dob, address, pincode, gender, resume_link) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

check_Drive_status = """
select drive_status from drive where drive_name = %s;
"""

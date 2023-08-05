import csv
import ladok3.cli

def print_student_data(student):
  """Prints the student data, all attributes, to stdout."""
  print(f"First name:   {student.first_name}")
  print(f"Last name:    {student.last_name}")
  print(f"Personnummer: {student.personnummer}")
  print(f"LADOK ID:     {student.ladok_id}")
  print(f"Alive:        {student.alive}")
def print_course_data(student, course):
  """Prints the courses"""
  print("Courses:")
  for course in student.courses(courde_code=course):
    print(f"- {course}")

def add_command_options(parser):
  student_parser = parser.add_parser("student",
    help="Shows a student's information in LADOK",
    description="""
    Show a student's information in LADOK.
    Shows information like name, personnummer, contact information.
    """
  )
  student_parser.set_defaults(func=command)
  student_parser.add_argument("id",
    help="The student's ID, either personnummer or LADOK ID"
  )
  student_parser.add_argument("-c", "--course",
    nargs="?", const=".*",
    help="A regular expression for which course codes to list, " \
      "use no value for listing all courses."
  )

def command(ladok, args):
  try:
    student = ladok.get_student(args.id)
    student.alive
  except Exception as err:
    ladok3.cli.err(-1, f"can't fetch student data for {args.id}: {err}")

  print_student_data(student)

  if args.course:
    print_course_data(student, args.course)

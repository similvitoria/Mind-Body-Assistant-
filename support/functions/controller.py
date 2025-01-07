from support.functions.chat.catch_problem import catch_problem
from support.functions.chat.follow_up import follow_up
from support.functions.chat.generate_report import generate_report
from support.functions.chat.get_location import get_location

tools = [catch_problem(), follow_up(), generate_report(), get_location()]

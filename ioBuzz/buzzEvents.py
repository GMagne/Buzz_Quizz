from enum import Enum

keys = {'R':0, 'Y':1, 'G':2, 'O':3, 'B':4}

class Event(Enum):
	def __str__(self):
		return self.name

class Pressed(Event):
	P1_red    = 0
	P1_yellow = 1
	P1_green  = 2
	P1_orange = 3
	P1_blue   = 4

	P2_red    = 5
	P2_yellow = 6
	P2_green  = 7
	P2_orange = 8
	P2_blue   = 9

	P3_red    = 10
	P3_yellow = 11
	P3_green  = 12
	P3_orange = 13
	P3_blue   = 14
	
	P4_red    = 15
	P4_yellow = 16
	P4_green  = 17
	P4_orange = 18
	P4_blue   = 19

class Released(Event):
	P1_red    = 0
	P1_yellow = 1
	P1_green  = 2
	P1_orange = 3
	P1_blue   = 4

	P2_red    = 5
	P2_yellow = 6
	P2_green  = 7
	P2_orange = 8
	P2_blue   = 9

	P3_red    = 10
	P3_yellow = 11
	P3_green  = 12
	P3_orange = 13
	P3_blue   = 14
	
	P4_red    = 15
	P4_yellow = 16
	P4_green  = 17
	P4_orange = 18
	P4_blue   = 19

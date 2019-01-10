import re

class ydsGrade:
	grade_format = re.compile("5.([0-9][0-5]?)([a-d]?[+-/]?[b-d]?)")

	#Default to ""
	letter_comparisons = {
		"a":   0,
		"-":   1,
		"a/b": 2,
		"b":   3,
		"":    4,
		"b/c": 5,
		"c":   6,
		"+":   7,
		"c/d": 8,
		"d":   9
	}

	def __init__(self, grade):
		self.grade = grade
		self.number_grade = int(self.grade_format.match(grade).group(1))
		self.letter_grade = self.grade_format.match(grade).group(2)
		if self.letter_grade not in self.letter_comparisons.keys():
			self.letter_grade = ""

	def __str__(self):
		return self.grade

	def __eq__(self, other):
		return (self.number_grade == other.number_grade and self.letter_grade == other.letter_grade)

	def __gt__(self, other):
		return (self.number_grade > other.number_grade or 
			(self.number_grade == other.number_grade and
			 self.letter_comparisons[self.letter_grade] > other.letter_comparisons[other.letter_grade]))

	def __lt__(self, other):
		return (self.number_grade < other.number_grade or 
			(self.number_grade == other.number_grade and
			 self.letter_comparisons[self.letter_grade] < other.letter_comparisons[other.letter_grade]))		

	def __ge__(self, other):
		return (self.number_grade > other.number_grade or 
			(self.number_grade == other.number_grade and
			 self.letter_comparisons[self.letter_grade] >= other.letter_comparisons[other.letter_grade]))

	def __le__(self, other):
		return (self.number_grade < other.number_grade or 
			(self.number_grade == other.number_grade and
			 self.letter_comparisons[self.letter_grade] <= other.letter_comparisons[other.letter_grade]))
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re
import random
import math
from datetime import datetime
import json
import os

class RwandanP2MathTutor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rwandan P2 Math Tutor - Primary Education")
        self.root.geometry("1000x750")
        self.root.configure(bg='#e8f5e8')  # Rwanda green theme

        # Student progress tracking
        self.student_data = {
            'problems_solved': 0,
            'correct_answers': 0,
            'topics_practiced': set(),
            'difficulty_level': 'Easy'
        }

        # Load existing progress if available
        self.load_progress()

        self.setup_ui()

    def setup_ui(self):
        # Main title with Rwanda theme
        title_frame = tk.Frame(self.root, bg='#e8f5e8')
        title_frame.pack(pady=10)

        title_label = tk.Label(title_frame, text="🇷🇼 Rwandan P2 Math Tutor",
                              font=('Arial', 24, 'bold'),
                              bg='#e8f5e8', fg='#0f5132')
        title_label.pack()

        subtitle_label = tk.Label(title_frame, text="Primary Two Mathematics - Republic of Rwanda Curriculum",
                                 font=('Arial', 12),
                                 bg='#e8f5e8', fg='#198754')
        subtitle_label.pack()

        # Student info frame
        info_frame = tk.Frame(self.root, bg='#d1e7dd', relief='ridge', bd=2)
        info_frame.pack(fill='x', padx=20, pady=5)

        tk.Label(info_frame, text=f"Problems Solved: {self.student_data['problems_solved']} | "
                                f"Accuracy: {self.get_accuracy():.1f}% | "
                                f"Level: {self.student_data['difficulty_level']}",
                font=('Arial', 10), bg='#d1e7dd').pack(pady=5)

        # Problem type selection - P2 Curriculum Topics
        selection_frame = tk.Frame(self.root, bg='#e8f5e8')
        selection_frame.pack(pady=10)

        tk.Label(selection_frame, text="Choose P2 Mathematics Topic:",
                font=('Arial', 14, 'bold'), bg='#e8f5e8', fg='#0f5132').grid(row=0, column=0, columnspan=3, pady=5)

        # P2 Curriculum problem types
        problem_types = [
            ("Numbers 0-999", self.numeration_problem),
            ("Comparing Numbers", self.comparison_problem),
            ("Addition (up to 999)", self.addition_problem),
            ("Subtraction (up to 999)", self.subtraction_problem),
            ("Multiplication", self.multiplication_problem),
            ("Division", self.division_problem),
            ("Measuring Lengths", self.length_measurement_problem),
            ("Measuring Capacity", self.capacity_measurement_problem),
            ("Measuring Mass", self.mass_measurement_problem),
            ("Unit Conversion", self.unit_conversion_problem),
            ("Geometric Shapes", self.geometry_problem),
            ("Perimeter", self.perimeter_problem),
            ("Probability", self.probability_problem),
            ("Word Problems", self.word_problem)
        ]

        for i, (text, command) in enumerate(problem_types):
            btn = tk.Button(selection_frame, text=text, command=command,
                           bg='#198754', fg='white', font=('Arial', 9, 'bold'),
                           width=15, height=2)
            btn.grid(row=1 + i//3, column=i%3, padx=3, pady=3)

        # Difficulty selection
        difficulty_frame = tk.Frame(self.root, bg='#e8f5e8')
        difficulty_frame.pack(pady=5)

        tk.Label(difficulty_frame, text="Difficulty:",
                font=('Arial', 12, 'bold'), bg='#e8f5e8').pack(side='left')

        self.difficulty_var = tk.StringVar(value=self.student_data['difficulty_level'])
        difficulty_combo = ttk.Combobox(difficulty_frame, textvariable=self.difficulty_var,
                                       values=['Easy', 'Medium', 'Hard'], state='readonly')
        difficulty_combo.pack(side='left', padx=10)
        difficulty_combo.bind('<<ComboboxSelected>>', self.update_difficulty)

        # Problem display area
        self.problem_frame = tk.Frame(self.root, bg='white', relief='ridge', bd=2)
        self.problem_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Chat/Tutorial area
        self.chat_area = scrolledtext.ScrolledText(self.problem_frame,
                                                  height=15, width=90,
                                                  font=('Arial', 11),
                                                  bg='#f8f9fa', fg='#212529')
        self.chat_area.pack(fill='both', expand=True, padx=10, pady=10)

        # Input area
        input_frame = tk.Frame(self.problem_frame, bg='white')
        input_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(input_frame, text="Your Answer:",
                font=('Arial', 12, 'bold'), bg='white').pack(side='left')

        self.answer_entry = tk.Entry(input_frame, font=('Arial', 12), width=15)
        self.answer_entry.pack(side='left', padx=10)
        self.answer_entry.bind('<Return>', self.check_answer)

        check_btn = tk.Button(input_frame, text="Check Answer",
                             command=self.check_answer,
                             bg='#198754', fg='white', font=('Arial', 10, 'bold'))
        check_btn.pack(side='left', padx=5)

        hint_btn = tk.Button(input_frame, text="Get Hint",
                            command=self.get_hint,
                            bg='#fd7e14', fg='white', font=('Arial', 10, 'bold'))
        hint_btn.pack(side='left', padx=5)

        # Current problem storage
        self.current_problem = None
        self.current_answer = None
        self.current_steps = []
        self.hint_count = 0

        # Welcome message
        self.add_message("🇷🇼 Muraho! Welcome to Rwandan P2 Math Tutor! Choose a topic to practice mathematics.", "tutor")

    def add_message(self, message, sender="tutor"):
        timestamp = datetime.now().strftime("%H:%M")

        if sender == "tutor":
            prefix = f"[{timestamp}] 🧑‍🏫 Mwarimu: "
            self.chat_area.insert(tk.END, prefix, "tutor_prefix")
            self.chat_area.insert(tk.END, message + "\n\n", "tutor_message")
        else:
            prefix = f"[{timestamp}] 👨‍🎓 Umunyeshuri: "
            self.chat_area.insert(tk.END, prefix, "student_prefix")
            self.chat_area.insert(tk.END, message + "\n\n", "student_message")

        # Configure text tags with Rwanda theme
        self.chat_area.tag_configure("tutor_prefix", foreground="#0f5132", font=('Arial', 11, 'bold'))
        self.chat_area.tag_configure("tutor_message", foreground="#212529")
        self.chat_area.tag_configure("student_prefix", foreground="#198754", font=('Arial', 11, 'bold'))
        self.chat_area.tag_configure("student_message", foreground="#212529")

        self.chat_area.see(tk.END)

    def update_difficulty(self, event=None):
        self.student_data['difficulty_level'] = self.difficulty_var.get()
        self.save_progress()

    def get_p2_number_range(self):
        """Get number ranges appropriate for P2 curriculum (0-999)"""
        if self.student_data['difficulty_level'] == 'Easy':
            return (1, 50)
        elif self.student_data['difficulty_level'] == 'Medium':
            return (10, 200)
        else:  # Hard
            return (50, 999)

    def numeration_problem(self):
        """Numbers 0-999: counting, reading, writing"""
        problem_types = ['write_number', 'read_number', 'count_sequence', 'place_value']
        problem_type = random.choice(problem_types)

        if problem_type == 'write_number':
            num = random.randint(1, 999)
            number_words = self.number_to_words(num)
            self.current_problem = f"Write this number in digits: {number_words}"
            self.current_answer = str(num)
            self.current_steps = [
                f"We need to write '{number_words}' in digits",
                f"Let's break down the number word by word",
                f"The answer is: {num}"
            ]
        elif problem_type == 'read_number':
            num = random.randint(1, 999)
            self.current_problem = f"Write this number in words: {num}"
            self.current_answer = self.number_to_words(num).lower()
            self.current_steps = [
                f"We need to write {num} in words",
                f"Let's break it down by place value",
                f"The answer is: {self.number_to_words(num)}"
            ]
        elif problem_type == 'count_sequence':
            start = random.randint(1, 980)
            self.current_problem = f"Continue this counting pattern: {start}, {start+1}, {start+2}, ?, {start+4}"
            self.current_answer = str(start + 3)
            self.current_steps = [
                f"Look at the pattern: {start}, {start+1}, {start+2}, ?, {start+4}",
                f"Each number increases by 1",
                f"The missing number is: {start + 3}"
            ]
        else:  # place_value
            num = random.randint(100, 999)
            place = random.choice(['hundreds', 'tens', 'ones'])
            if place == 'hundreds':
                answer = num // 100
            elif place == 'tens':
                answer = (num // 10) % 10
            else:
                answer = num % 10

            self.current_problem = f"What digit is in the {place} place in the number {num}?"
            self.current_answer = str(answer)
            self.current_steps = [
                f"In the number {num}:",
                f"Hundreds place: {num // 100}",
                f"Tens place: {(num // 10) % 10}",
                f"Ones place: {num % 10}",
                f"The digit in the {place} place is: {answer}"
            ]

        self.student_data['topics_practiced'].add('Numeration 0-999')
        self.hint_count = 0
        self.add_message(f"📊 Numeration Problem (0-999):\n{self.current_problem}", "tutor")
        self.answer_entry.focus()

    def comparison_problem(self):
        """Comparing numbers less than 1000"""
        min_val, max_val = self.get_p2_number_range()
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, max_val)

        # Ensure they're different
        while a == b:
            b = random.randint(min_val, max_val)

        comparison_type = random.choice(['greater', 'less', 'equal', 'symbol'])

        if comparison_type == 'greater':
            self.current_problem = f"Which number is greater: {a} or {b}?"
            self.current_answer = str(max(a, b))
        elif comparison_type == 'less':
            self.current_problem = f"Which number is less: {a} or {b}?"
            self.current_answer = str(min(a, b))
        else:  # symbol
            self.current_problem = f"Compare these numbers using >, < or =: {a} __ {b}"
            if a > b:
                self.current_answer = ">"
            elif a < b:
                self.current_answer = "<"
            else:
                self.current_answer = "="

        self.current_steps = [
            f"We need to compare {a} and {b}",
            f"Let's look at the place values",
            f"Comparing digit by digit from left to right",
            f"Result: {a} {'>' if a > b else '<' if a < b else '='} {b}"
        ]

        self.student_data['topics_practiced'].add('Comparing Numbers')
        self.hint_count = 0
        self.add_message(f"⚖️ Number Comparison Problem:\n{self.current_problem}", "tutor")
        self.answer_entry.focus()

    def addition_problem(self):
        """Addition up to 999"""
        min_val, max_val = self.get_p2_number_range()
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, min(max_val, 999 - a))  # Ensure sum ≤ 999

        self.current_problem = f"{a} + {b}"
        self.current_answer = a + b
        self.current_steps = [
            f"We need to add {a} + {b}",
            f"Let's use column addition:",
            f"Start with the ones place: {a%10} + {b%10}",
            f"Then the tens place: {(a//10)%10} + {(b//10)%10}",
            f"Finally hundreds place if needed",
            f"Result: {a} + {b} = {a + b}"
        ]

        self.student_data['topics_practiced'].add('Addition up to 999')
        self.hint_count = 0
        self.add_message(f"➕ Addition Problem (up to 999):\n{self.current_problem} = ?", "tutor")
        self.answer_entry.focus()

    def subtraction_problem(self):
        """Subtraction up to 999"""
        min_val, max_val = self.get_p2_number_range()
        a = random.randint(min_val, max_val)
        b = random.randint(min_val, a)  # Ensure positive result

        self.current_problem = f"{a} - {b}"
        self.current_answer = a - b
        self.current_steps = [
            f"We need to subtract {b} from {a}",
            f"Let's use column subtraction:",
            f"Start with the ones place: {a%10} - {b%10}",
            f"Then the tens place: {(a//10)%10} - {(b//10)%10}",
            f"Check if we need to borrow",
            f"Result: {a} - {b} = {a - b}"
        ]

        self.student_data['topics_practiced'].add('Subtraction up to 999')
        self.hint_count = 0
        self.add_message(f"➖ Subtraction Problem (up to 999):\n{self.current_problem} = ?", "tutor")
        self.answer_entry.focus()

    def multiplication_problem(self):
        """Multiplication for P2 level"""
        if self.student_data['difficulty_level'] == 'Easy':
            a = random.randint(1, 5)
            b = random.randint(1, 10)
        elif self.student_data['difficulty_level'] == 'Medium':
            a = random.randint(2, 10)
            b = random.randint(2, 12)
        else:  # Hard
            a = random.randint(5, 15)
            b = random.randint(2, 20)

        self.current_problem = f"{a} × {b}"
        self.current_answer = a * b
        self.current_steps = [
            f"We need to multiply {a} × {b}",
            f"This means adding {a} exactly {b} times",
            f"Or we can use the multiplication table",
            f"{a} × {b} = {a * b}"
        ]

        self.student_data['topics_practiced'].add('Multiplication')
        self.hint_count = 0
        self.add_message(f"✖️ Multiplication Problem:\n{self.current_problem} = ?", "tutor")
        self.answer_entry.focus()

    def division_problem(self):
        """Division for P2 level"""
        if self.student_data['difficulty_level'] == 'Easy':
            divisor = random.randint(2, 5)
            quotient = random.randint(1, 10)
        elif self.student_data['difficulty_level'] == 'Medium':
            divisor = random.randint(2, 10)
            quotient = random.randint(2, 15)
        else:  # Hard
            divisor = random.randint(3, 12)
            quotient = random.randint(3, 20)

        dividend = divisor * quotient  # Ensure clean division

        self.current_problem = f"{dividend} ÷ {divisor}"
        self.current_answer = quotient
        self.current_steps = [
            f"We need to divide {dividend} by {divisor}",
            f"How many times does {divisor} go into {dividend}?",
            f"We can think: {divisor} × ? = {dividend}",
            f"Since {divisor} × {quotient} = {dividend}",
            f"Result: {dividend} ÷ {divisor} = {quotient}"
        ]

        self.student_data['topics_practiced'].add('Division')
        self.hint_count = 0
        self.add_message(f"➗ Division Problem:\n{self.current_problem} = ?", "tutor")
        self.answer_entry.focus()

    def length_measurement_problem(self):
        """Measuring lengths - metric system"""
        measurement_types = ['measuring', 'estimation', 'comparison']
        problem_type = random.choice(measurement_types)

        if problem_type == 'measuring':
            objects = ['pencil', 'book', 'desk', 'classroom', 'playground']
            obj = random.choice(objects)
            if obj in ['pencil']:
                unit = 'cm'
                value = random.randint(10, 25)
            elif obj in ['book', 'desk']:
                unit = 'cm'
                value = random.randint(20, 100)
            else:
                unit = 'm'
                value = random.randint(3, 50)

            self.current_problem = f"What is the most appropriate unit to measure a {obj}? (cm, m, or km)"
            self.current_answer = unit
            self.current_steps = [
                f"We need to choose the best unit for measuring a {obj}",
                f"Centimeters (cm) for small objects",
                f"Meters (m) for medium objects",
                f"Kilometers (km) for long distances",
                f"Best unit for {obj}: {unit}"
            ]
        else:
            length1 = random.randint(10, 100)
            length2 = random.randint(10, 100)
            self.current_problem = f"Which is longer: {length1} cm or {length2} cm?"
            self.current_answer = f"{max(length1, length2)} cm"
            self.current_steps = [
                f"Compare {length1} cm and {length2} cm",
                f"The larger number represents the longer length",
                f"Answer: {max(length1, length2)} cm is longer"
            ]

        self.student_data['topics_practiced'].add('Length Measurement')
        self.hint_count = 0
        self.add_message(f"📏 Length Measurement Problem:\n{self.current_problem}", "tutor")
        self.answer_entry.focus()

    def capacity_measurement_problem(self):
        """Measuring capacity - metric system"""
        containers = ['cup', 'bottle', 'bucket', 'tank', 'spoon']
        container = random.choice(containers)

        if container in ['spoon']:
            unit = 'ml'
            value = random.randint(5, 20)
        elif container in ['cup', 'bottle']:
            unit = 'ml'
            value = random.randint(200, 1000)
        else:
            unit = 'l'
            value = random.randint(5, 50)

        self.current_problem = f"What is the most appropriate unit to measure the capacity of a {container}? (ml or l)"
        self.current_answer = unit
        self.current_steps = [
            f"We need to choose the best unit for measuring a {container}'s capacity",
            f"Milliliters (ml) for small amounts",
            f"Liters (l) for larger amounts",
            f"Best unit for {container}: {unit}"
        ]

        self.student_data['topics_practiced'].add('Capacity Measurement')
        self.hint_count = 0
        self.add_message(f"🥤 Capacity Measurement Problem:\n{self.current_problem}", "tutor")
        self.answer_entry.focus()

    def mass_measurement_problem(self):
        """Measuring mass - metric system"""
        objects = ['coin', 'apple', 'book', 'person', 'car', 'feather']
        obj = random.choice(objects)

        if obj in ['coin', 'feather']:
            unit = 'g'
            value = random.randint(1, 50)
        elif obj in ['apple', 'book']:
            unit = 'g'
            value = random.randint(100, 1000)
        else:
            unit = 'kg'
            value = random.randint(20, 1000)

        self.current_problem = f"What is the most appropriate unit to measure the mass of a {obj}? (g or kg)"
        self.current_answer = unit
        self.current_steps = [
            f"We need to choose the best unit for measuring a {obj}'s mass",
            f"Grams (g) for light objects",
            f"Kilograms (kg) for heavy objects",
            f"Best unit for {obj}: {unit}"
        ]

        self.student_data['topics_practiced'].add('Mass Measurement')
        self.hint_count = 0
        self.add_message(f"⚖️ Mass Measurement Problem:\n{self.current_problem}", "tutor")
        self.answer_entry.focus()

    def unit_conversion_problem(self):
        """Converting between units of measurement"""
        conversion_types = ['length', 'capacity', 'mass']
        conv_type = random.choice(conversion_types)

        if conv_type == 'length':
            if random.choice([True, False]):
                meters = random.randint(1, 10)
                self.current_problem = f"Convert {meters} meters to centimeters"
                self.current_answer = str(meters * 100)
                self.current_steps = [
                    f"We need to convert {meters} meters to centimeters",
                    f"1 meter = 100 centimeters",
                    f"{meters} meters = {meters} × 100 = {meters * 100} centimeters"
                ]
            else:
                cm = random.randint(100, 1000)
                if cm % 100 == 0:  # Only use values that convert evenly
                    self.current_problem = f"Convert {cm} centimeters to meters"
                    self.current_answer = str(cm // 100)
                    self.current_steps = [
                        f"We need to convert {cm} centimeters to meters",
                        f"100 centimeters = 1 meter",
                        f"{cm} centimeters = {cm} ÷ 100 = {cm // 100} meters"
                    ]
                else:
                    cm = 500  # Use a simple conversion
                    self.current_problem = f"Convert {cm} centimeters to meters"
                    self.current_answer = str(cm // 100)
                    self.current_steps = [
                        f"We need to convert {cm} centimeters to meters",
                        f"100 centimeters = 1 meter",
                        f"{cm} centimeters = {cm} ÷ 100 = {cm // 100} meters"
                    ]

        elif conv_type == 'capacity':
            if random.choice([True, False]):
                liters = random.randint(1, 5)
                self.current_problem = f"Convert {liters} liters to milliliters"
                self.current_answer = str(liters * 1000)
                self.current_steps = [
                    f"We need to convert {liters} liters to milliliters",
                    f"1 liter = 1000 milliliters",
                    f"{liters} liters = {liters} × 1000 = {liters * 1000} milliliters"
                ]
            else:
                ml = random.choice([1000, 2000, 3000, 4000, 5000])
                self.current_problem = f"Convert {ml} milliliters to liters"
                self.current_answer = str(ml // 1000)
                self.current_steps = [
                    f"We need to convert {ml} milliliters to liters",
                    f"1000 milliliters = 1 liter",
                    f"{ml} milliliters = {ml} ÷ 1000 = {ml // 1000} liters"
                ]

        else:  # mass
            if random.choice([True, False]):
                kg = random.randint(1, 5)
                self.current_problem = f"Convert {kg} kilograms to grams"
                self.current_answer = str(kg * 1000)
                self.current_steps = [
                    f"We need to convert {kg} kilograms to grams",
                    f"1 kilogram = 1000 grams",
                    f"{kg} kilograms = {kg} × 1000 = {kg * 1000} grams"
                ]
            else:
                g = random.choice([1000, 2000, 3000, 4000, 5000])
                self.current_problem = f"Convert {g} grams to kilograms"
                self.current_answer = str(g // 1000)
                self.current_steps = [
                    f"We need to convert {g} grams to kilograms",
                    f"1000 grams = 1 kilogram",
                    f"{g} grams = {g} ÷ 1000 = {g // 1000} kilograms"
                ]

        self.student_data['topics_practiced'].add('Unit Conversion')
        self.hint_count = 0
        self.add_message(f"🔄 Unit Conversion Problem:\n{self.current_problem}", "tutor")
        self.answer_entry.focus()

    def geometry_problem(self):
        """Identifying and drawing geometric shapes"""
        shapes = ['square', 'rectangle', 'triangle', 'circle']
        problem_types = ['identify', 'properties', 'count_sides']

        shape = random.choice(shapes)
        problem_type = random.choice(problem_types)

        if problem_type == 'identify':
            descriptions = {
                'square': 'has 4 equal sides and 4 right angles',
                'rectangle': 'has 4 sides with opposite sides equal and 4 right angles',
                'triangle': 'has 3 sides and 3 angles',
                'circle': 'is round with no corners'
            }
            self.current_problem = f"What shape {descriptions[shape]}?"
            self.current_answer = shape

        elif problem_type == 'properties':
            if shape == 'square':
                self.current_problem = f"How many sides does a square have?"
                self.current_answer = "4"
            elif shape == 'rectangle':
                self.current_problem = f"How many right angles does a rectangle have?"
                self.current_answer = "4"
            elif shape == 'triangle':
                self.current_problem = f"How many sides does a triangle have?"
                self.current_answer = "3"
            else:  # circle
                self.current_problem = f"How many corners does a circle have?"
                self.current_answer = "0"

        else:  # count_sides
            sides = {'square': 4, 'rectangle': 4, 'triangle': 3, 'circle': 0}
            self.current_problem = f"How many sides does a {shape} have?"
            self.current_answer = str(sides[shape])

        self.current_steps = [
            f"Let's think about the properties of a {shape}",
            f"A {shape} is a geometric shape with specific characteristics",
            f"The answer is: {self.current_answer}"
        ]

        self.student_data['topics_practiced'].add('Geometric Shapes')
        self.hint_count = 0
        self.add_message(f"🔺 Geometry Problem:\n{self.current_problem}", "tutor")
        self.answer_entry.focus()

    def perimeter_problem(self):
        """Calculating perimeter of geometric figures"""
        shapes = ['square', 'rectangle', 'triangle']
        shape = random.choice(shapes)

        if shape == 'square':
            side = random.randint(3, 15)
            self.current_problem = f"Find the perimeter of a square with side length {side} cm"
            self.current_answer = str(4 * side)
            self.current_steps = [
                f"A square has 4 equal sides of length {side} cm",
                f"Perimeter = side + side + side + side",
                f"Perimeter = 4 × {side} = {4 * side} cm"
            ]

        elif shape == 'rectangle':
            length = random.randint(5, 20)
            width = random.randint(3, length-1)
            self.current_problem = f"Find the perimeter of a rectangle with length {length} cm and width {width} cm"
            self.current_answer = str(2 * (length + width))
            self.current_steps = [
                f"A rectangle has length {length} cm and width {width} cm",
                f"Perimeter = length + width + length + width",
                f"Perimeter = 2 × (length + width)",
                f"Perimeter = 2 × ({length} + {width}) = 2 × {length + width} = {2 * (length + width)} cm"
            ]

        else:  # triangle
            side1 = random.randint(3, 12)
            side2 = random.randint(3, 12)
            side3 = random.randint(3, 12)
            self.current_problem = f"Find the perimeter of a triangle with sides {side1} cm, {side2} cm, and {side3} cm"
            self.current_answer = str(side1 + side2 + side3)
            self.current_steps = [
                f"A triangle has three sides: {side1} cm, {side2} cm, and {side3} cm",
                f"Perimeter = side1 + side2 + side3",
                f"Perimeter = {side1} + {side2} + {side3} = {side1 + side2 + side3} cm"
            ]

        self.student_data['topics_practiced'].add('Perimeter')
        self.hint_count = 0
        self.add_message(f"📐 Perimeter Problem:\n{self.current_problem}", "tutor")
        self.answer_entry.focus()

    def probability_problem(self):
        """Understanding and applying probability concepts"""
        problem_types = ['basic_probability', 'certain_impossible', 'likely_unlikely']
        problem_type = random.choice(problem_types)

        if problem_type == 'basic_probability':
            colors = ['red', 'blue', 'green', 'yellow']
            target_color = random.choice(colors)
            total_balls = random.randint(5, 10)
            target_balls = random.randint(1, total_balls-1)

            self.current_problem = f"In a bag, there are {target_balls} {target_color} balls and {total_balls - target_balls} other colored balls. What is the chance of picking a {target_color} ball? (likely, unlikely, certain, impossible)"

            if target_balls > total_balls // 2:
                self.current_answer = "likely"
            elif target_balls == total_balls:
                self.current_answer = "certain"
            elif target_balls == 0:
                self.current_answer = "impossible"
            else:
                self.current_answer = "unlikely"

            self.current_steps = [
                f"There are {target_balls} {target_color} balls out of {total_balls} total balls",
                f"If more than half are {target_color}, it's likely",
                f"If less than half are {target_color}, it's unlikely",
                f"Answer: {self.current_answer}"
            ]

        elif problem_type == 'certain_impossible':
            scenarios = [
                ("The sun will rise tomorrow", "certain"),
                ("You will grow wings and fly", "impossible"),
                ("It will rain sometime this year", "likely"),
                ("You will meet a dinosaur today", "impossible"),
                ("You will breathe air today", "certain")
            ]
            scenario, answer = random.choice(scenarios)
            self.current_problem = f"Is this certain, impossible, likely, or unlikely: '{scenario}'?"
            self.current_answer = answer
            self.current_steps = [
                f"Let's think about: {scenario}",
                f"Certain = will definitely happen",
                f"Impossible = will never happen",
                f"Likely = probably will happen",
                f"Unlikely = probably won't happen",
                f"Answer: {answer}"
            ]

        else:  # likely_unlikely
            activities = [
                ("It will rain in the desert", "unlikely"),
                ("A coin will land on heads or tails", "certain"),
                ("You will eat food today", "likely"),
                ("You will win the lottery", "unlikely"),
                ("The sun will set tonight", "certain")
            ]
            activity, answer = random.choice(activities)
            self.current_problem = f"Is this likely, unlikely, certain, or impossible: '{activity}'?"
            self.current_answer = answer
            self.current_steps = [
                f"Let's analyze: {activity}",
                f"Think about how often this happens",
                f"Answer: {answer}"
            ]

        self.student_data['topics_practiced'].add('Probability')
        self.hint_count = 0
        self.add_message(f"🎲 Probability Problem:\n{self.current_problem}", "tutor")
        self.answer_entry.focus()

    def word_problem(self):
        """Word problems incorporating P2 curriculum topics"""
        problem_categories = ['shopping', 'measurement', 'school', 'geometry']
        category = random.choice(problem_categories)

        if category == 'shopping':
            item1 = random.choice(['apples', 'bananas', 'oranges', 'mangoes'])
            item2 = random.choice(['notebooks', 'pencils', 'erasers', 'rulers'])
            price1 = random.randint(100, 800)  # Rwanda Francs
            price2 = random.randint(50, 500)

            operation = random.choice(['addition', 'subtraction'])
            if operation == 'addition':
                self.current_problem = f"Marie bought {item1} for {price1} Rwf and {item2} for {price2} Rwf. How much did she spend in total?"
                self.current_answer = str(price1 + price2)
                self.current_steps = [
                    f"Marie spent {price1} Rwf on {item1}",
                    f"She spent {price2} Rwf on {item2}",
                    f"Total = {price1} + {price2} = {price1 + price2} Rwf"
                ]
            else:
                if price1 > price2:
                    self.current_problem = f"Jean had {price1} Rwf. He bought something for {price2} Rwf. How much money does he have left?"
                    self.current_answer = str(price1 - price2)
                    self.current_steps = [
                        f"Jean started with {price1} Rwf",
                        f"He spent {price2} Rwf",
                        f"Money left = {price1} - {price2} = {price1 - price2} Rwf"
                    ]
                else:
                    # Swap to ensure positive result
                    self.current_problem = f"Jean had {price2} Rwf. He bought something for {price1} Rwf. How much money does he have left?"
                    self.current_answer = str(price2 - price1)
                    self.current_steps = [
                        f"Jean started with {price2} Rwf",
                        f"He spent {price1} Rwf",
                        f"Money left = {price2} - {price1} = {price2 - price1} Rwf"
                    ]

        elif category == 'measurement':
            measurements = [
                ('height', 'meters', random.randint(1, 3)),
                ('length', 'centimeters', random.randint(20, 200)),
                ('mass', 'kilograms', random.randint(5, 50)),
                ('capacity', 'liters', random.randint(2, 20))
            ]
            measure_type, unit, value1 = random.choice(measurements)
            value2 = random.randint(1, value1)

            self.current_problem = f"A rope is {value1} {unit} long. If we cut off {value2} {unit}, how long is the remaining rope?"
            self.current_answer = str(value1 - value2)
            self.current_steps = [
                f"Original rope length: {value1} {unit}",
                f"Length cut off: {value2} {unit}",
                f"Remaining length = {value1} - {value2} = {value1 - value2} {unit}"
            ]

        elif category == 'school':
            students = random.randint(20, 40)
            groups = random.randint(2, 8)
            if students % groups == 0:  # Ensure even division
                self.current_problem = f"There are {students} students in Primary 2. The teacher wants to divide them into {groups} equal groups. How many students will be in each group?"
                self.current_answer = str(students // groups)
                self.current_steps = [
                    f"Total students: {students}",
                    f"Number of groups: {groups}",
                    f"Students per group = {students} ÷ {groups} = {students // groups}"
                ]
            else:
                # Adjust to make it work
                students = groups * random.randint(3, 8)
                self.current_problem = f"There are {students} students in Primary 2. The teacher wants to divide them into {groups} equal groups. How many students will be in each group?"
                self.current_answer = str(students // groups)
                self.current_steps = [
                    f"Total students: {students}",
                    f"Number of groups: {groups}",
                    f"Students per group = {students} ÷ {groups} = {students // groups}"
                ]

        else:  # geometry
            shape = random.choice(['square', 'rectangle'])
            if shape == 'square':
                side = random.randint(4, 12)
                self.current_problem = f"A square garden has sides of {side} meters each. What is the perimeter of the garden?"
                self.current_answer = str(4 * side)
                self.current_steps = [
                    f"Square garden with side = {side} meters",
                    f"Perimeter of square = 4 × side",
                    f"Perimeter = 4 × {side} = {4 * side} meters"
                ]
            else:
                length = random.randint(8, 20)
                width = random.randint(4, length-1)
                self.current_problem = f"A rectangular field is {length} meters long and {width} meters wide. What is the perimeter of the field?"
                self.current_answer = str(2 * (length + width))
                self.current_steps = [
                    f"Rectangular field: length = {length}m, width = {width}m",
                    f"Perimeter = 2 × (length + width)",
                    f"Perimeter = 2 × ({length} + {width}) = {2 * (length + width)} meters"
                ]

        self.student_data['topics_practiced'].add('Word Problems')
        self.hint_count = 0
        self.add_message(f"📚 Word Problem:\n{self.current_problem}", "tutor")
        self.answer_entry.focus()

    def number_to_words(self, num):
        """Convert number to words (English)"""
        if num == 0:
            return "zero"

        ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
                "seventeen", "eighteen", "nineteen"]

        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

        result = ""

        if num >= 100:
            result += ones[num // 100] + " hundred"
            num %= 100
            if num > 0:
                result += " "

        if num >= 20:
            result += tens[num // 10]
            num %= 10
            if num > 0:
                result += "-" + ones[num]
        elif num > 0:
            result += ones[num]

        return result

    def get_hint(self):
        if not self.current_problem:
            self.add_message("Please select a problem type first!", "tutor")
            return

        if self.hint_count < len(self.current_steps):
            hint = self.current_steps[self.hint_count]
            self.add_message(f"💡 Hint {self.hint_count + 1}: {hint}", "tutor")
            self.hint_count += 1
        else:
            self.add_message("💡 No more hints available! Try to solve it with the steps provided.", "tutor")

    def check_answer(self, event=None):
        if not self.current_problem:
            self.add_message("Please select a problem type first!", "tutor")
            return

        user_answer = self.answer_entry.get().strip()
        if not user_answer:
            self.add_message("Please enter your answer!", "tutor")
            return

        self.add_message(user_answer, "student")

        # Check if answer is correct
        try:
            # Handle different answer types
            if isinstance(self.current_answer, str):
                # For text answers (like units, shapes, probability)
                is_correct = user_answer.lower().strip() == self.current_answer.lower().strip()
            else:
                # For numeric answers
                is_correct = float(user_answer) == float(self.current_answer)

            if is_correct:
                self.student_data['problems_solved'] += 1
                self.student_data['correct_answers'] += 1

                encouragement = random.choice([
                    "🎉 Byiza cyane! (Very good!)",
                    "👏 Ni ukuri! (That's correct!)",
                    "⭐ Wakoze neza! (Well done!)",
                    "🌟 Excellent work!",
                    "🎊 Urakoze! (Thank you!) Perfect answer!"
                ])

                self.add_message(f"{encouragement} You got it right!\n\nHere's the complete solution:", "tutor")

                # Show complete solution
                for i, step in enumerate(self.current_steps, 1):
                    self.add_message(f"Step {i}: {step}", "tutor")

            else:
                self.student_data['problems_solved'] += 1

                self.add_message(f"Ntabwo ari ukuri (Not quite right). The correct answer is {self.current_answer}.\n\nLet me show you how to solve it:", "tutor")

                # Show complete solution
                for i, step in enumerate(self.current_steps, 1):
                    self.add_message(f"Step {i}: {step}", "tutor")

        except ValueError:
            self.add_message("Please enter a valid answer!", "tutor")
            return

        # Clear the problem
        self.current_problem = None
        self.current_answer = None
        self.current_steps = []
        self.answer_entry.delete(0, tk.END)

        # Save progress
        self.save_progress()
        self.update_progress_display()

        # Encourage next problem
        self.add_message("Witeguye indi nkuru? (Ready for another problem?) Choose a topic above! 🚀", "tutor")

    def get_accuracy(self):
        if self.student_data['problems_solved'] == 0:
            return 0.0
        return (self.student_data['correct_answers'] / self.student_data['problems_solved']) * 100

    def update_progress_display(self):
        # Update the progress display in the info frame
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == '#d1e7dd':
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.config(text=f"Problems Solved: {self.student_data['problems_solved']} | "
                                         f"Accuracy: {self.get_accuracy():.1f}% | "
                                         f"Level: {self.student_data['difficulty_level']}")

    def save_progress(self):
        try:
            # Convert set to list for JSON serialization
            data_to_save = self.student_data.copy()
            data_to_save['topics_practiced'] = list(data_to_save['topics_practiced'])

            with open('rwanda_p2_math_progress.json', 'w') as f:
                json.dump(data_to_save, f)
        except Exception as e:
            print(f"Could not save progress: {e}")

    def load_progress(self):
        try:
            if os.path.exists('rwanda_p2_math_progress.json'):
                with open('rwanda_p2_math_progress.json', 'r') as f:
                    data = json.load(f)
                    self.student_data.update(data)
                    # Convert list back to set
                    self.student_data['topics_practiced'] = set(self.student_data['topics_practiced'])
        except Exception as e:
            print(f"Could not load progress: {e}")

    def run(self):
        self.root.mainloop()

# Additional utility functions for P2 curriculum
class RwandanP2MathUtils:
    @staticmethod
    def is_valid_p2_number(num):
        """Check if number is within P2 range (0-999)"""
        return 0 <= num <= 999

    @staticmethod
    def convert_to_rwandan_francs(amount):
        """Format amount as Rwandan Francs"""
        return f"{amount} Rwf"

    @staticmethod
    def get_shape_properties(shape):
        """Get properties of geometric shapes for P2 level"""
        properties = {
            'square': {'sides': 4, 'angles': 4, 'equal_sides': True},
            'rectangle': {'sides': 4, 'angles': 4, 'equal_sides': False},
            'triangle': {'sides': 3, 'angles': 3, 'equal_sides': False},
            'circle': {'sides': 0, 'angles': 0, 'equal_sides': False}
        }
        return properties.get(shape, {})

    @staticmethod
    def metric_conversion_factor(from_unit, to_unit):
        """Get conversion factors for metric units"""
        conversions = {
            ('m', 'cm'): 100,
            ('cm', 'm'): 0.01,
            ('l', 'ml'): 1000,
            ('ml', 'l'): 0.001,
            ('kg', 'g'): 1000,
            ('g', 'kg'): 0.001
        }
        return conversions.get((from_unit, to_unit), 1)

# Main execution
if __name__ == "__main__":
    print("🇷🇼 Starting Rwandan P2 Math Tutor System...")
    print("📚 Based on Republic of Rwanda Primary Two Curriculum:")
    print("   ✅ Numeration and Operations (0-999)")
    print("   ✅ Number comparison")
    print("   ✅ Addition and Subtraction (up to 999)")
    print("   ✅ Multiplication and Division")
    print("   ✅ Metric Systems (Length, Capacity, Mass)")
    print("   ✅ Unit Conversions")
    print("   ✅ Geometric Figures (Squares, Rectangles, Triangles)")
    print("   ✅ Perimeter Calculations")
    print("   ✅ Probability Concepts")
    print("   ✅ Contextual Word Problems")
    print("\n🎯 Perfectly aligned with Rwandan Primary Education Standards!")
    print("🌟 Features Kinyarwanda greetings and local context")

    # Create and run the tutor
    tutor = RwandanP2MathTutor()
    tutor.run()

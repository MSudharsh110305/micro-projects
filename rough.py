"""
Simplified Python Dataclasses Demonstration Program
Comparing regular class vs dataclass with all decorator parameters
"""

from dataclasses import dataclass, field, asdict, astuple, replace, InitVar
from typing import ClassVar, List, Dict

# ============================================================================
# REGULAR CLASS (Traditional Approach)
# ============================================================================

class RegularStudent:
    """Traditional class with manual implementation of all methods"""
    
    school_name = "Regular High School"  # Class variable
    
    def __init__(self, name: str, grade: int, subjects: List[str] = None):
        self.name = name
        self.grade = grade
        self.subjects = subjects if subjects is not None else []  # Avoid mutable default
        self.student_id = f"REG{hash(name) % 1000:03d}"
    
    def __repr__(self):
        return f"RegularStudent(name='{self.name}', grade={self.grade}, subjects={self.subjects})"
    
    def __eq__(self, other):
        if not isinstance(other, RegularStudent):
            return False
        return self.name == other.name and self.grade == other.grade
    
    def __lt__(self, other):
        if not isinstance(other, RegularStudent):
            return NotImplemented
        return (self.grade, self.name) < (other.grade, other.name)

# ============================================================================
# DATACLASS EXAMPLES - ALL DECORATOR PARAMETERS DEMONSTRATED
# ============================================================================

print("=" * 60)
print("DATACLASS DECORATOR PARAMETERS DEMONSTRATION")
print("=" * 60)

# Example 1: ALL PARAMETERS SET TO TRUE
@dataclass(
    init=True,          # ✅ Generate __init__ method
    repr=True,          # ✅ Generate __repr__ method  
    eq=True,            # ✅ Generate __eq__ method
    order=True,         # ✅ Generate ordering methods (__lt__, __gt__, etc.)
    unsafe_hash=True,   # ✅ Force __hash__ generation 
    frozen=False        # ❌ Don't make immutable (can modify after creation)
)
class AllTrueStudent:
    """Dataclass with all decorator parameters set to True"""
    
    school_name: ClassVar[str] = "All True High School"
    
    name: str
    grade: int
    subjects: List[str] = field(default_factory=list)
    gpa: float = 0.0

print("\n--- Example 1: All Parameters True ---")
student1 = AllTrueStudent("Alice", 10, ["Math", "Science"], 3.8)
student2 = AllTrueStudent("Bob", 9, ["English", "History"], 3.5)

print(f"Student 1: {student1}")                    # Works: repr=True
print(f"Student 2: {student2}")                    # Works: repr=True
print(f"student1 == student2: {student1 == student2}")  # Works: eq=True  
print(f"student1 > student2: {student1 > student2}")    # Works: order=True
print(f"Hash of student1: {hash(student1)}")           # Works: unsafe_hash=True

# Can modify because frozen=False
student1.gpa = 4.0
print(f"Modified GPA: {student1.gpa}")

# ============================================================================

# Example 2: SOME PARAMETERS SET TO FALSE
@dataclass(
    init=True,          # ✅ Generate __init__
    repr=False,         # ❌ DON'T generate __repr__ 
    eq=False,           # ❌ DON'T generate __eq__
    order=False,        # ❌ DON'T generate ordering methods
    unsafe_hash=False,  # ❌ Don't force hash
    frozen=False        # ❌ Not immutable
)
class SomeFalseStudent:
    """Dataclass with some parameters set to False"""
    
    name: str
    grade: int
    age: int = 16

print("\n--- Example 2: Some Parameters False ---")
student3 = SomeFalseStudent("Charlie", 11)
student4 = SomeFalseStudent("Diana", 11)

print(f"Student 3: {student3}")  # Uses default object repr (not pretty)
print(f"student3 == student4: {student3 == student4}")  # Uses identity comparison (False)

# These would cause errors:
# print(student3 > student4)  # Error: order=False, no ordering methods
# print(hash(student3))       # Error: not hashable

# ============================================================================

# Example 3: FROZEN=TRUE (Immutable)
@dataclass(
    init=True,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,  # Let dataclass auto-decide hash (will be True because frozen=True)
    frozen=True         # ✅ Make IMMUTABLE
)
class FrozenStudent:
    """Immutable dataclass - cannot modify after creation"""
    
    name: str
    grade: int
    final_score: float = 0.0

print("\n--- Example 3: Frozen (Immutable) ---")
frozen_student = FrozenStudent("Eva", 12, 95.5)
print(f"Frozen student: {frozen_student}")

# This student is hashable because frozen=True
print(f"Hash: {hash(frozen_student)}")

# This would cause FrozenInstanceError:
try:
    frozen_student.grade = 13
except Exception as e:
    print(f"Error modifying frozen dataclass: {type(e).__name__}")

# ============================================================================

# Example 4: FIELD CONFIGURATIONS
@dataclass
class FieldDemoStudent:
    """Demonstrating different field() configurations"""
    
    # Required field
    name: str
    
    # Field with simple default
    grade: int = 10
    
    # Field with default_factory (for mutable types)
    subjects: List[str] = field(default_factory=list)
    courses: Dict[str, int] = field(default_factory=dict)
    
    # Field excluded from __repr__ (sensitive data)
    student_id: str = field(repr=False, default="UNKNOWN")
    
    # Field excluded from comparison
    nickname: str = field(compare=False, default="")
    
    # Field not included in __init__ (computed later)
    full_info: str = field(init=False, default="")
    
    # Field with metadata
    gpa: float = field(default=0.0, metadata={"min": 0.0, "max": 4.0})
    
    def __post_init__(self):
        """Called after __init__ to compute derived fields"""
        self.full_info = f"{self.name} (Grade {self.grade})"
        if not self.student_id or self.student_id == "UNKNOWN":
            self.student_id = f"STU{hash(self.name) % 1000:03d}"

print("\n--- Example 4: Field Configurations ---")
field_student = FieldDemoStudent("Frank", 11)
field_student.subjects.extend(["Math", "Physics"])
field_student.courses = {"Math": 95, "Physics": 88}

print(f"Field demo student: {field_student}")  # student_id not shown (repr=False)
print(f"Full info: {field_student.full_info}")
print(f"Student ID: {field_student.student_id}")

# ============================================================================

# Example 5: USING InitVar
@dataclass
class InitVarStudent:
    """Demonstrating InitVar - parameter only for initialization"""
    
    name: str
    base_grade: int
    
    # InitVar is passed to __post_init__ but not stored as field
    bonus_points: InitVar[int] = 0
    
    # Computed field
    final_grade: int = field(init=False)
    
    def __post_init__(self, bonus_points):
        """InitVar parameter is passed here"""
        self.final_grade = min(self.base_grade + bonus_points, 12)  # Max grade 12

print("\n--- Example 5: InitVar Usage ---")
initvar_student = InitVarStudent("Grace", 9, bonus_points=2)
print(f"InitVar student: {initvar_student}")
print(f"Final grade: {initvar_student.final_grade}")

# bonus_points is not stored as an attribute:
print(f"Has bonus_points attribute: {hasattr(initvar_student, 'bonus_points')}")

# ============================================================================

# Example 6: DEFAULT vs DEFAULT_FACTORY Demonstration
print("\n" + "="*50)
print("DEFAULT vs DEFAULT_FACTORY DEMONSTRATION")
print("="*50)

# WRONG WAY - Mutable default
@dataclass
class BadStudent:
    name: str
    grades: List[int] = []  # ⚠️ DANGEROUS! All instances share same list

# CORRECT WAY - Using default_factory
@dataclass
class GoodStudent:
    name: str
    grades: List[int] = field(default_factory=list)  # ✅ Each instance gets new list

print("\n--- Bad Example (Shared Mutable Default) ---")
bad1 = BadStudent("Bad1")
bad2 = BadStudent("Bad2")

bad1.grades.append(85)
print(f"bad1.grades: {bad1.grades}")  # [85]
print(f"bad2.grades: {bad2.grades}")  # [85] - OOPS! They share the same list

print("\n--- Good Example (default_factory) ---")
good1 = GoodStudent("Good1") 
good2 = GoodStudent("Good2")

good1.grades.append(85)
print(f"good1.grades: {good1.grades}")  # [85]
print(f"good2.grades: {good2.grades}")  # [] - Correct! Separate lists

# ============================================================================

# Example 7: INHERITANCE
@dataclass
class Person:
    """Base dataclass"""
    name: str
    age: int

@dataclass
class Student(Person):
    """Inherited dataclass"""
    grade: int
    school: str = "Unknown School"

print("\n--- Example 7: Inheritance ---")
inherited_student = Student("Henry", 16, 10, "Math High")
print(f"Inherited student: {inherited_student}")

# ============================================================================

# Example 8: UTILITY FUNCTIONS
@dataclass
class SimpleStudent:
    name: str
    grade: int
    subjects: List[str] = field(default_factory=list)

print("\n--- Example 8: Utility Functions ---")
util_student = SimpleStudent("Ivy", 11, ["Biology", "Chemistry"])

# Convert to dictionary
student_dict = asdict(util_student)
print(f"As dictionary: {student_dict}")

# Convert to tuple
student_tuple = astuple(util_student)  
print(f"As tuple: {student_tuple}")

# Create modified copy
modified_student = replace(util_student, grade=12)
print(f"Modified copy: {modified_student}")
print(f"Original unchanged: {util_student}")

# ============================================================================

# COMPARISON SUMMARY
print("\n" + "="*60)
print("DECORATOR PARAMETER EFFECTS SUMMARY")
print("="*60)

effects = {
    "init=True":  "✅ Auto-generates __init__ method",
    "init=False": "❌ No __init__, you must provide your own",
    
    "repr=True":  "✅ Auto-generates nice __repr__ method", 
    "repr=False": "❌ Uses default object __repr__ (not readable)",
    
    "eq=True":    "✅ Auto-generates __eq__ for value comparison",
    "eq=False":   "❌ Uses identity comparison (is)",
    
    "order=True": "✅ Generates __lt__, __gt__, etc. for sorting",
    "order=False": "❌ No ordering methods, can't sort or compare",
    
    "unsafe_hash=True": "✅ Forces __hash__ generation",
    "unsafe_hash=False": "❌ Hash only if frozen=True or specific conditions",
    
    "frozen=True":  "✅ Immutable after creation, automatically hashable",
    "frozen=False": "❌ Mutable, fields can be changed after creation"
}

for param, effect in effects.items():
    print(f"{param:20} -> {effect}")

print("\n" + "="*60) 
print("FIELD PARAMETERS SUMMARY")
print("="*60)

field_effects = {
    "default=value": "Simple default value (for immutable types)",
    "default_factory=func": "Function to create default (for mutable types)", 
    "init=False": "Exclude from __init__, compute in __post_init__",
    "repr=False": "Hide from string representation",
    "compare=False": "Exclude from equality/ordering comparisons"
}

for param, effect in field_effects.items():
    print(f"{param:25} -> {effect}")

print("\n🎉 All dataclass features demonstrated with simple examples!")

class Student:
    def __init__(self, student_id: str, name: str, weight: int = 1):
        self.id = student_id
        self.name = name
        self.weight = weight
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "weight": self.weight
        }
from typing import Dict


class Prediction:
    def __init__(self, brand: Dict[int, int], gender: Dict[int, int], category: Dict[int, str], score: Dict[int, float], liked: Dict[int, bool]):
        self.brand = brand
        self.gender = gender
        self.category = category
        self.score = score
        self.liked = liked

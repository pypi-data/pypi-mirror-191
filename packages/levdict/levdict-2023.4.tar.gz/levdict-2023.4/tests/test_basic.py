import unittest
from src.levdict import LevDict

DICT_1 = {
    "fruit": {
        "oranges": 10,
        "apples": 20,
        "bananas": 30,
    },
    "vegetables": {
        "carrots": 10,
        "aubergines": 15,
    },
}


class TestBasic(unittest.TestCase):
    def setUp(self) -> None:
        self.dict1 = LevDict(DICT_1)

    def tearDown(self) -> None:
        super().tearDown()

    def test_init(self):
        self.assertEqual(self.dict1.as_dict(), DICT_1)

        dict2 = LevDict(a=1, b=2)
        self.assertEqual(dict2.a, 1)
        self.assertEqual(dict2["a"], 1)
        self.assertEqual(dict2, {"a": 1, "b": 2})

    def test_normal_dict(self):
        result = self.dict1["vegetables"]
        expected = {"carrots": 10, "aubergines": 15}
        self.assertEqual(result, expected)

        result = self.dict1["fruit"]["apples"]
        expected = 20
        self.assertEqual(result, expected)

    def test_dotted_dict(self):
        result = self.dict1.vegetables
        expected = {"carrots": 10, "aubergines": 15}
        self.assertEqual(result, expected)

        result = self.dict1.fruit.apples
        expected = 20
        self.assertEqual(result, expected)

    def test_mixed_dict(self):
        result = self.dict1.fruit["apples"]
        expected = 20
        self.assertEqual(result, expected)

        result = self.dict1["fruit"].apples
        expected = 20
        self.assertEqual(result, expected)

    def test_assignment(self):
        new_dict: LevDict = LevDict(self.dict1)
        new_dict.fruit.oranges = 1
        new_dict.fruit["apples"] = 0

        result = new_dict.fruit
        expected = {"oranges": 1, "apples": 0, "bananas": 30}
        self.assertEqual(result, expected)

    def test_simple_update(self):
        self.dict1.fruit.update(oranges=88)
        self.dict1.fruit.update({"pears": 5})

        result = self.dict1.fruit
        expected = {"oranges": 88, "apples": 20, "bananas": 30, "pears": 5}
        self.assertEqual(result, expected)

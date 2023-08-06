import unittest
from pathlib import Path
from src.levdict import LevDictToml, LevDictJson, LevDictYaml


class TestLevDict(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tfile = Path("tests") / "examples" / "example1.toml"
        self.jfile = self.tfile.with_suffix(".json")
        self.yfile = self.tfile.with_suffix(".yaml")
        self.jfile.unlink(missing_ok=True)
        self.yfile.unlink(missing_ok=True)

    def tearDown(self) -> None:
        super().tearDown()

    def test_load(self):
        self.tdict = LevDictToml()
        self.tdict.load(self.tfile)

        self.jdict = LevDictJson()
        self.jdict.from_dict(self.tdict)

        result = self.jdict.as_dict()
        expected = self.tdict.as_dict()

        self.assertEqual(result, expected)

    def test_save_partial(self):
        self.tdict = LevDictToml()
        self.tdict.load(self.tfile)

        ddd: dict = self.tdict.user.as_dict()

        newd = LevDictToml()
        newd.from_dict({"user": ddd})
        newd.dump(self.tfile.with_stem("example1_mod"), force=True)

        newy = LevDictYaml()
        newy.from_dict({"user": ddd})
        newy.dump(self.tfile.with_suffix(".yaml"), force=True)

        newj = LevDictJson()
        newj.from_dict({"user": ddd})
        newj.dump(self.tfile.with_suffix(".json"), force=True, indent=4)

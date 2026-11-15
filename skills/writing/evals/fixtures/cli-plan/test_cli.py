import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import cli


class LoadTest(unittest.TestCase):
    def test_load_keeps_open_rows(self) -> None:
        with TemporaryDirectory() as temp:
            path = Path(temp) / "incidents.csv"
            path.write_text("id,severity,title,status\n1,high,DB down,open\n2,low,Typo,closed\n", encoding="utf-8")
            self.assertEqual([row["id"] for row in cli.load(str(path))], ["1"])


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
from domain.ports import StoragePort

class LocalFileStorage(StoragePort):
    def __init__(self, base_in: Path = Path("input"), base_out: Path = Path("output")):
        self.base_in = base_in ; self.base_out = base_out
        self.base_in.mkdir(exist_ok=True) ; self.base_out.mkdir(exist_ok=True)

    def read(self, filename: str) -> str:
        return (self.base_in / filename).read_text(encoding="utf-8")

    def write(self, filename: str, content: str) -> str:
        out_path = self.base_out / filename
        out_path.write_text(content, encoding="utf-8")
        return str(out_path)

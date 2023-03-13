from main.src.config.constants import FilePathTo
from main.src.utils.load_files import loadfile


def return_kwargs(qry_name: str, **kwargs: dict) -> str:
    queries = loadfile(FilePathTo.Queries)
    get_qry = " ".join(queries[f'{qry_name}']).format(**kwargs)
    return get_qry

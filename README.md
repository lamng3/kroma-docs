# KROMA API notes

Static API site for [kroma](https://github.com/lamng3/kroma): the command line, the matching run, loaders, query strategies, models, retrieval, refinement, and metrics.

`python3 build.py` rewrites the HTML. GitHub Pages serves the files at the repository root.

## Shared structure

`normalize.py` (a copy of the one in `memcommit-docs`) runs at the end of the build. It gives every content page a search box, an "On this page" list, previous and next links, and one title format, and writes `search-index.json`. It is called by `build.py`.

# Why's this whole module not in the normal test suite (yet)
Getting stuff from infer assumes rollout and by extension deps finder stuff are run from __main__ module
which isn't true for pytest tests.

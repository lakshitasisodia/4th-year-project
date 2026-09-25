"""Compatibility entry point.

The old monolithic trainer has been retired. Use train_pipeline.py so the
training and production inference paths share the same saved pipeline.
"""
from train_pipeline import main

if __name__ == "__main__":
    main()

#!/bin/bash
playwright install --with-deps
python3 ihouse_checker_playwright.py

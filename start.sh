#!/bin/bash
playwright install --with-deps
python ihouse_checker_playwright.py

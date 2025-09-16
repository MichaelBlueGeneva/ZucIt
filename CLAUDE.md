# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ZucIt is a Flask application designed to simulate the effects of the Zucman tax. The application demonstrates economic impacts by modeling company valuations, profits, employee counts, and growth over a 20-year period.

## Key Features

- Company selection from examples (Apple, Microsoft, Google, Startup) or custom company creation
- Modifiable financial parameters (valuation, profit, employee count, growth rate)
- 20-year simulation showing:
  - Company profit evolution (accounting for growth and 2.857% valuation tax impact)
  - Employee count (proportional to profit)
  - State tax revenue (25% profit tax + 2.857% valuation tax under Zucman)
- Interactive charts using Chart.js
- KPI visualization showing Zucman tax effects after 20 years
- Professional responsive web interface

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
# Server runs on http://127.0.0.1:5001

# Test endpoints
curl http://127.0.0.1:5001/company/apple
curl -X POST http://127.0.0.1:5001/simulate -H "Content-Type: application/json" -d '{"valuation": 1000000000, "profit": 50000000, "employees": 1000, "growth_rate": 8}'
```

## Architecture

### Backend (Flask)
- `app.py`: Main Flask application with simulation logic
- `/`: Home page with interactive form
- `/company/<id>`: Get predefined company data
- `/simulate`: POST endpoint for running simulations

### Frontend
- `templates/index.html`: Single-page application with forms and visualization
- `static/css/style.css`: Professional responsive styling
- `static/js/app.js`: Interactive JavaScript with Chart.js integration

### Simulation Logic
- 20-year projection with and without Zucman tax
- Zucman tax: 2.857% on valuation (2% + flat tax)
- Normal tax: 25% on profits
- Growth impact modeling (reduced growth with Zucman)
- Employment impact (proportional to profit changes)

## Tech Stack
- Backend: Flask 2.3.3, Python
- Frontend: Vanilla JavaScript, Chart.js, CSS Grid/Flexbox
- No database required (in-memory data)
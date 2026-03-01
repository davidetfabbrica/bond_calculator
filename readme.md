# 🇬🇧 UK Bond & Gilt Calculator

A desktop application for calculating Yield to Maturity (YTM) and projecting investment returns for UK bonds and gilts.

Built with Python and CustomTkinter as a learning project.

---

## Features

### YTM Calculator
Calculate the Yield to Maturity for any UK bond or gilt by entering:
- Face value, coupon rate, and current market price
- Settlement and maturity dates (DD-MM-YYYY format)
- Coupon frequency (semi-annual, annual, or quarterly)

The app returns the annualised YTM percentage and tells you whether the bond is trading at a discount, premium, or par.

### Investment Projector
Enter an amount you wish to invest and see:
- How many bonds you can purchase at the current price
- Coupon income per payment period and per year
- Total coupon income over the full term
- Capital gain or loss at maturity
- Total return in £ and as a percentage
- A year-by-year income and portfolio value breakdown

---

## Installation

### Prerequisites
- Python 3.11 or higher — [python.org](https://python.org/downloads)
- Git — [git-scm.com](https://git-scm.com)

> **macOS users:** It is recommended to install Python via Homebrew to ensure tkinter GUI support works correctly.
> ```bash
> brew install python-tk
> ```

### Setup

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/bond_calculator.git
cd bond_calculator
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip3 install -r requirements.txt
```

**4. Run the app**
```bash
python3 main.py
```

---

## How to Use

### YTM Calculator

| Field | Description | Example |
|---|---|---|
| Face Value (£) | The nominal/par value of the bond | 100 |
| Annual Coupon Rate (%) | The bond's annual interest rate | 4.5 |
| Current Market Price (£) | The price you would pay today | 97.50 |
| Settlement Date | The date of purchase (DD-MM-YYYY) | 01-03-2026 |
| Maturity Date | The date the bond matures (DD-MM-YYYY) | 01-03-2031 |
| Coupon Frequency | How often interest is paid | Semi-Annual |

Click **Calculate YTM** to see the result.

> 💡 For UK gilts, face value is typically £100 and coupon frequency is semi-annual.

### Investment Projector

Fill in the same bond details as above, then enter an **Amount to Invest (£)**. Click **Project Returns** to see a full breakdown of your projected returns and a year-by-year income table.

---

## Project Structure

```
bond_calculator/
│
├── main.py                 # App entry point — launches the UI
│
├── logic/
│   ├── __init__.py
│   └── calculator.py       # All financial calculation logic (no UI)
│
├── ui/
│   ├── __init__.py
│   └── app_window.py       # All UI layout and interaction (no logic)
│
├── requirements.txt        # Python dependencies
└── README.md
```

The project deliberately separates UI code from calculation logic. This means:
- The maths can be tested independently of the interface
- Either layer can be changed without affecting the other
- The codebase is easy to navigate and extend

---

## How YTM is Calculated

Yield to Maturity cannot be solved algebraically — it requires an iterative numerical approach. This app uses **Brent's method** via `scipy.optimize.brentq` to find the discount rate that makes the present value of all future cash flows (coupons + face value repayment) equal to the bond's current market price.

This is the same approach used by financial professionals and is accurate to 10 decimal places.

---

## Dependencies

| Package | Purpose |
|---|---|
| customtkinter | Modern desktop UI framework |
| scipy | Numerical solver for YTM calculation |

---

## Limitations

- Assumes clean pricing (no accrued interest calculation)
- Does not account for tax on coupon income
- Capital gains on gilts are currently tax-free for UK investors — please verify current HMRC rules before making investment decisions

---

## Disclaimer

This tool is for educational purposes only and does not constitute financial advice. Always consult a qualified financial adviser before making investment decisions.

---

## Licence

MIT License — see [LICENSE](LICENSE) for details.
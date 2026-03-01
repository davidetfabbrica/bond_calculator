# ui/app_window.py
# ---------------------------------------------------------------
# This module defines the entire UI for the Bond Calculator app.
# It imports from logic/calculator.py to perform calculations,
# but contains no financial logic itself.
# ---------------------------------------------------------------

import customtkinter as ctk
from datetime import date
from logic.calculator import calculate_ytm, calculate_investment_returns


# --- App Appearance ---
# CustomTkinter supports "light", "dark", or "system" themes
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class BondCalculatorApp(ctk.CTk):
    """
    Main application window.
    Inherits from CTk (CustomTkinter's main window class).
    Contains two tabs: YTM Calculator and Investment Projector.
    """

    def __init__(self):
        super().__init__()

        # --- Window configuration ---
        self.title("UK Bond & Gilt Calculator")
        self.geometry("680x750")
        self.resizable(False, False)  # Fixed size for consistent layout

        # --- Main heading ---
        heading = ctk.CTkLabel(
            self,
            text="🇬🇧 UK Bond & Gilt Calculator",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        heading.pack(pady=(24, 4))

        subtitle = ctk.CTkLabel(
            self,
            text="Calculate Yield to Maturity and projected investment returns",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 16))

        # --- Tab view ---
        self.tabs = ctk.CTkTabview(self, width=640, height=640)
        self.tabs.pack(padx=20, pady=(0, 20))

        # Create the two tabs
        self.tabs.add("YTM Calculator")
        self.tabs.add("Investment Projector")

        # Build content for each tab
        self._build_ytm_tab()
        self._build_investment_tab()

    # ==============================================================
    # TAB 1: YTM CALCULATOR
    # ==============================================================

    def _build_ytm_tab(self):
        """Build all widgets for the YTM Calculator tab."""

        tab = self.tabs.tab("YTM Calculator")

        ctk.CTkLabel(
            tab,
            text="Bond Details",
            font=ctk.CTkFont(size=15, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(16, 8), sticky="w", padx=20)

        # Face Value
        ctk.CTkLabel(tab, text="Face Value (£)").grid(
            row=1, column=0, padx=20, pady=8, sticky="w")
        self.ytm_face_value = ctk.CTkEntry(
            tab, placeholder_text="e.g. 100", width=260)
        self.ytm_face_value.grid(row=1, column=1, padx=20, pady=8)

        # Coupon Rate
        ctk.CTkLabel(tab, text="Annual Coupon Rate (%)").grid(
            row=2, column=0, padx=20, pady=8, sticky="w")
        self.ytm_coupon_rate = ctk.CTkEntry(
            tab, placeholder_text="e.g. 4.5", width=260)
        self.ytm_coupon_rate.grid(row=2, column=1, padx=20, pady=8)

        # Market Price
        ctk.CTkLabel(tab, text="Current Market Price (£)").grid(
            row=3, column=0, padx=20, pady=8, sticky="w")
        self.ytm_market_price = ctk.CTkEntry(
            tab, placeholder_text="e.g. 97.50", width=260)
        self.ytm_market_price.grid(row=3, column=1, padx=20, pady=8)

        # Settlement Date — UK format DD-MM-YYYY
        ctk.CTkLabel(tab, text="Settlement Date (DD-MM-YYYY)").grid(
            row=4, column=0, padx=20, pady=8, sticky="w")
        self.ytm_settlement = ctk.CTkEntry(
            tab, placeholder_text=date.today().strftime("%d-%m-%Y"), width=260)
        self.ytm_settlement.grid(row=4, column=1, padx=20, pady=8)

        # Maturity Date — UK format DD-MM-YYYY
        ctk.CTkLabel(tab, text="Maturity Date (DD-MM-YYYY)").grid(
            row=5, column=0, padx=20, pady=8, sticky="w")
        self.ytm_maturity = ctk.CTkEntry(
            tab, placeholder_text="e.g. 01-03-2031", width=260)
        self.ytm_maturity.grid(row=5, column=1, padx=20, pady=8)

        # Coupon Frequency dropdown
        ctk.CTkLabel(tab, text="Coupon Frequency").grid(
            row=6, column=0, padx=20, pady=8, sticky="w")
        self.ytm_frequency = ctk.CTkOptionMenu(
            tab,
            values=["Semi-Annual (UK Standard)", "Annual", "Quarterly"],
            width=260
        )
        self.ytm_frequency.grid(row=6, column=1, padx=20, pady=8)
        self.ytm_frequency.set("Semi-Annual (UK Standard)")

        # Calculate button
        self.ytm_button = ctk.CTkButton(
            tab,
            text="Calculate YTM",
            command=self._run_ytm_calculation,
            width=300,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.ytm_button.grid(row=7, column=0, columnspan=2, pady=(20, 8))

        # Result display — shown in green when calculation succeeds
        self.ytm_result_label = ctk.CTkLabel(
            tab,
            text="",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#2ecc71"
        )
        self.ytm_result_label.grid(row=8, column=0, columnspan=2, pady=4)

        # Secondary result line — shows coupon vs YTM context
        self.ytm_context_label = ctk.CTkLabel(
            tab,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.ytm_context_label.grid(row=9, column=0, columnspan=2, pady=2)

        # Error label — shown in red when something goes wrong
        self.ytm_error_label = ctk.CTkLabel(
            tab,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#e74c3c"
        )
        self.ytm_error_label.grid(row=10, column=0, columnspan=2, pady=4)

    # ==============================================================
    # TAB 2: INVESTMENT PROJECTOR
    # ==============================================================

    def _build_investment_tab(self):
        """Build all widgets for the Investment Projector tab."""

        tab = self.tabs.tab("Investment Projector")

        ctk.CTkLabel(
            tab,
            text="Bond Details",
            font=ctk.CTkFont(size=15, weight="bold")
        ).grid(row=0, column=0, columnspan=2, pady=(16, 8), sticky="w", padx=20)

        # Face Value
        ctk.CTkLabel(tab, text="Face Value (£)").grid(
            row=1, column=0, padx=20, pady=6, sticky="w")
        self.inv_face_value = ctk.CTkEntry(
            tab, placeholder_text="e.g. 100", width=260)
        self.inv_face_value.grid(row=1, column=1, padx=20, pady=6)

        # Coupon Rate
        ctk.CTkLabel(tab, text="Annual Coupon Rate (%)").grid(
            row=2, column=0, padx=20, pady=6, sticky="w")
        self.inv_coupon_rate = ctk.CTkEntry(
            tab, placeholder_text="e.g. 4.5", width=260)
        self.inv_coupon_rate.grid(row=2, column=1, padx=20, pady=6)

        # Market Price
        ctk.CTkLabel(tab, text="Current Market Price (£)").grid(
            row=3, column=0, padx=20, pady=6, sticky="w")
        self.inv_market_price = ctk.CTkEntry(
            tab, placeholder_text="e.g. 97.50", width=260)
        self.inv_market_price.grid(row=3, column=1, padx=20, pady=6)

        # Settlement Date — UK format DD-MM-YYYY
        ctk.CTkLabel(tab, text="Settlement Date (DD-MM-YYYY)").grid(
            row=4, column=0, padx=20, pady=6, sticky="w")
        self.inv_settlement = ctk.CTkEntry(
            tab, placeholder_text=date.today().strftime("%d-%m-%Y"), width=260)
        self.inv_settlement.grid(row=4, column=1, padx=20, pady=6)

        # Maturity Date — UK format DD-MM-YYYY
        ctk.CTkLabel(tab, text="Maturity Date (DD-MM-YYYY)").grid(
            row=5, column=0, padx=20, pady=6, sticky="w")
        self.inv_maturity = ctk.CTkEntry(
            tab, placeholder_text="e.g. 01-03-2031", width=260)
        self.inv_maturity.grid(row=5, column=1, padx=20, pady=6)

        # Coupon Frequency
        ctk.CTkLabel(tab, text="Coupon Frequency").grid(
            row=6, column=0, padx=20, pady=6, sticky="w")
        self.inv_frequency = ctk.CTkOptionMenu(
            tab,
            values=["Semi-Annual (UK Standard)", "Annual", "Quarterly"],
            width=260
        )
        self.inv_frequency.grid(row=6, column=1, padx=20, pady=6)
        self.inv_frequency.set("Semi-Annual (UK Standard)")

        # Investment Amount
        ctk.CTkLabel(
            tab,
            text="Amount to Invest (£)",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=7, column=0, padx=20, pady=6, sticky="w")
        self.inv_amount = ctk.CTkEntry(
            tab, placeholder_text="e.g. 5000", width=260)
        self.inv_amount.grid(row=7, column=1, padx=20, pady=6)

        # Calculate button
        self.inv_button = ctk.CTkButton(
            tab,
            text="Project Returns",
            command=self._run_investment_calculation,
            width=300,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.inv_button.grid(row=8, column=0, columnspan=2, pady=(16, 8))

        # Scrollable results text box — monospace font keeps columns aligned
        self.inv_result_box = ctk.CTkTextbox(
            tab,
            width=580,
            height=200,
            font=ctk.CTkFont(family="Courier", size=12),
            state="disabled"  # Read-only; we enable it briefly to write results
        )
        self.inv_result_box.grid(
            row=9, column=0, columnspan=2, padx=20, pady=(0, 8))

        # Error label
        self.inv_error_label = ctk.CTkLabel(
            tab,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#e74c3c"
        )
        self.inv_error_label.grid(row=10, column=0, columnspan=2)

    # ==============================================================
    # HELPER METHODS
    # ==============================================================

    def _parse_date(self, date_string: str) -> date:
        """
        Parse a date string in DD-MM-YYYY format (UK standard).
        Splits on hyphens and reassembles in the order Python expects (Y, M, D).
        Raises ValueError with a friendly message if format is wrong.
        """
        try:
            day, month, year = date_string.strip().split("-")
            return date(int(year), int(month), int(day))
        except (ValueError, IndexError):
            raise ValueError(
                f"Invalid date '{date_string}' — please use DD-MM-YYYY format (e.g. 01-03-2031)."
            )

    def _parse_float(self, value_string: str, field_name: str) -> float:
        """
        Parse a string to float.
        Raises ValueError with a friendly message if not a valid number.
        """
        try:
            return float(value_string.strip())
        except ValueError:
            raise ValueError(f"'{field_name}' must be a number (e.g. 4.5).")

    def _frequency_to_int(self, frequency_string: str) -> int:
        """Convert the dropdown selection string to an integer."""
        mapping = {
            "Semi-Annual (UK Standard)": 2,
            "Annual": 1,
            "Quarterly": 4
        }
        return mapping[frequency_string]

    def _clear_ytm_results(self):
        """Clear any previous results or errors from the YTM tab."""
        self.ytm_result_label.configure(text="")
        self.ytm_context_label.configure(text="")
        self.ytm_error_label.configure(text="")

    def _clear_inv_results(self):
        """Clear any previous results or errors from the Investment tab."""
        self.inv_error_label.configure(text="")
        # Enable the textbox briefly to clear it, then disable again
        self.inv_result_box.configure(state="normal")
        self.inv_result_box.delete("1.0", "end")
        self.inv_result_box.configure(state="disabled")

    # ==============================================================
    # CALCULATION HANDLERS
    # ==============================================================

    def _run_ytm_calculation(self):
        """
        Reads inputs from the YTM tab, calls calculate_ytm(),
        and displays the result or a friendly error message.
        """
        # Always clear previous results before a new calculation
        self._clear_ytm_results()

        try:
            # --- Read and parse all inputs ---
            # If any field is empty or invalid, _parse_float/_parse_date
            # will raise a ValueError with a helpful message
            face_value = self._parse_float(
                self.ytm_face_value.get(), "Face Value")
            coupon_rate = self._parse_float(
                self.ytm_coupon_rate.get(), "Coupon Rate")
            market_price = self._parse_float(
                self.ytm_market_price.get(), "Market Price")
            settlement = self._parse_date(self.ytm_settlement.get())
            maturity = self._parse_date(self.ytm_maturity.get())
            frequency = self._frequency_to_int(self.ytm_frequency.get())

            # --- Run the calculation ---
            ytm = calculate_ytm(
                face_value=face_value,
                coupon_rate=coupon_rate,
                market_price=market_price,
                settlement_date=settlement,
                maturity_date=maturity,
                coupon_frequency=frequency
            )

            # --- Display the result ---
            self.ytm_result_label.configure(
                text=f"Yield to Maturity: {ytm:.4f}%"
            )

            # Show helpful context — is the bond trading at discount or premium?
            # A YTM above the coupon rate means the bond was bought at a discount
            # A YTM below the coupon rate means it was bought at a premium
            if ytm > coupon_rate:
                context = f"Bond trading at a discount (price below face value) — YTM > coupon rate of {coupon_rate}%"
            elif ytm < coupon_rate:
                context = f"Bond trading at a premium (price above face value) — YTM < coupon rate of {coupon_rate}%"
            else:
                context = f"Bond trading at par — YTM equals the coupon rate of {coupon_rate}%"

            self.ytm_context_label.configure(text=context)

        except ValueError as e:
            # Display the error message in red — no crash, just clear feedback
            self.ytm_error_label.configure(text=str(e))

    def _run_investment_calculation(self):
        """
        Reads inputs from the Investment tab, calls calculate_investment_returns(),
        and displays a formatted breakdown of projected returns.
        """
        # Always clear previous results before a new calculation
        self._clear_inv_results()

        try:
            # --- Read and parse all inputs ---
            face_value = self._parse_float(
                self.inv_face_value.get(), "Face Value")
            coupon_rate = self._parse_float(
                self.inv_coupon_rate.get(), "Coupon Rate")
            market_price = self._parse_float(
                self.inv_market_price.get(), "Market Price")
            settlement = self._parse_date(self.inv_settlement.get())
            maturity = self._parse_date(self.inv_maturity.get())
            frequency = self._frequency_to_int(self.inv_frequency.get())
            investment = self._parse_float(
                self.inv_amount.get(), "Investment Amount")

            # --- Run the calculation ---
            results = calculate_investment_returns(
                face_value=face_value,
                coupon_rate=coupon_rate,
                market_price=market_price,
                settlement_date=settlement,
                maturity_date=maturity,
                investment_amount=investment,
                coupon_frequency=frequency
            )

            # --- Format the results as a readable text block ---
            # We use f-strings with fixed-width formatting to align columns
            lines = [
                "=" * 52,
                "  INVESTMENT SUMMARY",
                "=" * 52,
                f"  Bonds purchased:        {results['bonds_purchased']:>10,}",
                f"  Amount invested:         £{results['actual_invested']:>10,.2f}",
                f"  Years to maturity:       {results['years_to_maturity']:>10.2f}",
                f"  YTM:                     {results['ytm']:>10.4f}%",
                "",
                "  RETURNS BREAKDOWN",
                "-" * 52,
                f"  Coupon per payment:      £{results['coupon_per_period']:>10,.2f}",
                f"  Annual coupon income:    £{results['annual_coupon_income']:>10,.2f}",
                f"  Total coupon income:     £{results['total_coupon_income']:>10,.2f}",
                f"  Capital gain / (loss):   £{results['capital_gain_loss']:>10,.2f}",
                "-" * 52,
                f"  TOTAL RETURN:            £{results['total_return_gbp']:>10,.2f}",
                f"  TOTAL RETURN %:          {results['total_return_pct']:>10.2f}%",
                "",
                "  YEAR-BY-YEAR COUPON INCOME",
                "-" * 52,
                f"  {'Year':<8} {'Income':>12} {'Cumulative':>14} {'Portfolio Value':>14}",
                "-" * 52,
            ]

            # Add one line per year from the breakdown
            for row in results['yearly_breakdown']:
                lines.append(
                    f"  {row['year']:<8} "
                    f"£{row['coupon_income_this_year']:>10,.2f} "
                    f"£{row['cumulative_coupon_income']:>12,.2f} "
                    f"£{row['cumulative_total_value']:>12,.2f}"
                )

            lines.append("=" * 52)

            # --- Write to the textbox ---
            # We must enable it to write, then disable again to keep it read-only
            self.inv_result_box.configure(state="normal")
            self.inv_result_box.insert("1.0", "\n".join(lines))
            self.inv_result_box.configure(state="disabled")

        except ValueError as e:
            # Display the error message in red
            self.inv_error_label.configure(text=str(e))
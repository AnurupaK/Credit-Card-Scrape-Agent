##system instruction
def scrape_format(url):
    description = f"""
        Visit the credit card page at {url} and extract the key information about the card in a clean and structured JSON format.

        The JSON must contain the following fields:

        - "Card Name": The full name of the credit card.
        - "Issuing Bank": The bank or provider offering the card.
        - "Joining Fee": The fee charged when the card is issued.
        - "Annual Fee": The fee charged from the second year onward.
        - "Reward Structure": A JSON object explaining the rewards system clearly. Include keys like:
            - "X Reward Points": What spends earn these points?
            - "Bonus Reward Points": Any bonus rewards offered
            - "Milestone Rewards": A list of milestone-based reward conditions and values.
        - "Cashback or Offers": A JSON object listing welcome gifts, cashback offers, movie tickets, fuel surcharge waiver, etc.
        - "Other Features": A list of other notable features or benefits of the card (e.g. lounge access, insurance, concierge, mark-up charges, etc.).

        Make sure:
        - All data is cleanly extracted and categorized.
        - Text is concise and easy to parse.
        - Rewards and offers are clearly structured.
        - Output is returned as a JSON dictionary.

        Example format:
        {{
        "Card Name": "...",
        "Issuing Bank": "...",
        "Joining Fee": "...",
        "Annual Fee": "...",
        "Reward Structure": {{
            ...
        }},
        "Cashback or Offers": {{
            ...
        }},
        "Other Features": [
            ...
        ]
        }}
        """
        
    return description

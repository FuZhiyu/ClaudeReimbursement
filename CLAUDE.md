# Travel Reimbursement Filing Instructions

## Overview

This project uses Claude Code, Gmail MCP, and Google Calendar MCP to collect relevant information for filing reimbursement. 

**Important:** Use the TodoWrite tool to track workflow steps throughout the reimbursement process. 



## Travel Reimbursement Workflow

Here we document the standardized process for filing travel reimbursements, including identifying trips, collecting receipts, organizing documentation, and building reimbursement indexes.

### 1. Calendar → Trip Windows

- **Detect trips** by searching for flight and hotel events in Google Calendar
- **Define trip dates:**
  - StartDate = date of first flight/hotel event
  - EndDate = date of return flight or hotel checkout
- **If ambiguous:** Ask for clarification; otherwise use event dates directly

### 1.1 Create a new folder and a markdown file documenting the trip

- **Folder structure:** `./{TripName}/`
- **Folder naming convention:** `YYYY-MM-City-Purpose` (e.g., “2025-07-Boston-NBER”)
- **Markdown file:** `./{TripName}/records.md`
  - This file will be used to document the trip and the receipts along the way. 

### 2. Gmail Search (per trip window)

Use Gmail MCP to search for relevant emails. 

- **Search period:** StartDate minus 1 day through EndDate plus 1 day
- **Keywords to include:**
  - Flights: airline names (Delta, United, American, Southwest, JetBlue), "flight", "booking", "confirmation", "itinerary"
  - Hotels: hotel names, "folio", "reservation", "stay"
  - Ground transport: "uber", "lyft", "taxi", "receipt", "ride", "trip", "parking", "garage", "rental car", "Hertz", "Avis"
  - Other: "wifi", "internet", specific expense types, "registration", "conference fee"

#### 2.1 Read emails

From the search results, read relevant emails, and save them in the `records` subfolder.

**CRITICAL: Verify Payment Information Before Downloading**
- Check if email contains payment method (last 4 digits of credit card)
- For rideshare services (Uber/Lyft): If email says "This is not a payment receipt", search for the actual payment receipt
- Payment receipts typically arrive 4-24 hours after service
- See Section 2.2 for detailed timing information

Do **NOT** use the `read_email` tool from the gmail MCP, as for large emails it will exceeds the maximum allowed tokens. Instead, download the email and attachments using the `download_gmail_message.py` script into in the subfolder `records`. 

**Script API:**
```bash
# IMPORTANT: Use the virtual environment Python to avoid module errors
/Users/zhiyufu/.venv/bin/python download_gmail_message.py <message_id> <output_directory>

# Arguments:
#   message_id: Gmail message ID (required)
#   output_directory: Directory to save files (required for trip records)
#
# Output files:
#   - {date}_{subject}.eml - Original email in EML format
#   - {date}_{subject}.md - AI-friendly Markdown with YAML frontmatter
#   - Attachments saved with original filenames

# Example:
/Users/zhiyufu/.venv/bin/python download_gmail_message.py 197fb19e3952fad8 ./2025-07-Boston-NBER/records/
```

The script saves emails in two formats:

- `.eml` file for archival purposes
- `.md` file for AI-friendly reading

Read the downloaded markdown file for the text content. For each relevant email, add a line to the markdown file documenting the email and pointing to the saved files. **Note whether it's a payment receipt or just a trip summary.** 

- **Collect ALL related items:**
  - Original bookings AND changes/modifications
  - Receipts, confirmations, and folios
  - Change/exchange/reissue/cancellation emails
  - Refund/credit notices
- **Exclude:** Items explicitly marked "Personal"

### 2.2 Payment Receipt Timing and Identification

**Important:** Different vendors send payment information at different times:

- **Airlines (Southwest, United, Delta, etc.)**: Payment info typically included in booking confirmation and change emails
- **Hotels**: Payment info shown on final folio, usually sent at or after checkout
- **Rideshare Services (Uber, Lyft, etc.)**: Send TWO types of emails per trip:
  1. **Trip Summary** (immediate): Shows route and fare but states "This is not a payment receipt"
  2. **Payment Receipt** (delayed 4-24 hours): Contains payment method (last 4 digits) and full payment details
- **WiFi/Internet Services**: Payment info typically in purchase confirmation
- **Parking/Transit**: Payment details usually in confirmation email

**Identifying Payment Receipts:**
- Look for keywords: "payment", "charged to", "paid", "Payments" section
- Card indicators: "Visa", "MasterCard", "AmEx", "Discover" with "••••" or "ending in" followed by 4 digits
- Rideshare payment receipts often arrive hours or even a day after the trip
- Check email timestamps - payment receipts frequently have different timestamps than trip summaries

**Search Strategy for Payment Receipts:**
- If initial search returns trip summaries without payment info, search 1-3 days after service date
- For rideshare: Look for duplicate email subjects with different timestamps
- Sort by date to find the later email which typically contains payment details

### 3. Important Notes on Receipts

- **Flight changes:** Keep BOTH original booking AND change confirmation receipts
- **Credits/vouchers:** If a receipt shows payment via earlier credit, include the original receipt that generated the credit
- **Multiple payment methods:** Record each payment separately
- **Missing transportation:** Typically expect 4 airport transfers per trip (2 each way)

### 4. Confirming the trip with the user

- Summarize the trip and receipts with the user and request confirmation. 
- Ask users for meal reimbursement details: See per-diem section below.

### 5. Prepare the reimbursement 

With the user confirmation, create subfolder named "Receipts". Include relevant receipts from `records` in the subfolder, and a tsv file named `reimbursement_summary.tsv` with these columns (in order):

- **ItemService**: Detailed description of expense
- **Amount**: Numeric amount (positive for charges, negative for refunds)
- **Currency**: Currency code (e.g., “USD”)
- **Category**: Air, Hotel, Transport, Meals, Other
- **PaymentMethodLast4**: Last 4 digits from receipt (or “MISSING” if not shown)
- **ReceiptFileName**: Name of the receipt file
- **Notes**: Additional details, payment method issues, credits applied, etc.

### 6. Categories

- **Air**: Flights, airline fees, seat upgrades
- **Hotel**: Accommodation charges
- **Transport**: Ground transportation (Uber, Lyft, taxi, train, parking)
- **Meals**: Restaurant charges or per diem
- **Other**: WiFi, conference fees, miscellaneous

## Rules and Best Practices

### Payment Methods

- **Must come from receipt itself** - only record last 4 digits
- If receipt doesn't show payment method:
  - Ask users to provide the payment method

### Foreign Currency

- **Record original amount** in the Amount column
- **Note exchange rate** and USD equivalent in Notes column
- **Format:** "EUR 150.00 (approx $165.00 at 1.10 exchange rate)"

### Flight Changes & Credits

- Keep ALL related receipts (original, changes, credits)
- Record each transaction as separate line item
- Note credit relationships in Notes column
- Example: “Applied credit from ticket #12345 on [date]”

### Deduplication

- Only remove exact duplicates (same supplier + date + amount + reference)
- When in doubt, keep both and note potential duplicate

### Per Diem Meals

- **Calculation:**
  - Departure day = 0.5 day
  - Full days = 1.0 day each
  - Return day = 0.5 day
- **Important:** Ask which meals were provided by conference/host
- **Method:** When using per diem, do NOT include actual meal receipts
- **Rates:** Check your institution's current per diem rates for the destination

## Quality Checks

Before finalizing:

1. **Receipt count:** Verify expected number of ground transportation receipts
1. **Payment methods:** Flag any "MISSING" entries for follow-up
1. **Math check:** Ensure flight costs add up (original + changes = total)
1. **Hotel folios:** Extract and review final folios with taxes included
1. **Drive links:** Verify all links are populated and working

## Payment Method Verification Checklist

Use this checklist to ensure all payment information is captured:

### ✓ Flight Receipts
- [ ] Original booking shows payment method
- [ ] Change/modification fees show payment method
- [ ] Credits properly linked to original payment
- [ ] WiFi purchases include payment info

### ✓ Hotel Receipts
- [ ] Final folio downloaded (not just confirmation)
- [ ] Payment method visible on folio
- [ ] All charges itemized (room, tax, fees, incidentals)
- [ ] Any advance deposits reconciled with final bill

### ✓ Ground Transportation
- [ ] All Uber/Lyft rides have payment receipts (not just trip summaries)
- [ ] Payment receipts show last 4 digits
- [ ] Expected number of rides: typically 4 for round trip
- [ ] Alternative transport (taxi, parking) has payment info

### ✓ Other Expenses
- [ ] Conference registration shows payment method
- [ ] Parking receipts include payment details
- [ ] Internet/WiFi purchases have payment info
- [ ] Any meal receipts (if not using per diem) show payment

### ✓ Common Red Flags
- [ ] Email says "This is not a payment receipt" → Need to find actual payment receipt
- [ ] Receipt dated same as service → Might be trip summary, not payment receipt
- [ ] No payment method shown → Check for follow-up email
- [ ] "MISSING" in PaymentMethodLast4 → Requires user input


## Common Issues & Solutions

### Payment Receipt Issues

- **Rideshare payment info missing:** 
  - Initial emails often show "This is not a payment receipt"
  - Search 4-24 hours after trip date for actual payment receipt
  - Look for duplicate subject lines with different timestamps
  - Try searching: `from:receipts@uber.com OR from:noreply@uber.com "payment" after:[trip_date]`

- **Hotel payment details not in confirmation:**
  - Final folio with payment usually sent at/after checkout
  - Search checkout date +1 day
  - Look for emails from hotel's billing system (often different from booking system)
  - Check attachments - folios often sent as PDFs

- **Missing last 4 digits on receipts:**
  - Some vendors send payment info in separate email
  - Check if using corporate card or expense system that masks numbers
  - Ask user to verify payment method from their records

### Receipt Collection Issues

- **Missing airport transportation:**
  - Expected: 4 rides per round trip (home→airport, airport→hotel, hotel→airport, airport→home)
  - Search broader date range (trip dates ±3 days)
  - Try alternate terms: "ride receipt", "trip receipt", "fare receipt"
  - Check if used alternative transport (taxi, public transit, colleague pickup)

- **Flight changes not captured:**
  - Search for "change", "modification", "reissue", "exchange"
  - Look for emails mentioning original confirmation number
  - Check for fare difference charges or credits

- **WiFi purchases on flights:**
  - Often sent hours after flight
  - Search airline domain + "internet" or "wifi"
  - May come from third-party provider (e.g., Gogo, Viasat)

### Email Search Challenges

- **Gmail search limitations:**
  - Use quotes for exact phrases
  - Combine multiple terms with OR
  - Exclude spam: `-category:promotions -category:social`
  - If too many results, narrow date range

- **Attachments not downloading:**
  - Verify message_id is correct
  - Check if attachment is inline vs. separate file
  - Some "attachments" are actually HTML parts of email

- **Module errors with download script:**
  - Always use: `/Users/zhiyufu/.venv/bin/python`
  - Do NOT use system python or bare `python` command

### Data Organization Issues

- **Duplicate receipts:**
  - Keep both unless exact duplicate (same date, amount, reference number)
  - Note relationship in records.md
  - For amendments/changes, keep entire chain

- **Foreign currency confusion:**
  - Always record original currency amount
  - Note exchange rate and USD equivalent in Notes
  - If receipt shows both currencies, record both

- **Split payments:**
  - Record each payment method as separate line
  - Note in records which parts paid by which method
  - Common with flight changes (original fare + change fee)

## Example Search Queries

### Initial Trip Search
```
# Comprehensive trip search
after:2025/07/07 before:2025/07/13 (flight OR hotel OR receipt OR confirmation OR booking OR uber OR lyft OR taxi) -category:promotions -category:social

# Alternative comprehensive search
after:2025/07/07 before:2025/07/13 (airline OR lodging OR transport OR "ride receipt" OR wifi OR parking) -category:promotions
```

### Finding Payment Receipts

#### Rideshare Payment Receipts
```
# Uber payment receipts (search 1-2 days after trip date)
after:2025/07/09 before:2025/07/11 from:noreply@uber.com subject:"Your Tuesday" payment
after:2025/07/09 before:2025/07/11 from:receipts@uber.com "American Express" OR "Visa" OR "Mastercard"

# Lyft payment receipts
after:2025/07/09 before:2025/07/11 from:no-reply@lyft.com "payment" "charged to"
after:2025/07/09 before:2025/07/11 from:receipts@lyft.com "ending in" OR "••••"
```

#### Flight Payment Information
```
# Southwest payment details
"Southwest" ("American Express" OR "Visa" OR "ending in") confirmation #2MIGGL

# United/Delta payment info
from:united.com OR from:delta.com "payment method" OR "charged to" after:2025/07/07

# Finding flight credits and changes
"Southwest" "credit" "ticket #5262344662867" OR "confirmation"
"flight change" "additional payment" OR "fare difference" after:2025/07/01
```

#### Hotel Payment Details
```
# Hotel folio search (usually sent at/after checkout)
"Royal Sonesta" (folio OR checkout OR "final bill") after:2025/07/10
from:noreply@sonesta.com "total charges" OR "payment" after:2025/07/10

# Generic hotel payment search
hotel ("folio" OR "final charges" OR "payment summary") after:2025/07/10
```

#### Other Common Expenses
```
# WiFi/Internet purchases
"wifi" OR "internet" "purchase" "receipt" after:2025/07/07
from:southwest.com "internet purchase receipt" after:2025/07/08

# Parking receipts
"parking" ("receipt" OR "payment confirmation") after:2025/07/07
from:spplus.com OR from:parkwhiz.com receipt after:2025/07/07

# Conference registration
"registration" ("confirmation" OR "receipt") "conference" OR "NBER" after:2025/05/01
```

### Troubleshooting Missing Receipts
```
# If payment info missing, search broader date range
after:2025/07/08 before:2025/07/14 from:uber.com "payment"

# Check for receipts sent to different addresses
from:*@uber.com OR from:*@lyft.com after:2025/07/08 before:2025/07/14

# Look for batch payment summaries
"monthly statement" OR "payment summary" uber OR lyft after:2025/07/01
```

## Workflow Optimization Tips

### Efficiency Strategies

1. **Batch Operations:**
   - Search for all receipts in one comprehensive query first
   - Download all relevant emails before reading any
   - Process similar receipts together (all flights, then all hotels, etc.)

3. **Search Optimization:**
   - Start broad, then narrow if too many results
   - Use sender domains when known (e.g., `from:uber.com`)
   - Save successful search queries in records.md for future reference

4. **Documentation Best Practices:**
   - Update records.md immediately after downloading each receipt
   - Note payment method as soon as found
   - Flag missing items in real-time rather than at end

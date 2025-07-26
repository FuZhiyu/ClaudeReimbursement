# Travel Reimbursement Workflow

This document guides the standardized process for filing travel reimbursements using Claude Code, Gmail MCP, and Google Calendar MCP.

**IMPORTANT:** Use TodoWrite tool to track progress throughout the workflow.

## Step 1: Find Trip Dates and Create Structure

1. **Search Google Calendar** for flight and hotel events
   - StartDate = first flight/hotel event
   - EndDate = return flight or hotel checkout
   - If ambiguous, ask for clarification

2. **Create folder structure:**
   - Folder: `./YYYY-MM-City-Purpose/` (e.g., "2025-07-Boston-NBER")
   - Create `records.md` to document receipts
   - Create `records/` subfolder for email downloads

## Step 2: Collect Receipts

Use the receipt-collector agent to find and download all receipts with payment information:

```
Task(
  subagent_type="receipt-collector",
  description="Find [City] trip receipts",
  prompt="""
  Trip: [City] from [StartDate] to [EndDate]
  Output directory: ./[TripFolder]/records/
  
  Search Gmail for dates: [StartDate-1] to [EndDate+1]
  
  Look for these vendors and keywords:
  - Airlines: [specific airlines from calendar], "flight", "booking", "confirmation"
  - Hotels: [specific hotel name], "folio", "reservation", "stay"
  - Ground transport: "uber", "lyft", "taxi", "parking", "receipt", "ride"
  - Other: "wifi", "internet", "registration", "conference fee"
  
  CRITICAL REMINDERS:
  - Rideshare payment receipts arrive 4-24 hours after service
  - Hotel folios sent at/after checkout
  - Skip emails saying "This is not a payment receipt"
  - Download using: download_gmail_message.py <message_id> <output_dir>
  
  Return summary of:
  - Total receipts found with payment info
  - Missing receipts that need follow-up
  - Any download failures
  """
)
```

## Step 3: Confirm with User

1. **Summarize trip expenses:**
   - List all receipts found by category
   - Note payment methods captured
   - Identify missing receipts

2. **Ask about meals:**
   - Use per diem? If yes:
     - Which meals were provided by conference?
     - What's the institution's per diem rate?
   - Or actual meal receipts?

3. **Get confirmation** before proceeding to final reimbursement

## Step 4: Generate Reimbursement Package

1. **Create `Receipts/` subfolder**
2. **Copy relevant receipts** from records/ to Receipts/
3. **Create `reimbursement_summary.tsv`** with columns:
   - ItemService (detailed description)
   - Amount (numeric, positive for charges)
   - Currency (e.g., "USD")
   - Category (Air, Hotel, Transport, Meals, Other)
   - PaymentMethodLast4 (from receipt or "MISSING")
   - ReceiptFileName
   - Notes (credits, issues, etc.)

## Categories and Rules

### Expense Categories
- **Air**: Flights, airline fees, seat upgrades, WiFi
- **Hotel**: Room charges, taxes, fees (exclude laundry/valet)
- **Transport**: Uber, Lyft, taxi, parking, trains
- **Meals**: Restaurant charges or per diem
- **Other**: Conference fees, miscellaneous

### Non-Reimbursable Items
Laundry, valet, personal expenses, in-room movies, minibar

### Per Diem Calculation
- Departure day: 0.5 day
- Full days: 1.0 day each  
- Return day: 0.5 day
- Subtract meals provided by conference

### Important Rules
- Record payment method last 4 digits from receipt only
- Keep all flight changes and original bookings
- Note credit relationships in Notes column
- Expected transport: ~4 rides for round trip

## Quick Reference

### Common Search Patterns
```
# Initial comprehensive search
after:[date-1] before:[date+1] (flight OR hotel OR receipt OR uber OR lyft) -category:promotions

# Rideshare payment receipts (search 1-2 days after)
from:receipts@uber.com "payment" after:[service_date]
from:no-reply@lyft.com "charged to" after:[service_date]

# Hotel folio
"[hotel name]" (folio OR "final bill") after:[checkout_date]
```

### Troubleshooting
- **Missing rideshare payment**: Search 24-48 hours after trip
- **No hotel folio**: Search checkout date +1 day
- **WiFi receipts**: May come hours after flight
- **Missing ground transport**: Check if used alternative (taxi, colleague)

### TSV Format Example
```
ItemService	Amount	Currency	Category	PaymentMethodLast4	ReceiptFileName	Notes
Southwest Airlines STL-BOS-STL	446.16	USD	Air	1009	Southwest_Original.eml	Confirmation #2MIGGL
Uber Airport to Hotel	40.95	USD	Transport	1009	Uber_Jul8_Evening.eml	July 8 evening
```

## Workflow Checklist

- [ ] Find trip dates from Calendar
- [ ] Create folder structure  
- [ ] Run receipt-collector agent
- [ ] Review downloaded receipts
- [ ] Confirm with user
- [ ] Create Receipts/ folder
- [ ] Generate reimbursement_summary.tsv
- [ ] Verify all payment methods captured
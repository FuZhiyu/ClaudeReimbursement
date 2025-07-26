# Travel Reimbursement Workflow

This document guides the standardized process for filing travel reimbursements using Claude Code, Gmail MCP, and Google Calendar MCP.

**IMPORTANT:** Use TodoWrite tool to track progress throughout the workflow.

## Step 1: Find Trip Dates and Create Structure

1. **Search Google Calendar** for flight and hotel events
   - StartDate = first flight/hotel event
   - EndDate = return flight or hotel checkout
   - **Check for Gmail-created events**: Look for calendar events with "This event was created from an email"
   - If ambiguous, ask for clarification

2. **Create folder structure:**
   - Folder: `./YYYY-MM-City-Purpose/` (e.g., "2025-07-Boston-NBER")
   - Create `records.md` to document receipts
   - Create `records/` subfolder for email downloads

## Step 2: Discover Trip Information and Collect Receipts

1. **Initial information gathering:**
   - Use details already extracted from Google Calendar
   - Note what information is missing or incomplete (e.g., exact hotel names, flight numbers)
   - Identify trip purpose and business context

2. **Iterative discovery with email-searcher agent:**
   
   The email-searcher agent serves as an intelligent filter between Gmail and the master agent, preventing information overload while finding relevant trip details and receipts.
   
   **Using the email-searcher:**
   - Start with whatever information is available from calendar
   - Let the agent determine optimal search strategies based on what's known
   - Iterate as needed to fill in missing details or collect receipts
   - The agent understands typical booking patterns (flights booked earlier than hotels, rideshare receipts arrive after service, etc.)
   
   **Information to provide to email-searcher:**
   - All known trip details from calendar and previous searches
   - **Gmail message IDs** from calendar events (if available) for direct access to booking confirmations
   - What specific information or receipts are needed
   - Business context for filtering personal expenses
   - Output directory for any downloads
   - Any special circumstances or vendors to focus on
   
   **What email-searcher returns:**
   - Structured summary of findings (not full emails)
   - Key information extracted (vendor names, dates, confirmation numbers)
   - List of downloaded receipts with payment validation
   - Recommendations for follow-up searches
   - Missing items that need attention

3. **Update records.md with relevant information:**
   
   After each email-searcher iteration, update `records.md` with:
   - Important trip details discovered (hotel names, flight numbers, etc.)
   - Receipt downloads and their payment methods
   - Missing receipts that need follow-up
   - Any issues or special notes
   
   This maintains a clear audit trail of the discovery process.

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
- [ ] Run email-searcher for trip discovery
- [ ] Iterate with email-searcher for missing details
- [ ] Collect receipts with email-searcher
- [ ] Review downloaded receipts
- [ ] Confirm with user
- [ ] Create Receipts/ folder
- [ ] Generate reimbursement_summary.tsv
- [ ] Verify all payment methods captured
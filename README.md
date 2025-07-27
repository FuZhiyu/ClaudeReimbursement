# Travel Reimbursement Workflow with Claude Code

An automated workflow for processing academic travel reimbursements using Claude Code with Gmail and Google Calendar integration. This system streamlines the tedious process of collecting receipts, organizing expenses, and generating reimbursement packages.

## Overview

This workflow helps academic researchers efficiently process travel reimbursements by:

- **Automatically discovering trip dates** from Google Calendar events
- **Intelligently searching Gmail** for booking confirmations and receipts
- **Organizing expenses** into standardized categories and formats
- **Generating final reimbursement packages** ready for institutional submission
- **Tracking per diem calculations** with conference meal deductions

## Key Features

- **Smart Trip Discovery**: Finds flight and hotel events in your calendar to determine trip dates
- **Intelligent Email Search**: Uses specialized email-searcher agent to find relevant receipts while filtering out noise
- **Automated Receipt Collection**: Downloads and organizes receipts from Gmail
- **Expense Categorization**: Automatically categorizes expenses (Air, Hotel, Transport, Meals, Other)
- **Per Diem Calculations**: Handles complex per diem rules with conference meal deductions
- **Payment Method Tracking**: Extracts payment method details from receipts
- **TSV Export**: Generates institution-ready expense summaries

## Prerequisites

### Required Software

1. **Claude Code** - Anthropic's official CLI
   - Install from: https://docs.anthropic.com/en/docs/claude-code

2. **Gmail MCP Server** - For Gmail integration
   - Install from: https://github.com/GongRzhe/Gmail-MCP-Server
   - Provides email search, reading, and attachment download capabilities

3. **Google Calendar MCP** - For calendar integration  
   - Install from: https://github.com/nspady/google-calendar-mcp
   - Enables automatic trip date discovery from calendar events

### Setup Requirements

- Gmail account with travel-related emails
- Google Calendar with flight/hotel bookings
- Institutional email confirmations and receipts
- Claude Code configured with MCP servers

## Installation

1. **Install Claude Code**
   ```bash
   # Follow installation guide at:
   # https://docs.anthropic.com/en/docs/claude-code
   ```

2. **Install Gmail MCP Server**
   ```bash
   git clone https://github.com/GongRzhe/Gmail-MCP-Server
   cd Gmail-MCP-Server
   # Follow setup instructions in repository
   ```

3. **Install Google Calendar MCP**
   ```bash
   git clone https://github.com/nspady/google-calendar-mcp
   cd google-calendar-mcp
   # Follow setup instructions in repository
   ```

4. **Configure MCP Servers in Claude Code**
   - Add Gmail and Calendar MCP servers to your Claude Code configuration
   - Ensure proper authentication for both Gmail and Google Calendar APIs

## Usage

### Basic Workflow

1. **Start the Process**
   ```
   I need help filing a reimbursement for my recent trip to [City] for [Conference/Purpose]
   ```

2. **Claude Code will automatically:**
   - Search your Google Calendar for trip dates
   - Create organized folder structure
   - Use email-searcher agent to find relevant receipts
   - Download and categorize expenses
   - Generate final reimbursement package

3. **Review and Submit**
   - Verify the generated `reimbursement_summary.tsv`
   - Check the `Receipts/` folder for supporting documents
   - Submit to your institution's reimbursement system

### Example Output Structure

```
2025-03-Chicago-Conference/
├── records.md                     # Detailed trip documentation
├── reimbursement_summary.tsv      # Final expense summary
├── Receipts/                      # Supporting documents
│   ├── Flight_Booking.eml
│   ├── Hotel_Folio.pdf
│   └── Transport_Receipts.eml
└── records/                       # Original email downloads
    └── [email archives]
```

## Expense Categories

- **Air**: Flights, airline fees, seat upgrades, WiFi
- **Hotel**: Room charges, taxes, fees (excludes personal items)
- **Transport**: Uber, Lyft, taxi, parking, trains
- **Meals**: Restaurant charges or per diem calculations
- **Other**: Conference fees, miscellaneous business expenses

## Example

See the `2025-03-Chicago-Example/` folder for a complete fictional example showing:
- Detailed trip records with receipt documentation
- Final TSV summary with proper categorization
- Empty Receipts folder structure for final package

## Workflow Documentation

Detailed workflow instructions are available in `CLAUDE.md`, including:
- Step-by-step process for each reimbursement
- Email search patterns and strategies
- Per diem calculation rules
- Troubleshooting common issues

## Benefits

- **Time Savings**: Reduces reimbursement processing from hours to minutes
- **Accuracy**: Automated categorization and calculation reduces errors
- **Completeness**: Systematic search ensures no receipts are missed
- **Compliance**: Generates institution-ready documentation
- **Audit Trail**: Maintains detailed records of all expenses and sources

## Support

For issues with:
- **Claude Code**: https://docs.anthropic.com/en/docs/claude-code
- **Gmail MCP**: https://github.com/GongRzhe/Gmail-MCP-Server/issues
- **Calendar MCP**: https://github.com/nspady/google-calendar-mcp/issues
- **This Workflow**: Check `CLAUDE.md` for detailed troubleshooting

## License

This workflow is provided as-is for academic and research use.
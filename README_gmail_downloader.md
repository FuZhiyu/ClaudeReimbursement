# Gmail Message and Attachment Downloader

A Python script that downloads Gmail messages and their attachments using the Gmail API.

## Features

- Downloads email content in two formats:
  - **EML format**: Original email for archival/legal purposes
  - **Markdown format**: Optimized for AI agent consumption (15% more token efficient)
- Converts HTML emails to plain text automatically
- Downloads all attachments from the email
- Command-line interface for easy usage
- Handles authentication with Gmail API
- Creates organized output with descriptive filenames

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Gmail API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Gmail API:
   - Go to "APIs & Services" > "Library"
   - Search for "Gmail API" and enable it
4. Create credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop app" as application type
   - Download the credentials JSON file

### 3. Configure Credentials Path

You can specify the location of your credentials file using a `.env` file:

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set the path to your credentials:
   ```bash
   GMAIL_CREDENTIALS_PATH=/path/to/your/credentials.json
   ```

   Examples:
   - `GMAIL_CREDENTIALS_PATH=./credentials.json` (current directory)
   - `GMAIL_CREDENTIALS_PATH=/Users/username/secrets/gmail-credentials.json` (absolute path)
   - `GMAIL_CREDENTIALS_PATH=~/.config/gmail/credentials.json` (home directory)

If you don't create a `.env` file, the script will look for `credentials.json` in the current directory by default.

## Usage

```bash
python download_gmail_message.py <message_id> [output_directory]
```

### Arguments

- `message_id`: The Gmail message ID (required)
- `output_directory`: Directory to save files (optional, defaults to "gmail_downloads")

### Example

```bash
# Download with default output directory
python download_gmail_message.py 197fb19e3952fad8

# Download to specific directory
python download_gmail_message.py 197fb19e3952fad8 ./receipts
```

### First Run

On first run, the script will:
1. Open a browser window for Gmail authentication
2. Ask you to grant permissions
3. Save authentication token for future use

## Output

The script creates:
- **EML file**: Complete original email in standard format
- **Markdown file**: AI-friendly version with:
  - Structured metadata (ID, date, from, to, subject)
  - Plain text body (HTML automatically converted)
  - List of attachments
- **Attachments**: All files downloaded with original filenames
- Organized in the specified output directory

### Example Markdown Output
```markdown
# Email: Your Hotel Receipt

## Metadata
- **Message ID**: 197fb19e3952fad8
- **Date**: 2025-07-11 20:07:42 UTC
- **From**: hotel@example.com
- **To**: user@example.com
- **Subject**: Your Hotel Receipt

## Body
Thank you for staying with us...

## Attachments
- receipt.pdf (saved as: receipt.pdf)
```

## Finding Message IDs

You can get message IDs from:
1. The Gmail MCP search results (as shown in your search)
2. Gmail web interface (in the URL when viewing an email)
3. Other Gmail API operations

## Troubleshooting

- **"credentials.json not found"**: 
  - Check your `.env` file has the correct path to your credentials
  - Download OAuth2 credentials from Google Cloud Console if you haven't already
- **Authentication errors**: Delete `token.pickle` (in the same directory as your credentials) and re-authenticate
- **API quota errors**: Check your Gmail API quotas in Google Cloud Console
- **Token file location**: The `token.pickle` file is automatically saved in the same directory as your credentials file
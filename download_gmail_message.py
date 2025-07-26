#!/usr/bin/env python3
"""
Gmail Message and Attachment Downloader

Downloads a Gmail message and its attachments given a message ID.
Saves the email in both EML format (for archival) and Markdown format (for AI consumption).

Usage:
    python download_gmail_message.py <message_id> [output_directory]
"""

import os
import sys
import base64
import pickle
import argparse
import email
from datetime import datetime
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from html import unescape
import re

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate and return Gmail service instance."""
    # Load .env file
    load_dotenv()
    
    # Get credentials path from environment or use default
    credentials_path = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials.json')
    
    # Store token in same directory as credentials
    if os.path.dirname(credentials_path):
        token_dir = os.path.dirname(credentials_path)
        token_path = os.path.join(token_dir, 'token.pickle')
    else:
        token_path = 'token.pickle'
    
    creds = None
    
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Check if credentials file exists
            if not os.path.exists(credentials_path):
                print(f"Error: Credentials file not found at '{credentials_path}'!")
                print("Please either:")
                print("1. Download your OAuth2 credentials from Google Cloud Console")
                print(f"   and save them to: {credentials_path}")
                print("2. Or update the GMAIL_CREDENTIALS_PATH in your .env file")
                sys.exit(1)
                
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)

def get_message_raw(service, message_id):
    """Retrieve a message in raw format by ID."""
    try:
        message = service.users().messages().get(
            userId='me', 
            id=message_id,
            format='raw'
        ).execute()
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def get_message_full(service, message_id):
    """Retrieve a message in full format for attachment info."""
    try:
        message = service.users().messages().get(
            userId='me', 
            id=message_id,
            format='full'
        ).execute()
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def save_email_as_eml(raw_message, output_path):
    """Save raw email message as EML file."""
    # Decode the raw message
    raw_email = base64.urlsafe_b64decode(raw_message['raw'].encode('ASCII'))
    
    # Save as EML file
    with open(output_path, 'wb') as f:
        f.write(raw_email)
    
    print(f"Email saved as EML: {output_path}")

def html_to_text(html):
    """Convert HTML to plain text."""
    # Remove script and style elements
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Replace breaks and paragraphs with newlines
    html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'</p>', '\n\n', html, flags=re.IGNORECASE)
    html = re.sub(r'</div>', '\n', html, flags=re.IGNORECASE)
    
    # Remove links but keep text only (no URLs)
    html = re.sub(r'<a[^>]+href="[^"]*"[^>]*>([^<]+)</a>', r'\1', html, flags=re.IGNORECASE)
    
    # Remove all other HTML tags
    html = re.sub(r'<[^>]+>', '', html)
    
    # Unescape HTML entities
    text = unescape(html)
    
    # Clean up whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    
    return text.strip()

def remove_urls_from_text(text):
    """Remove URLs from plain text."""
    # Remove URLs in square brackets like [https://example.com]
    text = re.sub(r'\[https?://[^\]]+\]', '', text)
    # Remove standalone URLs
    text = re.sub(r'https?://[^\s]+', '', text)
    # Clean up extra whitespace
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n\s*\n', '\n\n', text)
    return text.strip()

def get_message_body(payload):
    """Extract message body from payload."""
    body = ''
    html_body = ''
    
    def extract_body(part):
        if part.get('body', {}).get('data'):
            return base64.urlsafe_b64decode(
                part['body']['data'].encode('ASCII')
            ).decode('utf-8', errors='ignore')
        return ''
    
    # Check if it's a simple message
    if payload.get('body', {}).get('data'):
        body_data = extract_body(payload)
        mime_type = payload.get('mimeType', '')
        if mime_type == 'text/html':
            html_body = body_data
            body = html_to_text(html_body)
        else:
            body = remove_urls_from_text(body_data)
        return body
    
    # Handle multipart messages
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                body = extract_body(part)
                if body:
                    return remove_urls_from_text(body)
            elif part['mimeType'] == 'text/html' and not body:
                html_body = extract_body(part)
                if html_body:
                    body = html_to_text(html_body)
            elif 'parts' in part:
                # Recursive call for nested parts
                nested_body = get_message_body(part)
                if nested_body and not body:
                    body = nested_body
    
    return body

def parse_message_headers(headers):
    """Extract relevant headers from message."""
    header_dict = {}
    for header in headers:
        name = header['name'].lower()
        if name in ['from', 'to', 'cc', 'subject', 'date']:
            header_dict[name] = header['value']
    return header_dict

def save_email_as_markdown(message_id, headers, body, attachments, output_path):
    """Save email content as Markdown file with YAML frontmatter."""
    with open(output_path, 'w', encoding='utf-8') as f:
        # YAML frontmatter
        f.write("---\n")
        f.write(f"message_id: {message_id}\n")
        
        # Format date nicely if possible
        date_str = headers.get('date', 'Unknown')
        try:
            from email.utils import parsedate_to_datetime
            date_obj = parsedate_to_datetime(date_str)
            formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S %Z')
            f.write(f"date: {formatted_date}\n")
        except:
            f.write(f"date: {date_str}\n")
        
        f.write(f"from: {headers.get('from', 'Unknown')}\n")
        f.write(f"to: {headers.get('to', 'Unknown')}\n")
        
        if 'cc' in headers:
            f.write(f"cc: {headers['cc']}\n")
        
        subject = headers.get('subject', 'No Subject')
        f.write(f"subject: {subject}\n")
        
        # Attachments in YAML list format
        if attachments:
            f.write("attachments:\n")
            for attachment in attachments:
                filename = os.path.basename(attachment)
                f.write(f"  - {filename}\n")
        else:
            f.write("attachments: []\n")
        
        f.write("---\n\n")
        
        # Title
        f.write(f"# {subject}\n\n")
        
        # Body section
        f.write("## Body\n\n")
        f.write(body)
        f.write("\n")
    
    print(f"Email saved as Markdown: {output_path}")

def download_attachments(service, message_id, payload, output_dir):
    """Download all attachments from a message."""
    attachments = []
    
    def process_parts(parts):
        for part in parts:
            if part.get('filename'):
                attachment_id = part['body'].get('attachmentId')
                if attachment_id:
                    attachment = service.users().messages().attachments().get(
                        userId='me',
                        messageId=message_id,
                        id=attachment_id
                    ).execute()
                    
                    file_data = base64.urlsafe_b64decode(
                        attachment['data'].encode('ASCII')
                    )
                    
                    # Save attachment
                    filename = part['filename']
                    filepath = os.path.join(output_dir, filename)
                    
                    # Handle duplicate filenames
                    if os.path.exists(filepath):
                        base, ext = os.path.splitext(filename)
                        counter = 1
                        while os.path.exists(filepath):
                            filename = f"{base}_{counter}{ext}"
                            filepath = os.path.join(output_dir, filename)
                            counter += 1
                    
                    with open(filepath, 'wb') as f:
                        f.write(file_data)
                    
                    attachments.append(filepath)
                    print(f"Downloaded attachment: {filename}")
            
            # Check for nested parts
            if 'parts' in part:
                process_parts(part['parts'])
    
    # Process main payload
    if 'parts' in payload:
        process_parts(payload['parts'])
    
    return attachments

def main():
    parser = argparse.ArgumentParser(
        description='Download Gmail message and attachments'
    )
    parser.add_argument('message_id', help='Gmail message ID')
    parser.add_argument(
        'output_dir', 
        nargs='?', 
        default='gmail_downloads',
        help='Output directory (default: gmail_downloads)'
    )
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Authenticate
    print("Authenticating with Gmail API...")
    service = authenticate_gmail()
    
    # Get message in both raw and full format
    print(f"Fetching message {args.message_id}...")
    raw_message = get_message_raw(service, args.message_id)
    full_message = get_message_full(service, args.message_id)
    
    if not raw_message or not full_message:
        print("Error: Could not retrieve message")
        sys.exit(1)
    
    # Parse headers and body
    payload = full_message['payload']
    headers = parse_message_headers(payload['headers'])
    body = get_message_body(payload)
    
    # Create filename for email files
    subject = headers.get('subject', 'No Subject')
    # Clean filename
    clean_subject = "".join(c for c in subject if c.isalnum() or c in (' ', '-', '_')).strip()
    clean_subject = clean_subject[:50]  # Limit length
    
    date_str = headers.get('date', '')
    try:
        # Parse date and format it
        from email.utils import parsedate_to_datetime
        date_obj = parsedate_to_datetime(date_str)
        date_prefix = date_obj.strftime('%Y-%m-%d')
    except:
        date_prefix = 'unknown_date'
    
    base_filename = f"{date_prefix}_{clean_subject}"
    eml_path = output_dir / f"{base_filename}.eml"
    md_path = output_dir / f"{base_filename}.md"
    
    # Save email as EML
    print(f"Saving email to {eml_path}...")
    save_email_as_eml(raw_message, str(eml_path))
    
    # Download attachments
    print("Checking for attachments...")
    attachments = download_attachments(service, args.message_id, payload, output_dir)
    
    # Save email as Markdown
    print(f"Saving email to {md_path}...")
    save_email_as_markdown(args.message_id, headers, body, attachments, str(md_path))
    
    if attachments:
        print(f"\nDownloaded {len(attachments)} attachment(s)")
    else:
        print("No attachments found")
    
    print(f"\nAll files saved to: {output_dir}")

if __name__ == '__main__':
    main()
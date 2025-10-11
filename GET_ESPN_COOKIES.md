# How to Get ESPN Cookies (Step-by-Step)

## Method 1: Chrome/Edge (Easiest)

1. **Open your browser** and go to: https://fantasy.espn.com/football
2. **Log into your ESPN account** if not already logged in
3. **Go to your league page** (League ID: 361353)
4. **Press F12** to open Developer Tools
5. **Click the "Application" tab** at the top of Developer Tools
   - If you don't see "Application", click the ">>" arrows and find it there
6. **In the left sidebar**, expand "Cookies" and click on `https://fantasy.espn.com`
7. **Find these two cookies:**
   - **SWID** - Click it and copy the "Value" column
   - **espn_s2** - Click it and copy the "Value" column

## Method 2: Firefox

1. **Open Firefox** and go to: https://fantasy.espn.com/football
2. **Log into your ESPN account**
3. **Go to your league page**
4. **Press F12** to open Developer Tools
5. **Click the "Storage" tab**
6. **Expand "Cookies"** and click on `https://fantasy.espn.com`
7. **Find and copy:**
   - **SWID** value
   - **espn_s2** value

## What They Should Look Like

### SWID
```
{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}
```
**Example:** `{AD9C8849-E351-41B7-9BDC-4085193C8A92}`
**Important:** Include the curly braces { }

### espn_s2
```
Long string of characters (usually 150-300 characters)
```
**Example:** `AECABCD1234567890abcdefghijk...` (very long)
**Important:** Copy the ENTIRE value - it's very long!

## Common Issues

### ❌ Problem: Cookies expire after 30 days
✅ **Solution:** Get fresh cookies by logging into ESPN again

### ❌ Problem: Copied cookies incorrectly
✅ **Solution:** Make sure to copy the ENTIRE espn_s2 value (it's very long!)

### ❌ Problem: Using incognito/private mode
✅ **Solution:** Use regular browser window where you stay logged in

## After Getting Cookies

Tell me the new cookies and I'll update your `.env` file!

Format:
```
SWID: {your-swid-here}
espn_s2: your-very-long-s2-cookie-here
```



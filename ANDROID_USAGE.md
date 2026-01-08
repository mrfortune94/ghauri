# Ghauri Android App - Usage Examples

This guide provides practical examples of how to use the Ghauri Android app for SQL injection testing.

## Table of Contents
1. [Basic SQL Injection Test](#basic-sql-injection-test)
2. [Testing with POST Data](#testing-with-post-data)
3. [Using Cookies for Authentication](#using-cookies-for-authentication)
4. [Database Enumeration](#database-enumeration)
5. [Dumping Table Data](#dumping-table-data)
6. [Advanced Configuration](#advanced-configuration)

---

## Basic SQL Injection Test

This is the simplest way to test a URL for SQL injection vulnerabilities.

### Steps:

1. Open the Ghauri Android app
2. Navigate to the **Basic** tab
3. Enter the target URL:
   ```
   http://testphp.vulnweb.com/artists.php?artist=1
   ```
4. Select **Test Injection** from the Action dropdown
5. Tap **Run Scan**

### What to expect:
- The app will test various SQL injection payloads
- If vulnerable, you'll see:
  ```
  [SUCCESS] SQL injection found!
  Parameter: artist
  Backend: MySQL
  Injection Type: boolean-based blind
  ```

---

## Testing with POST Data

Some applications use POST requests instead of GET parameters.

### Steps:

1. Navigate to the **Basic** tab
2. Enter the target URL:
   ```
   http://example.com/login.php
   ```
3. Enter POST Data:
   ```
   username=admin&password=test
   ```
4. Select your preferred DBMS (or keep "Auto Detect")
5. Select **Test Injection** action
6. Tap **Run Scan**

### Use Case:
Testing login forms, contact forms, or any POST-based application.

---

## Using Cookies for Authentication

Test authenticated areas of a web application.

### Steps:

1. Navigate to the **Basic** tab
2. Enter the authenticated URL:
   ```
   http://example.com/dashboard.php?id=1
   ```
3. Enter your session cookie:
   ```
   PHPSESSID=abcd1234efgh5678; security=low
   ```
4. Select **Test Injection** action
5. Tap **Run Scan**

### Getting Cookies:
- Use a browser's Developer Tools (F12)
- Go to Application/Storage > Cookies
- Copy the cookie values

---

## Database Enumeration

After successfully detecting an injection, enumerate the database.

### List All Databases:

1. After successful injection detection
2. Select **List Databases** from Action dropdown
3. Tap **Run Scan**

**Expected Output:**
```
Databases:
- information_schema
- mysql
- performance_schema
- webapp_db
- test_db
```

### Get Current Database:

1. Select **Get Current DB** from Action dropdown
2. Tap **Run Scan**

**Expected Output:**
```
Current Database: webapp_db
```

### Get Database Banner:

1. Select **Get Banner** from Action dropdown
2. Tap **Run Scan**

**Expected Output:**
```
Banner: 5.7.29-0ubuntu0.18.04.1
```

---

## Dumping Table Data

Extract data from specific database tables.

### List Tables in a Database:

1. Select **List Tables** from Action dropdown
2. Enter the database name in the **Database** field:
   ```
   webapp_db
   ```
3. Tap **Run Scan**

**Expected Output:**
```
Tables in webapp_db:
- users
- products
- orders
- sessions
```

### Dump Specific Table Data:

1. Select **Dump Data** from Action dropdown
2. Enter database name:
   ```
   webapp_db
   ```
3. Enter table name:
   ```
   users
   ```
4. (Optional) Specify columns:
   ```
   username,password,email
   ```
   Or leave blank to dump all columns
5. Tap **Run Scan**

**Expected Output:**
```
Dumped data from webapp_db.users:
+----------+-----------+-------------------+
| username | password  | email             |
+----------+-----------+-------------------+
| admin    | 5f4dcc... | admin@example.com |
| user1    | e10adc... | user1@example.com |
+----------+-----------+-------------------+
```

---

## Advanced Configuration

Use the **Advanced** tab for fine-tuned control.

### Using a Proxy:

1. Navigate to the **Advanced** tab
2. Enter proxy address:
   ```
   http://127.0.0.1:8080
   ```
3. Go back to **Basic** tab and run your scan

**Use Case:** Route traffic through Burp Suite or another proxy tool.

### Custom User-Agent:

1. Navigate to the **Advanced** tab
2. Enter custom User-Agent:
   ```
   Mozilla/5.0 (Android 12; Mobile) Ghauri/1.4.3
   ```
3. Or enable **Random Agent** checkbox

### Adjusting Timeout:

For slow networks or servers:
1. Navigate to the **Advanced** tab
2. Set **Timeout** to a higher value (e.g., 60 seconds)
3. Run your scan

### Using Multiple Threads:

For faster scanning:
1. Navigate to the **Advanced** tab
2. Set **Threads** to 5-10
3. Run your scan

**Warning:** Higher thread counts may trigger WAF/IPS systems.

### Setting Test Level:

1. Navigate to the **Advanced** tab
2. Select **Level** (1-3):
   - **Level 1**: Basic tests (faster, fewer payloads)
   - **Level 2**: Extended tests (more parameters)
   - **Level 3**: Thorough tests (all parameters, slower)

---

## Real-World Example Workflow

Here's a complete workflow for testing a vulnerable application:

### Scenario: Testing a Blog Application

1. **Initial Test**
   ```
   URL: http://blog.example.com/post.php?id=123
   Action: Test Injection
   ```
   
2. **If Vulnerable, Get Banner**
   ```
   Action: Get Banner
   Result: MySQL 5.7.31
   ```

3. **List Databases**
   ```
   Action: List Databases
   Result: blog_db, mysql, information_schema
   ```

4. **List Tables**
   ```
   Action: List Tables
   Database: blog_db
   Result: users, posts, comments, sessions
   ```

5. **Dump User Table**
   ```
   Action: Dump Data
   Database: blog_db
   Table: users
   Columns: username,email,password
   ```

6. **Extract Specific Rows** (if needed)
   - Use Advanced options
   - Set start/stop limits in future versions

---

## Tips and Best Practices

### 1. Start Simple
- Begin with basic injection tests
- Add complexity only if needed

### 2. Check Results Tab Regularly
- Monitor scan progress
- Look for error messages
- Review successful findings

### 3. Enable Batch Mode
- Reduces user prompts
- Useful for automated testing
- Enabled by default

### 4. Use Appropriate Timeout
- Local testing: 10-30 seconds
- Remote testing: 30-60 seconds
- Slow networks: 60+ seconds

### 5. Respect Rate Limits
- Don't set threads too high
- Add delay between requests if needed
- Avoid triggering security systems

### 6. Save Important Findings
- Screenshot results
- Copy relevant output
- Document injection points

---

## Troubleshooting

### "Error: Please enter a target URL"
- Make sure URL field is not empty
- Include http:// or https://

### "No SQL injection found"
- Try different techniques (B, E, T, S)
- Increase test level (2 or 3)
- Check if parameter is vulnerable
- Verify network connectivity

### "Connection timeout"
- Increase timeout value
- Check internet connection
- Verify target is accessible

### "Permission denied" or Network errors
- Ensure app has internet permission
- Check if device is connected
- Verify firewall settings

### Scan Takes Too Long
- Reduce test level
- Use fewer threads
- Add delay between requests
- Test specific DBMS if known

---

## Legal and Ethical Considerations

### ⚠️ IMPORTANT:

1. **Only test systems you own or have explicit permission to test**
2. **Unauthorized testing is illegal in most jurisdictions**
3. **Use the app responsibly and ethically**
4. **Document your authorization before testing**
5. **Be aware of local laws and regulations**

### Legitimate Use Cases:
- Penetration testing engagements
- Bug bounty programs
- Personal lab environments
- Educational purposes (with consent)
- Security research (authorized)

---

## Additional Resources

- **Main Documentation**: See README.md
- **Build Instructions**: See ANDROID_BUILD.md
- **CLI Documentation**: Run `ghauri --help` on desktop
- **GitHub Issues**: Report bugs or request features

---

## Support

For questions or issues:
- Open an issue on GitHub
- Provide detailed logs from Results tab
- Include app version and Android version
- Describe steps to reproduce the problem

---

**Remember:** With great power comes great responsibility. Use Ghauri ethically and legally.

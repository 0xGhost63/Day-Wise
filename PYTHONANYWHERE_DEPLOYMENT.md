# 🐍 PythonAnywhere Deployment Guide for Day Wise

## ✅ Pre-deployment Setup Complete

The following files have been prepared for PythonAnywhere deployment:
- ✅ `wsgi.py` - WSGI configuration file for PythonAnywhere
- ✅ `requirements.txt` - All necessary dependencies
- ✅ `app.py` - Database initialization configured
- ✅ GitHub repo: https://github.com/0xGhost63/Day-Wise

---

## 🚀 Deploy to PythonAnywhere (100% FREE)

### Step 1: Create PythonAnywhere Account
1. Go to [www.pythonanywhere.com](https://www.pythonanywhere.com)
2. Click **"Pricing & signup"**
3. Choose **"Create a Beginner account"** (FREE forever!)
4. Fill in your details and verify your email

---

### Step 2: Set Up Your Web App

#### 2.1: Open a Bash Console
1. Once logged in, go to the **"Consoles"** tab
2. Click **"Bash"** to open a new bash console

#### 2.2: Clone Your Repository
In the bash console, run:
```bash
git clone https://github.com/0xGhost63/Day-Wise.git My_Diary
cd My_Diary
```

#### 2.3: Create Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 daywise-env
```

#### 2.4: Install Dependencies
```bash
pip install -r requirements.txt
```

---

### Step 3: Create Web App in PythonAnywhere

#### 3.1: Go to Web Tab
1. Click on the **"Web"** tab in the top menu
2. Click **"Add a new web app"**
3. Click **"Next"** for the domain (you'll get: `YOUR_USERNAME.pythonanywhere.com`)
4. Select **"Manual configuration"**
5. Choose **Python 3.10**
6. Click **Next**

#### 3.2: Configure WSGI File
1. In the **Web** tab, scroll to the **"Code"** section
2. Click on the **WSGI configuration file** link (it will be something like `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`)
3. **Delete all the content** in that file
4. **Replace it with the following** (update YOUR_USERNAME):

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/My_Diary'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load environment variables from .env file
from dotenv import load_dotenv
project_folder = os.path.expanduser(project_home)
load_dotenv(os.path.join(project_folder, '.env'))

# Import Flask app
from app import app as application
```

5. **Save** the file (Ctrl+S or click Save button)

#### 3.3: Configure Virtual Environment
1. Back in the **Web** tab, scroll to **"Virtualenv"** section
2. Enter the path: `/home/YOUR_USERNAME/.virtualenvs/daywise-env`
3. Click the checkmark to save

#### 3.4: Configure Static Files
In the **Web** tab, under **"Static files"**, add:
- **URL**: `/static/`
- **Directory**: `/home/YOUR_USERNAME/My_Diary/static`

---

### Step 4: Set Up Environment Variables

#### 4.1: Create .env File
Go back to your **Bash console** and create the `.env` file:
```bash
cd ~/My_Diary
nano .env
```

#### 4.2: Add Your Environment Variables
In the editor, add:
```
OPEN_ROUTER_API=your_actual_api_key_here
```

Press **Ctrl+X**, then **Y**, then **Enter** to save.

---

### Step 5: Initialize Database

In your Bash console, run:
```bash
cd ~/My_Diary
python
```

Then in the Python shell:
```python
from app import app, db
with app.app_context():
    db.create_all()
exit()
```

---

### Step 6: Reload and Launch! 🚀

1. Go back to the **Web** tab
2. Scroll to the top
3. Click the big green **"Reload"** button
4. Your app will be live at: `https://YOUR_USERNAME.pythonanywhere.com`

---

## 🔐 Important Security Notes

### Protect Your Database
Your SQLite database file will be at `/home/YOUR_USERNAME/My_Diary/instance/Users_Data.db`

### Keep .env Secret
- The `.env` file is automatically ignored by git (in your `.gitignore`)
- Never commit API keys to GitHub!

---

## 🔄 Updating Your App

Whenever you make changes to your code:

1. **SSH into PythonAnywhere** or use the Bash console:
   ```bash
   cd ~/My_Diary
   git pull origin main
   pip install -r requirements.txt  # if you added new dependencies
   ```

2. Go to **Web** tab and click **"Reload"**

---

## 📊 PythonAnywhere Free Tier Limits

✅ **What you get FREE:**
- 1 web app at `YOUR_USERNAME.pythonanywhere.com`
- 512 MB disk space
- Always-on (no sleeping!)
- Enough for personal projects
- HTTPS included

❌ **Limitations:**
- Can't use custom domain (need paid plan)
- Can only access whitelisted external sites (openrouter.ai should work)
- Limited CPU time per day

---

## 🛠️ Troubleshooting

### Issue: "502 Bad Gateway"
- Check error logs in **Web** tab → **"Error log"**
- Make sure WSGI file path is correct
- Verify virtual environment path

### Issue: "Module not found"
- Activate virtual environment: `workon daywise-env`
- Reinstall: `pip install -r requirements.txt`

### Issue: "API not working"
- Check if `.env` file exists: `cat ~/My_Diary/.env`
- Verify API key is correct
- Check if `python-dotenv` is installed

### Issue: Database errors
- Reinitialize database (run database setup commands again)
- Check file permissions

### View Logs
- **Error Log**: Shows Python errors
- **Server Log**: Shows access logs
- Both available in the **Web** tab

---

## 💡 Pro Tips

1. **Keep your repo updated**: Always push to GitHub first, then pull on PythonAnywhere
2. **Test locally first**: Make sure everything works locally before deploying
3. **Monitor your CPU quota**: Check the **"Account"** tab for daily CPU usage
4. **Backup your database**: Periodically download your SQLite database file

---

## 🎓 Resources

- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Flask on PythonAnywhere](https://help.pythonanywhere.com/pages/Flask/)
- [Debugging Web Apps](https://help.pythonanywhere.com/pages/DebuggingImportError/)

---

**Need help?** The PythonAnywhere forums are very helpful!

**Your app will be live at**: `https://YOUR_USERNAME.pythonanywhere.com` 🎉

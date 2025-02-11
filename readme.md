# Discord Bot with Google API Integration

This project is a guide to setting up a Discord bot with Python and integrating it with Google APIs (Google Sheets API and Google Drive API). It provides step-by-step instructions for configuring the environment, installing dependencies, and running the bot.

---

## **Features**
- Set up a Discord bot and interact with it on a server.
- Simplified setup for developers using virtual environments and pip.
- Integrate Google APIs for data manipulation and automation.

---

## **Table of Contents**
1. [Prerequisites](#prerequisites)
2. [Discord Bot Setup](#discord-bot-setup)
3. [Python Environment Setup](#python-environment-setup)
4. [Google API Setup](#google-api-setup)
5. [Workflow](#workflow)

---

## **Prerequisites**
- **Python 3.8+** installed on your machine.
- A **Discord account** with access to a server where you can add the bot.
- A **Google account** for accessing Google Cloud services.
- Basic knowledge of Python and Git.

---

## **Discord Bot Setup**
1. **Register as a Developer**
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications) and log in.

2. **Create Your First Application**
   - Click "New Application" and follow the steps in [this tutorial](https://www.youtube.com/watch?v=UYJDKSah-Ww).

3. **Add the Bot to Your Server**
   - Configure bot permissions.
   - Generate an invite link from the Developer Portal and use it to add the bot to your Discord server.

---

## **Python Environment Setup**
1. **Create a Virtual Environment**
   - For macOS/Linux:
     ```bash
     python -m venv myenv
     source myenv/bin/activate
     ```
   - For Windows:
     ```bash
     myenv\Scripts\activate
     ```

2. **Install Dependencies**
   - Install all required packages using:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Bot**
   - Start the Python server:
     ```bash
     python main.py
     ```

4. **Interact with the Bot**
   - Open Discord and test your bot in the configured server.

---

## **Google API Setup**
1. **Enable Google APIs**
   - Enable the following APIs in your Google Cloud Console:
     - [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python)
     - [Google Drive API](https://developers.google.com/drive/api/quickstart/python)

2. **Download Credentials**
   - Create credentials in the Cloud Console.
   - Download the `.json` file, rename it to `credentials.json`, and place it in the project's root directory.

---

## **Workflow**
1. **Update `requirements.txt`**
   - When adding a new package, update `requirements.txt`:
     ```bash
     pip freeze > requirements.txt
     ```

2. **Keep Documentation Updated**
   - Update the `README.md` file whenever there are changes to the workflow or dependencies.

3. **Best Practices**
   - Ensure all dependencies are listed in `requirements.txt`.
   - Regularly test the bot and API integrations after updates.

---

## **Console Tips for macOS**
- Open the console in Chrome:
  ```bash
  Command + Option + C
  ```

---

## **Final Notes**
This guide ensures a smooth handoff for future collaborators. They only need to:
1. Install dependencies using `pip install -r requirements.txt`.
2. Configure Discord and Google API services as outlined.
3. Regularly update the documentation and freeze dependencies.

## **Problem for API auth**
Currently developing on local, hence using OAuth 2.0 credentials. 
Might need to change the auth process if decided to launch the service on cloud. Such as, Workload Identity Pool 


### **Where to Add the Installation & Setup Process?**
You should **add the "Full Installation & Setup Process" right after the "Python Environment Setup" section**.  
This will ensure that users have installed dependencies before proceeding with the next steps.

---

### **Modified README with Installation & Setup Process in English**
#### **New Section: "Full Installation & Setup Process"**
(Insert this section **after "Python Environment Setup"** and before "Google API Setup")

---

## **Full Installation & Setup Process**
Follow these steps to properly set up and run the bot on your local machine.

### **1. Clone the Repository**
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```

### **2. Create a Virtual Environment**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # macOS/Linux
   myenv\Scripts\activate  # Windows
   ```

### **3. Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### **4. Add provided `.env` to the folder**  
   - Ensure the provided `.env` file is placed in the project root directory.
   - It should contain the following variables:
     ```ini
     DISCORD_TOKEN=your-discord-bot-token
     GOOGLE_APPLICATION_CREDENTIALS=credentials.json
     DISCORD_TOKEN=your-discord-bot-token
     DISCORD_SERVER_ID=your-discord-server-id
     DISCORD_CHANNEL_ID=your-discord-channel-id
     CREDENTIALS_FILE=credentials.json
     TOKEN_FILE=token.json
     SPREADSHEET_ID=your-google-sheets-id
     RANGE_NAME=Sheet-number!A1:B6
     ```
   - Ensure the `credentials.json` file is also in the root directory.

   - 📂 **Project Structure**
   ```
   /your-project
   ├── main.py
   ├── .env <-- Include this file
   ├── requirements.txt
   ├── README.md
   ├── credentials.json
   ```

### **5. Run the Bot**
   ```bash
   python main.py
   ```

### **6. Verify the Bot is Running**
   - Open Discord and test the bot with a command (e.g., `/ping`).
   - Check the terminal for the output:  
     ```
     BOT is running！
     ```

## **Github Action to Ec2 Setup Process**
Follow these steps to properly set up github action and EC2.

### **1. create pair keys**
   - Local or EC2 env -> create rsa key pair (private: id_rsa and public: id_rsa.pub)

### **2. setup private key in GitHub Secrets**
   - Bot Repository -> Settings -> Secrets and variables -> Actions -> create a Secret (eg. EC2_SSH_KEY)
   - add content of id_rsa to EC2_KEY

### **2. setup public key in EC2**
   - add id_rsa.pub content to EC2 (~/.ssh/authorized_keys)

### **2. setup credential content in GitHub Secrets**
   - It should contain the following variables:
     ```ini
     DISCORD_SERVER_ID=your-discord-server-id
     DISCORD_CHANNEL_ID=your-discord-channel-id
     DISCORD_TOKEN=your-discord-bot-token
     EC2_HOST=EC2-public-IP（eg. 1.11.22.128）
     EC2_USER=EC2-user-name（eg. ken）
     EC2_SSH_KEY=EC2-private-key (eg. id_rsa)
     EC2_PROJECT_PATH=project-path-in-EC2 (eg. /home/ken/Bot)
     GOOGLE_CREDENTIALS=content-of-credentials.json
     GOOGLE_TOKEN=content-of-token.json
     SPREADSHEET_ID=your-google-sheets-id
     RANGE_NAME=Sheet-number!A1:B6
     ```

### **3. github action triggered when pushing to dev branch**
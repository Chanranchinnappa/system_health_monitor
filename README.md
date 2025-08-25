# 🚀 System Health Monitoring Dashboard

This project is a simple, lightweight system health monitoring solution. It's designed to collect key health metrics from client machines and display them on a centralized web dashboard. The system is built with Python for the backend and data collection, and a simple HTML/CSS/JS frontend for visualization.

## ✨ Features

  - **Multi-OS Support**: Collects health data from Windows, macOS, and Linux machines.
  - **Key Health Checks**: Monitors for critical security and maintenance issues:
      - Disk encryption status (BitLocker, FileVault, LUKS)
      - Pending OS updates
      - Presence of antivirus software
      - Inactivity sleep settings
  - **Centralized Dashboard**: A web-based interface to view the status of all connected machines at a glance.
  - **Real-time Updates**: The dashboard automatically refreshes to show the latest data.
  - **Filtering**: Easily filter machines by operating system or health status (OK/Issue).
  - **Lightweight**: Uses Flask for the backend and a JSON file for data storage, making it easy to set up and run.

## 📦 Project Structure

The project is organized into three main directories:

  - `utility/`: Contains the Python script (`agent.py`) that runs on client machines to collect and send health data.
  - `backend/`: Houses the Python Flask server (`app.py`) that receives data from the clients and serves the dashboard.
  - `frontend/`: Holds the static files for the web dashboard (`index.html`, `styles.css`, `script.js`).

## ⚙️ Getting Started

Follow these steps to set up and run the system.

### 1\. Project Setup

First, clone the repository and navigate to the project directory.

```bash
git clone https://github.com/Chanranchinnappa/system_health_monitor.git
cd system_health_monitor
```

### 2\. The Python Backend Server

The backend receives data from the client utility and stores it.

  - **Install dependencies**:

    ```bash
    pip install flask flask-cors
    ```

  - **Run the server**:
    Navigate to the `backend` directory and start the Flask server.

    ***On Windows Command Prompt (cmd)***

    ```bash
    cd backend
    set FLASK_APP=app.py
    flask run
    ```

    ***On Windows PowerShell***

    ```bash
    cd backend
    $env:FLASK_APP = "app.py"
    flask run
    ```

    ***On macOS/Linux***

    ```bash
    cd backend
    export FLASK_APP=app.py
    flask run
    ```

    > The server will start on `http://127.0.0.1:5000`. Leave this terminal open.

### 3\. The Python System Utility (Client)

This script collects health data and sends it to the backend. You can run it on your local machine to test the setup.

  - **Install dependencies**:
    ```bash
    # On macOS/Linux
    pip install psutil requests
    # On Windows, you also need the wmi package
    pip install psutil requests wmi
    ```
  - **Run the utility**:
    Open a **new terminal**, navigate to the `utility` directory, and run the script.
    ```bash
    cd utility
    python agent.py
    ```
    > The utility will start and send data to the backend every 15 minutes.

### 4\. The Admin Dashboard (Frontend)

The dashboard allows you to view the health status of all connected machines.

  - **Access the dashboard**:
    For the best experience, use a simple local web server to serve the frontend files.

      - Open a **new terminal** and navigate to the `frontend` directory.
        ```bash
        cd frontend
        ```
      - Start the server:
        ```bash
        # For Python 3
        python -m http.server
        # For Python 2
        python -m SimpleHTTPServer
        ```

  - Open your web browser and navigate to `http://localhost:8000`. You should see the dashboard populate with your machine's data.

## 🤝 Contributing

This project is a great starting point for a more robust monitoring system. Feel free to fork the repository and contribute. Here are some ideas for future improvements:

  - **Database**: Replace the JSON file with a more robust database like SQLite or PostgreSQL.
  - **Authentication**: Add user authentication to secure the dashboard.
  - **More Checks**: Implement more detailed health checks (e.g., CPU/RAM usage, running services, network connectivity).
  - **Notifications**: Add a notification system for critical issues (e.g., email or Slack alerts).

## 📄 License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

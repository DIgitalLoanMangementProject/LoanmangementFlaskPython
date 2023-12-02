# LoanmangementFlaskPython
Loan Management sytem implementing prominent standard design patterns to demonstrate knowledge on design patterns learnt

<details>
  <summary>Setting up DB locally [traditional hardway]</summary>
  Setting up MySQL on a Linux system involves several steps. Below is a general guide to get you started. Please note that the exact commands might vary slightly depending on your Linux distribution.

### Step 1: Install MySQL

1. **Update Package Repository** (for most distributions):
   ```bash
   sudo apt-get update
   ```
   Or if you're using a Red Hat-based distribution like CentOS:
   ```bash
   sudo yum update
   ```

2. **Install MySQL**:
   For Debian-based distributions (like Ubuntu):
   ```bash
   sudo apt-get install mysql-server
   ```
   For Red Hat-based distributions:
   ```bash
   sudo yum install mysql-server
   ```

### Step 2: Secure MySQL Installation

After installation, it's important to secure your MySQL installation.

1. **Run the Security Script**:
   ```bash
   sudo mysql_secure_installation
   ```
   This script will guide you through setting a root password, removing anonymous users, restricting root user access to the local machine, and removing the test database.

### Step 3: Start and Enable MySQL Service

1. **Start the MySQL Service**:
   ```bash
   sudo systemctl start mysql
   ```

2. **Enable MySQL to Start on Boot**:
   ```bash
   sudo systemctl enable mysql
   ```

### Step 4: Verify MySQL Installation

1. **Check MySQL Service Status**:
   ```bash
   sudo systemctl status mysql
   ```

2. **Log into MySQL**:
   ```bash
   mysql -u root -p
   ```
   You'll be prompted to enter the root password that you set during the secure installation process.

### Step 5: Create a New Database and User (Optional)

You might want to create a new database and a new user for your applications.

1. **Create a New Database**:
   ```sql
   CREATE DATABASE mydatabase;
   ```

2. **Create a New User and Grant Permissions**:
   ```sql
   CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';
   GRANT ALL PRIVILEGES ON mydatabase.* TO 'myuser'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Step 6: Additional Configuration (Optional)

Depending on your requirements, you may need to configure MySQL further, like setting up remote access, tuning performance, etc.

### Troubleshooting and Documentation

- If you encounter issues, checking the MySQL logs can be helpful. These are typically located in `/var/log/mysql/`.
- For more detailed information, consult the MySQL documentation relevant to your specific version.

Remember that these steps are quite general. If you're using a specific Linux distribution or have specific requirements, the steps might differ.
</details>

<details>
  <summary>Setting up DB using docker[Easy modern approach]</summary>
  To set up MySQL using Docker with a single command, you would typically pull a MySQL image from Docker Hub and run a container based on that image. Here's a basic example of how to do this:

```bash
docker run --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:tag
```

In this command:

- `--name some-mysql`: Assigns the name `some-mysql` to your container.
- `-e MYSQL_ROOT_PASSWORD=my-secret-pw`: Sets the environment variable `MYSQL_ROOT_PASSWORD`, which is used to define the password for the MySQL root user. Replace `my-secret-pw` with your desired password.
- `-d`: Runs the container in detached mode, meaning the container runs in the background.
- `mysql:tag`: Specifies which version of MySQL you want to use. Replace `tag` with the specific MySQL version tag (e.g., `8.0`, `5.7`). If you omit the tag, Docker will pull the latest version by default.

### Additional Options

- **Data Persistence**: To persist data, you should mount a volume to the MySQL container:
  ```bash
  docker run --name some-mysql -v /my/own/datadir:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql
  ```
  Replace `/my/own/datadir` with the path on your host where you want to store MySQL data.

- **Port Mapping**: To access the MySQL server from outside the container (like from your host machine), map the container's port to a host port:
  ```bash
  docker run --name some-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql
  ```
  This command maps port 3306 inside the container (the default MySQL port) to port 3306 on your host machine.

Remember, running a database in a Docker container is great for development and testing, but for production environments, you should consider additional configurations for security and performance. Always ensure your MySQL server is properly secured, especially if it's exposed to the internet.

</details>

docker run --name admin -e MYSQL_ROOT_PASSWORD=adminPass -p 3306:3306 -v /home/akshith/Desktop/New Folder/Dbs:/var/lib/mysql -d mysql:latest

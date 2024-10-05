## **NITC-firewall-authenticator**

## **Introduction**

NITC-firewall-authenticator is a project that ease the process of login and logout of nitc network.
It can automate whole nitc network management in one click
It allow user to setup auto logout before shutting down

Windows distro will be available soon

## **Installation for linux based system**

To install NITC-firewall-authenticator, follow these steps:

1. Clone the repository: **`git clone https://github.com/Utkarsh-0192a/NITC-firewall-authenticator`**
2. Navigate to the NITC-firewall-authenticator directory: **`cd NITC-firewall-authenticator`**
3. Make setup executable : **`chmod +x setup`**
4. Setup the NITC-firewall-authenticator: **`./setup`**
6. Start the project: **`NITCc`**

## **Manual**
1. Login to network using saved password : **`NITCc -l`**
2. Login to network using new username and password : **`NITCc -l -u newusername -p passwordforuser`**
3. Change saved username password : **`NITCc -cd -u username -p password`**
4. Logout from NITC network : **`NITCc -lo`**

## **Contributing**

If you'd like to contribute to NITC-firewall-authenticator, here are some guidelines:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes.
4. Write tests to cover your changes.
5. Run the tests to ensure they pass.
6. Commit your changes.
7. Push your changes to your forked repository.
8. Submit a pull request.


## **Authors and Acknowled

UTKARSH GAUTAM

NITC-firewall-authenticator was created by **[Utkarsh Gautam](https://github.com/Utkarsh-0192a)**.




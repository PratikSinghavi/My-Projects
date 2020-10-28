# MOGLIE (Movie Offer Getter & Limber Information Emailer)
As a frequent moviegoer myself, this is an attempt to get great offers and discounts on the next screening of your favourite movie!

Have a look at the video in the folder **'demo/Demo.mov'** to see it in action! ;)

## Recommendations:
* I personally use this project regularly and have setup (and recommend) a **cron job** to run the script every 15 days.
* The email is an easy way to access the offers and immediately book tickets as it takes you to the page with offer details and has a 'Book Now' button.


## Additional Use Case
* For a client of the app, the benefits are obvious as the offers can be used to save on the movie tickets.
* Another use case is that this can be used for marketing by extending the application to send out offer details to (multiple) customers in order to get a larger audience and incease sales. 
* This might require additional customer information and could be generally available with the business through previous online bookings. 
* Additional ML models can be added to customize the offers further or decide on which offers attract the customers the most.

## Technical Details
* Implements **Selenium python bindings** with **Firefox webdriver** to automate the process of searching for offers on the website.
* html content in the email prepared using **yattag**.
* **smtplib** to send out the email to the recipient.

### Requirements: 
* Python(v3.7.3)
* yattag==1.14.0
* python-decouple==3.3
* selenium==3.141.0
* smtplib

## Steps to configure/run :

### Step 1 : Configuration 
* Open the env file and setup the following config parameters : 
    | Parameter | Description |
    | --- | --- |
    |CITY | City where the offers are to be searched|
    |BANK_NAME | Bank name in lowercase eg. axis |
    |SAVE_HTML | Saves the mail htmlcontent if this is set to True  |
    |RECEIVER_EMAIL_ID | Users email ID|
    |SENDER_EMAIL_ID* | Any email id that can log in using smtplib functions|
    |SENDER_PASSWORD | Password for the SENDER_EMAIL_ID|
* Save it as '**.env**' file, the script will throw an error suggesting config parameter not found if this step is not done correctly. **DO NOT FORGET** 

Note - 
* *The Sender email id has to enable Less secure apps access using [this](https://myaccount.google.com/lesssecureapps) link. 
* Another (**Recommended**) way is to create an App-password if you have 2-factor-authentication enabled.


### Step 2 : Execution/Run 
* Simply run using the following command after navigating to the directory where main.py is located:

``` >> python3 main.py ```

#### Additional Notes:
* The output.html will not show images when opened, the purpose is to verify if the html document is genreated with correct img tags and src property. Inspect the code to understand how the images are attached in the mail.
* To see the html completely, the src property will have to be modified to point to the correct images in the html document.
* **'/demo'** contains the complete demonstration of the code execution called **Demo.mov**.
* The above directory also includes a mail sample (for a different bank).

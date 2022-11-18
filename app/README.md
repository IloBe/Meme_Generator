[//]: # (Image References)

[image1]: ../assets/Meme_wolf_example.png "General start page:"
[image2]: ../assets/creatorStartPage.PNG "Creator start page:"
[image3]: ../assets/greeceImageIvanKarpov_quoteKhalilGibran_65perc.png "Correct creator workflow:"
[image4]: ../assets/pageNotFound-Message.PNG "Invalid creator workflow:"
[image5]: ../assets/FlaskApp_pageIfSomethingWentCompletelyWrong-onlyActiveButtons.PNG "Something went completely wrong:"


# User Guidance of the Flask Meme Application

This **readme** delivers some more information about the meme workflow by usage of the browser application. We deal 
with randomly created meme images or could create our own ones by execution a manually added URL of a .jpg resp. .png 
image or a .webp photo.

## Application Start
As already mentioned, we start by calling the `app.py` Python script on the **command-line interface** via
```python3
python app.py
```
Some information about Flask and specific project directory status will be printed on the terminal. If nothing happens anymore,
you can do the second step.

Then, start the web application with your **browser** by calling your localhost with port 3001
```
https://localhost:3001
```

Because no certifications are created, your browser will probably show you some risk messages. Being on a development system and
not on a production server, ignore them by now and accept the risk by clicking on the associated buttons.

You are there ... see the start page, something like this:

![General start page][image1]

The first random meme is created for you. Mostly, it will be different each time you start the Flask application. Now, there are 
2 possibilities for you to work on.

<br>

## 2 Ways of Working
### Random
If you want to show randomly created meme images only click on the **Random** button. Everything else happens in the background and 
a new dog or wolf image is displayed on the screen with randomly chosen and positioned text out of given lists of images and texts.

### Own Creation
If you think at your own image stored on a web server, accessible via URL and a text you want to add to the image content, then use
the **Creator** button. After click on it, the following page is shown:

![Creator start page][image2]

As an important note:
- The URL attribute parameter must be a real image URL from the web. If you use a directory path from your system, the workflow aborts.
- If you write an arbitrary character string (not starting with https: or http:) you will see a message in your configured system language
to add a valid URL.
- If you have added an URL of a .jpg, .png or .webp file and have not added one of this extensions (in upper- or lowercase characters), 
the software will convert your file to a .jpg image automatically.

But if your input to the mentioned attribute parameters are fine and the workflow happens correctly, you will see your meme. Something like

![Correct creator workflow][image3]

<br>

## Forseen Exceptions
Nevertheless as you know, dealing with the web may end up in exceptions and unknown issues. As a simple example, the server your image is on is down. Another reason could be that the image URL you have entered maps to an image being too big. All image URLs used for positive testing have had an image size of nearly 100 KB. Negative testing images to trigger the 'not-found-page' have had an image size around 900 KB.

In this cases, the application will lead you to another page, telling you that your page is not found and delivering some additional information.

![Invalid creator workflow][image4]

There you can click on the link, telling you *go somewhere nice* to come back to the start page where the application has already created a 
random meme for you.<br>
Or as another option use the already known *Random* or *Creator* buttons to start again.

<br>

## Application Ending
Have in mind, that this is still a simple browser application, because main project focus has been object-oriented programming and quality concepts 
regarding software engineering, so, you can stop the application by simplest ending only:
- on command-line terminal press CTRL+C to quit the meme application.

<br>

## Additional Final Note: Something Weird Appears
Being a human, mistakes may happen which have not been foreseen. So, if you are playing around with this software and get an image like this, 
please tell me via *GitHub issue* creation about your workflow that leads to that situation. 

![Something went completely wrong][image5]

I appreciate your comments and say thank you in advance.


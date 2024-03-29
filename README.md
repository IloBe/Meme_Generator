[//]: # (Image References)
[image0]: https://readthedocs.org/projects/pycodestyle/badge/ "Inline docs"
[image1]: ./assets/creatorExample_Berlin-IvanKarpov_55perc.png "None wrapped text"
[image2]: ./assets/MemeWithVeryLongWordSplittedByTextWrapper_55perc.png "Wrong wrapped text"
[image3]: ./assets/mod_photo-1651307313221-51c1ce725da6_55perc.png "Correct wrapped text"
[image4]: ./assets/Python_Meme_Generator_project_structure.png "Python project structure"
[image5]: ./assets/Meme_wolf_example.png "Random button example"
[image6]: ./assets/greeceImageIvanKarpov_quoteKhalilGibran_65perc.png "Creator button example"

![example workflow](https://github.com/IloBe/Meme_Generator/actions/workflows/codeql-analysis.yml/badge.svg) ![Inline docs][image0]
[![Known Vulnerabilities](https://snyk.io/test/github/IloBe/Meme_Generator/badge.svg)](https://snyk.io/test/github/IloBe/Meme_Generator)

# Python Meme Generator Project

## General Overview

Welcome to this project to build a **Meme Generator Application** for random or customized 
images. The goal is a multimedia application of dynamically generating memes, in other 
words including images with an overlaid quote. So, not a real meme :smile:, but something to
put text on an image.

The beautiful, professional photos are from unsplash collections of
[Ivan Karpov](https://unsplash.com/@ivkrpv) for testing the URL access of the Flask application. 
The wolf images are from 
[freepngs.com](https://www.freepngs.com/wolf-pngs?pgid=ivye5l9w-25173dad-5461-11e8-a9ff-063f49e9a7e4)
and stored in the project data directory for random meme creation of the Flask application and for
command line interface call of the application. The same applies for the dog images which are delivered 
by [Udacity](https://www.udacity.com/) regarding this project 2 of the course *IntermediatePython*.

Amongst others, main motivation for project implementation are the usage of object-oriented 
concepts of `Python`, regarding decorators, DRY (don’t repeat yourself) principles of class 
resp. method design and working with modules and packages.

Another project topic has been to follow [PEP 8](https://peps.python.org/pep-0008/#introduction) coding style guide and [PEP 257](https://peps.python.org/pep-0257/) docstring conventions which are checked by usage of the tools [pycodestyle](https://pypi.org/project/pycodestyle/) and [pydocstyle](https://pypi.org/project/pydocstyle/).

<br>

## Technical Information

### 1. Project Structure
Beside the top level source code, the project is separated in Python modules for quote 
handling and meme image creation.
Some logging is added for module parts via `__init__.py` files and `app.logger` for the 
Flask application part.

Regarding the general application workflow, we use different files for the types of quotes 
that we'll be overlaying on images.
Furthermore, we actual preprocess our images - default ones of .jpg dogs and .png wolfs 
are given - using `Pillow`. Photo URL delivered .webp files are converted to .jpg images.

As font .ttf file *standard arial* is added.

Regarding the project structure, some files and directories are relevant for development 
but not for the application, like log files or the mypy cache directory. They are 
excluded via .gitignore files.

**Our main modules are:**
#### 1.1 Quote Engine
The Quote Engine module is responsible for ingesting many types of files containing quotes.
For our purposes, a quote includes a body and an author information:
```
"This is a quote body" - Author
```

Strategy *Ingestor helper classes* handle the different file types (csv, docx, 
pdf, txt) containing quotes by implementing the abstract base class `IngestorInterface` 
method signatures:
```python3
def can_ingest(cls, path: str) -> boolean
def parse(cls, path: str) -> List[QuoteModel]
```

The final `Ingestor` class encapsulates all of this Ingestor helper classes.

<br>

#### 1.2 Meme Generator
The Meme Generator module is responsible for manipulating and drawing text onto images 
by usage of the third party library 'Pillow' for image manipulation. We handle .png and 
.jpg image types by usage of strategy *Image Ingestor helper classes*.
The same strategy design pattern concept as for quotes is implemented.

Via `MemeEngine` class the process - including preprocessing - is triggered. The following 
image preprocessing happens:
- resizing the image, so, the width is at most 500px and the height is scaled proportionally 
(preserve aspect ratio)
- additionally, .png images are transformed to grayscale images
- text wrapping happens for long text parts, so, the whole text can be positioned inside the
bounding box of the image including some marginal free space. A litte mistake is still there: 
If a word is too long for font depending text bounding box, the text wrapper instance breaks 
it down into few parts, fitting to availabe position area.
The separation might not fit to spelling as shown in the following example images (non wrapped text, 
wrong wrapped text, correct wrapped text).

![None wrapped text][image1], ![Wrong wrapped text][image2], ![Correct wrapped text][image3]

<br>

The MemeEngine class implements the following instance method signature which returns the path to 
the manipulated meme image:
```
make_meme(self, img_path, text, author, width=500) -> str
```
<br>

#### 1.3 Project Implementation Structure
Our final project software is structured like this:

![Python project structure][image4]
Image source - own created image

<br>

### 2. Project Instructions

#### 2.1 Installation
For implementing this project *Python V3.9.12* is used in a virtual environment called **meme**.
All tests have happened on different Windows systems. So in general, an appropriate conda installation is expected. 
Furthermore, we need the C++ library `pdftotext`, therefore some conditions exist to be fulfilled.

As **first prerequisite**, according to pypi information about the [library](https://pypi.org/project/pdftotext/) on Windows, it is currently tested only 
when using conda by following the mentioned process. This library relys on the *poppler* library which is a utility for rendering PDFs and 
it is common to Linux systems, but not Windows! So, we have to install it by ourself:
- Install the Microsoft Visual C++ Build Tools
- Install *poppler* through conda:<br>
	$ conda install -c conda-forge poppler

**Second prerequisite** is having the C++ library `pdftotext` installed used by a subprocess call for pdf documents. Therefore, we need to install `xpdf` library which includes such tool. For *Windows*, you'll need to:
- Download the Windows command-line tools from the [xpdf website](https://www.xpdfreader.com/download.html). 
- Unzip the files in a location of your choice. 
- Get this full file path to the folder named bin32 (if you have a 32-bit machine) or bin64 (if you have a 64-bit machine). 
- Add this path to the Path environment variable of your system. This will allow you to use the xpdf command from the command line. 
If you've never done this before, for Windows systems: check out this [Stack Overflow post](https://stackoverflow.com/questions/44272416/how-to-add-a-folder-to-path-environment-variable-in-windows-10-with-screensho) on how to add a folder to the Path environment variable. 

For *Linux*, you can use [Homebrew](https://brew.sh/) or apt-get to install via
```
sudo apt-get install -y xpdf 
```
in your command line interface. Note: the project is tested with Windows 8 and Windows 10 only. 

<br>

**Afterwards**, for working with this project codings, you can use the *requirements.txt* file directly to create 
your own virtual environment. This file has been created with the *pip freeze* command, so, all libraries are included installed 
via pip for the projects virtual environment. Inside that environment, the installation happens e.g. by calling
```
pip install -r requirements.txt
```

<br>

#### 2.2 Getting started
We can start the appliation via CLI terminal with **main.py** or by Flask call with **app.py**.
So, change to the associated project directory that includes these files and execute it.
Depending on your Python environment configuration, it is started with command 'python' or 'python3'.
Having Python 3 versions installed and configured, we use 'python' during the following text.

##### 2.2.1 CLI with or without arguments
The **main.py** script can be invoked from the command line with and without arguments.
If no argument is given, a random meme is created using default images and quotes.
By using your own arguments for --body and --author put double quotes around their values
to handle string sentences including blanks.<br>
Have in mind that all such arguments always belong together.

```
$ python main.py [args] with args being --path, --body, --author
```

The script returns a path to a generated image stored in the 'tmp' directory of the project. 
If any argument is not defined, a random selection is used.

##### 2.2.2 Flask Web Application
[Flask](https://palletsprojects.com/p/flask/) is a popular Python microframework to build 
web applications for easy up to more complex tasks. Information how to use it can be found 
on this [Quickstart](https://flask.palletsprojects.com/en/1.1.x/quickstart/#static-files) page 
or on Miguel Grinbergs Flask [Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

The project contains a flask app starter code in **app.py** for a simple web application. 

- It runs by usage of the following command as first action point on your command-line terminal being in the 
projects top level directory:
```python3
python app.py
```
Means, as implemented there on localhost with port number 3001 we have to trigger the following second action point.

- Then on your browser using the *original given app.run() method*, by using the call 
```
https://localhost:3001
```
to start the web application the following error appears:
- code 400, message Bad HTTP/0.9 request type

Therefore the **Flask run() task** has been changed by adding the parameter *ssl_context='adhoc'*.
Furthermore, we have to install the *pyopenssl* library to use the https-call.

Have in mind, that this application is only for testing and not for a save production server.
No valid certificate is created which in general is necessary.
As a consequence, for this project status you have to deal with browser safety messages.<br>
E.g. Firefox mozilla tells you using an invalid certificate:
```
Error code: MOZILLA_PKIX_ERROR_SELF_SIGNED_CERT
```
Not being on a production system, we accept the risk and continue.
For details regarding certification handling, have a look to the blog post of 
[Qiang Zhang](https://zhangtemplar.github.io/flask/)

Another error may appear regarding JAVA, if you don't use a *JDK >= version 13*, because in a 
former version a bug exists working with Server and ServerSocket classes, called:
> TLSv1.3 may generate TLSInnerPlainText longer than 2^14+1 bytes

If this is the case on your local machine, you will get the error message 
```
Error code: SSL_ERROR_RX_RECORD_TOO_LONG
```
Fix it by upgrading the JDK as explained e.g. on the following blog post of 
[Nam Ha Minh](https://www.codejava.net/java-se/download-and-install-oracle-jdk-16).

On my machine, I am using Java SE Development Kit 18.0.1.1 [downloads](https://www.oracle.com/java/technologies/downloads/#jdk18-windows)
with SHA256 checksum bd284974e9c5a80902a2e5ea17660ad248cef3684da0b1ce4b58f48696cc9bb9.
<br>

**So finally, if your meme browser app is running:**<br>
The app uses the Quote Engine and Meme Generator modules to generate a random captioned meme
image by user click (see left image example below) on a button or creates a new meme by given user 
information about image path (URL of the graphic image or photo), quote body and author by specific 
creator start page. There the Flask application uses the `requests` package to fetch an image from 
a submitted URL (see right image example below). The newly created meme images are stored in the 
*static* directory of the project.

Note: It is still a simple application, so, if you want to stop it, on command-line terminal press *CTRL+C* 
to quit the meme application. If something went wrong with your input parameters a page-not-found message with 
some additional information appears.

A small *user guidance* delivers the [readme file](https://github.com/IloBe/Meme_Generator/tree/main/app#readme) 
of this projects *app directory*.

![Random button example][image5], ![Creator button example][image6]

<br>

## License
This project coding is released under the 
[MIT License](https://github.com/IloBe/Meme_Generator/blob/main/LICENSE).

[//]: # (Image References)
[image1]: ./Docker_image.png "Docker icon"
[image2]: ./Python_Meme_Generator_project_structure.png "Python project structure"
[image3]: ./Meme_wolf_example.png "Meme example"

# Python Meme Generator Project

## General Overview

Welcome to this project to build a **Meme Generator Application** for random or customized 
images. The goal is a multimedia application of dynamically generating memes, in other 
words including images with an overlaid quote.

Amongst others, motivation for project implementation are the usage of object-oriented 
concepts of Python, regarding decorators, DRY (don’t repeat yourself) principles of class 
resp. method design and working with modules and packages.

As an improvement, the source code is handled by containerisation mechanism with 
[Docker](https://www.docker.com/products/docker-desktop/) for having an isolated 
application. 

![Docker icon:][image1]
[Image source](https://www.docker.com/products/docker-desktop/)

Nevertheless, the project includes a *requirements.txt* file containing 
used library dependencies.

The realisation of this containerisation concept is based on the medium blog post of 
[Angelica Lo Duca](https://towardsdatascience.com/how-to-run-a-data-science-project-in-a-docker-container-2ab1a3baa889).

<br>

## Technical Information

### 1. Project Structure
Beside the top level source code, the project is separated in Python modules for quote 
handling and meme image creation.
Some logging is added for module parts via `__init__.py` files.

Regarding the application workflow, we use different files for the types of quotes that 
we'll be overlaying on images.
Furthermore, we actual preprocess our images - default ones of .jpg dogs and .png wolfs 
are given - using `Pillow`.

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
def can_ingest(cls, path) -> boolean
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

The class implements the following instance method signature which returns the path to 
the manipulated meme image:
```
make_meme(self, img_path, text, author, width=500) -> str
```
<br>

#### 1.3 Docker
For creation of the Docker image and Docker container *Docker desktop for Windows V4.8.1* 
(at least Windows 10 as basic operating system) is used. It is expected, because during 
its installation WSL 2 is recommended instead of Hyper-V, Docker usage is possible in 
Windows Container modus only (e.g. Windows Server Core). With this version Docker-Compose 
is included already.

If you want to work with docker desktop, take care of the *service agreement*. For this 
project it is for private use and therefore for free.

Regarding the deployment of the application, a *Docker image* is build which runs in a 
*Docker container*. Thus, we need at least
- our application source code and 
- a [Dockerfile](https://docs.docker.com/engine/reference/builder/) to build the image.


So, our workflow is *Dockerfile –> Docker Image –> Docker Container*.

As Angelica writes, the basic structure of the Dockerfile is
```
FROM <BASE_IMAGE>
COPY <SRC> <DTS>
RUN <COMMANDS_AT_BUILD_TIME>
CMD <ENTRY_COMMANDS_AT_RUNTIME>
```
which is in our case extended i.a. by the WORKDIR parameter defining the current directory in the Docker image.

The Docker image - the private file system providing all files and codes the container needs - 
is created with help of the Dockerfile by the command:
```
docker build -t pythonmemegenerator .
```

After this build, here are some Docker commands to work with:
- **docker ps -a** shows all Docker container, running or not
- **docker image ls** listed all downloaded Docker images
- **docker run –help** shows all information about the run command usage
- for more see [fosstechnix cheat-sheet](https://www.fosstechnix.com/docker-command-cheat-sheet/)

The created Docker image and its container are not pushed to Docker-Hub. All files to create 
the image are stored on this GitHub repository only. If you want to share a docker image, 
you must be signed in to Docker Hub and use the following commands:
- docker tag pythonmemegenerator /pythonmemegenerator
- docker push /pythonmemegenerator
<br>

#### 1.4 Project Implementation Structure
Our final project software is structured like this:

![Python project structure:][image2]
Image source - own created image

<br>

### 2. Project Instructions

#### 2.1 Installation
For implementing this project *Python V3.9.12* is used in a virtual environment called **meme**.
So in general, a conda installation is expected. For our Docker handling we deliver an *environment.yml* file,
needed for conda inside the Dockerfile. Furthermore, we need the C++ library `pdftotext`, therefore some 
conditions exist to be fulfilled.

As **first prerequisite**, we need to install `xpdf` library. For *Windows*, you'll need to:
- Download the Windows command-line tools from the [xpdf website](https://www.xpdfreader.com/download.html). 
- Unzip the files in a location of your choice. 
- Get the full file path to the folder named bin32 (if you have a 32-bit machine) or bin64 (if you have a 64-bit machine). 
- Add this path to the Path environment variable. This will allow you to use the xpdf command from the command line. 
If you've never done this before, check out this [Stack Overflow post](https://stackoverflow.com/questions/44272416/how-to-add-a-folder-to-path-environment-variable-in-windows-10-with-screensho) 
on how to add a folder to the Path environment variable. 

For *Linux*, you can use [Homebrew](https://brew.sh/) or apt-get to install via
```
sudo apt-get install -y xpdf 
```
in your command line interface. Note: the project is tested with Windows 8 (general behaviour without docker) and Windows 10 (with Docker) only.

**Second prerequisite** is having the C++ library `pdftotext` installed used by a subprocess call for pdf documents.
According to pypi information about the [library](https://pypi.org/project/pdftotext/) on Windows it is currently tested only 
when using conda by following the process. This library relys on the *poppler* library which is a utility for rendering PDFs and 
it is common to Linux systems, but not Windows!
- Install the Microsoft Visual C++ Build Tools
- Install *poppler* through conda:<br>
	$ conda install -c conda-forge poppler

<br>
Afterwards, for working with this project codings, you can use the *requirements.txt* file directly to create 
your own virtual environment. This file has been created with the *pip freeze* command, so, all libraries are included installed 
via pip for the virtual environment. Inside that environment, their installation happens e.g. by calling
```
pip install -r requirements.txt
```
<br>

Or we start a Docker container based on the Docker image of our previous project step. It includes 
all installation dependencies and installs them for you automatically. Running the container launches
the application with private resources, isolated from the rest of the machine.
Run it with the following command in the directory you want to use as project home:
```
docker run -p 80:80 --name container-memegenerator pythonmemegenerator
```
<br>

#### 2.2 Getting started
We can start the appliation via terminal with **main.py** or by Flask call with **app.py**.
So, change to the associated directory that includes these files and execute it.
Depending on your Python environment it is started with command 'python' or 'python3'.

##### 2.2.1 CLI with or without arguments
The **main.py** script can be invoked from the command line with and without arguments.
If no argument is given, a random meme is created using default images and quotes.
By using your own arguments for --body and --author put double quotes around their values
to handle string sentences including blanks.<br>
Have in mind that all such arguments always belong together.

```
$ python3 main.py [args] with args being --path, --body, --author
```

The script returns a path to a generated image stored in the 'tmp' directory of the project. 
If any argument is not defined, a random selection is used.

##### 2.2.2 Flask Web Application
[Flask](https://palletsprojects.com/p/flask/) is a popular Python microframework to build 
web applications for easy up to more complex tasks. Information how to use it can be found 
on this [Quickstart](https://flask.palletsprojects.com/en/1.1.x/quickstart/#static-files) page 
or on Miguel Grinbergs Flask [Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world).

The project contains a flask app starter code in **app.py** for a simple web application. 

- It runs by usage of the following command on your command-line terminal being in the 
projects *app* directory:
```python3
python app.py
```
means, on localhost with port number 3001.

- Then on your browser using the *original given app.run() method*, the call works fine with 
```
http://localhost:3001
```
to start the web application. But using the browser call:
```
https://localhost:3001
```
to start the web application with the original app.run() task, the following error appears:
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
image by user click on a button or creates a new meme by given user information about image
path, quote body and author. It uses the `requests` package to fetch an image from 
a submitted URL. The newly created meme images are stored in the *static* directory of the project.

Note: It is still a simple application, so, if you want to stop it, on command-line terminal press *CTRL+C* 
to quit the meme application.

![Meme example:][image3]
[Image source](https://www.udacity.com/) and there project 2 of the course *IntermediatePython*.

<br>

## License
This project coding is released under the 
[MIT License](https://github.com/IloBe/Meme_Generator/blob/main/LICENSE).

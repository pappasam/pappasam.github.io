##########################################################################
Smaller Python Docker Containers with Multi-Stage Builds and Python Wheels
##########################################################################

:date: 2018-04-21
:category: Software Development
:modified: 2018-04-21
:tags: Docker, Python, pip

If your Docker Python build requires system dependencies that are NOT required
at runtime, structure your build as follows:

1. Use a `multistage build`_
2. Stage 1 installs system dependencies and uses them to build local wheels_
3. Stage 2 begins from the same base as Stage 1, copies wheels from
   Stage 1, and installs the wheels
4. The rest of your build will be based on Stage 2

.. _`multistage build`: https://docs.docker.com/develop/develop-images/multistage-build/
.. _wheels: https://pythonwheels.com/

If you follow these steps, you'll end up with the smallest-possible Python
Docker container all your desired dependencies intact.

.. PELICAN_END_SUMMARY

Note: this post references Docker 18.03, Python 3.6, and pip 10. I assume that
you are running CPython_ (Python's reference implementation).

.. _CPython: https://github.com/python/cpython

The problem
===========

We want to do a Python system build using Docker. Python system builds often
require installing third-party code. This third-party code may contain code or
resources that must be compiled during their installation. For simplicity's
sake, assume we are talking about source code in the C programming language.
Since a Docker container will be our "target machine", we'll need a C compiler
in our Docker container. Unfortunately, C compilers are large programs. Since
we plan to scale our number of containers up and down based on the demand for
its provided service, the image should ideally be as small as possible.

Basically, we want to build C code with a C compiler and then throw away the C
compiler to save space in our deployment image.

Examples
========

The following examples should clarify the problem and its resolution. Note: I'm
assuming that you're using a POSIX_-inspired system.

.. _POSIX: https://en.wikipedia.org/wiki/POSIX

Setup
-----

Copy the following Makefile into your current working directory.

.. include:: docker-python-install-wheels/Makefile
    :code: make
    :class: highlight
    :encoding: utf-8

Example 1: broken build requiring a C compiler
----------------------------------------------

We have a simple, entrypoint_-less Docker container in which we must install
uWSGI_. In the uWSGI quickstart_ guide, its developers clarify that it "is a
(big) C application, so you need a C compiler (like gcc or clang) and the
Python development headers".

Copy the following code into a file called "Dockerfile.break":

.. _entrypoint: https://docs.docker.com/engine/reference/builder/#entrypoint
.. _uWSGI: https://uwsgi-docs.readthedocs.io/en/latest/
.. _quickstart: https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html

.. include:: docker-python-install-wheels/Dockerfile.break
    :code: docker
    :class: highlight
    :encoding: utf-8

Now run the following shell command in the same directory as your
Dockerfile.break.

.. code:: bash

   make build-break

At the end of our failed build, we see this Traceback (in addition to other
helpful messages):

.. code:: py3tb

   Traceback (most recent call last):
     File "<string>", line 1, in <module>
     File "/tmp/pip-install-tkd8plx9/uwsgi/setup.py", line 137, in <module>
       'Programming Language :: Python :: 3.6',
     File "/usr/local/lib/python3.6/site-packages/setuptools/__init__.py", line 129, in setup
       return distutils.core.setup(**attrs)
     File "/usr/local/lib/python3.6/distutils/core.py", line 148, in setup
       dist.run_commands()
     File "/usr/local/lib/python3.6/distutils/dist.py", line 955, in run_commands
       self.run_command(cmd)
     File "/usr/local/lib/python3.6/distutils/dist.py", line 974, in run_command
       cmd_obj.run()
     File "/tmp/pip-install-tkd8plx9/uwsgi/setup.py", line 77, in run
       conf = uc.uConf(get_profile())
     File "/tmp/pip-install-tkd8plx9/uwsgi/uwsgiconfig.py", line 747, in __init__
       raise Exception("you need a C compiler to build uWSGI")
   Exception: you need a C compiler to build uWSGI

Consistent with the uWSGI documentation, our system has said that we "need a C
compiler to build uWSGI". We'll do that in example 2.

Example 2: large build with C compiler installed
------------------------------------------------

In this example, we'll install our system dependencies so uWSGI can actually be
built.

Copy the following code into a file called "Dockerfile.big":

.. include:: docker-python-install-wheels/Dockerfile.big
    :code: docker
    :class: highlight
    :encoding: utf-8

Now run the following shell command:

.. code:: bash

   make build-big

In the "build-big" make target, I've included a command to list all Docker
images on your system. Because of this command, you should see something close
to the following in your terminal:

.. code:: text

   REPOSITORY          TAG                 IMAGE ID            CREATED                  SIZE
   blog-python         big                 8a68d0dad407        Less than a second ago   251MB
   python              3.6-alpine          8eb1c554687d        16 hours ago             90.4MB


The good
~~~~~~~~

The image built successfully.

The bad
~~~~~~~

The image is unnecessarily large.

We're planning on scaling our web-service to handle a decent amount of traffic.
Scaling will involve deploying many images on many servers. Larger images take
longer to deploy and (obviously) take up more space than smaller images.

The ugly
~~~~~~~~

We are including an unnecessary dependency.

We don't need a C compiler in the image, so the C compiler is an unnecessary
dependency.  Including an unnecessary dependency in our runtime image is a
horrible design, similar to including an unnecessary Python dependency in our
requirements.txt or setup.py. As great software developers, we HATE bad system
design, so let's find a way to resolve the "bad" and the "ugly" while
preserving the "good"!

Example 3: failed attempt at simply "uninstalling" C compiler
-------------------------------------------------------------

Unfortunately, if we want to reduce our image size, we cannot simply
"uninstall" the C compiler. For reasons that I do not fully comprehend at this
time, Docker caches anything you install in an image, so uninstalling a
dependency does NOT reduce the image size.

Copy the following code into a file called "Dockerfile.uninstall":

.. include:: docker-python-install-wheels/Dockerfile.uninstall
    :code: docker
    :class: highlight
    :encoding: utf-8

Now run the following shell command:

.. code:: bash

   make build-uninstall-big

You should see something close to the following in your terminal:

.. code:: text

    REPOSITORY          TAG                 IMAGE ID            CREATED                  SIZE
    blog-python         big-uninstall       10a0eb5d42aa        Less than a second ago   251MB
    blog-python         big                 8a68d0dad407        11 minutes ago           251MB
    python              3.6-alpine          8eb1c554687d        16 hours ago             90.4MB

Our efforts at removing our C compiler proved futile. At this point, lesser
developers would give up and assume we've reached the end of the road. But you,
dear reader, are reading my blog, and I know you're better than that! Let's dig
deeper and find an elegant way shrink our Docker image!

Example 4: small final build without C compiler
-----------------------------------------------

This final example results in a small image with uWSGI installed and without a
C compiler. It relies heavily on multi-stage builds and on pip wheels.

Copy the following code into a file called "Dockerfile.small":

.. include:: docker-python-install-wheels/Dockerfile.small
    :code: docker
    :class: highlight
    :encoding: utf-8

Now run the following shell command:

.. code:: bash

   make build-small

You should see something close to the following in your terminal:

.. code:: text

   REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
   blog-python         small               b952f6280b00        1 second ago        97.4MB
   <none>              <none>              91c7bb911f32        3 minutes ago       249MB
   blog-python         big-uninstall       10a0eb5d42aa        23 minutes ago      251MB
   blog-python         big                 8a68d0dad407        34 minutes ago      251MB
   python              3.6-alpine          8eb1c554687d        16 hours ago        90.4MB

Notice that the image tagged "small" is ~61% smaller than its "big"
counterparts. It has 7 additional MB from its base alpine container. These
megabytes represent only the uWSGI library itself. We'll need to make
modifications to uWSGI itself to get any smaller. I leave uWSGI modifications
as an exercise for the reader.

Explanation
===========

Two key points are responsible for our Docker build's success:

1. Reliance on copying between image stages in Docker multi-stage
   builds. This gets around caching problems with a single image
2. Understanding the difference between "pip install" and "pip wheel"

Copying betwen Docker build stages in multi-stage build
-------------------------------------------------------

Unless we explicitly specify a `--target`_, Docker multi-stage builds will tag
their last stage. Downstream build stages can reference upstream build stages
and copy resources from them, similarly to how resources can be copied from any
local or remote file system into a traditional Docker container. Therefore, we
"compile" our Python code in one build stage and copy this compiled code in
another build stage. Since the code no longer needs to be compiled, we don't
need to a C compiler or Linux headers. As the coup de grâce, our build's final
stage is not based on any image with a C compiler installed, so this approach
completely avoids Docker's caching complexities.

.. _`--target`: https://docs.docker.com/engine/reference/commandline/build/#specifying-target-build-stage---target

Thanks to Docker's multi-stage builds, we are able to compile our Python
package and avoid deploying the build's system dependencies in our final image.

Difference between "pip install" and "pip wheel"
------------------------------------------------

Docker multi-stage builds are cool and all, but I've seen many articles about
them. Python's packaging tool, pip_, hasn't gotten as much careful attention
from the blogging community. Hopefully this section can clear up one common
point of confusion: `pip install`_ vs `pip wheel`_.

.. _pip: https://pip.pypa.io/en/stable/
.. _`pip install`: https://pip.pypa.io/en/stable/reference/pip_install/
.. _`pip wheel`: https://pip.pypa.io/en/stable/reference/pip_wheel/

pip install
~~~~~~~~~~~

This is the command most people are familiar with. At a high level, it takes a
Python package, runs its setup.py, downloads and installs its dependencies, and
potentially does a lot more. Run "pip install" when you want to expand a
package's contents and use it as its author intended.

A good mental model: "pip install" takes a consolidated bundle of code / build
instructions and places the package's content and dependencies wherever they
need to go on an operating system. Once "pip install" runs on our machine, file
placement throughout our file system can be pretty hamajang_, depending on a
package author's instructed in setup.py.

.. _hamajang: http://stayhawaiian.blogspot.com/2010/05/hamajang.html

pip wheel
~~~~~~~~~

This tool is mostly used by library developers wanting to distribute their
packages in a user-friendly way. For example, scikitlearn_, a popular Python
library for machine learning, requires `a lot of system dependencies`_ to
build. Many Python users, especially data scientists, are either unwilling or
unable to install these dependencies on their host machines. This
user-characteristic led to unfortunate platforms like Anaconda_ (author
opinion). On a more mature note, for those of us with the appropriate
dependencies installed, the installation process would often take a very long
time; C, FORTRAN, and possibly other languages each needed to be compiled, and
installing code written in these languages often leads to a long coffee break.

Wheels enable Python developers to compile a package, and its dependencies, in
a distributable form targeting common operating system architectures. Today,
most scikitlearn users install it `using its wheel`_, which takes a fraction of
the time of the regular build process.

A good mental model: "pip wheel" takes a Python package, makes it ready to be
installed on any target machine WITHOUT its build dependencies, and puts it in
ONE easily-distributed archive file.

.. _scikitlearn: http://scikit-learn.org
.. _`a lot of system dependencies`: http://scikit-learn.org/stable/developers/advanced_installation.html
.. _Anaconda: https://www.anaconda.com/what-is-anaconda/
.. _`using its wheel`: http://scikit-learn.org/stable/install.html

Why we care about this?
~~~~~~~~~~~~~~~~~~~~~~~

Not all Python packages are distributed as wheels. There are some packages,
based mostly on C, that are hard to compile once and use in many places. uWSGI
appears to be one of those packages. To build our final image, we construct
a throw-away container to construct a wheel for uWSGI.

Conclusion
==========

When building a Docker container for a Python application, we can install
packages requiring build-time system dependencies AND remove these system
dependencies from our final Docker image through a combination of Docker
multi-stage builds, pip wheel, and pip install.

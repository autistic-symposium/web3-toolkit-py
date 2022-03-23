# EPen: Art + Logic Pen Language 

This program creates an interface for a digital pen for drawing, as described on [this document](https://github.com/bt3gl/PRIV-Interview_take_home_projects/blob/master/art_and_logic/2-epen/AlpcPart2-190801.pdf).

----

## Installing

Create and source virtual enviroment. You can use [virtualenv](https://virtualenv.pypa.io/en/latest/) or [conda](https://docs.conda.io/en/latest/):

```bash
virtualenv venv
source venv/bin/activate
```

Create and customize an enviroment file:

```bash
cp .env_example .env
vim .env
```

Install dependencies:

```bash
make setup
```

Install EPen:

```bash
make install
```
-----


## Usage

Edit the stream data to be read by the program:

```
vim data/InputStream.txt
```

Run this program with:

```bash
make run
```

or simply

```bash
epen
```

These commands run `./src/main.py`, which calls a class called `Epen()`. 
This is the main class that defines all the functionalities of this application.

-----

## Examples

The stream:

```bash
F0A04000417F4000417FC040004000804001C05F205F20804000
```

prints

```bash
CLR;
CO 0 255 0 255;
MV (0, 0);
PEN DOWN;
MV (4000, 4000);
PEN UP;
```

The stream:


```bash
F0A0417F40004000417FC067086708804001C0670840004000187818784000804000
```

prints

```bash
CLR;
CO 255 0 0 255;
MV (5000, 5000);
PEN DOWN;
MV (8191, 5000);
PEN UP;
MV (8191, 0);
PEN DOWN;
MV (5000, 0);
PEN UP;
```

And the stream:

```bash
F0A040004000417F417FC04000400080400047684F5057384000804001C05F204000400001400140400040007E405B2C4000804000
```

prints

```bash
CLR;
CO 0 0 255 255;
MV (0, 0);
PEN DOWN;
MV (4000, 0) (4000, -8000) (-4000, -8000) (-4000, 0) (-500, 0);
PEN UP;
(base)
```


## Developer

### Linting

You can lint the code with:

```bash
make lint
```

### Cleaning up

Clean residual compilation and installation files with:

```bash
make clean
```


----

Thank you for reading my code!

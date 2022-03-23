# Efun: Art + Logic Enconding + Decoding 

This program i) converts and encodes a 14-bit decimal input value to a 2-byte hexadecimal, ii) decodes hexadecimal representations to 14-bit decimal (as described in [this doc](https://github.com/bt3gl/PRIV-Interview_take_home_projects/blob/master/art_and_logic/1-efun/AlpcPart1-190801.pdf).


## Installing

Create and source virtual enviroment. You can use [virtualenv](https://virtualenv.pypa.io/en/latest/) or [conda](https://docs.conda.io/en/latest/):

```bash
virtualenv venv
source venv/bin/activate
```

Install dependencies:

```bash
make setup
```

Install Efun:

```bash
 make install
```


## Usage

### Encoding

To enconde a integer, run:

```bash
efun -e <integer>
```

Note that the value must be in the range `[-8192, 8191]`.

#### Decoding

To decode an integer, run:

```bash
efun -d <integer>
```

Note that the value must be in the range `[0x0000, 0x7F7F]`.


## Developer

### Running tests

You can run tests with:

```bash
make test
```

### Linting

You can lint your code with:

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

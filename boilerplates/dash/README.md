# Infrastructure Dashboards

This repository contains the source code for the infrastructure dashboards developed with [plot.ly and dash](https://dash.plot.ly/).

### Why Plotly

Plotly allows you to make beautiful and interactive dashboards in just a few lines of code, with data virtually any source that has a Python API.

### How do the Infrastructure Dashboards work?

Plotly objects consist of one or more data components and a layout component. Both have subcomponents. Most, but not all, of the formatting is controlled in the layout.

This app is divided into the following resources:

* `wrappers/`: where the API wrappers, `style.py` and `settings.py` live.
* `.env`: where all the constants and keys/secrets are set.
* `app.py`: entry point for the dashboard app: where the layout elements and the callback functions are set.

-----

## Running locally in dev mode

### Setting up

Add an `.env` file:

```
cp .env_example .env
```

Create an virtual environment and install dependencies:

```
virtualenv venv
source venv/bin/activate
```

### Installing

```
make install
```

### Running

Run server at localhost:

```
make run
```

The dahsboard should be available at `http://127.0.0.1:8051/` (note that the port is set in `.env`).


-------------

## Learning Resources

* [Build Your own Data Dashboard](https://towardsdatascience.com/build-your-own-data-dashboard-93e4848a0dcf).
* [A Python Programmers’ Guide to Dashboarding](https://medium.com/@drimik99/a-python-programmers-guide-to-dashboarding-part-1-8db0c48eee9d).
* [Interactive Python Dashboards with Plotly and Dash](https://www.udemy.com/course/interactive-python-dashboards-with-plotly-and-dash).
* [Make Your Data Visualizations Interactive with Plotly](https://towardsdatascience.com/its-2019-make-your-data-visualizations-interactive-with-plotly-b361e7d45dc6).


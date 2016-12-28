# solar-production

Tool for monitoring production from solar panels

## Code Organization

The system is organized hierarchically, with the main module
contained in `solar_production.py`. This creates the database
object and the monitor object, and hands the database object
to the monitor. The monitor then kicks off the processing loop
and calls db.record_production periodically with a `reading`
dictionary object of the form:

    {
        "current": <current production in watts>,
        "today":   <production today in watts>,
        "week":    <production this week in watts>,
        "install": <production since system installation, in watts>
    }
        
Production values are floats. The timestamp is a UNIX timestamp 
as per `time.time()`

The user interface is provided by the `ui` module. Details will
be filled out here as the code evolves.

## Data storage

The data is stored in a SQLite database. The table structure 
schema looks like this:

    currentProduction
        time    <timestamp>
        power   <float: watts>
                
    dailyProduction
        year    <integer>
        month   <integer>
        day     <integer>
        power   <float: watts>

## Sample Data

There is a single sample data file in the tests directory. To
serve it locally, run `python -m SimpleHTTPServer` from the tests
directory and then direct the code to pull from http://127.0.0.1:8000/sample.html
instead of the site-configured URL.

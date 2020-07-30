# Planetary data from NASA and EU databases

Online NASA database (NASA Exoplanet Archive): https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=planets

Online EU database (The Extrasolar Planets Encyclopaedia): http://exoplanet.eu/catalog/

**REQUIREMENTS**

In order to make use of these codes, one needs to:
- use Python 3
- have the pandas module (if not, see https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html for two possible ways of installing it)
- have the pyExoplaneteu module (if not, see https://pypi.org/project/pyExoplaneteu/ on how to do a quick installation)


**FILES**

- ***dictio.py***: python file which corresponds EU database parameters to NASA database parameters, when possible.
- ***functions.py***: Main file. Python file with functions to extract planetary information from SWEET-Cat, NASA and EU databases.
  - *coor_sc2deg*: Converts coordinates of the SWEET-Cat star to degrees.
  - *match*: Given a SWEETCat star, verifies if it already exists in the NASA and EU database. Returns all or specified information.
  - *verify_database*: Given a SWEET-Cat star, uses the database column of SWEET-Cat to verify which database contains information of the star and its planets.
  - *get_sc*: Given the name of a SWEET-Cat star, returns all information or the selected parameters as they are in SWEET-Cat.
  - *coor2deg*: Converts all SWEET-Cat coordinates (right ascension and declination) to degrees.
- ***nasa.py***: python file responsible for the downloading and storing of NASA database in a dictionary.
- ***new_nasa.py***: python file modifying the NASA data base, adding 3 columns for the parameters m_sini and its upper and lower uncertainties.
- ***WEBSITE_online_EU-NASA_full_database_clean_06-04-2020.rdb***: file with data from the SWEET-Cat database.


**FOLDERS**
- **Plots**: *plots.py* and *plot2.py* are two different ways to plot the planet's period as a function of the stellar metallicity, for planets with mass M < 30 M_Earth and a precision above 20%.
- **Older versions codes**: *funcoes.py* is an older version of *functions.py*, added with some unused functions.

**TUTORIAL: HOW TO USE THESE CODES**

**I. Load NASA database**

To get the NASA database in a pandas DataFrame as it is online, we must first load the ```pandas``` module and the use the ```get_data()``` function from ```nasa.py``` to download and store the data in a dictionary. Lastly, we load the dictionary in a pandas DataFrame

```python
import pandas as pd
from nasa import get_data

# Data from NASA database in pandas DataFrame
na = pd.DataFrame.from_dict(get_data())
```

**II. Load NASA database with mass and m_sini separated**

The ```na``` database only has one column with all the information related to mass (and two columns for the upper and lower uncertainties, respectively), be it the mass or m_sini parameter. Therefore, if one wants to work with this information in a separate way (not mixing mass with m_sini information), they can use the NASA database from ```new_nasa.py```. This dataframe already has columns for the mass values and its uncertainties and columns for the m_sini values and its uncertainties. In this case, we just do

```python
from new_nasa import new_na
new_nasa_data = new_na()
```
**III. Load EU database**

To load the EU database in a pandas DataFrame, we do

```python
from pyexoplaneteu import get_data as eudata
eu = pd.DataFrame.from_dict(eudata())
```
Note that the function ```get_data()``` from the EU database was renamed as ```eudata()``` to avoid confusion with the ```get_data()``` function from NASA database.

**IV. How to use functions from ```functions.py```**

The main function to be used is the *match* function in the file ```functions.py```. The search for planetary information from both NASA and EU can be done through the corresponding SWEET-Cat star name or its coordinates (also in SWEET-Cat). This function return a dataframe for each NASA and EU found matches, therefore it should be assigned two variables (although it works all the same even if the variables aren't assigned).

```pyhton
# Search by name
nasa_name, eu_name = match('75 Cet')

# Search by name and specifying parameters
nasa_name_par, eu_name_par = match('75 Cet', list_of_parameters=['mass','radius','orbital_period'])

# Search by coordinates --> Star 'eps Eridani'
nasa_coor, eu_coor = match(r_asc='03 32 55.84', declin='-09 27 29.73')

# Search by coordinates and specifying parameters --> Star 'eps Eridani'
nasa_coor_par, eu_coor_par = match(r_asc='03 32 55.84', declin='-09 27 29.73', list_of_parameters=['mass','radius','orbital_period'])
```
Similarly, to make use of the ```get_sc, coor_sc2deg``` and ```verify_database``` functions, one just needs to provide the SWEET-Cat star name and parameters required (when appliable).

```python
verify_database('gamma Cephei')
coor_sc2deg('gamma Cephei')
get_sc('gamma Cephei')
get_sc('gamma Cephei', list_of_parameters=['Teff','logg','feh'])
```

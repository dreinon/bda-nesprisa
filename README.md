# BDA Project - Nesprisa
#### We are group CDA14 and this is the code for injecting test data into our database.

### Code locations:
All code with explanations as comments can be found in `src/bda_nesprisa`, but we recommend looking into three files:
1. `__main__.py`: this is the entrypoint of our script and handles the main table loop which calls functions for each table and handles database operations
2. `tables/__init__.py`: here is where all table related code is defined, so here there can be found the functions that create the row instances for each table and the number of rows that we chose to define for each table.
3. `tables/types.py`: here is where all table row classes are defined.

Other files:
1. `tables/helpers.py`: here is a couple functions we created in order to help us create fake data

### Do you need to execute this code?
This project is a bit laborious to start working with since it is using [PDM Package Manager](https://pdm-project.org/latest/). This package manager provides a really comfortable developer experience, better than just using `pip` with no package manager.

In case you need to execute this code, contact [Daniel Reinón](mailto:dreigar@inf.upv.es) by mail using the link or just open an issue in this repo.

Thanks and sorry for the inconvenience!
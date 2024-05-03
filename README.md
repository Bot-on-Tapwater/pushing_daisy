# Introduction
This is a Django application that inserts csv records into a postgresql database and allows users to perform specific queries using provided api routes.

# Routes
Here are the routes that can be accessed.

## All Records
Returns all records in the database, the results are paginated (100 results per page).

[https://daisy.botontapwater.tech/csv_parser/all](https://daisy.botontapwater.tech/csv_parser/all)

## All Towns
Returns a list of all towns in the records, for each town a link is provided to access all records associated with that town.

[https://daisy.botontapwater.tech/csv_parser/towns](https://daisy.botontapwater.tech/csv_parser/towns)

## All Industries
Returns a list of all industries in the records, for each industry a link is provided to access all records associated with that industry.

[https://daisy.botontapwater.tech/csv_parser/industries](https://daisy.botontapwater.tech/csv_parser/industries)

## All Main Tiers
Returns a list of all main tiers in the records, for each main tier a link is provided to access all records associated with that main tier.

[https://daisy.botontapwater.tech/csv_parser/main_tiers](https://daisy.botontapwater.tech/csv_parser/main_tiers)

## All Sub Tiers
Returns a list of all sub tiers in the records, for each sub tier a link is provided to access all records associated with that sub tier.

[https://daisy.botontapwater.tech/csv_parser/sub_tiers](https://daisy.botontapwater.tech/csv_parser/sub_tiers)

# SQL Dump
There is a sql dump file `daisy_csv.sql` at the root of this repository, this file can be used to recreate the database and all records in it.RE
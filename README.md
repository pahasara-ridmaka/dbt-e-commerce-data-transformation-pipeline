# E-Commerce Data Transformation Pipeline

This project builds a small e-commerce analytics warehouse with dbt and DuckDB, then serves the transformed data in a Streamlit dashboard.



https://github.com/user-attachments/assets/b8c8f16b-4e7a-467a-992c-d7758b600694




## Project Layout

```text
e-commerce-data-transformation-pipeline/
├── dashboard/
│   └── app.py
├── data/
│   ├── generator.py
│   └── raw/
│       ├── orders.csv
│       ├── products.csv
│       ├── promotions.csv
│       └── users.csv
├── dbt/
│   ├── dbt_project.yml
    ├── profiles.yml
│   ├── dev.duckdb
│   ├── macros/
│   ├── models/
│   │   ├── staging/
│   │   │   ├── stg_orders.sql
│   │   │   ├── stg_products.sql
│   │   │   ├── stg_promotions.sql
│   │   │   ├── stg_users.sql
│   │   │   └── schema.yml
│   │   ├── intermediate/
│   │   │   ├── int_orders_enriched.sql
│   │   │   ├── int_orders_joined_products.sql
│   │   │   ├── int_product_inventory_status.sql
│   │   │   └── schema.yml
│   │   └── marts/
│   │       ├── dim_products.sql
│   │       ├── dim_promotions.sql
│   │       ├── dim_users.sql
│   │       ├── fct_orders.sql
│   │       └── schema.yml
│   ├── packages.yml
│   ├── package-lock.yml
│   ├── seeds/
│   ├── snapshots/
│   └── tests/
└── logs/
```

## What The Project Does

- `data/generator.py` creates sample CSV files for users, products, orders, and promotions under `data/raw/`.
- dbt loads and cleans those sources into staging models.
- Intermediate models enrich the data and create reusable joins.
- Mart models publish analytics-friendly dimensions and a fact table.
- `dashboard/app.py` reads from `dbt/dev.duckdb` and displays the transformed tables in Streamlit.

## dbt Model Layers

- Staging: `stg_users`, `stg_orders`, `stg_products`, `stg_promotions`
- Intermediate: `int_orders_enriched`, `int_orders_joined_products`, `int_product_inventory_status`
- Marts: `dim_users`, `dim_products`, `dim_promotions`, `fct_orders`

The project config in `dbt/dbt_project.yml` materializes staging and intermediate models as views, and mart models as tables.

## Dependencies

- dbt packages:
    - `dbt-labs/dbt_utils` `1.4.1`
    - `metaplane/dbt_expectations` `0.10.10`
- The DuckDB database file is stored at `dbt/dev.duckdb`.

## Installation Guide

### Prerequisites

- Python 3.10 or newer
- `pip`
- `dbt-duckdb`
- Streamlit and the dashboard dependencies

### Set Up A Virtual Environment

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Install Required Packages

Install the packages used by the dbt project and the dashboard:

```bash
pip install dbt-duckdb streamlit pandas plotly sqlalchemy duckdb-sqlalchemy
```

### Copy Or Create Your dbt Profile

dbt looks for `profiles.yml` in `~/.dbt/` by default. Create that directory if it does not exist, then add a profile that points to `dbt/dev.duckdb`.

Example `~/.dbt/profiles.yml`:

```yaml
dbt_project:
    target: dev
    outputs:
        dev:
            type: duckdb
            path: "/home/phsr/workspace/active/project-alpha/dbt/dev.duckdb"
            threads: 4
```

If you already have a shared profiles file, you can copy it into place with:

```bash
mkdir -p ~/.dbt
cp /path/to/profiles.yml ~/.dbt/profiles.yml
```

If you need the dbt packages to be installed directly, run from the `dbt/` directory:

```bash
dbt deps
```

### Verify The Setup

Run these commands to confirm the environment is ready:

```bash
cd dbt
dbt debug
dbt build
```

Then launch the dashboard from the repository root:

```bash
streamlit run dashboard/app.py
```

## Typical Workflow

1. Generate or refresh the raw CSV data with `python data/generator.py`.
2. Run dbt from the `dbt/` directory with `dbt deps` and then `dbt build`.
3. Open the dashboard with `streamlit run dashboard/app.py` from the repository root.

## Testing And Validation

Model-level tests are defined in the `schema.yml` files alongside the models. They cover uniqueness, not-null constraints, type checks, and basic data-quality expectations for the source tables.

## Notes

- The dashboard expects the mart models to exist in `dbt/dev.duckdb`.
- The repository contains generated artifacts in `dbt/target/` and logs under `dbt/logs/`; these are runtime outputs rather than source files.













_Built with ❤️ using dbt and DuckDB_

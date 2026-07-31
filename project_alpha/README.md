Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices


```
├── dashboard
│   └── app.py
├── data
│   ├── generator.py
│   └── raw
│       ├── orders.csv
│       ├── products.csv
│       ├── promotions.csv
│       └── users.csv
└── project_alpha
    ├── analyses
    ├── dbt_project.yml
    ├── macros
    ├── models
    │   ├── intermediate
    │   │   ├── int_orders_enriched.sql
    │   │   ├── int_orders_joined_products.sql
    │   │   ├── int_product_inventory_status.sql
    │   │   └── schema.yml
    │   ├── marts
    │   │   ├── dim_products.sql
    │   │   ├── dim_promotions.sql
    │   │   ├── dim_users.sql
    │   │   ├── fct_orders.sql
    │   │   └── schema.yml
    │   └── staging
    │       ├── schema.yml
    │       ├── stg_orders.sql
    │       ├── stg_products.sql
    │       ├── stg_promotions.sql
    │       └── stg_users.sql
    ├── README.md
    ├── seeds
    ├── snapshots
    └── tests


```
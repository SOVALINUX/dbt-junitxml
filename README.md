# dbt-junitxml

Convert your dbt test results into jUnit XML format so that CI/CD platforms (such as Jenkins, CircleCI, etc.)
can better report on tests in their UI.

## About this fork

This is the fork repository based on https://github.com/chasleslr/dbt-junitxml/ version 0.1.5
On top of that here were added:
1. Support of DBT Core 1.3+ (originally it supported only up to 1.2). Versions 0.2.x Tested on DBT 1.5
2. In case of test failures Junit XML contains additional information regarding Stored Results and original test SQL. Details can be found below.
3. Test name in the resulted xml is more specific rather than in original version .
4. Supported integration with https://reportportal.io/

## Installation

Publishing as a regular pip module is considered

```shell
pip install "git+https://github.com/SOVALINUX/dbt-junitxml@0.2.2#egg=dbt-junitxml"
```

We recommend you to stick to some specific version, since newer versions might contain changes that may impact your operations (not being backward incompatible at all, but rather change some visualizations you might be used to).

## Usage

When you run your dbt test suite, the output is saved under `target/run_results.json`. Run the following command
to parse your run results and output a jUnit XML formatted report named `report.xml`.

```shell
dbt-junitxml parse --manifest target/manifest.json --run_result target/run_results.json --output report.xml
```

By default, --manifest is `target/manifest.json`, --run_result is `target/run_results.json` and --output is `report.xml`, so in case your input isn't different from these values, you could run:

```shell
dbt-junitxml parse
```


## Features description

### Rich XML output in case of test failure

In order to help you handle test failures right where you see it we're adding supporting information into Junit XML in case of test failure
It's even more than you see in the DBT CLI console output!
For example:

```
Got 19 results, configured to fail if != 0
2023-06-08 10:47:02
------------------------------------------------------------------------------------------------
select * from db_dbt_test__audit.not_null_table_reporter_employee_id
------------------------------------------------------------------------------------------------

select *
from (select * from "datacatalog"."db"."table" where NOT regexp_like(reporter_email_address, 'auto_.*?@company.com') AND reporter_email_address NOT IN ('exclude@company.com') AND reporter_email_address IS NOT NULL) dbt_subquery
where reporter_employee_id is null
```

### Saving test SQL files for further analysis

Sometimes it's handy to see the exact SQL that was executed and tested by DBT without repeating compilation steps.
To achieve it we suggest you to save compiled tests SQL during your test run.
Below you can find a reference script:
```shell
dbt test --store-failures
mkdir -p target/compiled_all_sql && find target/compiled/ -name *.sql -print0 | xargs -0 cp -t target/compiled_all_sql/
zip -r -q compiled_all_sql.zip target/compiled_all_sql
```

### Integration with Report Portal

https://reportportal.io/ helps you to manage your test launches. Here at EPAM we're using this tool to manage over 4,000 DBT tests

In order to upload your test run to reportportal you can use the following script:
```shell
dbt-junitxml parse target/run_results.json target/manifest.json dbt_test_report.xml
zip dbt_test_report.zip dbt_test_report.xml
REPORT_PORTAL_TOKEN=`Your token for Report Portal`
RESPONSE=`curl -X POST "https://reportportal.io/api/v1/plugin/{project_name}/JUnit/import" -H  "accept: */*" -H  "Content-Type: multipart/form-data" -H  "Authorization: bearer ${REPORT_PORTAL_TOKEN}" -F "file=@dbt_test_report.zip;type=application/x-zip-compressed"`
LAUNCH_ID=`echo "${RESPONSE}" | sed 's/.*Launch with id = \(.*\) is successfully imported.*/\1/'`
```

### Test Case Attribute displayed in Report Portal

Since 0.2.2 version you will be able to put attributes within an junit xml report. It can be beneficial for large dbt projects where we aim to categorize or group data quality tests based on the file structure. For this you'll need additionally provide --custom_properties:

```shell
dbt-junitxml parse --manifest target/manifest.json --run_result target/run_results.json --output report.xml --custom_properties Area=path_levels[2] --custom_properties Source=path_levels[1]
```

where `path_levels` is a reserved variable, pointing to the directory that  models stored, and index is a level of each subdirectory starting from the root of dbt project.


Each test case will be enriched with properties, example:
```xml
<properties>
    <property name="attribute" value="Area:source_data"/>
    <property name="attribute" value="Source:sources_sharepoint.yml"/>
</properties>
```


## Limitations

Currently, only v4 of the [Run Results](https://docs.getdbt.com/reference/artifacts/run-results-json) specifications is supported.

## Contribution

Development of this fork was partially sponsored by EPAM Systems Inc. https://www.epam.com/

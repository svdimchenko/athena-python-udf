# Multithreading example

This example simply takes a string and returns the lowercase version.
The lambda is using python `ThreadPoolExecutor` to speed up execution.

## Example usage

Assuming the lambda function is called `my-lambda` then run a query like this:

```sql
USING EXTERNAL FUNCTION my_udf(col1 varchar) RETURNS varchar LAMBDA 'athena-test'

SELECT my_udf('FooBar');
```

Which will yield the result `foobar`.

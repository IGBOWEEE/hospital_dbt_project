WITH source AS (
    SELECT * FROM {{ source('raw_hospital_data', 'employees') }}
)

SELECT
  "c1" AS employee_id,
  "c2" AS name,
  "c3" AS age,
  "c4" AS gender,
  "c5" AS emp_phone_number,
  "c6" AS emp_email,
  "c7" AS department_id,
  "c8" AS department_name,
  "c9" AS branch_name,
  "c10" AS state,
  "c11" AS job_role,
  CURRENT_TIMESTAMP() AS _loaded_at

FROM source










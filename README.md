# hardware-design

## Introduction of functions




<pre>
### Error updating database.  Cause: java.sql.SQLIntegrityConstraintViolationException: Duplicate entry '2222' for key 'sensor.PRIMARY'
### The error may exist in com/lzz/climate/dao/SensorDao.java (best guess)
### The error may involve com.lzz.climate.dao.SensorDao.insert-Inline
### The error occurred while setting parameters
### SQL: INSERT INTO sensor  ( id, name, isopen )  VALUES  ( ?, ?, ? )
### Cause: java.sql.SQLIntegrityConstraintViolationException: Duplicate entry '2222' for key 'sensor.PRIMARY'
; Duplicate entry '2222' for key 'sensor.PRIMARY'; nested exception is java.sql.SQLIntegrityConstraintViolationException: Duplicate entry '2222' for key 'sensor.PRIMARY'
</pre>

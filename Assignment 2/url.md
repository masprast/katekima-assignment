### 1. Items

| method | endpoint      | desc                                          |
| ------ | ------------- | --------------------------------------------- |
| [GET]  | /items/       | get all items                                 |
| [GET]  | /items/{code} | get an item with corresponding code on params |
| [POST] | /items/       | create an item                                |
| [PUT]  | /items/{code} | update an item                                |
| [DEL]  | /items/{code} | soft delete item                              |

### 2. Purchases

| method | endpoint                        | desc                                                                                                                                              |
| ------ | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| [GET]  | /purchase/                      | get all purchases                                                                                                                                 |
| [GET]  | /purchase/{code}                | get a purchase with corresponding code on params                                                                                                  |
| [POST] | /purchase/                      | create a purchase                                                                                                                                 |
| [PUT]  | /purchase/{code}                | update a purchase                                                                                                                                 |
| [DEL]  | /purchase/{code}                | delete                                                                                                                                            |
| [GET]  | /purchase/{header_code}/details | get all purchases detail with corresponding header code on params                                                                                 |
| [POST] | /purchase/{header_code}/details | create purchases detail with corresponding header code on params. Should add item stock and balance based on quantity and unit_price when created |

### 3. Sells

| method | endpoint                    | desc                                                                                                                                                      |
| ------ | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [GET]  | /sell/                      | get all sells                                                                                                                                             |
| [GET]  | /sell/{code}                | get a sell with corresponding code on params                                                                                                              |
| [POST] | /sell/                      | create a sell                                                                                                                                             |
| [PUT]  | /sell/{code}                | update a sell                                                                                                                                             |
| [DEL]  | /sell/{code}                | soft delete sell                                                                                                                                          |
| [GET]  | /sell/{header_code}/details | get all sells detail with corresponding header code on params                                                                                             |
| [POST] | /sell/{header_code}/details | create sell detail with corresponding header code on params. Should decrease item stock and balance based on quantity and purchasing stock that happened. |

### 4. Reporting

| method | endpoint                                                       | desc                                       |
| ------ | -------------------------------------------------------------- | ------------------------------------------ |
| [GET]  | /report/{item_code}/?start_date=yyyy-mm-dd&end_date=yyyy-mm-dd | Get a report with corresponding item code. |

> Query params : <br/>
> start_date: contain string of start date of the report <br/>
> start_date: contain string of end date of the report <br/> > `[GET]/report/I-001/?start_date=2025-01-01&end_date=2025-03-31`

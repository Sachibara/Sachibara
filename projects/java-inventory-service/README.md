# Stock Ledger

Java 17 / Spring Boot / Spring Security / Spring Data JPA inventory software with a browser UI. Unique normalized SKUs, bounded stock adjustments, required movement reasons, transactional history, pessimistic row locking and optimistic version checks. H2 file persistence for local use; PostgreSQL configurable.

## Run
Install JDK 17+ and Maven. Set `INVENTORY_ADMIN_PASSWORD` to a password of at least 12 characters, then:
```sh
mvn spring-boot:run
```
Open http://127.0.0.1:8084 and connect with that password. Create a product, receive stock with a positive adjustment, issue stock with a negative adjustment, and view History. An overdraw or stale version is rejected. Password exists only in UI memory after sign-in; refresh requires reconnecting. Basic authentication must use TLS for any remote deployment.

`INVENTORY_DB_URL`, `INVENTORY_DB_USER`, `INVENTORY_DB_PASSWORD` configure PostgreSQL; otherwise data persists in `data/`. Hibernate update is a demo schema bootstrap; use versioned migrations for deployment. No order processing, multiple operator identities or purchase accounting is claimed.

## Checks
`mvn test` compiles the Spring application (no Spring integration suite is supplied). The standalone business-rule check needs no downloads:
```sh
javac -d target/rules src/main/java/com/sachibara/inventory/StockRules.java tests/StockRulesCheck.java
java -cp target/rules StockRulesCheck
```
Verify authentication, duplicate SKU rejection, stock receipt/issue, negative-stock rejection and persistence in the browser after installing dependencies. The source includes a functional JavaScript UI; React/Angular are demonstrated separately in the collection.

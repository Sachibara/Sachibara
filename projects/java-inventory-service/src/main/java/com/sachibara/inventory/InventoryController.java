package com.sachibara.inventory;
import java.util.*;import jakarta.validation.Valid;import jakarta.validation.constraints.*;import org.springframework.web.bind.annotation.*;import org.springframework.http.*;import org.springframework.transaction.annotation.Transactional;import org.springframework.web.server.ResponseStatusException;import org.springframework.data.domain.*;
@RestController @RequestMapping("/api") public class InventoryController {
 private final ProductRepository products;private final MovementRepository movements;
 public InventoryController(ProductRepository products,MovementRepository movements){this.products=products;this.movements=movements;}
 record NewProduct(@NotBlank @Size(max=40) String sku,@NotBlank @Size(max=120) String name){}
 record Adjustment(@NotNull Long version,@Min(-1000000) @Max(1000000) int delta,@NotBlank @Size(max=200) String reason){}
 @GetMapping("/products") List<Product> list(){return products.findAll(PageRequest.of(0,500,Sort.by("sku"))).getContent();}
 @PostMapping("/products") @ResponseStatus(HttpStatus.CREATED) Product create(@Valid @RequestBody NewProduct body){return products.saveAndFlush(new Product(StockRules.sku(body.sku()),body.name().trim()));}
 @PostMapping("/products/{id}/adjust") @Transactional Product adjust(@PathVariable Long id,@Valid @RequestBody Adjustment body){Product product=products.lockById(id).orElseThrow(()->new ResponseStatusException(HttpStatus.NOT_FOUND));if(!Objects.equals(product.version,body.version()))throw new ResponseStatusException(HttpStatus.CONFLICT,"Stock changed; refresh and retry.");product.quantity=StockRules.apply(product.quantity,body.delta());movements.save(new Movement(id,body.delta(),body.reason().trim()));return products.saveAndFlush(product);}
 @GetMapping("/products/{id}/movements") List<Movement> movements(@PathVariable Long id){if(!products.existsById(id))throw new ResponseStatusException(HttpStatus.NOT_FOUND);return movements.findTop100ByProductIdOrderByCreatedDesc(id);}
}

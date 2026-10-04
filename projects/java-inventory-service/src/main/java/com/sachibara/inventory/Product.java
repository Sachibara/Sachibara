package com.sachibara.inventory;
import jakarta.persistence.*;
@Entity public class Product {
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY) public Long id;
 @Column(nullable=false,unique=true,length=40) public String sku;
 @Column(nullable=false,length=120) public String name;
 @Column(nullable=false) public int quantity;
 @Version public Long version;
 public Product(){}
 public Product(String sku,String name){this.sku=sku;this.name=name;}
}

package com.sachibara.inventory;
import jakarta.persistence.*;import java.time.Instant;
@Entity public class Movement {
 @Id @GeneratedValue(strategy=GenerationType.IDENTITY) public Long id;
 @Column(nullable=false) public Long productId;
 public int delta;
 @Column(nullable=false,length=200) public String reason;
 public Instant created=Instant.now();
 public Movement(){}
 public Movement(Long id,int delta,String reason){this.productId=id;this.delta=delta;this.reason=reason;}
}
